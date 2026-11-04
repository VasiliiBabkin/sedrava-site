"""Copy reviewed compiler reference content into the native site's declared Markdown inputs."""
import argparse,hashlib,json,posixpath,re,subprocess
from pathlib import Path
ROOT=Path(__file__).parent

def main(compiler,check=False):
    compiler=Path(compiler).resolve()
    pin=json.loads((ROOT/'compiler.json').read_text());sha=pin['sha']
    if subprocess.check_output(['git','-C',str(compiler),'rev-parse','HEAD'],text=True).strip()!=sha:raise ValueError('Import only the pinned reference revision')
    records=[]
    for lang in ('en','ru'):
        filename='011_WEB_PLATFORM.'+lang+'.md';source=(compiler/'docs'/filename).read_text();body=source.split('\n',1)[1].lstrip()
        def rewrite(match):
            label,target=match.groups()
            if target.startswith(('https://','http://','#')):return match[0]
            if target=='011_WEB_PLATFORM.en.md':return '['+label+'](/web-platform/)'
            if target=='011_WEB_PLATFORM.ru.md':return '['+label+'](/ru/web-platform/)'
            path=posixpath.normpath('docs/'+target)
            return '['+label+'](https://github.com/VasiliiBabkin/sedrava/blob/'+sha+'/'+path+')'
        # Rewrite prose links only; do not change any fenced example source.
        parts=re.split(r'(```[^\n]*\n.*?```)',body,flags=re.S)
        for i in range(0,len(parts),2):parts[i]=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',rewrite,parts[i])
        body=''.join(parts)
        body=body.replace('int|text|bool|Record, ...','int|text|bool|Record|list<Record>(max=N), ...').replace('type of the collection\'s record','type of the collection\'s record')
        if lang=='en':
            body=body.replace('expanded expression/function/collection work','expanded expression/function/query complexity score')
            body+='\n\n## Bounded list function contracts and embedded navigation\n\nPure functions also accept/return exact `list<Record>(max=N)` types, including capacity. Passing a list explicitly allows cross-collection predicates without mutable captures. The CRM uses `rule all(contacts, linked, companies)` so orphaned relationships reject both actions and restored snapshots.\n\nStandalone WebApp Back/Forward retains browser semantics. Documentation embeds instead own a bounded frame-local route trail so one demo cannot consume another demo or the parent document history. See [native site authoring](/site-authoring/).\n'
        else:
            body+='\n\n## Функции коллекций и навигация внутри примеров\n\nПараметры и результаты чистых функций также принимают точный `list<Record>(max=N)` с проверкой вместимости. Явная передача списка позволяет проверять связи без захвата изменяемого состояния. В CRM `rule all(contacts, linked, companies)` отклоняет потерянные ссылки как при действиях, так и при восстановлении.\n\nОтдельный WebApp сохраняет Browser Back/Forward. Во встроенной документации каждый iframe ведёт ограниченную собственную историю, не забирая историю соседних примеров и документа. См. [создание нативного сайта](/ru/site-authoring/).\n'
        body+='\n\n[Compiler reference source](https://github.com/VasiliiBabkin/sedrava/blob/'+sha+'/docs/'+filename+'). Apache-2.0; the full license is included in local assets.\n'
        target=ROOT/'content'/lang/'web-platform.md'
        if check:assert target.read_text()==body,'Compiler reference snapshot changed'
        else:target.write_text(body)
        records.append({'source':'docs/'+filename,'compiler_sha':sha,'source_sha256':hashlib.sha256(source.encode()).hexdigest(),'target':target.relative_to(ROOT).as_posix(),'target_sha256':hashlib.sha256(body.encode()).hexdigest()})
    manifest=json.dumps(records,ensure_ascii=False,indent=2)+'\n'
    if check:assert (ROOT/'compiler-content.json').read_text()==manifest,'Reference provenance differs'
    else:(ROOT/'compiler-content.json').write_text(manifest)
    print('PASS: complete bilingual compiler reference bound to '+sha)
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--compiler',type=Path,required=True);parser.add_argument('--check',action='store_true');args=parser.parse_args();main(args.compiler,args.check)
