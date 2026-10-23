# 시간별로 각 도시가 실을 수 있는 금·은 조합을 직접 만들고 도시들을 합칩니다. 세 가지 용량 부등식의 충분성을 작은
# 화물량에서 대조합니다.
# 작은 입력의 비교·검증용입니다. 원래 최대 입력 제출에는 기본 풀이를 사용합니다.
def solution(a,b,g,s,w,t):
    for deadline in range(1+2*max(t)*(a+b+1)):
        states={(0,0)}
        for gold,silver,weight,travel in zip(g,s,w,t):
            trips=sum(arrival<=deadline for arrival in range(travel,deadline+1,2*travel))
            cap=trips*weight
            choices=[(x,y) for x in range(min(gold,a,cap)+1)
                     for y in range(min(silver,b,cap-x)+1)]
            states={(min(a,u+x),min(b,v+y)) for u,v in states for x,y in choices}
        if (a,b) in states:return deadline
