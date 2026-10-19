def solution(n,l,r):
    answer=0
    for position in range(l-1,r):
        value=position
        for _ in range(n):
            value,digit=divmod(value,5)
            if digit==2: break
        else:
            answer+=1
    return answer
