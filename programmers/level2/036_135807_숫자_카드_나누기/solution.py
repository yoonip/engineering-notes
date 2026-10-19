# 문제: 숫자 카드 나누기
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/135807
# 풀이: 각 배열의 최대공약수만 후보로 검사한다. 그 후보가 반대편 수 하나를 나누면 후보의 약수들도 같은 수를 나누므로 제외한다.
# 복잡도: 카드 총 N개·최댓값 V: 정수 연산 기준 시간 O(N log V), 추가 공간 O(1).

from math import gcd
from functools import reduce

def solution(arrayA, arrayB):
    a = reduce(gcd, arrayA)
    b = reduce(gcd, arrayB)
    if any(value % a == 0 for value in arrayB):
        a = 0
    if any(value % b == 0 for value in arrayA):
        b = 0
    return max(a, b)
