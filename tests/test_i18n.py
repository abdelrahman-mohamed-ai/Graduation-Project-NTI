"""Language is a view concern: exercise real artifacts with isolated storage."""
import csv
import io
import json
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from unittest.mock import patch
from app import create_app
from services.i18n_service import CATALOG, translate


class Controls(HTMLParser):
    def __init__(self, html):
        super().__init__(); self.fields=[]; self.options=[]; self.feed(html)
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if tag in ('input','select') and attrs.get('name'): self.fields.append(attrs['name'])
        if tag=='option': self.options.append(attrs.get('value'))


class LanguageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory()
        cls.app=create_app({'TESTING':True,'DATABASE':str(Path(cls.temp.name)/'language.db')})
        cls.model=cls.app.extensions['model_service'];cls.repo=cls.app.extensions['student_repository']
    @classmethod
    def tearDownClass(cls): cls.temp.cleanup()
    def setUp(self):
        self.client=self.app.test_client();self.client.get('/')
        with self.client.session_transaction() as session:self.csrf=session['csrf']
        self.sample=self.client.get('/api/sample').json['features']
    def post(self,url,**kwargs):return self.client.post(url,headers={'X-CSRF-Token':self.csrf},**kwargs)
    def manual(self,language):
        self.client.get('/analyze?lang='+language)
        return self.post('/api/analyze/manual',json={'Student ID':'High','Student Name':'English','features':self.sample})
    def test_01_english_default(self):
        self.assertIn('<html lang="en" dir="ltr">',self.client.get('/').text)
    def test_02_arabic_switch_persists(self):
        self.client.get('/?lang=ar')
        self.assertIn('<html lang="ar" dir="rtl">',self.client.get('/reports').text)
    def test_03_all_arabic_routes(self):
        for path in ['/','/dashboard','/students','/analyze','/upload','/model','/dataset','/reports','/powerpoint','/about']:
            with self.subTest(path=path):
                response=self.client.get(path+'?lang=ar');self.assertEqual(response.status_code,200)
                self.assertIn('<html lang="ar" dir="rtl">',response.text)
    def test_04_switch_back_ltr(self):
        self.client.get('/?lang=ar');self.client.get('/?lang=en')
        self.assertIn('<html lang="en" dir="ltr">',self.client.get('/dataset').text)
    def test_05_navigation_and_codes_unchanged(self):
        en=Controls(self.client.get('/analyze?lang=en').text);ar=Controls(self.client.get('/analyze?lang=ar').text)
        self.assertEqual(en.fields,ar.fields);self.assertEqual(en.options,ar.options)
        for feature in self.model.features:self.assertIn(feature,ar.fields)
    def test_06_manual_english(self): self.assertEqual(self.manual('en').status_code,200)
    def test_07_manual_arabic_exact_probability(self):
        en=self.manual('en').json['result'];response=self.manual('ar');self.assertEqual(response.status_code,200)
        ar=response.json['result'];self.assertEqual(en,ar)
        self.assertEqual(en['risk_probability'],ar['risk_probability'])
    def test_08_existing_student_exact_probability(self):
        self.client.get('/?lang=en');en=self.post('/api/analyze/STU-000001').json['result']
        self.client.get('/?lang=ar');ar=self.post('/api/analyze/STU-000001').json['result']
        self.assertEqual(en,ar);self.assertEqual(en['risk_probability'],ar['risk_probability'])
    def test_09_thresholds_identical(self):
        thresholds=(self.model.medium,self.model.high,self.model.margin)
        en=self.manual('en').json['result'];ar=self.manual('ar').json['result']
        self.assertEqual(thresholds,(self.model.medium,self.model.high,self.model.margin))
        self.assertEqual((en['risk_level'],en['manual_review']),(ar['risk_level'],ar['manual_review']))
        for language in ('en','ar'):
            self.assertIn(str(self.model.high),self.client.get('/?lang='+language).text)
    def test_10_csv_import_both_languages(self):
        for language in ('en','ar'):
            self.client.get('/upload?lang='+language)
            row={'Student ID':'LANG-CSV-'+language,**self.sample};stream=io.StringIO()
            writer=csv.DictWriter(stream,fieldnames=list(row));writer.writeheader();writer.writerow(row)
            preview=self.post('/api/upload',data={'file':(io.BytesIO(stream.getvalue().encode()),'students.csv')},content_type='multipart/form-data')
            self.assertEqual(preview.status_code,200);self.assertEqual(preview.json['valid_rows'],1)
            result=self.post('/api/upload/commit',json={'token':preview.json['token']})
            self.assertEqual(result.status_code,200);self.assertEqual(result.json['imported'],1)
    def test_11_switch_does_not_write_database(self):
        with self.repo.connection() as db:before='\n'.join(db.iterdump())
        for path in ['/','/students','/analyze','/upload','/model','/dataset','/reports','/powerpoint','/about','/students/STU-000001']:
            for language in ('ar','en'):self.client.get(path+'?lang='+language)
        with self.repo.connection() as db:after='\n'.join(db.iterdump())
        self.assertEqual(before,after)
    def test_12_student_details_arabic(self):
        response=self.client.get('/students/STU-000001?lang=ar')
        self.assertEqual(response.status_code,200);self.assertIn('الملخص المالي',response.text)
        self.assertIn('سجل التحليلات',response.text)
    def test_13_dataset_arabic(self):
        html=self.client.get('/dataset?lang=ar').text
        self.assertIn('فهم بيانات الطلاب',html);self.assertIn('تسرب البيانات',html)
        self.assertIn('وليس نسبة الحضور',html)
    def test_14_api_presentation_catalog_shared(self):
        html=self.client.get('/analyze?lang=ar').text
        embedded=html.split('<script id="i18n-catalog" type="application/json">')[1].split('</script>')[0]
        self.assertEqual(json.loads(embedded),CATALOG)
        self.assertEqual(translate('Calibrated Dropout Risk'),'مخاطر الانسحاب الأكاديمي المقدّرة بالنموذج')
        self.assertEqual(translate('High'),'مرتفع')
    def test_15_exact_feature_names_at_prediction(self):
        original=self.model.model.predict_proba
        with patch.object(self.model.model,'predict_proba',wraps=original) as predict:
            for language in ('en','ar'):
                response=self.manual(language);self.assertEqual(response.status_code,200)
                frame=predict.call_args.args[0]
                self.assertEqual(list(frame.columns),self.model.features)
                self.assertNotIn('Student ID',frame.columns);self.assertNotIn('Student Name',frame.columns)
    def test_16_dictionary_and_category_coverage(self):
        for field in self.model.dictionary:
            for key in ['Feature','Type','What it means','Encoding / unit','Why it may matter (not causal)','Availability']:
                value=field[key];self.assertNotEqual(value,translate(value),value)
        for field in self.model.schema:
            self.assertNotEqual(field['label'],translate(field['label']))
            for option in field['options'] or []:self.assertNotEqual(option['label'],translate(option['label']))
    def test_17_invalid_language_falls_back_to_english(self):
        self.assertIn('<html lang="en" dir="ltr">',self.client.get('/?lang=invalid').text)
    def test_18_error_page_arabic(self):
        response=self.client.get('/not-a-route?lang=ar')
        self.assertEqual(response.status_code,404);self.assertIn('لم يتم العثور على هذه الصفحة',response.text)
    def test_19_export_feature_headers_are_canonical(self):
        en=self.client.get('/exports/template.csv?lang=en').data
        ar=self.client.get('/exports/template.csv?lang=ar').data
        self.assertEqual(en,ar)
    def test_20_source_filter_values_are_canonical(self):
        for language in ('en','ar'):
            options=Controls(self.client.get('/students?lang='+language).text).options
            for value in ('Enrolled dataset','Upload','Manual entry','High','Medium','Low'):
                self.assertIn(value,options)
    def test_21_semester_two_stays_excluded(self):
        for language in ('en','ar'):
            result=self.manual(language).json['result']
            self.assertEqual(list(result['features']),self.model.features)
            self.assertFalse(any('2nd sem' in key for key in result['features']))

    def test_22_powerpoint_language_switch_and_rtl(self):
        english = self.client.get('/powerpoint?lang=en').text
        arabic = self.client.get('/powerpoint?lang=ar').text
        self.assertIn('<html lang="en" dir="ltr">', english)
        self.assertIn('<html lang="ar" dir="rtl">', arabic)
        self.assertIn('العرض التقديمي', arabic)
        self.assertEqual(translate('PowerPoint'), 'العرض التقديمي')
        self.assertIn('"type": "conclusion"', english)
        self.assertIn('"type": "conclusion"', arabic)
        self.assertIn('"title": "Model selection and cross-validation"', english)
        arabic_payload = json.loads(arabic.split('<script id="presentation-data" type="application/json">', 1)[1].split('</script>', 1)[0])
        self.assertEqual(len(arabic_payload['slides']['ar']), 20)
        self.assertEqual(arabic_payload['slides']['ar'][17]['type'], 'enrolled')
