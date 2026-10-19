# 문제: N개의 최소공배수
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/12953
# 풀이: 현재 최소공배수와 다음 값의 최소공배수를 반복 계산한다. 곱하기 전에 최대공약수로 나눠 중간 정수의 크기를 줄인다.
# 복잡도: 원소 N개·중간 최댓값 V: 정수 연산 기준 시간 O(N log V), 추가 공간 O(1).

from math import gcd

def solution(arr):
    answer = 1
    for number in arr:
        answer = answer // gcd(answer, number) * number
    return answer
