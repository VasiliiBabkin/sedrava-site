"""Compile a source-authored native site with an immutable checked compiler pin.

Only declared Markdown provenance data is generated before compilation. No output
HTML/CSS/JS is patched or wrapped by Astro or this orchestration script.
"""
import argparse,hashlib,importlib.metadata,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];SOURCE=ROOT/'sedrava-next'
def git(folder,*args):return subprocess.check_output(['git','-C',str(folder),*args],text=True).strip()
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--compiler',type=Path,required=True);parser.add_argument('--output',type=Path,default=ROOT/'build/native-site');args=parser.parse_args()
    compiler=args.compiler.resolve();pin=json.loads((SOURCE/'compiler.json').read_text());actual=git(compiler,'rev-parse','HEAD')
    if actual!=pin['sha']:raise SystemExit('Compiler SHA differs from compiler.json')
    if git(compiler,'status','--porcelain','--untracked-files=no'):raise SystemExit('Refusing a modified compiler checkout')
    site_sha=git(ROOT,'rev-parse','HEAD');dirty=bool(git(ROOT,'status','--porcelain'));env=os.environ.copy();env['PYTHONPATH']=str(compiler)
    with tempfile.TemporaryDirectory(prefix='sedrava-native-inputs-') as tmp:
        source=Path(tmp)/'project';shutil.copytree(SOURCE,source,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        generated=source/'generated';generated.mkdir(exist_ok=True)
        provenance='## Compiler / Компилятор\n\nExperimental 0.11 compiler; published language remains 0.10.0.\n\n- Compiler Git SHA: `'+actual+'`\n- [Compiler source](https://github.com/VasiliiBabkin/sedrava/tree/'+actual+')\n- [Compiler extension PR #37](https://github.com/VasiliiBabkin/sedrava/pull/37)\n\n## Website / Сайт\n\n- Website Git SHA: `'+site_sha+'`\n- [Actual .sdr website source](https://github.com/VasiliiBabkin/sedrava-site/blob/'+site_sha+'/sedrava-next/site.sdr)\n- Working tree modified: `'+str(dirty).lower()+'`\n\n## Trust and release status / Статус\n\nThis website is built with Sedrava. Этот сайт написан на Sedrava.\n\nTrusted same-origin demos are not isolated untrusted code. The HTTP demo endpoint is CI-only; static hosting must not invent responses. No production deployment or 0.11 release is implied.\n'
        (generated/'provenance.md').write_text(provenance)
        for command in [['check',source/'site.sdr'],['build','site',source/'site.sdr','--output',args.output.resolve()]]:subprocess.run([sys.executable,'-m','sedrava_cli',*map(str,command)],env=env,check=True)
    output=args.output.resolve();demos=json.loads((output/'docs-demos.json').read_text())
    independent={}
    for name in ('counter','tasks','crm','catalog'):
        demo_source=SOURCE/'demos'/f'{name}.sdr';standalone=ROOT/'build/native-independent'/name
        for command in [['check',demo_source],['build','webapp',demo_source,'--output',standalone]]:
            subprocess.run([sys.executable,'-m','sedrava_cli',*map(str,command)],env=env,check=True)
        expected=demos['/live/'+name+'/']['files'];file_hashes={file:hashlib.sha256((standalone/file).read_bytes()).hexdigest() for file in expected}
        if file_hashes!=expected:raise SystemExit('Embedded output differs from independent build webapp: '+name)
        independent[name]=file_hashes
    manifest={'schema':1,'website_sha':site_sha,'website_dirty':dirty,'compiler_sha':actual,'compiler_pin':pin,'python':sys.version,'docs_dependencies':{name:importlib.metadata.version(name) for name in ('markdown-it-py','Pygments')},'ci_run':os.environ.get('GITHUB_RUN_ID'),'independent_demo_files':independent,'files':{p.relative_to(output).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(output.rglob('*')) if p.is_file()}}
    receipt=ROOT/'build/native-provenance.json';receipt.parent.mkdir(parents=True,exist_ok=True);receipt.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');print(receipt)
if __name__=='__main__':main()
