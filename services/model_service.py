"""The exported Semester-1 pipeline is authoritative; no fitting occurs here."""
import json
import logging
import math
from threading import RLock
import joblib
import numpy as np
import pandas as pd
from .recommendation_service import recommendations, snapshot, S1

log = logging.getLogger(__name__)


class ValidationError(ValueError):
    def __init__(self, errors):
        self.errors = errors
        super().__init__('Please correct the highlighted values.')


def group_for(name):
    if name == 'Target': return 'Outcome'
    if '2nd sem' in name: return 'Semester 2 · excluded'
    if '1st sem' in name: return 'Semester 1'
    if name in ['Unemployment rate', 'Inflation rate', 'GDP']: return 'Economic'
    if name in ['Debtor', 'Tuition fees up to date', 'Scholarship holder']: return 'Financial'
    if name.startswith(("Mother's", "Father's")): return 'Family / Socioeconomic'
    if name in ['Application mode', 'Application order', 'Course', 'Previous qualification', 'Previous qualification (grade)', 'Admission grade']: return 'Admission'
    return 'Personal'


def friendly(name):
    if name.startswith(S1):
        return {'credited': 'Credited units', 'enrolled': 'Enrolled units', 'evaluations': 'Evaluations',
                'approved': 'Approved units', 'grade': 'Semester-1 average grade',
                'without evaluations': 'Units without evaluation'}[name.split('(')[1][:-1]]
    return 'Nationality' if name == 'Nacionality' else name


