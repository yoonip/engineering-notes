from copy import deepcopy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def load(filename):
    namespace = {}
    path = ROOT / filename
    exec(compile(path.read_text(encoding='utf-8'), str(path), 'exec'), namespace)
    return namespace['solution']

def invoke(func,pid,args,expected=None,alternative=False):
    args=deepcopy(args)
    if pid==468378:
        if len(args)==3:depth,money,hidden=args
        else:depth,money=args;hidden=expected
        cost=0
        def excavate(column):
            nonlocal cost
            assert isinstance(column,int) and 1<=column<=len(depth)
            cost+=depth[column-1]
            assert cost<=money,(pid,'budget',cost,money)
            return (hidden>column)-(hidden<column)
        result=func(depth,money,excavate)
        assert result==hidden,(pid,result,hidden)
        return result
    if pid==451808:
        n=args[0];hidden=args[1] if len(args)>1 else expected
        count=0
        def submit(number):
            nonlocal count
            count+=1
            assert count<=(3024 if alternative else n)
            guess=str(number);secret=str(hidden)
            strikes=sum(a==b for a,b in zip(guess,secret))
            common=sum(min(guess.count(ch),secret.count(ch)) for ch in set(guess))
            return f'{strikes}S {common-strikes}B'
        result=func(3024 if alternative else n,submit)
        assert result==hidden,(pid,result,hidden)
        return result
    return func(*args)

def main():
    payload = json.loads((ROOT / 'cases.json').read_text(encoding='utf-8'))
    pid = payload['problem_id']
    primary = load('solution.py')
    alternative_path = next(ROOT.glob('alternative*.py'))
    alternative = load(alternative_path.name)
    checked = comparisons = 0
    for case in payload['cases']:
        expected = case['expected']
        actual = invoke(primary, pid, case['args'], expected)
        assert actual == expected, (case['label'], actual, expected)
        checked += 1
        if case.get('alternative_checked', True):
            actual = invoke(alternative, pid, case['args'], expected, True)
            assert actual == expected, (case['label'], '비교 풀이', actual, expected)
            comparisons += 1
    print(json.dumps({'problem_id': pid, 'primary_cases_passed': checked,
                      'alternative_cases_passed': comparisons}, ensure_ascii=False))

if __name__ == '__main__':
    main()
