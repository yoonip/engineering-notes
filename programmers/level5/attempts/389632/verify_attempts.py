"""미통과 버전의 작은 입력 비교와 제한된 크기의 실행시간을 기록한다."""
from pathlib import Path
from collections import Counter
import importlib.util
import json
import random
import time
import sys
import cProfile
import pstats

ROOT=Path(__file__).resolve().parent


def load(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/f'{name}.py')
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.solution


def reference(s,queries):
    owners=[0]*len(s)
    newest=0
    result=[]
    for query in queries:
        parts=query.split()
        kind=parts[0]
        if kind=='1':
            result.append('YES' if owners[int(parts[1])-1]==owners[int(parts[2])-1] else 'NO')
        elif kind in ('2','3'):
            newest+=1
            word=set(parts[-1])
            if kind=='2':
                group=owners[int(parts[1])-1]
                selected=[i for i,c in enumerate(s) if c in word and owners[i]==group]
            else:
                selected=[i for i in range(int(parts[1])-1,int(parts[2])) if s[i] in word]
            for i in selected: owners[i]=newest
        elif kind=='4':
            a,b=owners[int(parts[1])-1],owners[int(parts[2])-1]
            older,newer=min(a,b),max(a,b)
            owners=[older if owner==newer else owner for owner in owners]
        else:
            for group in sorted(set(owners)):
                counts=Counter(c for i,c in enumerate(s) if owners[i]==group)
                result.append(' '.join(value for c in sorted(counts) for value in (c,str(counts[c]))))
    return result


def make_case(rng,n,q):
    s=''.join(rng.choice('abcd') for _ in range(n))
    queries=[]
    for _ in range(q):
        kind=rng.randrange(1,5)
        x,y=sorted([rng.randint(1,n),rng.randint(1,n)])
        word=''.join(rng.sample('abcdef',rng.randint(1,6)))
        if kind in (1,4): queries.append(f'{kind} {x} {y}')
        elif kind==2: queries.append(f'2 {x} {word}')
        else: queries.append(f'3 {x} {y} {word}')
    return s,queries+['5']


def main():
    functions={f'v{i}':load(f'solution_v{i}') for i in range(1,5)}
    rng=random.Random(389632)
    for _ in range(24):
        s,queries=make_case(rng,rng.randint(1,30),70)
        expected=reference(s,queries)
        for name,function in functions.items():
            assert function(s,queries)==expected,name
    records=[]
    s='abcdefghijklmnopqrstuvwxyz'*1153
    rng=random.Random(389633)
    queries=[]
    for _ in range(6000):
        x,y=sorted([rng.randint(1,len(s)),rng.randint(1,len(s))])
        word=''.join(rng.sample('abcdefghijklmnopqrstuvwxyz',rng.randint(1,26)))
        queries.append(f'3 {x} {y} {word}')
    queries.append('5')
    expected=None
    for name,function in functions.items():
        start=time.perf_counter()
        output=function(s,queries)
        elapsed=time.perf_counter()-start
        if expected is None: expected=output
        assert output==expected,name
        records.append({'version':name,'characters':len(s),'queries':len(queries),'seconds':round(elapsed,4),'outputs_equal':True})
    # Count recursive calls on the same input; these timings are excluded above.
    profiler=cProfile.Profile()
    profiler.runcall(functions['v1'],s,queries)
    calls={name:{'primitive_calls':v[0],'total_calls':v[1]} for (_,_,name),v in pstats.Stats(profiler).stats.items() if name in ('assign','find','locate')}
    report={'python':sys.version.split()[0],'seed':389632,'reference_cases':24,
            'scope':'Local comparisons only; not an accepted solution or a judge replay',
            'benchmark':records,'v1_profile_calls':calls}
    (ROOT/'local_comparison.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))


if __name__=='__main__': main()
