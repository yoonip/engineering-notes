# 문제: 소수 찾기
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/42839
# 풀이: 숫자 순열을 정수로 만들어 set으로 중복을 없앤다. 각 후보는 제곱근까지 약수가 없는지 검사한다.
# 복잡도: 입력 길이 N·생성 순열 T개·고유 후보 U개·최댓값 V: 시간 O(TN+U√V), 추가 공간 O(U+N).

from itertools import permutations
from math import isqrt

def solution(numbers):
    candidates = set()
    for size in range(1, len(numbers) + 1):
        candidates.update(int(''.join(parts)) for parts in permutations(numbers, size))
    answer = 0
    for value in candidates:
        if value >= 2 and all(value % divisor for divisor in range(2, isqrt(value) + 1)):
            answer += 1
    return answer
