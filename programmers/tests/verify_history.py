"""과거 제출본의 AST·주석본·공개 예제를 확인한다. 사이트 재채점은 아니다."""
from pathlib import Path
import ast
import contextlib
import copy
import hashlib
import io
import json
import sys

ROOT=Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_script(source,stdin):
    previous=sys.stdin
    output=io.StringIO()
    try:
        sys.stdin=io.StringIO(stdin)
        with contextlib.redirect_stdout(output):
            exec(compile(source,'<archived-script>','exec'),{'__name__':'__main__'})
    finally:
        sys.stdin=previous
    return output.getvalue()


def main():
    problems=read(ROOT/'historical_submissions.json')['problems']
    assert len(problems)==len({p['id'] for p in problems})==86
    records=[]
    for p in problems:
        original_path=ROOT/p['original']
        source_path=ROOT/p['solution']
        original=original_path.read_text(encoding='utf-8')
        source=source_path.read_text(encoding='utf-8')
        assert digest(original_path)==p['original_sha256'],p['id']
        assert digest(source_path)==p['solution_sha256'],p['id']
        assert ast.dump(ast.parse(source))==ast.dump(ast.parse(original)),p['id']
        code,tail=source.split('\n# 전체 코드 줄별 설명\n',1)
        annotated,summary=tail.split('\n\n# 풀이 요약\n',1)
        restored=[]
        for line in annotated.splitlines():
            assert line.startswith('# '),p['id']
            body=line[2:]
            if not body.strip():restored.append('');continue
            actual,note=body.rsplit('  # ',1)
            assert note.strip(),p['id']
            restored.append(actual)
        assert '\n'.join(restored).rstrip()==code.rstrip(),p['id']
        assert source.rstrip() in (ROOT/p['readme']).read_text(encoding='utf-8'),p['id']
        cases=read(source_path.parent/'examples.json')['cases']
        assert cases,p['id']
        namespaces=[]
        if 'arguments' in cases[0]:
            for text in [original,source]:
                namespace={}
                exec(compile(text,'<accepted-solution>','exec'),namespace)
                namespaces.append(namespace)
        checks=[]
        for index,case in enumerate(cases,1):
            if 'arguments' in case:
                outputs=[namespace['solution'](*copy.deepcopy(case['arguments'])) for namespace in namespaces]
                expected=case['expected']
            else:
                outputs=[run_script(text,case['stdin']) for text in [original,source]]
                expected=case['stdout']
            assert outputs[0]==outputs[1]==expected,(p['id'],index,outputs,expected)
            checks.append({'case':index,'original_passed':True,'annotated_passed':True})
        grade=read(source_path.parent/'grading.json')
        assert grade['score']==100 and grade['original_sha256']==p['original_sha256'],p['id']
        record={'id':p['id'],'public_examples':len(cases),'checks':checks,
          'original_hash_match':True,'annotated_hash_match':True,'executable_ast_match':True,
          'exact_commented_copy':True,'nonempty_line_notes':True,'saved_website_grade':100,
          'scope':'Original website submission plus local public-example comparisons; not a new judge submission'}
        (source_path.parent/'validation.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        records.append(record)
    report={'checked_on':'2026-10-19','python':sys.version.split()[0],'problems':len(records),
        'public_examples':sum(r['public_examples'] for r in records),
        'execution_comparisons':2*sum(r['public_examples'] for r in records),
        'passed':len(records),'records':records}
    (ROOT/'HISTORICAL_VALIDATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='records'},ensure_ascii=False))


if __name__=='__main__':main()
