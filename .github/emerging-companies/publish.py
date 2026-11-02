"""Copy and commit only paths emitted by the research pipeline manifest."""
import argparse
from datetime import datetime
import json
from pathlib import Path
import subprocess

from pipeline import CATEGORY, CONTROL, KST, digest, json_load, within


def git(root, *args):
    return subprocess.run(['git','-C',str(root),*args],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout


def allowed(path):
    if not isinstance(path,str) or '\\' in path or ':' in path or any(part in ('.','..','') for part in path.split('/')): return False
    if path==CONTROL+'/state.json': return True
    prefix=CATEGORY+'/'
    if not path.startswith(prefix): return False
    rest=path[len(prefix):]
    if rest in ('README.md','출처_sources.md','기업목록_companies.json','조사기록_research-log.md'): return True
    return (rest.startswith('기업분석_companies/') or rest.startswith('자동분석_auto-research/')) and rest.endswith('.md')


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path.cwd())
    parser.add_argument('--output',type=Path,default=Path('research-output'))
    parser.add_argument('--push',action='store_true')
    args=parser.parse_args(argv)
    root=args.root.resolve(); output=args.output.resolve()
    manifest=json_load(output/'manifest.json')
    paths=manifest['paths']
    if not paths or len(paths)!=len(set(paths)) or any(not allowed(p) for p in paths):
        raise ValueError('Manifest includes invalid, duplicate or out-of-scope paths')
    if git(root,'diff','--cached','--name-only','-z'):
        raise ValueError('Existing staged files must not be committed')
    hashes=manifest.get('base_sha256',{})
    if set(hashes)!=set(paths):raise ValueError('Manifest base identities are incomplete')
    for path in paths:
        destination=within(root,path)
        actual=digest(destination.read_bytes()) if destination.is_file() else None
        if actual!=hashes[path]:
            raise ValueError('Destination changed since research; refusing to overwrite: '+path)
    for path in paths:
        origin=within(output,path); destination=within(root,path)
        if not origin.is_file(): raise ValueError('Prepared output is missing')
        destination.parent.mkdir(parents=True,exist_ok=True)
        destination.write_bytes(origin.read_bytes())
    git(root,'add','--',*paths)
    staged=git(root,'diff','--cached','--name-only','-z').decode('utf-8').split('\0')
    staged={p for p in staged if p}
    if not staged: print('No changes to publish'); return 0
    if not staged.issubset(set(paths)):
        raise ValueError('Staged files exceed the publication manifest')
    git(root,'diff','--cached','--check')
    git(root,'config','user.name','github-actions[bot]')
    git(root,'config','user.email','41898282+github-actions[bot]@users.noreply.github.com')
    stamp=datetime.now(KST).strftime('%Y-%m-%d %H:%M')
    has_articles=any('/기업분석_companies/' in p or '/자동분석_auto-research/' in p for p in staged)
    title=('신생기업 공개 원문의 자동 분석 추가 ' if has_articles else '신생기업 공식 원문 후보 확인 상태 갱신 ')+stamp
    git(root,'commit','-m',title)
    if args.push:
        for attempt in range(3):
            git(root,'fetch','origin','main')
            git(root,'rebase','origin/main')
            try:
                git(root,'push','origin','HEAD:main')
                break
            except subprocess.CalledProcessError:
                if attempt==2: raise
    print(json.dumps({'sha':git(root,'rev-parse','HEAD').decode().strip(),'files':sorted(staged),'pushed':args.push},ensure_ascii=False))
    return 0


if __name__=='__main__': raise SystemExit(main())
