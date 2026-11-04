"""Read-only verification of actual dev bytes, static routes and caching policy."""
import argparse,hashlib,json,re
from pathlib import Path
from urllib.request import urlopen,Request
from urllib.error import HTTPError
from urllib.parse import urlsplit
BASE='https://dev.virtreal.ru/'
def cache_error(name,headers):
    if re.search(r'(?:^|/)[a-f0-9]{64}\.',name):return None
    if not name.endswith(('.html','.js','.css','.json')):return None
    control=headers.get('Cache-Control','').lower()
    if 'no-cache' in control or 'no-store' in control:return None
    age=re.search(r'(?:^|,)\s*max-age=([0-9]+)',control)
    if age and int(age[1])<=300:return None
    return 'Mutable HTML/JS/CSS/JSON needs explicit revalidation or max-age <= 300'
def verify(manifest,output):
    report={'base':BASE,'website_sha':manifest['website_sha'],'compiler_sha':manifest['compiler_sha'],'files':{},'errors':[]}
    for name,expected in sorted(manifest['files'].items()):
        route=name[:-10] if name.endswith('index.html') else name
        with urlopen(Request(BASE+route,headers={'Cache-Control':'no-cache','User-Agent':'Sedrava-native-staging-verifier'}),timeout=20) as response:
            if urlsplit(response.url).netloc!='dev.virtreal.ru':raise ValueError('Unexpected staging redirect origin')
            data=response.read(manifest['sizes'][name]+1);actual=hashlib.sha256(data).hexdigest();headers=response.headers
            if actual!=expected:report['errors'].append(name+': bytes differ from accepted build')
            error=cache_error(name,headers)
            if error:report['errors'].append(name+': '+error)
            report['files'][name]={'sha256':actual,'Cache-Control':headers.get('Cache-Control'),'ETag':headers.get('ETag'),'Last-Modified':headers.get('Last-Modified')}
    try:
        with urlopen(BASE+'__sedrava_native_missing_route__/',timeout=20) as response:report['missing_route_status']=response.status;report['errors'].append('Unknown static routes must return 404')
    except HTTPError as error:
        report['missing_route_status']=error.code
        if error.code!=404:report['errors'].append('Unknown route did not return 404')
    report['status']='PASS' if not report['errors'] else 'NO-GO';Path(output).write_text(json.dumps(report,indent=2)+'\n');return report
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('manifest',type=Path);p.add_argument('--output',type=Path,default=Path('build/native-staging-http.json'));args=p.parse_args()
    result=verify(json.loads(args.manifest.read_text()),args.output)
    print(f"Staging HTTP verification: {result['status']}; checked {len(result['files'])} file(s), {len(result['errors'])} error(s)")
    if result['errors']:
        from collections import Counter
        groups=Counter(error.partition(': ')[2] if ': ' in error else error for error in result['errors'])
        for message,count in groups.most_common():
            print(f"  {count} x {message}")
        for error in result['errors'][:5]:
            print(f"  Example: {error}")
        if any('Mutable HTML/JS/CSS/JSON needs explicit' in error for error in result['errors']):
            print("ACTION REQUIRED: dev.virtreal.ru serves mutable files without acceptable Cache-Control.")
            print("Configure an explicit Nginx cache policy for THIS DEV HOST only, e.g. expires 0;")
            print("After applying/reloading the reviewed vhost settings, rerun the manual GitHub workflow.")
        print(f"Full failure evidence: {args.output}")
    raise SystemExit(0 if result['status']=='PASS' else 1)
