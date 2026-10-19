# 나머지가 1이 되는 수 찾기
# 분류: n-1의 최소 약수
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/87389
# 선택 이유: n % x == 1은 (n-1) % x == 0과 같다. 작은 약수를 먼저 찾고 없으면 n-1 자체가 답이다.
# 비용: n>=3에서 시간 O(√n), 추가 공간 O(1). 정수 제곱근으로 탐색 끝을 정한다.

from math import isqrt


def solution(n):
    target = n - 1
    for factor in range(2, isqrt(target) + 1):
        if target % factor == 0:
            return factor
    return target
