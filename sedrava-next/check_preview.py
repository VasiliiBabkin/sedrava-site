"""Independent static acceptance: all routes/anchors/resources and exact demo sources."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,unquote
import hashlib,json,posixpath,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];OUTPUT=ROOT/'build/native-site'
class Page(HTMLParser):
    def __init__(self):super().__init__();self.ids=set();self.links=[];self.code=[];self.current=None;self.text=[];self.h1=0
    def handle_starttag(self,tag,attrs):
        props=dict(attrs)
        assert not any(key.lower().startswith('on') for key in props),'Inline event handler'
        if 'id' in props:assert props['id'] not in self.ids,'Duplicate ID';self.ids.add(props['id'])
        if tag=='h1':self.h1+=1
        if tag=='script':assert props.get('src'),'Inline script forbidden'
        if tag in ('a','link') and props.get('href'):self.links.append(props['href'])
        if tag in ('iframe','script','img') and props.get('src'):self.links.append(props['src'])
        if tag=='iframe':assert not props.get('sandbox'),'Do not misrepresent same-origin sandbox isolation'
        if tag=='code' and 'data-source-sha256' in props:self.current=[props['data-source-sha256'],[]]
    def handle_endtag(self,tag):
        if tag=='code' and self.current:self.code.append((self.current[0],''.join(self.current[1])));self.current=None
    def handle_data(self,data):
        self.text.append(data)
        if self.current:self.current[1].append(data)
def main():
    subprocess.run([sys.executable,str(ROOT/'sedrava-next/migrate_content.py'),'--check'],check=True)
    receipt=json.loads((ROOT/'build/native-provenance.json').read_text())
    pin=json.loads((ROOT/'sedrava-next/compiler.json').read_text())
    assert receipt['compiler_sha']==pin['sha'],'Compiler provenance must be its exact immutable SHA'
    assert receipt['website_sha']==subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'Wrong website checkout provenance'
    actual_files={p.relative_to(OUTPUT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in OUTPUT.rglob('*') if p.is_file()}
    assert receipt['files']==actual_files,'Receipt must cover the exact complete output bytes'
    assert set(receipt['independent_demo_files'])=={'counter','tasks','crm','catalog'}
    pages={};checked=0
    for path in OUTPUT.rglob('*.html'):
        parser=Page();parser.feed(path.read_text());pages[path.relative_to(OUTPUT).as_posix()]=parser
        if not path.relative_to(OUTPUT).as_posix().startswith('live/'):assert parser.h1==1,f'{path}: expected one h1'
        else:assert parser.h1>=1,f'{path}: missing app view headings'
    for path,page in pages.items():
        for href in page.links:
            url=urlsplit(href)
            if url.scheme:assert url.scheme in ('https','http','mailto','tel');continue
            target=posixpath.normpath(posixpath.join(posixpath.dirname(path),unquote(url.path))) if url.path else path
            if url.path.startswith('/'):target=url.path.lstrip('/')
            if target=='.' or url.path.endswith('/'):target=target.rstrip('/')+'/index.html' if target!='.' else 'index.html'
            resolved=OUTPUT/target
            assert resolved.resolve().is_relative_to(OUTPUT.resolve()) and resolved.is_file(),f'{path}: broken local URL {href} -> {target}'
            if url.fragment:assert target in pages and unquote(url.fragment) in pages[target].ids,f'{path}: broken anchor {href}'
            checked+=1
    # All visitor-facing pages identify their actual Sedrava generator.
    for path,page in pages.items():
        if path.startswith('live/'):
            continue
        visible=''.join(page.text)
        assert 'astro' not in visible.casefold(), f'{path}: obsolete generator claim'
        claim='Этот сайт написан на Sedrava' if path.startswith('ru/') else 'This website is built with Sedrava'
        assert claim in visible, f'{path}: missing native Sedrava attribution'
    migration=json.loads((ROOT/'sedrava-next/migration.json').read_text())
    for row in migration:assert row['route'].lstrip('/')+'index.html' in pages,'Lost old route '+row['route']
    demos=json.loads((OUTPUT/'docs-demos.json').read_text())
    assert len(demos)==4
    for route,demo in demos.items():
        source=(OUTPUT/demo['source_url']).read_bytes();assert hashlib.sha256(source).hexdigest()==demo['source_sha256']
        name=route.strip('/').split('/')[-1];assert source==(ROOT/'sedrava-next/demos'/f'{name}.sdr').read_bytes()
        for file,sha in demo['files'].items():assert hashlib.sha256((OUTPUT/route.lstrip('/')/file).read_bytes()).hexdigest()==sha,'Demo bundle was changed after compilation'
        for path in ('examples/index.html','ru/examples/index.html'):
            matches=[code for sha,code in pages[path].code if sha==demo['source_sha256']]
            assert matches==[source.decode()],f'{path}: source drift for {name}'
    for path,claim in [('index.html','This website is built with Sedrava'),('ru/index.html','Этот сайт написан на Sedrava')]:assert claim in ''.join(pages[path].text)
    assert 'Disallow: /' in (OUTPUT/'robots.txt').read_text()
    native_count=sum(not path.startswith('live/') for path in pages)
    assert native_count==30
    assert (OUTPUT/'sitemap.xml').read_text().count('<url>')==native_count
    assert list((OUTPUT/'assets').glob('*.woff2')) and list((OUTPUT/'assets').glob('license-*.txt'))
    report={'status':'PASS','site_pages':native_count,'live_demos':len(demos),'legacy_routes':len(migration),'checked_local_links':checked,'displayed_source_panels':8}
    (ROOT/'build/native-parity.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
