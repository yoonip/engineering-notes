# B의 모든 순서를 A와 직접 비교합니다. 정렬 후 탐욕으로 얻는 승점이 최대인지 작은 배열에서 확인합니다.
# 작은 입력의 비교·검증용입니다. 원래 최대 입력 제출에는 기본 풀이를 사용합니다.
from itertools import permutations

def solution(A,B):
    return max(sum(b>a for a,b in zip(A,order)) for order in permutations(B))
