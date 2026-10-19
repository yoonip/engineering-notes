from itertools import permutations
from math import isqrt

def solution(numbers):
    # 조각으로 만든 정수 후보 저장.
    candidates = set()
    for size in range(1, len(numbers) + 1):
        # 선행 0·중복 순열은 집합에서 통합.
        candidates.update(int(''.join(parts)) for parts in permutations(numbers, size))
    answer = 0
    for value in candidates:
        # all로 제곱근 이하 약수가 없는지 검사.
        if value >= 2 and all(value % divisor for divisor in range(2, isqrt(value) + 1)):
            answer += 1
    return answer
