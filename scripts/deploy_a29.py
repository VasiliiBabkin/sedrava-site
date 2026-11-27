#!/usr/bin/env python3
"""Explicit A29 two-site static deployment on the existing VDS.

No downloads, system configuration or unrelated sites are modified.
Back up every replaced file, stage files on target FS, roll back on failure.
Run only with trusted source/build trees and exclusive operator access.
"""
import argparse,hashlib,os,pwd,shutil,stat,tempfile,time,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
WEB=Path("/var/www/virtreal_ru_usr27/data/www")
BACKUPS=WEB.parent/".sedrava-a29-backups"
SQL_FILES=("favicon.svg","robots.txt","sitemap.xml","status.json","docs/index.html","index.html")
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def regular(p,uid):
    m=p.lstat()
    assert stat.S_ISREG(m.st_mode) and m.st_uid==uid,(p,"not owned regular file")
def directory(p,uid):
    m=p.lstat()
    assert stat.S_ISDIR(m.st_mode) and m.st_uid==uid,(p,"not owned directory")
def parents(p,root,uid):
    for d in reversed(p.parents):
        if d==root or root in d.parents:
            if d.exists() or d.is_symlink():directory(d,uid)
def downloads(root):
    out={}
    for p in (root/"downloads").rglob("*"):
        assert not p.is_symlink(),p
        if p.is_file():out[str(p.relative_to(root))]=sha(p)
    return out
def fetch(url):
    with urllib.request.urlopen(url,timeout=20) as response:
        assert response.status==200,(url,response.status)
        return hashlib.sha256(response.read()).hexdigest()
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--sql-source",type=Path,required=True)
    ap.add_argument("--deploy",action="store_true")
    a=ap.parse_args()
    owner=pwd.getpwnam("virtreal_ru_usr27")
    uid,gid=owner.pw_uid,owner.pw_gid
    src=ROOT/"dist";sql=a.sql_source/"site"
    lang_target=WEB/"virtreal.ru/sedrava";sql_target=WEB/"sql.virtreal.ru"
    entries=[]
    for source,target,names in [(src,lang_target,None),(sql,sql_target,SQL_FILES)]:
        directory(source,ROOT.stat().st_uid if source==src else sql.stat().st_uid)
        directory(target,uid)
        if names is None:
            names=[str(p.relative_to(source)) for p in source.rglob("*") if p.is_file() or p.is_symlink()]
        for name in sorted(names):
            p=Path(name)
            assert not p.is_absolute() and ".." not in p.parts and p.parts[0]!="downloads",name
            f=source/p;d=target/p
            parents(f,source,source.stat().st_uid);regular(f,source.stat().st_uid)
            parents(d,target,uid)
            if d.exists() or d.is_symlink():regular(d,uid)
            entries.append((source,target,p,sha(f)))
    assert 20<len(entries)<1000 and sum((s/p).stat().st_size for s,t,p,h in entries)<32*1024*1024
    old_downloads={r:downloads(r) for r in (lang_target,sql_target)}
    assert all(old_downloads.values()),"existing downloads must be present"
    print("PRECHECK",len(entries),"static files;",sum(map(len,old_downloads.values())),"existing download files protected")
    for url in ("https://sedrava.virtreal.ru/downloads/0.12.0-alpha.2/","https://sql.virtreal.ru/downloads/0.1.0-alpha.1/"):
        print("PREVIOUS DOWNLOAD",url,fetch(url))
    if not a.deploy:
        print("DRY_RUN PASS");return
    assert os.geteuid()==0,"requires authorized privileged deployment"
    if not BACKUPS.exists():BACKUPS.mkdir(mode=0o700)
    directory(BACKUPS,0)
    backup=Path(tempfile.mkdtemp(prefix=time.strftime("%Y%m%d-%H%M%S-"),dir=BACKUPS))
    records=[];published=[];created_dirs=[]
    try:
        for source,target,p,h in entries:
            dest=target/p
            old=backup/("language" if target==lang_target else "sql")/p
            exists=dest.exists()
            if exists:
                old.parent.mkdir(parents=True,exist_ok=True)
                shutil.copy2(dest,old)
                assert sha(dest)==sha(old)
            records.append((source,target,p,h,old,exists))
        # Immutable assets before HTML; search metadata and status last.
        records.sort(key=lambda x:(x[2].suffix in (".html",".json",".xml"),str(x[2])))
        for source,target,p,h,old,exists in records:
            dest=target/p
            missing=[]
            d=dest.parent
            while not d.exists():missing.append(d);d=d.parent
            for d in reversed(missing):
                d.mkdir();os.chown(d,uid,gid);d.chmod(0o755);created_dirs.append(d)
            parents(dest,target,uid)
            assert sha(source/p)==h
            fd,tmp=tempfile.mkstemp(prefix=".a29-stage-",dir=dest.parent)
            stage=Path(tmp)
            try:
                with os.fdopen(fd,"wb") as f:
                    f.write((source/p).read_bytes());f.flush();os.fsync(f.fileno())
                os.chown(stage,uid,gid);stage.chmod(0o644)
                assert sha(stage)==h
                os.replace(stage,dest);published.append((dest,old,exists))
                assert sha(dest)==h
            finally:
                if stage.exists():stage.unlink()
        for source,target,p,h in entries:assert sha(target/p)==h
        for r,previous in old_downloads.items():assert downloads(r)==previous
        checks=[(lang_target,"","https://sedrava.virtreal.ru/"),(lang_target,"ru/","https://sedrava.virtreal.ru/ru/"),(lang_target,"platform/","https://sedrava.virtreal.ru/platform/"),(lang_target,"ru/platform/","https://sedrava.virtreal.ru/ru/platform/"),(sql_target,"","https://sql.virtreal.ru/"),(sql_target,"docs/","https://sql.virtreal.ru/docs/")]
        for root,route,url in checks:
            assert fetch(url)==sha(root/route/"index.html"),url
            print("LIVE PASS",url)
        assert fetch("https://sql.virtreal.ru/status.json")==sha(sql_target/"status.json")
        for url in ("https://sedrava.virtreal.ru/downloads/0.12.0-alpha.2/","https://sql.virtreal.ru/downloads/0.1.0-alpha.1/"):
            print("DOWNLOAD STILL AVAILABLE",url,fetch(url))
        print("DEPLOY PASS; backup",backup,"; downloads unchanged")
    except BaseException:
        for dest,old,exists in reversed(published):
            if exists:
                fd,tmp=tempfile.mkstemp(prefix=".a29-rollback-",dir=dest.parent);os.close(fd)
                shutil.copy2(old,tmp);os.chown(tmp,uid,gid);os.replace(tmp,dest)
                assert sha(dest)==sha(old)
            else:dest.unlink()
        for d in reversed(created_dirs):
            if not any(d.iterdir()):d.rmdir()
        print("ROLLBACK; backup",backup)
        raise
if __name__=="__main__":main()
