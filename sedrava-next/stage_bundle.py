"""Validate an accepted preview artifact and package only its exact static files."""
import argparse,gzip,hashlib,io,json,re,tarfile
from pathlib import Path

def prepare(evidence,sha,output):
    if not re.fullmatch('[a-f0-9]{40}',sha):raise ValueError('Expected immutable website SHA')
    evidence=Path(evidence);receipt_file=evidence/'native-provenance.json';root=evidence/'native-site'
    if receipt_file.stat().st_size>1048576 or root.is_symlink() or not root.resolve().is_relative_to(evidence.resolve()):raise ValueError('Unsafe staging artifact root/receipt')
    receipt=json.loads(receipt_file.read_text());pin=json.loads((Path(__file__).parent/'compiler.json').read_text())
    if receipt.get('schema')!=1 or receipt['compiler_sha']!=pin['sha']:raise ValueError('Artifact compiler differs from the reviewed pin')
    if receipt['website_sha']!=sha or receipt['website_dirty'] is not False:raise ValueError('Artifact is not a clean build of the requested commit')
    expected=receipt['files'];actual={};payloads={};total=0
    if not isinstance(expected,dict) or not 1<=len(expected)<=512:raise ValueError('Invalid artifact file count')
    for path in root.rglob('*'):
        if path.is_symlink():raise ValueError('Symlink in staging artifact')
        if path.is_file():
            name=path.relative_to(root).as_posix()
            if not re.fullmatch('[A-Za-z0-9_./-]+',name) or '..' in Path(name).parts:raise ValueError('Unsafe staging filename')
            if path.suffix.lower() not in {'.html','.css','.js','.json','.svg','.png','.jpg','.jpeg','.webp','.woff','.woff2','.sdr','.txt','.xml'}:raise ValueError('Non-static staging file')
            with path.open('rb') as stream:data=stream.read(4*1024*1024+1)
            total+=len(data)
            if len(data)>4*1024*1024 or total>16*1024*1024 or len(actual)>=512:raise ValueError('Artifact budget exceeded')
            payloads[name]=data;actual[name]=hashlib.sha256(data).hexdigest()
    if actual!=expected:raise ValueError('Staging payload differs from tested artifact or exceeds budget')
    output=Path(output);output.mkdir(parents=True,exist_ok=True);archive=output/'native-site.tar.gz'
    with archive.open('wb') as target,gzip.GzipFile(fileobj=target,mode='wb',mtime=0,filename='') as zipped,tarfile.open(fileobj=zipped,mode='w') as tar:
        for name in sorted(actual):
            data=payloads[name];info=tarfile.TarInfo(name);info.size=len(data);info.mode=0o644;info.mtime=0;tar.addfile(info,io.BytesIO(data))
    (output/'files.sha256').write_text(''.join(digest+'  '+name+'\n' for name,digest in sorted(actual.items())))
    manifest={'website_sha':sha,'compiler_sha':receipt['compiler_sha'],'files':actual,'sizes':{name:len(data) for name,data in payloads.items()},'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'target_host':'dev.virtreal.ru','status':'prepared-not-deployed'}
    (output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');return manifest
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('evidence',type=Path);parser.add_argument('sha');parser.add_argument('output',type=Path);args=parser.parse_args();manifest=prepare(args.evidence,args.sha,args.output);print(json.dumps({key:value for key,value in manifest.items() if key not in ('files','sizes')}))