class ModelService:
    def __init__(self, root):
        self.root, self.ready, self.error = root, False, None
        self.metadata, self.features, self.schema, self.dictionary = {}, [], [], []
        self.maps, self.course_map, self.importance, self.source = {}, {}, [], pd.DataFrame()
        self.explainer, self.lock = None, RLock()
        self.dataset_error = None
        try:
            self.metadata = json.loads((root / 'models' / 'model_metadata.json').read_text())
            bundle_path = root / 'models' / 'student_dropout_flask_bundle.pkl'
            if bundle_path.exists():
                b = joblib.load(bundle_path)
                self.model, self.calibrator = b['model'], b['calibrator']
                self.features, self.class_index = b['input_features'], b['dropout_class_index']
                self.medium, self.high, self.margin = b['medium_risk_threshold'], b['high_risk_threshold'], b['review_margin']
                self.course_map, self.maps = b['course_map'], b['binary_maps']
                self.artifact = bundle_path.name
            else:
                self.model = joblib.load(root / 'models' / 'student_risk_model.pkl')
                self.calibrator = joblib.load(root / 'models' / 'probability_calibrator.pkl')
                self.features = self.metadata['features']
                self.class_index = list(self.model.classes_).index(1)
                self.medium, self.high, self.margin = [self.metadata[k] for k in ('medium_risk_threshold', 'decision_threshold', 'review_margin')]
                self.course_map, self.maps = {}, {}
                self.artifact = 'student_risk_model.pkl + probability_calibrator.pkl + model_metadata.json'
            assert self.features == list(self.model.feature_names_in_) == self.metadata['features']
            assert not any('2nd sem' in f for f in self.features)
            assert self.model.classes_[self.class_index] == 1
            assert 0 <= self.medium < self.high <= 1 and 0 <= self.margin <= 1
            self.preprocessor = self.model.named_steps['preprocessor']
            self.classifier = self.model.named_steps['classifier']
            self.classifier.set_params(n_jobs=2)
            self.category_values = {}
            for name, transformer, columns in self.preprocessor.transformers_:
                if name == 'cat':
                    encoder = transformer.named_steps.get('onehot')
                    if encoder is None:
                        encoder = next(v for v in transformer.named_steps.values() if hasattr(v, 'categories_'))
                    self.category_values.update({f: [int(v) for v in values] for f, values in zip(columns, encoder.categories_)})
            transformed = self.preprocessor.get_feature_names_out()
            self.raw_names = []
            for name in transformed:
                tail = name.split('__', 1)[-1]
                self.raw_names.append(next(f for f in sorted(self.features, key=len, reverse=True) if tail == f or tail.startswith(f + '_')))
            imp = dict.fromkeys(self.features, 0.)
            for f, v in zip(self.raw_names, self.classifier.feature_importances_): imp[f] += float(v)
            self.importance = [{'feature': f, 'label': friendly(f), 'value': v} for f, v in sorted(imp.items(), key=lambda x: -x[1])]
            self.ready = True
        except Exception:
            log.exception('Model initialization failed')
            self.error = 'The operational model could not be loaded. Check the original artifacts and compatible dependencies.'
        try:
            self.source = pd.read_csv(root / 'data' / 'raw' / 'data.csv', sep=';')
            self.source.columns = self.source.columns.str.strip()
            self.dictionary = pd.read_csv(root / 'artifacts' / 'feature_dictionary.csv').fillna('').to_dict('records')
            for row in self.dictionary: row['Category'] = group_for(row['Feature'])
        except Exception:
            self.dataset_error = 'Source dataset or feature dictionary is unavailable. Restore the original CSV files.'
            log.exception('Dataset initialization failed')
        if self.ready:
            self.training_categories = {f: set(values) for f, values in self.category_values.items()}
            # The fitted encoder intentionally supports unknown categories. Include
            # documented source codes absent from the training split without fitting.
            for f in self.category_values:
                if f in self.source:
                    self.category_values[f] = sorted(set(self.category_values[f]) | {int(v) for v in self.source[f].dropna().unique()})
            mapping_file = root / 'data' / 'reference' / 'category_labels.json'
            if mapping_file.exists():
                for f, mapping in json.loads(mapping_file.read_text(encoding='utf-8')).items():
                    self.maps.setdefault(f, {}).update({int(k): v for k, v in mapping.items()})
            self.maps['Course'] = self.course_map
            for f in self.features:
                choices = self.category_values.get(f)
                low, high, step = self.bounds(f)
                self.schema.append({'name': f, 'label': friendly(f), 'group': group_for(f), 'min': low, 'max': high, 'step': step,
                    'options': [{'value': v, 'label': self.maps.get(f, {}).get(v, f'Source code {v}')} for v in choices] if choices is not None else None,
                    'help': self.help_text(f)})

    def bounds(self, f):
        if f == 'Age at enrollment': return 14, 100, 1
        if f == 'Application order': return 0, 9, 1
        if f in ['Admission grade', 'Previous qualification (grade)']: return 0, 200, 'any'
        if f == f'{S1} (grade)': return 0, 20, 'any'
        if '1st sem' in f: return 0, None, 1
        return None, None, 'any'

    def help_text(self, f):
        if f == 'Daytime/evening attendance': return 'Study schedule, not attendance percentage.'
        if f in ['Admission grade', 'Previous qualification (grade)']: return 'Source scale: 0–200.'
        if f == f'{S1} (grade)': return 'Source scale: 0–20.'
        if f in ['Unemployment rate', 'Inflation rate', 'GDP']: return 'Use the source-compatible economic context; never substitute a missing value.'
        return ''

    def validate(self, data):
        if not isinstance(data, dict): raise ValidationError({'form': 'Provide a student record.'})
        errors, cleaned = {}, {}
        for f in self.features:
            try:
                if isinstance(data.get(f), bool) or data.get(f) is None or str(data.get(f)).strip() == '': raise ValueError()
                v = float(data[f])
                if not math.isfinite(v): raise ValueError()
                lo, hi, step = self.bounds(f)
                if lo is not None and v < lo or hi is not None and v > hi: raise ValueError()
                if step == 1 and not v.is_integer(): raise ValueError()
                if f in self.category_values and v not in self.category_values[f]:
                    errors[f] = 'Select a valid source-dataset category.'
                cleaned[f] = int(v) if v.is_integer() else v
            except (ValueError, TypeError, OverflowError):
                errors[f] = f'Enter a valid finite value. {self.help_text(f)}'
        a, e = f'{S1} (approved)', f'{S1} (enrolled)'
        w = f'{S1} (without evaluations)'
        if a in cleaned and e in cleaned and cleaned[a] > cleaned[e]: errors[a] = 'Approved units cannot exceed enrolled units.'
        if w in cleaned and e in cleaned and cleaned[w] > cleaned[e]: errors[w] = 'Units without evaluation cannot exceed enrolled units.'
        if errors: raise ValidationError(errors)
        return cleaned

    def ensure_ready(self):
        if not self.ready: raise RuntimeError(self.error)

    def explain_batch(self, frame):
        try:
            with self.lock:
                if self.explainer is None:
                    import shap
                    self.explainer = shap.TreeExplainer(self.classifier)
                values = np.asarray(self.explainer.shap_values(self.preprocessor.transform(frame)))
            if values.ndim != 2: raise ValueError('Unsupported SHAP shape')
            result = []
            for row in values:
                aggregated = dict.fromkeys(self.features, 0.)
                for f, v in zip(self.raw_names, row): aggregated[f] += float(v)
                positive = sorted([(f, v) for f, v in aggregated.items() if v > 0], key=lambda x: -x[1])[:5]
                negative = sorted([(f, v) for f, v in aggregated.items() if v < 0], key=lambda x: x[1])[:5]
                pack = lambda rows: [{'feature': f, 'label': friendly(f), 'contribution': round(v, 5)} for f, v in rows]
                result.append({'method': 'Tree SHAP', 'risk_factors': pack(positive), 'protective_factors': pack(negative),
                    'note': 'SHAP contributions explain the underlying XGBoost score in log-odds, before isotonic calibration. They are associations, not causes or percentage-point changes.'})
            return result
        except Exception:
            log.exception('SHAP unavailable; using explicitly labeled observed signals')
            results = []
            for f in frame.to_dict('records'):
                risk, protective = [], []
                for key, adverse, label in [(f'{S1} (grade)', f[f'{S1} (grade)'] < 10, 'Semester-1 grade'), ('Tuition fees up to date', not f['Tuition fees up to date'], 'Tuition status')]:
                    (risk if adverse else protective).append({'feature': key, 'label': label, 'contribution': None})
                results.append({'method': 'Observed signals (rule-based fallback)', 'risk_factors': risk, 'protective_factors': protective,
                    'note': 'SHAP is unavailable. These observed signals are advisory rules, not measured model contributions.'})
            return results

    def predict_many(self, rows, validate=True):
        self.ensure_ready()
        clean = [self.validate(row) for row in rows] if validate else rows
        if not clean: return []
        frame = pd.DataFrame(clean, columns=self.features)
        raw = self.model.predict_proba(frame)[:, self.class_index]
        probabilities = self.calibrator.predict(raw)
        explanations = self.explain_batch(frame)
        results = []
        for f, p, ex in zip(clean, probabilities, explanations):
            p = float(p)
            if not math.isfinite(p) or not 0 <= p <= 1: raise RuntimeError('Invalid model output')
            results.append({'risk_probability': p, 'risk_score': round(p * 100, 2),
                'risk_level': 'High' if p >= self.high else 'Medium' if p >= self.medium else 'Low',
                'manual_review': abs(p-self.high) <= self.margin, 'explanation': ex,
                'data_notes': [f'{friendly(k)}: valid source category absent from the training split; handled by the exported encoder as an unseen category.' for k, categories in self.training_categories.items() if f[k] not in categories],
                'recommendations': recommendations(f), 'snapshot': snapshot(f),
                'model_stage': self.metadata['prediction_point'], 'features': f})
        return results

    def predict(self, data): return self.predict_many([data])[0]

    def course(self, code): return self.course_map.get(int(code), f'Course {code}')
