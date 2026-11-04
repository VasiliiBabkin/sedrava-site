"""Independent browser acceptance of the actual source-generated native site and embeds."""
import functools,hashlib,html,importlib.metadata,json,os,re,shutil,tempfile,threading,time,unittest
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'build/native-site';EVIDENCE=ROOT/'build/native-browser-evidence'
class ControlledEndpoint(SimpleHTTPRequestHandler):
    mode='normal';rows=[{'id':1,'title':'Real CI product','available':True}];calls=[]
    def log_message(self,*args):pass
    def reply(self,value,status=200):
        raw=(value if isinstance(value,str) else json.dumps(value)).encode();self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(raw)));self.end_headers()
        try:self.wfile.write(raw)
        except (BrokenPipeError,ConnectionResetError):pass
    def do_GET(self):
        if urlsplit(self.path).path!='/api/products':return super().do_GET()
        self.calls.append({'method':'GET','path':self.path})
        if self.mode=='missing':return self.reply({'error':'CI-only endpoint not provided'},404)
        if self.mode=='error':return self.reply({'error':'fixture unavailable'},503)
        if self.mode=='invalid':return self.reply('[{"id":1,"id":2,"title":"bad","available":true}]')
        if self.mode=='slow':time.sleep(1.3)
        return self.reply(self.rows)
    def mutate(self):
        value=json.loads(self.rfile.read(int(self.headers.get('Content-Length','0')))) if self.headers.get('Content-Length') else None
        self.calls.append({'method':self.command,'path':self.path,'body':value})
        if self.command=='DELETE':ControlledEndpoint.rows=[];return self.reply('',204)
        if not isinstance(value,dict) or set(value)!={'title','available'} or type(value['title']) is not str or type(value['available']) is not bool:return self.reply({'error':'invalid request'},422)
        row={'id':1,**value};ControlledEndpoint.rows=[row];return self.reply(row)
    do_POST=mutate;do_PUT=mutate;do_PATCH=mutate;do_DELETE=mutate
