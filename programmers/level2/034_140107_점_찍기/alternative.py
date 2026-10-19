def solution(k,d):
    top=d//k
    answer=0
    for x in range(d//k+1):
        while k*k*(x*x+top*top)>d*d: top-=1
        answer+=top+1
    return answer
