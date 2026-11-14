"""Copy and commit only paths emitted by the research pipeline manifest."""
import argparse
from datetime import datetime
import json
import os
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


def report_publication(paths, *, sha=None, pushed=False):
    articles=[p for p in paths if '/기업분석_companies/' in p or '/자동분석_auto-research/' in p]
    result={'sha':sha,'files':sorted(paths),'analyses_published':len(articles),
            'state_only':bool(paths) and not articles,'pushed':pushed}
    summary=os.environ.get('GITHUB_STEP_SUMMARY')
    if summary:
        with open(summary,'a',encoding='utf-8') as stream:
            stream.write(f"## 신생기업 게시 결과\n\n- 새 분석 글: {len(articles)}개\n- 변경 파일: {len(paths)}개\n")
            if paths and not articles:
                stream.write('- 이번 커밋에는 조사 상태만 저장했습니다. 새 분석 글은 게시하지 않았습니다.\n')
            if not paths:
                stream.write('- 저장소에 반영할 변경이 없습니다.\n')
            if sha: stream.write(f'- 커밋: `{sha}`\n')
    print(json.dumps(result,ensure_ascii=False))


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
    if not staged:
        report_publication([])
        return 0
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
    report_publication(staged,sha=git(root,'rev-parse','HEAD').decode().strip(),pushed=args.push)
    return 0


if __name__=='__main__': raise SystemExit(main())
