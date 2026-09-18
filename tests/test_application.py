"""End-to-end regression checks against the actual exported ML artifacts.

Run: .\venv\Scripts\python.exe -m unittest discover -s tests -v
All writes go to temporary SQLite databases; original artifacts are read-only.
"""
import csv
import io
import json
import math
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import joblib
import numpy as np
import pandas as pd
from openpyxl import Workbook
from app import create_app
from config import BASE_DIR
from services.model_service import ModelService
from services.recommendation_service import recommendations


class ApplicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.app = create_app({'TESTING': True, 'DATABASE': str(Path(cls.temp.name) / 'test.db')})
        cls.client = cls.app.test_client()
        cls.client.get('/')
        with cls.client.session_transaction() as session: cls.token = session['csrf']
        cls.model = cls.app.extensions['model_service']
        cls.repo = cls.app.extensions['student_repository']
        cls.sample = cls.client.get('/api/sample').json['features']

    @classmethod
    def tearDownClass(cls): cls.temp.cleanup()

    def post(self, url, **kwargs):
        return self.client.post(url, headers={'X-CSRF-Token': self.token}, **kwargs)

    def upload(self, rows, name='students.csv'):
        frame = pd.DataFrame(rows)
        if name.endswith('.xlsx'):
            workbook = Workbook(); sheet = workbook.active
            sheet.append(list(frame.columns))
            for values in frame.itertuples(index=False, name=None): sheet.append(list(values))
            stream = io.BytesIO(); workbook.save(stream); stream.seek(0)
        else: stream = io.BytesIO(frame.to_csv(index=False).encode())
        return self.post('/api/upload', data={'file': (stream, name)}, content_type='multipart/form-data')

    def test_01_model_load_feature_order_and_calibration(self):
        self.assertTrue(self.model.ready)
        self.assertEqual(len(self.model.features), 30)
        self.assertEqual(self.model.features, list(self.model.model.feature_names_in_))
        self.assertFalse(any('2nd sem' in f for f in self.model.features))
        bundle = joblib.load(BASE_DIR / 'models' / 'student_dropout_flask_bundle.pkl')
        frame = pd.DataFrame([self.sample], columns=bundle['input_features'])
        expected = float(bundle['calibrator'].predict(bundle['model'].predict_proba(frame)[:, bundle['dropout_class_index']])[0])
        actual = self.model.predict(dict(reversed(list(self.sample.items()))))
        self.assertAlmostEqual(expected, actual['risk_probability'], places=12)
        self.assertEqual(actual['explanation']['method'], 'Tree SHAP')

    def test_02_seed_and_idempotency(self):
        seeded = self.repo.query({'source': 'Enrolled dataset'}, all_rows=True)['students']
        self.assertEqual(len(seeded), 794)
        self.assertTrue(all(s['student_name'] is None for s in seeded))
        self.assertEqual(self.repo.seed(self.model), 0)
        source = pd.read_csv(BASE_DIR / 'artifacts' / 'enrolled_students_risk_scores.csv')
        by_id = sorted(seeded, key=lambda s: s['student_uid'])
        np.testing.assert_allclose([s['risk_score'] for s in by_id], source['Risk Score'], atol=.01)

    def test_03_page_routes_and_static_assets(self):
        for url in ['/', '/dashboard', '/students', '/students/STU-000001', '/analyze', '/upload', '/dataset', '/model', '/reports', '/powerpoint', '/about',
                    '/static/css/app.css', '/static/css/powerpoint.css', '/static/js/app.js', '/static/js/analyze.js', '/static/js/upload.js', '/static/js/powerpoint.js', '/static/vendor/chart.umd.min.js', '/static/vendor/lucide.min.js']:
            with self.subTest(url=url):
                with self.client.get(url) as response: self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.get('/students/NOT-FOUND').status_code, 404)
        self.assertNotIn(b'Traceback', self.client.get('/no-such-page').data)

    def test_03b_powerpoint_is_bilingual_and_uses_v2_evidence(self):
        english = self.client.get('/powerpoint?lang=en').text
        arabic = self.client.get('/powerpoint?lang=ar').text
        self.assertIn('PowerPoint', english)
        self.assertIn('presentation-data', english)
        self.assertIn('"XGBoost"', english)
        self.assertIn('"train_pr_auc": 0.9866443336008119', english)
        self.assertIn('<html lang="ar" dir="rtl">', arabic)
        self.assertIn('العرض التقديمي', arabic)
        self.assertIn('"enrolled_total": 794', arabic)
        self.assertIn('/static/js/powerpoint.js', english)
        self.assertIn('/static/css/powerpoint.css', english)
        payload_text = english.split('<script id="presentation-data" type="application/json">', 1)[1].split('</script>', 1)[0]
        payload = json.loads(payload_text)
        self.assertEqual(len(payload['slides']['en']), 20)
        self.assertEqual([slide['title'] for slide in payload['slides']['en']][0:5], ['EduGuard AI', 'Project idea', 'Problem statement', 'Project objectives', 'System scope'])
        self.assertEqual(payload['slides']['en'][12]['title'], 'Model selection and cross-validation')
        self.assertEqual(payload['slides']['en'][14]['title'], 'Final test results')
        self.assertIn('There is a moderate Train-to-CV gap', payload['slides']['en'][12]['note'])
        self.assertEqual(payload['metrics']['risk_counts'], {'Low': 309, 'Medium': 0, 'High': 485})
        self.assertEqual(payload['metrics']['enrolled_total'], 794)
        self.assertEqual(sum(slide['type'] == 'cover' for slide in payload['slides']['en']), 1)

    def test_04_search_filters_pagination_sort(self):
        d = self.client.get('/api/students/search?q=STU-000001').json
        self.assertEqual(d['students'][0]['student_uid'], 'STU-000001')
        page = self.client.get('/api/students?risk=High&review=1&per_page=5&sort=risk&direction=asc').json
        self.assertLessEqual(len(page['students']), 5)
        self.assertTrue(all(s['risk_level']=='High' and s['manual_review'] for s in page['students']))
        scores = [s['risk_probability'] for s in page['students']]
        self.assertEqual(scores, sorted(scores))
        self.assertEqual(self.client.get('/api/students?q=not-a-student').json['total'], 0)
        self.assertEqual(self.client.get('/api/students?min_risk=101').status_code, 400)
        self.assertEqual(self.client.get('/api/students?date=bad').status_code, 400)

    def test_05_existing_prediction_and_history(self):
        uid='STU-000001'; before=len(self.repo.get(uid)['history'])
        response=self.post('/api/analyze/'+uid)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json['result']['risk_level'],'High')
        self.assertEqual(len(self.repo.get(uid)['history']),before+1)

    def test_06_manual_prediction_same_operational_model(self):
        response=self.post('/api/analyze/manual',json={'Student ID':'TEST-PREVIEW','features':self.sample})
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json['result']['risk_probability'],self.model.predict(self.sample)['risk_probability'])
        self.assertIsNone(self.repo.get('TEST-PREVIEW'))

    def test_07_invalid_manual_data(self):
        for name,value in [('Curricular units 1st sem (approved)',999),('Age at enrollment',-1),('Admission grade',201),('Previous qualification (grade)',201),('Curricular units 1st sem (grade)',21),('Application order',1.5),('Gender',99),('GDP','NaN'),('GDP','Infinity'),('GDP',''),('Debtor',None)]:
            with self.subTest(feature=name,value=value):
                row={**self.sample,name:value};response=self.post('/api/analyze/manual',json={'features':row})
                self.assertEqual(response.status_code,422)
                self.assertIn(name,response.json['errors'])
        row=dict(self.sample);del row['Course']
        self.assertEqual(self.post('/api/analyze/manual',json={'features':row}).status_code,422)

    def test_08_save_and_find_manual_student(self):
        response=self.post('/api/students',json={'Student ID':'TEST-MANUAL','features':self.sample})
        self.assertEqual(response.status_code,201)
        self.assertEqual(self.client.get('/api/students/search?q=TEST-MANUAL').json['students'][0]['student_uid'],'TEST-MANUAL')
        self.assertEqual(self.client.get('/students/TEST-MANUAL').status_code,200)
        self.assertEqual(self.post('/api/analyze/TEST-MANUAL').status_code,200)
        self.assertEqual(self.post('/api/students',json={'Student ID':'TEST-MANUAL','features':self.sample}).status_code,409)

    def test_09_csv_preview_commit_and_replay(self):
        response=self.upload([{'Student ID':'TEST-CSV',**self.sample}])
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json['valid_rows'],1)
        token=response.json['token'];self.assertIsNone(self.repo.get('TEST-CSV'))
        result=self.post('/api/upload/commit',json={'token':token})
        self.assertEqual(result.status_code,200);self.assertEqual(result.json['imported'],1)
        before=self.repo.count();replay=self.post('/api/upload/commit',json={'token':token})
        self.assertEqual(replay.json,result.json);self.assertEqual(self.repo.count(),before)
        export=self.client.get('/exports/students.csv?batch='+token)
        self.assertEqual(export.status_code,200);self.assertIn(b'TEST-CSV',export.data)

    def test_10_excel_import_and_generated_id(self):
        response=self.upload([self.sample],name='students.xlsx')
        self.assertEqual(response.status_code,200)
        result=self.post('/api/upload/commit',json={'token':response.json['token']})
        self.assertEqual(result.json['imported'],1)
        uid=result.json['student_uids'][0];self.assertRegex(uid,r'^STU-\d{6}$')
        self.assertIsNone(self.repo.get(uid)['student_name'])

    def test_11_missing_columns_bad_extensions_and_empty(self):
        response=self.upload([{'Age at enrollment':20}])
        self.assertEqual(response.json['valid_rows'],0);self.assertIn('Course',response.json['missing'])
        self.assertEqual(self.post('/api/upload/commit',json={'token':response.json['token']}).status_code,400)
        self.assertEqual(self.upload([self.sample],name='bad.exe').status_code,400)
        self.assertEqual(self.post('/api/upload',data={'file':(io.BytesIO(b''),'empty.csv')}).status_code,400)
        self.assertEqual(self.post('/api/upload',data={}).status_code,400)

    def test_12_mixed_rows_duplicates_and_no_overwrite(self):
        response=self.upload([{'Student ID':'TEST-MIXED',**self.sample},{'Student ID':'STU-000001',**self.sample},{'Student ID':'INVALID',**self.sample,'Admission grade':999}])
        self.assertEqual(response.json['valid_rows'],1)
        self.assertEqual(len(response.json['problems']),2)
        result=self.post('/api/upload/commit',json={'token':response.json['token']})
        self.assertEqual(result.json['imported'],1);self.assertEqual(len(result.json['failed_rows']),2)
        response=self.upload([{'Student ID':'DUPLICATE',**self.sample}]*2)
        self.assertEqual(response.json['valid_rows'],0)

    def test_13_exports_dashboard_and_dataset(self):
        for url in ['/exports/students.csv','/exports/students.csv?risk=High','/exports/summary.csv','/exports/template.csv']:
            response=self.client.get(url);self.assertEqual(response.status_code,200)
            self.assertIn('attachment',response.headers['Content-Disposition'])
            self.assertTrue(list(csv.reader(io.StringIO(response.data.decode('utf-8-sig')))))
        d=self.client.get('/api/dashboard').json
        self.assertEqual(sum(d['counts'].values()),d['analyzed'])
        self.assertEqual(sum(d['histogram']),d['analyzed'])
        self.assertEqual(d['total'],self.repo.count())
        self.assertTrue(d['courses']);self.assertTrue(d['importance'])
        self.assertEqual(len(self.model.source),4424)
        self.assertEqual(self.model.source['Target'].value_counts().to_dict(),{'Graduate':2209,'Dropout':1421,'Enrolled':794})
        self.assertIn(b'Not available in exported metadata',self.client.get('/model').data)

    def test_14_threshold_boundaries(self):
        for probability,level in [(0,'Low'),(.3,'Medium'),(self.model.high,'High'),(1,'High')]:
            with patch.object(self.model.calibrator,'predict',return_value=np.array([probability])):
                result=self.model.predict(self.sample)
                self.assertEqual(result['risk_level'],level)
                self.assertEqual(result['manual_review'],abs(probability-self.model.high)<=self.model.margin)

    def test_15_no_sensitive_recommendations(self):
        changed={**self.sample,'Gender':1-self.sample['Gender'],'Age at enrollment':90,'Nacionality':999,"Mother's occupation":999,"Father's qualification":999}
        self.assertEqual(recommendations(self.sample),recommendations(changed))

    def test_16_shap_failure_preserves_prediction(self):
        with patch.object(self.model.explainer,'shap_values',side_effect=RuntimeError('test failure')):
            result=self.model.predict(self.sample)
            self.assertIn('fallback',result['explanation']['method'])
            self.assertTrue(math.isfinite(result['risk_probability']))

    def test_17_csrf_and_batch_ownership(self):
        self.assertEqual(self.client.post('/api/analyze/manual',json={'features':self.sample}).status_code,403)
        self.assertEqual(self.post('/api/analyze/manual',json=[]).status_code,422)
        response=self.upload([self.sample]);token=response.json['token']
        other=self.app.test_client();other.get('/')
        with other.session_transaction() as session: csrf=session['csrf']
        self.assertEqual(other.post('/api/upload/commit',json={'token':token},headers={'X-CSRF-Token':csrf}).status_code,400)

    def test_18_model_missing_and_dataset_missing_states(self):
        with tempfile.TemporaryDirectory() as directory:
            missing=ModelService(Path(directory))
            self.assertFalse(missing.ready);self.assertTrue(missing.error);self.assertTrue(missing.dataset_error)

    def test_19_unseen_source_categories_are_explicit(self):
        rows=pd.read_csv(BASE_DIR/'artifacts'/'enrolled_students_risk_scores.csv')
        row=rows.iloc[38][self.model.features].to_dict()
        result=self.model.predict(row)
        self.assertTrue(result['data_notes'])
        self.assertEqual(row["Father's occupation"],121)

    def test_20_csv_formula_protection(self):
        self.post('/api/students',json={'Student ID':'FORMULA-TEST','Student Name':'=1+1','features':self.sample})
        response=self.client.get('/exports/students.csv?q=FORMULA-TEST')
        self.assertIn("'=1+1",response.data.decode('utf-8-sig'))

    def test_21_oversized_upload(self):
        response=self.post('/api/upload',data={'file':(io.BytesIO(b'a'*(15*1024*1024+1)),'big.csv')})
        self.assertEqual(response.status_code,413)

    def test_22_duplicate_columns(self):
        response=self.post('/api/upload',data={'file':(io.BytesIO(b'Course,Course\n1,2\n'),'duplicate.csv')})
        self.assertEqual(response.status_code,400)
        self.assertIn('unique',response.json['error'])


if __name__=='__main__': unittest.main(verbosity=2)
