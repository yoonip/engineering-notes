# 아직 덮이지 않은 가장 왼쪽 아파트를 잡습니다. 기존 기지국이 덮으면 건너뛰고, 아니면 그 지점을 덮도록 새 기지국을
# 최대한 오른쪽에 설치합니다. 구간 길이 나눗셈과 다른 직접 배치입니다.
def solution(n,stations,w):
    point=1;index=answer=0
    while point<=n:
        if index<len(stations) and stations[index]-w<=point:
            point=max(point,stations[index]+w+1);index+=1
        else:
            answer+=1;point+=2*w+1
    return answer
