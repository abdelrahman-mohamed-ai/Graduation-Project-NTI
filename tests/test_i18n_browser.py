"""Real browser checks, using a temporary server, profile and student database."""
import base64
import csv
import json
import os
from pathlib import Path
import subprocess
import tempfile
import threading
import time
import unittest
import urllib.request
from werkzeug.serving import make_server
from app import create_app
try:
    import websocket
except ImportError:
    websocket = None

CHROME=Path(os.environ.get('PROGRAMFILES','C:/Program Files'))/'Google/Chrome/Application/chrome.exe'

@unittest.skipUnless(CHROME.exists() and websocket, 'Chrome and websocket-client required for browser checks')
class BrowserLanguageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Path('test-output').mkdir(exist_ok=True)
        cls.temp=tempfile.TemporaryDirectory();root=Path(cls.temp.name)
        cls.app=create_app({'TESTING':True,'DATABASE':str(root/'browser.db')})
        cls.server=make_server('127.0.0.1',0,cls.app,threaded=True)
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()
        cls.origin='http://127.0.0.1:'+str(cls.server.server_port)
        cls.process=subprocess.Popen([str(CHROME),'--headless=new','--disable-gpu','--no-first-run','--no-default-browser-check','--remote-debugging-port=0','--user-data-dir='+str(root/'profile'),'about:blank'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        portfile=root/'profile/DevToolsActivePort'
        for _ in range(100):
            if portfile.exists():break
            time.sleep(.1)
        port=portfile.read_text().splitlines()[0]
        targets=json.load(urllib.request.urlopen('http://127.0.0.1:'+port+'/json'))
        cls.socket=websocket.create_connection(next(t['webSocketDebuggerUrl'] for t in targets if t['type']=='page'),suppress_origin=True,timeout=15)
        cls.sequence=0;cls.exceptions=[]
        cls.command('Runtime.enable');cls.command('Page.enable')
        cls.command('Emulation.setDeviceMetricsOverride',width=1440,height=1000,deviceScaleFactor=1,mobile=False)
    @classmethod
    def tearDownClass(cls):
        cls.socket.close();cls.process.terminate();cls.process.wait(timeout=15)
        cls.server.shutdown();cls.server.server_close();cls.thread.join(timeout=5)
        for _ in range(20):
            try:cls.temp.cleanup();break
            except PermissionError:time.sleep(.2)
    @classmethod
    def command(cls,method,**params):
        cls.sequence+=1;seq=cls.sequence
        cls.socket.send(json.dumps({'id':seq,'method':method,'params':params}))
        while True:
            response=json.loads(cls.socket.recv())
            if response.get('method')=='Runtime.exceptionThrown':cls.exceptions.append(response['params'])
            if response.get('id')==seq:
                if 'error' in response:raise AssertionError(response)
                return response.get('result',{})
    @classmethod
    def js(cls,expression):
        result=cls.command('Runtime.evaluate',expression=expression,returnByValue=True,awaitPromise=True)
        if result.get('exceptionDetails'):raise AssertionError(result['exceptionDetails'])
        return result.get('result',{}).get('value')
    def wait(self,expression,timeout=20):
        start=time.monotonic()
        while time.monotonic()-start<timeout:
            if self.js(expression):return
            time.sleep(.1)
        self.fail('Timed out: '+expression)
    def page(self,path,language='ar'):
        self.command('Page.navigate',url=self.origin+path+('&' if '?' in path else '?')+'lang='+language)
        self.wait('location.pathname==='+json.dumps(path.split('?')[0])+" && document.readyState==='complete' && !!window.I18N")
    def screenshot(self,name):
        self.js("new Promise(resolve=>setTimeout(resolve,1000))")
        target=Path('test-output')/(name+'.png');target.parent.mkdir(exist_ok=True)
        target.write_bytes(base64.b64decode(self.command('Page.captureScreenshot',captureBeyondViewport=False)['data']))
    def audit(self,name):
        text=self.js("""(()=>{const walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let node;const rows=[];while(node=walker.nextNode()){if(!node.parentElement?.closest('script,style,[data-i18n-skip]')&&/[A-Za-z]{2}/.test(node.textContent))rows.push(node.textContent.trim());}return [...new Set(rows)];})()""")
        Path('test-output/'+name+'-text.json').write_text(json.dumps(text,ensure_ascii=False,indent=2),encoding='utf-8')
    def test_01_arabic_pages_and_desktop_rtl(self):
        for path in ['/','/students','/analyze','/upload','/dataset','/model','/reports','/about','/students/STU-000001']:
            with self.subTest(path=path):
                self.page(path)
                self.assertEqual(self.js('document.documentElement.dir'),'rtl')
                self.assertTrue(self.js('Math.abs(document.querySelector(".sidebar").getBoundingClientRect().right-document.documentElement.clientWidth)<1'))
                self.assertTrue(self.js('document.documentElement.scrollWidth<=innerWidth'))
                self.js('new Promise(resolve=>setTimeout(resolve,300))');self.audit('arabic-'+(path.strip('/').replace('/','-') or 'dashboard'))
        self.page('/dataset');self.screenshot('arabic-dataset')
    def test_02_instant_switch_preserves_form_and_model_inputs(self):
        self.page('/analyze','en')
        self.js("document.querySelector('[data-mode=manual]').click();document.querySelector('[name=\"Student ID\"]').value='High';document.querySelector('[name=\"Student Name\"]').value='English';document.querySelector('#sample-student').click();window.languageSentinel=42")
        self.wait("!document.querySelector('#sample-student').disabled")
        self.js("for(let i=0;i<7;i++)document.querySelector('#step-next').click()")
        self.assertEqual(self.js("document.querySelector('[data-step=\"7\"]').hidden"),False)
        before=self.js("Object.fromEntries(new FormData(document.querySelector('#manual-form')))")
        self.js("document.querySelector('[data-language=ar]').click()")
        self.assertEqual(self.js('window.languageSentinel'),42)
        self.assertEqual(before,self.js("Object.fromEntries(new FormData(document.querySelector('#manual-form')))"))
        self.assertEqual(self.js("document.querySelectorAll('#manual-review [data-model-input]').length"),30)
        self.assertEqual(self.js("document.querySelector('[data-identifier=\"Student ID\"] dd').textContent"),'High')
        self.assertIn('البيانات المالية',self.js("document.querySelector('#manual-review').innerText"))
        self.screenshot('arabic-manual-review')
        self.js("document.querySelector('#manual-submit').click()")
        self.wait("!!document.querySelector('#analysis-result .risk-panel')")
        self.assertIn('مخاطر الانسحاب الأكاديمي المقدّرة بالنموذج',self.js("document.querySelector('#analysis-result').innerText"))
        self.audit('arabic-manual-result')
        score=self.js("document.querySelector('.gauge-label strong').textContent")
        self.js("document.querySelector('[data-language=en]').click()")
        self.assertIn('Calibrated Dropout Risk',self.js("document.querySelector('#analysis-result').innerText"))
        self.assertEqual(score,self.js("document.querySelector('.gauge-label strong').textContent"))
    def test_03_charts_switch_without_changing_values(self):
        self.page('/','en');self.wait("!!Chart.getChart('course-chart')")
        before=self.js("Chart.getChart('risk-donut').data.datasets[0].data")
        self.js("I18N.setLanguage('ar')")
        self.assertEqual(before,self.js("Chart.getChart('risk-donut').data.datasets[0].data"))
        self.assertEqual(self.js("Chart.getChart('risk-donut').data.labels"),['مخاطر مرتفعة','مخاطر متوسطة','مخاطر منخفضة'])
        self.assertTrue(self.js("Chart.getChart('risk-donut').options.plugins.tooltip.rtl"))
        self.screenshot('arabic-dashboard')
    def test_04_mobile_rtl_and_language_persistence(self):
        self.command('Emulation.setDeviceMetricsOverride',width=390,height=844,deviceScaleFactor=1,mobile=True)
        try:
            self.page('/dataset');self.assertTrue(self.js('document.documentElement.scrollWidth<=innerWidth'))
            self.js("document.querySelector('#menu-toggle').click()")
            self.wait("Math.abs(document.querySelector('.sidebar').getBoundingClientRect().right-innerWidth)<1")
            self.screenshot('arabic-mobile-navigation')
            self.js("document.querySelector('a.nav-item[href=\"/students\"]').click()")
            self.wait("location.pathname==='/students'&&document.readyState==='complete'")
            self.assertEqual(self.js('document.documentElement.dir'),'rtl')
        finally:self.command('Emulation.setDeviceMetricsOverride',width=1440,height=1000,deviceScaleFactor=1,mobile=False)
    def test_05_feature_filters_and_dynamic_upload_arabic(self):
        self.page('/dataset');self.js("document.querySelector('[data-feature-group=Financial]').click()")
        self.assertEqual(self.js("document.querySelectorAll('#dictionary-rows tr:not([hidden])').length"),3)
        self.page('/upload','en')
        model=self.app.extensions['model_service'];row=model.validate(model.source.loc[model.source.Target=='Enrolled',model.features].iloc[0].to_dict())
        path=Path(self.temp.name)/'language-upload.csv'
        with path.open('w',newline='') as file:
            writer=csv.DictWriter(file,fieldnames=['Student ID',*model.features]);writer.writeheader();writer.writerow({'Student ID':'BROWSER-LANGUAGE',**row})
        root=self.command('DOM.getDocument')['root']['nodeId']
        node=self.command('DOM.querySelector',nodeId=root,selector='#upload-file')['nodeId']
        self.command('DOM.setFileInputFiles',nodeId=node,files=[str(path)])
        self.js("document.querySelector('#preview-upload').click()")
        self.wait("!!document.querySelector('#commit-upload')")
        self.js("I18N.setLanguage('ar')")
        self.assertIn('الأعمدة المطلوبة موجودة',self.js("document.querySelector('#upload-preview').innerText"))
        self.js("document.querySelector('#commit-upload').click()")
        self.wait("!document.querySelector('#upload-summary').hidden")
        self.assertIn('تم التحليل بنجاح',self.js("document.querySelector('#upload-summary').innerText"))
        self.audit('arabic-upload-result')
    def test_06_english_pages_and_current_url_preserved(self):
        for path in ['/','/students','/analyze','/upload','/dataset','/model','/reports','/about','/students/STU-000001']:
            with self.subTest(path=path):
                self.page(path,'en')
                self.assertEqual(self.js('document.documentElement.lang'),'en')
                self.assertEqual(self.js('document.documentElement.dir'),'ltr')
                self.assertEqual(self.js('document.querySelector(".sidebar").getBoundingClientRect().left'),0)
                self.assertTrue(self.js('document.documentElement.scrollWidth<=innerWidth'))
        self.page('/analyze?mode=manual','en')
        self.js("I18N.setLanguage('ar')")
        self.assertEqual(self.js('location.pathname+location.search'),'/analyze?mode=manual')
        self.js("I18N.setLanguage('en')")
        self.assertEqual(self.js('location.pathname+location.search'),'/analyze?mode=manual')
        self.page('/','en');self.wait("!!Chart.getChart('course-chart')");self.screenshot('english-dashboard')
    def test_07_all_manual_steps_validation_loading_and_toasts(self):
        self.page('/analyze')
        self.js("document.querySelector('[data-mode=manual]').click();document.querySelector('#step-next').click();document.querySelector('#step-next').click()")
        self.wait("document.querySelector('[data-step=\"1\"] .field-error').textContent.includes('مطلوب')")
        self.js("document.querySelector('#sample-student').click()")
        self.wait("!document.querySelector('#sample-student').disabled")
        self.assertIn('تم تحميل بيانات طالب حقيقي',self.js("document.querySelector('#toast-region').textContent"))
        for index in range(1,8):
            self.assertFalse(self.js("document.querySelector('[data-step=\""+str(index)+"\"]').hidden"))
            self.assertTrue(self.js("/[\\u0600-\\u06ff]/.test(document.querySelector('[data-step=\""+str(index)+"\"] legend').textContent)"))
            if index<7:self.js("document.querySelector('#step-next').click()")
        self.js("document.querySelector('.student-review').scrollIntoView()")
        self.screenshot('arabic-review-values')
        self.js("window.originalFetch=fetch;window.fetch=(...args)=>String(args[0]).includes('/api/analyze/manual')?new Promise(resolve=>setTimeout(()=>resolve(originalFetch(...args)),700)):originalFetch(...args);document.querySelector('#manual-submit').click()")
        self.assertIn('جارٍ تحليل مخاطر الطالب',self.js("document.querySelector('#analysis-result').textContent"))
        self.wait("!!document.querySelector('.risk-panel')")
        self.js("document.querySelector('#analysis-result').scrollIntoView()")
        self.screenshot('arabic-prediction-result')
    def test_08_dynamic_search_tooltips_notifications_and_filters(self):
        self.page('/students')
        self.js("const search=document.querySelector('#global-search');search.value='NO-SUCH-STUDENT-8934';search.dispatchEvent(new Event('input',{bubbles:true}))")
        self.wait("document.querySelector('#global-results').textContent.includes('لم يتم العثور')")
        self.js("document.querySelector('#more-filters').click();const select=document.querySelector('#source-filter');select.value='Enrolled dataset';select.dispatchEvent(new Event('change',{bubbles:true}))")
        self.wait("document.querySelector('#table-count').textContent.includes('794')")
        self.assertEqual(self.js("document.querySelector('#source-filter').value"),'Enrolled dataset')
        self.wait("!!document.querySelector('time[data-i18n-date]')")
        self.assertTrue(self.js("/[\\u0600-\\u06ff]/.test(document.querySelector('time[data-i18n-date]').textContent)"))
        self.js("I18N.setLanguage('en')")
        self.assertFalse(self.js("/[\\u0600-\\u06ff]/.test(document.querySelector('time[data-i18n-date]').textContent)"))
        self.page('/')
        self.js("document.querySelector('.tooltip-trigger').click()")
        self.assertIn(str(self.app.extensions['model_service'].high),self.js("document.querySelector('[role=tooltip]').textContent"))
        self.assertIn('احتمال الانسحاب المقدّر',self.js("document.querySelector('[role=tooltip]').textContent"))
        self.js("document.querySelector('#notifications').click()")
        self.wait("document.querySelector('#notification-content').textContent.includes('المراجعة البشرية')")
        self.assertFalse(self.js("/[A-Za-z]{3}/.test(document.querySelector('#notification-content').textContent)"))
    def test_09_mobile_pages_and_rtl_visuals(self):
        for width in (390,320):
            self.command('Emulation.setDeviceMetricsOverride',width=width,height=844,deviceScaleFactor=1,mobile=True)
            try:
                for path in ['/','/students','/analyze','/upload','/dataset','/model','/reports','/about','/students/STU-000001']:
                    with self.subTest(path=path,width=width):
                        self.page(path);self.assertTrue(self.js('document.documentElement.scrollWidth<=innerWidth'))
                self.page('/dataset');self.screenshot('arabic-mobile-dataset-'+str(width))
            finally:self.command('Emulation.setDeviceMetricsOverride',width=1440,height=1000,deviceScaleFactor=1,mobile=False)
        self.page('/dataset');self.js("document.querySelector('.prediction-stages').scrollIntoView()")
        self.screenshot('arabic-prediction-stages')
        self.js("document.querySelector('.feature-explorer').scrollIntoView()")
        self.screenshot('arabic-feature-table')
    def test_99_no_javascript_exceptions(self):self.assertEqual(self.exceptions,[])
    def test_10_intro_session_skip_and_languages(self):
        for language,width in [('en',1440),('ar',1440),('en',390),('ar',390)]:
            self.command('Emulation.setDeviceMetricsOverride',width=width,height=900,deviceScaleFactor=1,mobile=width<760)
            self.js("sessionStorage.removeItem('eduguard.intro.seen')")
            self.page('/',language)
            self.assertTrue(self.js("!!document.querySelector('#app-intro:not([hidden])')"))
            expected='الإنذار المبكر لمخاطر الطلاب' if language=='ar' else 'Student Risk Intelligence'
            self.assertIn(expected,self.js("document.querySelector('#app-intro').textContent"))
            self.assertTrue(self.js('document.documentElement.scrollWidth<=innerWidth'))
            self.screenshot('intro-'+language+'-'+str(width))
            self.wait("!document.querySelector('#app-intro')",timeout=4)
            self.page('/students',language);self.assertFalse(self.js("!!document.querySelector('#app-intro')"))
            self.command('Page.reload');self.wait("document.readyState==='complete'&&!!window.I18N")
            self.assertFalse(self.js("!!document.querySelector('#app-intro')"))
        self.js("sessionStorage.removeItem('eduguard.intro.seen')");self.page('/','en')
        self.js("document.querySelector('#intro-skip').focus();document.querySelector('#intro-skip').click()")
        self.wait("!document.querySelector('#app-intro')",timeout=2)
        self.command('Emulation.setDeviceMetricsOverride',width=1440,height=1000,deviceScaleFactor=1,mobile=False)
    def test_11_intro_reduced_motion(self):
        self.command('Emulation.setEmulatedMedia',features=[{'name':'prefers-reduced-motion','value':'reduce'}])
        try:
            self.js("sessionStorage.removeItem('eduguard.intro.seen')");self.page('/','ar')
            self.wait("!document.querySelector('#app-intro')",timeout=2)
            self.assertTrue(self.js("matchMedia('(prefers-reduced-motion: reduce)').matches"))
        finally:self.command('Emulation.setEmulatedMedia',features=[])
    def test_12_complete_responsive_matrix(self):
        for width in (320,360,390,430,768,1024,1280,1440,1920,2560):
            self.command('Emulation.setDeviceMetricsOverride',width=width,height=1000,deviceScaleFactor=1,mobile=width<760)
            for language in ('en','ar'):
                for path in ['/','/students','/analyze','/upload','/students/STU-000001','/dataset','/model','/reports','/about']:
                    with self.subTest(width=width,language=language,path=path):
                        self.page(path,language)
                        self.wait("!document.querySelector('#app-intro')")
                        self.js('new Promise(resolve=>setTimeout(resolve,100))')
                        self.assertTrue(self.js('document.documentElement.scrollWidth<=innerWidth'),str(self.js('({width:innerWidth,scroll:document.documentElement.scrollWidth})')))
                        if path=='/analyze':
                            self.js("document.querySelector('[data-mode=manual]').click();document.querySelector('#sample-student').click()")
                            self.wait("!document.querySelector('#sample-student').disabled")
                            for step in range(8):
                                self.assertTrue(self.js('document.documentElement.scrollWidth<=innerWidth'))
                                if step<7:self.js("document.querySelector('#step-next').click()")
                if width in (390,768,1440):
                    self.page('/',language);self.wait("!!Chart.getChart('course-chart')")
                    self.screenshot('responsive-'+language+'-'+str(width))
        self.command('Emulation.setDeviceMetricsOverride',width=1440,height=1000,deviceScaleFactor=1,mobile=False)
    def test_13_powerpoint_viewer_languages_controls_and_responsive(self):
        for language in ('en','ar'):
            for width in (320,375,768,1440,1920):
                self.command('Emulation.setDeviceMetricsOverride',width=width,height=900,deviceScaleFactor=1,mobile=width<760)
                self.js("try{sessionStorage.setItem('eduguard.intro.seen','1')}catch(e){}")
                self.page('/powerpoint',language)
                self.wait("!!window.presentationViewer && document.querySelectorAll('.pp-slide').length===20")
                self.assertEqual(self.js('document.documentElement.dir'),'rtl' if language=='ar' else 'ltr')
                self.assertTrue(self.js('document.documentElement.scrollWidth<=innerWidth'))
                self.assertEqual(self.js("getComputedStyle(document.body).overflowY"),'hidden')
                self.assertTrue(self.js("document.documentElement.scrollHeight<=innerHeight+1"))
                self.assertEqual(self.js("document.querySelectorAll('.pp-slide.active').length"),1)
                self.assertTrue(self.js("document.querySelectorAll('.pp-slide:not(.active)').length===19"))
                self.assertEqual(self.js("document.querySelector('#pp-count').textContent"),'1 / 20')
                self.js("window.presentationViewer.go(1)")
                self.assertEqual(self.js("document.querySelector('#pp-count').textContent"),'2 / 20')
                self.js("document.dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowLeft',bubbles:true}))")
                expected_count = '1 / 20' if language == 'en' else '3 / 20'
                self.assertEqual(self.js("document.querySelector('#pp-count').textContent"),expected_count)
                self.js("I18N.setLanguage(I18N.language==='en'?'ar':'en')")
                expected = 'ar' if language == 'en' else 'en'
                self.wait("document.documentElement.lang===" + json.dumps(expected))
                self.assertTrue(self.js("/[\\u0600-\\u06ff]/.test(document.querySelector('.pp-slide.active').innerText)")) if language=='en' else self.assertTrue(self.js("/[A-Za-z]{3}/.test(document.querySelector('.pp-slide.active').innerText)"))
                self.assertEqual(self.js("document.querySelector('#pp-count').textContent"),expected_count)
                self.js("window.presentationViewer.state.index=12;window.presentationViewer.render()")
                self.wait("document.querySelector('#pp-count').textContent==='13 / 20'")
                self.assertIn('92.77%',self.js("document.querySelector('.pp-slide.active').innerText"))
                self.assertIn('98.66%',self.js("document.querySelector('.pp-slide.active').innerText"))
                self.assertEqual(self.js("document.querySelectorAll('.pp-slide.active').length"),1)
        self.command('Emulation.setDeviceMetricsOverride',width=1440,height=1000,deviceScaleFactor=1,mobile=False)
    def test_14_powerpoint_true_sixteen_nine_geometry_matrix(self):
        viewports=((1366,768),(1536,864),(1920,1080),(2560,1440),(1024,768),(768,900),(375,812))
        for language in ('en','ar'):
            for width,height in viewports:
                self.command('Emulation.setDeviceMetricsOverride',width=width,height=height,deviceScaleFactor=1,mobile=width<760)
                self.page('/powerpoint',language)
                self.wait("!!window.presentationViewer && document.querySelectorAll('.pp-slide.active').length===1")
                geometry=self.js("(()=>{const frame=document.querySelector('#pp-slide-frame').getBoundingClientRect();const stage=document.querySelector('#pp-stage').getBoundingClientRect();const controls=document.querySelector('.pp-controls').getBoundingClientRect();const app=document.querySelector('#powerpoint-app').getBoundingClientRect();return {ratio:frame.width/frame.height,frameWidth:frame.width,frameHeight:frame.height,stageWidth:stage.width,stageHeight:stage.height,controlsTop:controls.top,controlsBottom:controls.bottom,appTop:app.top,appBottom:app.bottom,progressWidth:document.querySelector('#pp-progress').getBoundingClientRect().width,scrollWidth:document.documentElement.scrollWidth,scrollHeight:document.documentElement.scrollHeight}})()")
                self.assertAlmostEqual(geometry['ratio'],16/9,delta=.02,msg=str((language,width,height,geometry)))
                self.assertLessEqual(geometry['frameWidth'],geometry['stageWidth']+1,str((language,width,height,geometry)))
                self.assertLessEqual(geometry['frameHeight'],geometry['stageHeight']+1,str((language,width,height,geometry)))
                self.assertGreaterEqual(geometry['controlsTop'],geometry['appTop'],str((language,width,height,geometry)))
                self.assertLessEqual(geometry['controlsBottom'],geometry['appBottom']+1,str((language,width,height,geometry)))
                self.assertGreater(geometry['progressWidth'],0,str((language,width,height,geometry)))
                self.assertLessEqual(geometry['scrollWidth'],width+1,str((language,width,height,geometry)))
                self.assertLessEqual(geometry['scrollHeight'],height+1,str((language,width,height,geometry)))
        self.command('Emulation.setDeviceMetricsOverride',width=1440,height=1000,deviceScaleFactor=1,mobile=False)
