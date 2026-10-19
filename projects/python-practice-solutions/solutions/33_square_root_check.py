# 정수 제곱근 판별
# 분류: 정수 제곱근
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/12934
# 선택 이유: isqrt로 정수 제곱근을 구하면 큰 정수도 부동소수점 반올림 없이 판정할 수 있다.
# 비용: 큰 정수 연산 비용은 입력 비트 길이에 따라 달라지며, 별도의 배열은 만들지 않는다.

from math import isqrt


def solution(n):
    root = isqrt(n)

    if root * root == n:
        return (root + 1) ** 2

    return -1
