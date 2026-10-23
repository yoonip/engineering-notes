# 차량의 진출 지점들 중 카메라를 둘 위치를 골라 모든 구간을 덮는지 검사합니다. 최적 카메라는 어느 구간의 오른쪽 끝으로
# 옮길 수 있다는 성질을 사용합니다.
# 작은 입력의 비교·검증용입니다. 원래 최대 입력 제출에는 기본 풀이를 사용합니다.
from itertools import combinations

def solution(routes):
    ends=sorted({right for left,right in routes})
    for count in range(len(ends)+1):
        for cameras in combinations(ends,count):
            if all(any(left<=camera<=right for camera in cameras) for left,right in routes):return count
