import os
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from app import create_app
from config import BASE_DIR, deployment_config

class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.path=str(Path(self.temp.name)/'release.db')
    def app(self):return create_app({'TESTING':True,'DATABASE':self.path,'SEED_DATABASE':False})
    def test_intro_assets_load(self):
        client=self.app().test_client()
        for url in ['/static/js/intro.js','/static/css/intro.css','/static/css/responsive.css']:
            with client.get(url) as response:self.assertEqual(response.status_code,200)
        self.assertIn('id="app-intro"',client.get('/').text)

    def test_powerpoint_assets_and_route_load(self):
        client=self.app().test_client()
        self.assertEqual(client.get('/powerpoint?lang=en').status_code,200)
        self.assertEqual(client.get('/powerpoint?lang=ar').status_code,200)
        for url in ['/static/js/powerpoint.js','/static/css/powerpoint.css']:
            self.assertEqual(client.get(url).status_code,200)
        js=(BASE_DIR/'static/js/powerpoint.js').read_text(encoding='utf-8')
        css=(BASE_DIR/'static/css/powerpoint.css').read_text(encoding='utf-8')
        self.assertIn('prefers-reduced-motion',css)
        self.assertIn('requestFullscreen',js)
        self.assertNotIn('<video',css+js)

    def test_health_route_returns_public_status_only(self):
        response=self.app().test_client().get('/health')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.get_json(),{'status':'ok'})
    def test_intro_language(self):
        client=self.app().test_client()
        self.assertIn('Early Detection. Explainable Risk. Better Intervention.',client.get('/?lang=en').text)
        html=client.get('/?lang=ar').text
        self.assertIn('الإنذار المبكر لمخاطر الطلاب',html);self.assertIn('اكتشاف مبكر • تفسير واضح • تدخل أفضل',html)
        self.assertIn('>تخطي</button>',html)
    def test_production_disables_debug_and_uses_secure_cookies(self):
        with patch.dict(os.environ,{'EDUGUARD_ENV':'production','SECRET_KEY':'test-only-key','EDUGUARD_DATABASE_PATH':self.path,'FLASK_DEBUG':'1'}):
            app=self.app();self.assertFalse(app.debug);self.assertFalse(app.config['PROPAGATE_EXCEPTIONS'])
            response=app.test_client().get('/',base_url='https://example.test')
            self.assertIn('Secure',response.headers['Set-Cookie']);self.assertIn('Strict-Transport-Security',response.headers)
    def test_production_requires_key_and_storage(self):
        with patch.dict(os.environ,{'EDUGUARD_ENV':'production'},clear=True):
            with self.assertRaisesRegex(RuntimeError,'SECRET_KEY'):deployment_config()
            os.environ['SECRET_KEY']='test-only-key'
            with self.assertRaisesRegex(RuntimeError,'persistent storage'):deployment_config()
    def test_postgres_never_silently_falls_back(self):
        with patch.dict(os.environ,{'DATABASE_URL':'postgresql://example.invalid/demo'}):
            with self.assertRaisesRegex(RuntimeError,'not supported'):deployment_config()
    def test_frontend_asset_paths_are_deploy_safe(self):
        for folder in ['templates','static/js','static/css']:
            for file in (BASE_DIR/folder).glob('*'):
                if file.suffix not in ('.js','.css','.html'):continue
                text=file.read_text(encoding='utf-8')
                self.assertIsNone(re.search(r'(?:https?://(?:localhost|127\.0\.0\.1)|file://|[A-Z]:\\)',text),str(file))
        html=self.app().test_client().get('/').text
        self.assertIn('width=device-width, initial-scale=1',html)
    def test_lightweight_intro_and_reduced_motion(self):
        js=(BASE_DIR/'static/js/intro.js').read_text();css=(BASE_DIR/'static/css/intro.css').read_text()
        self.assertLess(len(js.encode())+len(css.encode()),8000)
        self.assertIn('sessionStorage',js);self.assertIn('prefers-reduced-motion',css)
        self.assertNotIn('<video',(BASE_DIR/'templates/_intro.html').read_text(encoding='utf-8'))
