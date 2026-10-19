"""공식 예제와 독립 대안의 고정 입력으로 풀이를 검사합니다."""
from pathlib import Path
import json,runpy,copy

def valid_decoding(sentence,decoded):
    if not decoded or decoded.strip()!=decoded or '  ' in decoded:return False
    words=decoded.split(' ')
    if any(not word.isupper() or not word.isalpha() for word in words):return False
    markers={ch for ch in sentence if ch.islower()}
    def match(index,position,used):
        if index==len(words):return position==len(sentence)
        word=words[index];options=[(word,set())]
        for outer in markers-used:
            options.append((outer+word+outer,{outer}))
            if len(word)>1:
                options.append((outer.join(word),{outer}))
                for inner in markers-used-{outer}:
                    options.append((outer+inner.join(word)+outer,{outer,inner}))
        return any(sentence.startswith(encoded,position) and match(index+1,position+len(encoded),used|added)
                   for encoded,added in options)
    return match(0,0,set())

def run():
    root=Path(__file__).parent
    main=runpy.run_path(str(root/'solution.py'))['solution'] if (root/'solution.py').exists() else None
    alternative=runpy.run_path(str(root/'alternative.py'))['solution']
    fixtures=json.loads((root/'test_cases.json').read_text('utf8'));checks=0
    for case in fixtures:
        for function,label in ((main,'main'),(alternative,'alternative')):
            if function is None or label=='alternative' and not case['check_alternative']:continue
            actual=function(*copy.deepcopy(case['args']));expected=case['expected']
            if case.get('multiple_decodings'):
                okay=actual=='invalid' if expected=='invalid' else actual!='invalid' and valid_decoding(case['args'][0],actual)
            else:okay=actual==expected
            if not okay:raise AssertionError((label,case['kind'],case['args'],expected,actual))
            checks+=1
    print(str(checks)+' solution checks passed')
    return checks

if __name__=='__main__':run()