class NativeSiteBrowser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture=tempfile.TemporaryDirectory(prefix='native-site-acceptance-');cls.output=Path(cls.fixture.name)/'site';shutil.copytree(OUT,cls.output)
        cls.demo_sources={name:(ROOT/'sedrava-next/demos'/f'{name}.sdr').read_text() for name in ('counter','tasks','crm','catalog')}
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(ControlledEndpoint,directory=str(cls.output)));cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()
        cls.pw=sync_playwright().start();cls.engine=os.environ.get('SEDRAVA_BROWSER','chromium')
        options={'executable_path':os.environ.get('SEDRAVA_CHROMIUM') or shutil.which('chromium'),'args':['--no-sandbox']} if cls.engine=='chromium' else {}
        cls.browser=getattr(cls.pw,cls.engine).launch(**options);cls.base='http://127.0.0.1:'+str(cls.server.server_port);EVIDENCE.mkdir(parents=True,exist_ok=True)
        (EVIDENCE/'toolchain.json').write_text(json.dumps({'engine':cls.engine,'version':cls.browser.version,'playwright':importlib.metadata.version('playwright')},indent=2))
    @classmethod
    def tearDownClass(cls):cls.browser.close();cls.pw.stop();cls.server.shutdown();cls.server.server_close();cls.thread.join();cls.fixture.cleanup()
    def setUp(self):
        ControlledEndpoint.mode='normal';ControlledEndpoint.rows=[{'id':1,'title':'Real CI product','available':True}];ControlledEndpoint.calls=[]
        self.context=self.browser.new_context();self.context.tracing.start(screenshots=True,snapshots=True);self.page=self.context.new_page();self.errors=[];self.page.on('pageerror',lambda e:self.errors.append(str(e)))
    def tearDown(self):
        self.context.tracing.stop(path=str(EVIDENCE/(self._testMethodName+'.zip')));self.context.close();self.assertEqual(self.errors,[],'Unhandled JavaScript exception')
    def goto(self,path):
        response=self.page.goto(self.base+path);self.assertIn(response.status,(200,304))
        # Firefox/WebKit expose a legitimate 304 for a revalidated navigation.
        # Verify the rendered cached page, not merely a permissive status code.
        file=self.output/path.strip('/')/'index.html';expected=html.unescape(re.search(r'<title>(.*?)</title>',file.read_text(),re.S)[1])
        expect(self.page).to_have_title(expected);expect(self.page.get_by_role('heading',level=1)).to_be_visible();return self.page
    def demo(self,name):
        panel=self.page.locator('[data-demo="/live/'+name+'/"]');panel.locator('iframe').scroll_into_view_if_needed();return panel,panel.frame_locator('iframe')
    def reload_demo(self,panel,reset=False):
        route=panel.get_attribute('data-demo')
        with self.page.expect_event('framenavigated',predicate=lambda f:f.parent_frame is not None and urlsplit(f.url).path.startswith(route)):
            panel.get_by_role('button',name='Reset this demo / Сбросить пример' if reset else 'Reload / Перезагрузить',exact=True).click()
    def test_bilingual_routes_navigation_metadata_and_provenance(self):
        p=self.goto('/');self.assertTrue(p.get_by_role('heading',name='This website is built with Sedrava',exact=True).is_visible())
        self.assertEqual(p.evaluate('async()=>{await document.fonts.ready;const faces=await document.fonts.load("400 16px SedravaInter","Alice Алиса");return faces.map(f=>f.status)}'),['loaded','loaded'])
        self.assertEqual(p.locator('astro-island').count(),0);p.get_by_role('link',name='Documentation',exact=True).click()
        p.get_by_role('link',name='Русский',exact=True).click();self.assertTrue(p.url.endswith('/ru/getting-started/'))
        self.assertTrue(p.get_by_role('heading',name='Начало работы',exact=True).is_visible())
        self.assertTrue(p.locator('.s-sidebar a[aria-current=page]').is_visible())
        p.set_viewport_size({'width':390,'height':900});expect(p.locator('.s-sidebar')).not_to_have_attribute('open','')
        p.locator('.s-sidebar summary').click();expect(p.locator('.s-sidebar a[aria-current=page]')).to_be_visible()
        p.locator('.s-sidebar summary').click();expect(p.locator('.s-sidebar')).not_to_have_attribute('open','')
        p.set_viewport_size({'width':1440,'height':900});expect(p.locator('.s-sidebar')).to_have_attribute('open','');expect(p.locator('.s-sidebar a[aria-current=page]')).to_be_visible()
        p.get_by_role('link',name='Происхождение сборки',exact=True).click();self.assertIn(json.loads((ROOT/'sedrava-next/compiler.json').read_text())['sha'],p.inner_text('body'))
        self.assertEqual(p.locator('link[rel=canonical]').get_attribute('href'),'https://dev.virtreal.ru/ru/provenance/')
        self.assertIn('Disallow: /',p.request.get(self.base+'/robots.txt').text())
    def test_offline_bilingual_search_keyboard_no_results_and_escaping(self):
        p=self.goto('/getting-started/');field=p.get_by_label('Search documentation',exact=True)
        self.context.route('**/*',lambda route:route.abort())
        field.fill('АТОМАР');expect(p.locator('[data-search-results] a').first).to_be_visible();self.assertIn('ru',p.locator('[data-search-results]').inner_text())
        field.press('ArrowDown');self.assertEqual(p.evaluate('document.activeElement.tagName'),'A');p.keyboard.press('ArrowUp');self.assertTrue(field.evaluate('e=>e===document.activeElement'))
        field.fill('atomic');self.assertIn('en',p.locator('[data-search-results]').inner_text())
        field.fill('<img src=x onerror=alert(1)>');self.assertEqual(p.locator('[data-search-results] img').count(),0);self.assertIn('No results',p.locator('[data-search-status]').inner_text())
        field.press('Escape');self.assertEqual(field.input_value(),'');self.assertEqual(p.locator('[data-search-results] a').count(),0)
    def test_counter_inline_exact_source_copy_persistence_and_scoped_reset(self):
        p=self.goto('/examples/');panel,frame=self.demo('counter');source=self.demo_sources['counter']
        self.assertEqual(panel.locator('code').text_content(),source)
        self.assertEqual(p.request.get(self.base+'/'+panel.get_attribute('data-demo').strip('/')+'/index.html').status,200)
        frame.get_by_role('button',name='Add one',exact=True).click();frame.get_by_role('button',name='Add one',exact=True).click();expect(frame.locator('output[data-state=count]')).to_have_text('2')
        p.evaluate('localStorage.setItem("unrelated-site-state","retained")');self.reload_demo(panel);expect(frame.locator('output[data-state=count]')).to_have_text('2')
        if self.engine=='chromium':self.context.grant_permissions(['clipboard-read','clipboard-write'],origin=self.base)
        panel.get_by_role('button',name='Copy / Копировать',exact=True).click();expect(panel.locator('[data-copy-status]')).to_have_text('Copied / Скопировано')
        if self.engine=='chromium':self.assertEqual(p.evaluate('navigator.clipboard.readText()'),source)
        self.reload_demo(panel,reset=True);expect(frame.locator('output[data-state=count]')).to_have_text('0')
        self.assertEqual(p.evaluate('localStorage.getItem("unrelated-site-state")'),'retained')
    def test_tasks_crud_search_filter_routes_reload_validation_and_delete(self):
        p=self.goto('/ru/examples/');panel,f=self.demo('tasks')
        self.assertEqual(p.locator('html').evaluate('e=>getComputedStyle(e).scrollBehavior'),'auto')
        self.assertEqual(p.locator('.s-navbar').evaluate('e=>getComputedStyle(e).position'),'static')
        self.assertEqual(f.locator('html').evaluate('e=>getComputedStyle(e).scrollBehavior'),'auto')
        f.get_by_label('New task',exact=True).fill('Native docs task');f.get_by_role('button',name='Add task',exact=True).click()
        f.get_by_role('button',name='Select Native docs task',exact=True).click();f.get_by_role('button',name='Open selected task',exact=True).click()
        f.get_by_label('Rename selected task',exact=True).fill('Renamed in frame');f.get_by_role('button',name='Rename task',exact=True).click();f.get_by_role('button',name='Toggle completion',exact=True).click()
        self.reload_demo(panel);expect(f.locator('[data-state=selected_title]')).to_have_text('Renamed in frame')
        f.get_by_role('button',name='Back to tasks',exact=True).click();f.get_by_label('Search tasks',exact=True).fill('missing');expect(f.locator('[data-each]')).to_contain_text('No matching tasks')
        f.get_by_label('Search tasks',exact=True).fill('');f.get_by_label('Filter by completion',exact=True).check();f.get_by_label('Completion status',exact=True).select_option('true');expect(f.locator('[data-each]')).to_contain_text('Completed')
        f.get_by_role('button',name='Select Renamed in frame',exact=True).click();f.get_by_role('button',name='Open selected task',exact=True).click();f.get_by_role('button',name='Delete task',exact=True).click();f.get_by_role('button',name='Confirm delete',exact=True).click();expect(f.get_by_role('button',name='Select Renamed in frame',exact=True)).to_have_count(0)
    def test_crm_relations_dialog_theme_recovery_and_independent_demo_storage(self):
        p=self.goto('/examples/');panel,f=self.demo('crm');f.get_by_role('button',name='Companies',exact=True).click()
        f.get_by_label('Company name',exact=True).fill('Docs Company');f.get_by_label('Industry',exact=True).fill('Education');f.get_by_label('Industry',exact=True).press('Enter')
        f.get_by_role('button',name='Select Docs Company',exact=True).click();f.get_by_role('button',name='Company contacts',exact=True).click()
        f.get_by_label('Contact name',exact=True).fill('Alice');f.get_by_label('Email',exact=True).fill('invalid');self.assertTrue(f.get_by_role('button',name='Add contact',exact=True).is_disabled())
        f.get_by_label('Email',exact=True).fill('alice@example.com');f.get_by_role('button',name='Add contact',exact=True).click();f.get_by_role('button',name='Select Alice',exact=True).click()
        f.get_by_role('button',name='Edit selected contact',exact=True).click();f.get_by_label('New contact name',exact=True).fill('Alice Docs');f.get_by_role('button',name='Save contact name',exact=True).click();f.get_by_role('button',name='Close editor',exact=True).click()
        f.get_by_role('button',name='Back to companies',exact=True).click();f.get_by_role('button',name='Delete company',exact=True).click();self.assertTrue(f.locator('#sedrava-error').is_visible());expect(f.get_by_role('table',name='Company directory',exact=True)).to_contain_text('Docs Company')
        f.get_by_role('button',name='Back to dashboard',exact=True).click();f.get_by_role('button',name='Settings',exact=True).click();f.get_by_label('Color theme',exact=True).select_option('"dark"')
        self.reload_demo(panel);expect(f.locator('html')).to_have_attribute('data-theme','dark')
        other,cf=self.demo('counter');cf.get_by_role('button',name='Add one',exact=True).click();expect(cf.locator('output[data-state=count]')).to_have_text('1')
        self.reload_demo(panel,reset=True);panel.locator('iframe').scroll_into_view_if_needed();expect(f.locator('[data-state=company_count]')).to_have_text('0');expect(cf.locator('output[data-state=count]')).to_have_text('1')
    def test_http_real_endpoint_methods_errors_retry_cancel_and_static_failure(self):
        p=self.goto('/examples/');panel,f=self.demo('catalog');remote=f.locator('[data-remote=catalog]');expect(remote).to_contain_text('Real CI product')
        for mode,text in [('error','HTTP 503'),('invalid','Duplicate')]:
            ControlledEndpoint.mode=mode;f.get_by_role('button',name='Refresh catalog',exact=True).click();expect(remote.locator('[data-remote-status]')).to_contain_text(text);expect(remote).to_contain_text('Real CI product')
        ControlledEndpoint.mode='slow';f.get_by_role('button',name='Refresh catalog',exact=True).click();expect(remote.locator('[data-remote-status]')).to_have_text('loading');f.get_by_role('button',name='Cancel loading',exact=True).click();expect(remote.locator('[data-remote-status]')).to_contain_text('cancelled')
        ControlledEndpoint.mode='normal';f.get_by_role('button',name='Refresh catalog',exact=True).click();expect(remote.locator('[data-remote-status]')).to_have_text('success')
        f.get_by_role('button',name='Manage products',exact=True).click();f.get_by_label('Product name',exact=True).fill('<img src=x onerror=alert(1)>')
        for title,name in [('Create product','create_product'),('Update product','update_product'),('Replace product','replace_product'),('Delete product','delete_product')]:
            f.get_by_role('button',name=title,exact=True).click();result=f.locator('[data-remote='+name+']');expect(result.locator('[data-remote-status]')).to_have_text('success');self.assertEqual(result.locator('img').count(),0)
        self.assertEqual({call['method'] for call in ControlledEndpoint.calls},{'GET','POST','PUT','PATCH','DELETE'})
        f.get_by_role('button',name='Back to catalog',exact=True).click();ControlledEndpoint.mode='missing';f.get_by_role('button',name='Refresh catalog',exact=True).click();expect(remote.locator('[data-remote-status]')).to_contain_text('HTTP 404')
        (EVIDENCE/'real-http-calls.json').write_text(json.dumps(ControlledEndpoint.calls,indent=2))
    def test_responsive_pages_frames_code_and_screenshots(self):
        p=self.page
        for width in (320,360,390,768,1024,1440):
            p.set_viewport_size({'width':width,'height':900})
            for route,name in [('/','home-en'),('/ru/','home-ru'),('/ru/getting-started/','docs-ru'),('/examples/','examples-en')]:
                self.goto(route);p.evaluate('document.fonts.ready');self.assertLessEqual(p.evaluate('document.documentElement.scrollWidth'),width+1)
                p.screenshot(path=str(EVIDENCE/f'{name}-{width}.png'),full_page=True)
            for name in ('counter','tasks','crm','catalog'):
                panel,f=self.demo(name);f.get_by_role('heading',level=1).first.wait_for()
                self.assertTrue(panel.locator('iframe').evaluate('e=>e.contentDocument.documentElement.scrollWidth<=e.contentWindow.innerWidth+1'),name+' frame overflow')
                panel.screenshot(path=str(EVIDENCE/f'{name}-embed-{width}.png'))
    def test_accessibility_keyboard_toc_and_source_downloads(self):
        axe=(ROOT/'build/a11y/node_modules/axe-core/axe.min.js').read_text();reports={}
        p=self.page
        for route in ('/','/getting-started/','/ru/getting-started/','/examples/','/web-platform/','/ru/web-platform/','/site-authoring/','/ru/site-authoring/'):
            self.goto(route);p.evaluate('document.fonts.ready');p.evaluate(axe)
            result=p.evaluate('async()=>await axe.run(document,{runOnly:{type:"tag",values:["wcag2a","wcag2aa","wcag21aa"]}})');reports[route]=result['violations'];self.assertEqual(result['violations'],[],json.dumps(result['violations'],ensure_ascii=False,indent=2))
        (EVIDENCE/'accessibility.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2))
        self.goto('/getting-started/');p.keyboard.press('Tab');self.assertEqual(p.evaluate('document.activeElement.textContent'),'Skip to content');p.keyboard.press('Enter');self.assertEqual(p.evaluate('document.activeElement.id'),'content')
        p.locator('.doc-toc summary').click();p.locator('.doc-toc a').first.click();self.assertTrue(urlsplit(p.url).fragment)
        self.goto('/examples/')
        demos=json.loads((self.output/'docs-demos.json').read_text())
        for route,entry in demos.items():
            panel=p.locator('[data-demo="'+route+'"]');self.assertEqual(panel.locator('code').text_content(),(self.output/entry['source_url']).read_text());self.assertEqual(p.request.get(self.base+'/'+entry['source_url']).body(),(self.output/entry['source_url']).read_bytes())
if __name__=='__main__':unittest.main(verbosity=2)
