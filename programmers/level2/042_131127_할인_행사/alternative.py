from collections import Counter

def solution(want,number,discount):
    need=dict(zip(want,number))
    current=Counter(discount[:10])
    answer=int(all(current[name]==count for name,count in need.items()))
    for end in range(10,len(discount)):
        current[discount[end-10]]-=1
        current[discount[end]]+=1
        answer+=all(current[name]==count for name,count in need.items())
    return answer
