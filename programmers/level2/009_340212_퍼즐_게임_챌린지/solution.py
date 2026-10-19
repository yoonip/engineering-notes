# 문제: 퍼즐 게임 챌린지
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/340212
# 풀이: 숙련도가 높아질수록 소요 시간이 늘지 않는 성질을 쓴다. 제한 시간 안에 가능한 최소 숙련도를 이분 탐색한다.
# 복잡도: 퍼즐 N개·최대 난도 D: 시간 O(N log D), 추가 공간 O(1).

def solution(diffs, times, limit):
    left = 1
    right = max(diffs)
    while left < right:
        level = (left + right) // 2
        elapsed = 0
        previous = 0
        for diff, current in zip(diffs, times):
            elapsed += current
            if diff > level:
                elapsed += (diff - level) * (current + previous)
            if elapsed > limit:
                break
            previous = current
        if elapsed <= limit:
            right = level
        else:
            left = level + 1
    return left
