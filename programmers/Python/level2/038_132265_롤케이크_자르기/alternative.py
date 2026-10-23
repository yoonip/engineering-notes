def solution(topping):
    n=len(topping)
    suffix=[0]*(n+1)
    seen=set()
    for i in range(n-1,-1,-1):
        seen.add(topping[i])
        suffix[i]=len(seen)
    seen=set()
    answer=0
    for i in range(n-1):
        seen.add(topping[i])
        answer+=len(seen)==suffix[i+1]
    return answer
