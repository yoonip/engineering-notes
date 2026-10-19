# 문제: 멀쩡한 사각형
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/62048
# 풀이: 잘린 칸 수는 W+H-gcd(W,H)이다. 공통 격자점의 중복을 최대공약수로 보정해 칸별 검사를 피한다.
# 복잡도: 가로 W·세로 H: 정수 연산 기준 시간 O(log min(W,H)), 추가 공간 O(1).

from math import gcd

def solution(w, h):
    broken = w + h - gcd(w, h)
    return w * h - broken
