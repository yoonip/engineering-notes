"""목록·파일 해시·주석본의 일치를 확인한다. 정답 판정 검사는 아니다."""
from pathlib import Path
from collections import Counter
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    full=read(ROOT/'catalog.json')['problems']
    recent=read(ROOT/'recent_submissions.json')['problems']
    historical=read(ROOT/'historical_submissions.json')['problems']
    recent=recent+historical
    combined=read(ROOT/'all_problems.json')['problems']
    assert len(combined)==len({p['id'] for p in combined})==672
    assert {p['id'] for p in combined}=={p['id'] for p in full+recent}
    records=[]
    for p in full:
        for field in ['readme','solution','alternative','test','original']:
            assert (ROOT/p[field]).is_file(),(p['id'],field)
        assert sha(ROOT/p['original'])==p['original_sha256'],p['id']
        assert sha(ROOT/p['solution'])==p['solution_sha256'],p['id']
        for field in ['solution','alternative']:
            path=ROOT/p[field]
            if path.suffix=='.py': compile(path.read_text(encoding='utf-8'),str(path),'exec')
        records.append({'id':p['id'],'documentation':'full_study_note','source_hash_match':True,'original_hash_match':True})
    for p in recent:
        path=ROOT/p['solution']
        source=path.read_text(encoding='utf-8')
        assert sha(path)==p['solution_sha256'],p['id']
        if path.suffix=='.py': compile(source,str(path),'exec')
        prefix='--' if path.suffix=='.sql' else '#'
        code,rest=source.split('\n'+prefix+' 전체 코드 줄별 설명\n',1)
        copy,summary=rest.split('\n\n'+prefix+' 풀이 요약\n',1)
        restored=[]
        for line in copy.splitlines():
            assert line.startswith(prefix+' '),p['id']
            line=line[len(prefix)+1:]
            if line.strip():
                text,note=line.rsplit('  '+prefix+' ',1)
                assert note.strip(),p['id']
                restored.append(text)
            else: restored.append('')
        assert '\n'.join(restored).rstrip()==code.rstrip(),p['id']
        assert summary.strip(),p['id']
        assert source.rstrip() in (ROOT/p['readme']).read_text(encoding='utf-8'),p['id']
        grade=read(path.parent/'grading.json')
        assert grade['score']==100 and grade['status']=='accepted',p['id']
        assert grade['source_sha256']==p['solution_sha256'],p['id']
        if p.get('provenance')=='accepted_submission_history':
            assert sha(ROOT/p['original'])==p['original_sha256'],p['id']
        records.append({'id':p['id'],'documentation':'commented_submission','source_hash_match':True,'exact_commented_copy':True,'nonempty_line_notes':True,'saved_grade':100})
    site=read(ROOT/'level0_1_catalog.json')['problems']
    archived01=[p for p in combined if p['level'] in (0,1)]
    assert len(site)==len(archived01)==359
    assert {p['id'] for p in site}=={p['id'] for p in archived01}
    report={'checked_on':'2026-10-19','accepted':len(combined),'full_study_notes':len(full),
        'commented_submissions':len(recent),'by_level':dict(Counter(p['level'] for p in combined)),
        'historical_submissions':len(historical),'level0_1_site_count':359,'level0_1_missing_ids':[],
        'languages':dict(Counter(p['language'] for p in combined)),
        'scope':'File integrity and annotation checks; saved grades, not new judge submissions',
        'records':records}
    (ROOT/'ARCHIVE_CHECK.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='records'},ensure_ascii=False))


if __name__=='__main__': main()
