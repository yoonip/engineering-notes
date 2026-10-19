# 문제: k진수에서 소수 개수 구하기
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/92335
# 풀이: K진수 문자열을 0으로 나누어 후보를 추린다. 후보를 10진 정수로 읽고 제곱근까지 약수를 검사한다.
# 복잡도: 변환 길이 L·후보 값 p들: 시간 O(L²+Σ√p), 추가 공간 O(L). 문자열 앞붙이기 비용을 포함한다.

from math import isqrt

def solution(n, k):
    digits = ''
    while n:
        n, remainder = divmod(n, k)
        digits = str(remainder) + digits
    answer = 0
    for piece in digits.split('0'):
        if not piece:
            continue
        value = int(piece)
        if value == 2:
            answer += 1
        elif value > 2 and value % 2 and all(value % divisor for divisor in range(3, isqrt(value) + 1, 2)):
            answer += 1
    return answer
