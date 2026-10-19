from functools import cache

def solution(a, s):
    if max(s)>14:raise ValueError("구간 길이 14 이하의 합성 과정 전수 비교용입니다")
    results=[];offset=0
    for length in s:
        values=a[offset:offset+length];offset+=length
        @cache
        def visit(index,stack):
            if index==len(values):return 1
            @cache
            def decide(current):
                # 합치지 않는 분기와 합치는 분기를 별개 기록으로 센다.
                total=visit(index+1,current)
                if len(current)>=2 and current[-1]==current[-2]:
                    total+=decide(current[:-2]+(current[-1]*2,))
                return total
            return decide(stack+(values[index],))
        results.append(visit(0,())%1_000_000_007)
    return results
