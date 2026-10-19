# 두 쐐기를 대각 꼭짓점으로 정한 뒤 다른 모든 쐐기가 직사각형의 엄격한 내부에 있는지 확인합니다. 경계에 있는 쐐기는
# 허용합니다.
# 작은 입력의 비교·검증용입니다. 원래 최대 입력 제출에는 기본 풀이를 사용합니다.
from itertools import combinations

def solution(n,data):
    answer=0
    for (x1,y1),(x2,y2) in combinations(data,2):
        if x1==x2 or y1==y2:continue
        left,right=sorted((x1,x2));bottom,top=sorted((y1,y2))
        if not any(left<x<right and bottom<y<top for x,y in data):answer+=1
    return answer
