from pathlib import Path
import copy, json, runpy

def verify():
    root=Path(__file__).resolve().parent
    primary=runpy.run_path(str(root/'solution.py'))['solution']
    alternative=runpy.run_path(str(root/'alternative.py'))['solution']
    records=json.loads((root/'test_cases.json').read_text(encoding='utf-8'))
    official=generated=compared=skipped=0
    for case in records:
        actual=primary(*copy.deepcopy(case['args']))
        assert actual==case['expected'],(case,actual)
        if case['kind']=='official':official+=1
        else:generated+=1
        try:other=alternative(*copy.deepcopy(case['args']))
        except ValueError:skipped+=1
        else:
            assert other==case['expected'],(case,other)
            compared+=1
    return dict(official_examples=official,generated_cases=generated,alternative_comparisons=compared,alternative_cap_skips=skipped)

if __name__=='__main__':
    print(json.dumps(verify(),ensure_ascii=False))
