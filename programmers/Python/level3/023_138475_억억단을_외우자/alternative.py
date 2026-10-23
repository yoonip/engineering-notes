# 각 약수의 배수를 방문해 약수 개수를 직접 더합니다. 오른쪽부터 최선의 수를 저장하면 시작점마다 상수 시간에 답합니다.
# 소인수 지수로 세는 기본 풀이보다 느리지만 단순합니다.
def solution(e, starts):
    count=[0]*(e+1)
    for divisor in range(1,e+1):
        for multiple in range(divisor,e+1,divisor): count[multiple]+=1
    best=[0]*(e+2)
    best[e]=e
    for value in range(e-1,0,-1):
        other=best[value+1]
        best[value]=value if count[value]>=count[other] else other
    return [best[start] for start in starts]
