# 약수의 개수와 덧셈
# 분류: 등차합 / 제곱합 수식
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/77884
# 선택 이유: 모든 수의 합에서 완전제곱수의 합을 두 번 빼면 약수 개수가 홀수인 수만 부호가 바뀐다.
# 비용: 구간 길이와 무관한 횟수의 정수 연산으로 계산한다. 정수 연산을 단위로 보면 시간·공간 O(1)이며 큰 정수 비용은 비트 길이에 따라 달라진다.

from math import isqrt


def solution(left, right):
    def square_sum(limit):
        return limit * (limit + 1) * (2 * limit + 1) // 6

    # sqrt(left-1)까지의 제곱수는 구간에 없으므로 누적 제곱합에서 뺀다.
    before = isqrt(left - 1)
    last = isqrt(right)
    total = (left + right) * (right - left + 1) // 2
    squares = square_sum(last) - square_sum(before)
    return total - 2 * squares
