# 노란불 신호등
# 분류: 최소공배수 / 주기 탐색
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/468371
# 선택 이유: 신호가 모두 반복되는 최소공배수 구간을 확인한다. 동시에 노란불인 시각이 없으면 -1이다.
# 비용: 신호 N개, 주기의 최소공배수 T: 시간 O(NT), 추가 공간 O(1). T가 커지면 탐색 비용도 커진다.

from math import gcd


def solution(signals):
    repeat_time = 1

    for green, yellow, red in signals:
        cycle = green + yellow + red
        repeat_time = repeat_time // gcd(repeat_time, cycle) * cycle

    for time in range(1, repeat_time + 1):
        all_yellow = True

        for green, yellow, red in signals:
            cycle = green + yellow + red
            phase = (time - 1) % cycle

            if not (green <= phase < green + yellow):
                all_yellow = False
                break

        if all_yellow:
            return time

    return -1
