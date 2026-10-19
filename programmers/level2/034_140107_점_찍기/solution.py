# 문제: 점 찍기
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/140107
# 풀이: x를 간격 K씩 옮기며 원 안의 최대 y를 isqrt로 구한다. 가능한 y의 배수 개수만 더해 좌표를 하나씩 만들지 않는다.
# 복잡도: 간격 K·반지름 D: 반복 O(D/K+1), 추가 공간 O(1). isqrt의 큰 정수 비용은 별도다.

from math import isqrt

def solution(k, d):
    answer = 0
    for x in range(0, d + 1, k):
        max_y = isqrt(d * d - x * x)
        answer += max_y // k + 1
    return answer
