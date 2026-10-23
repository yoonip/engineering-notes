from math import gcd


def solution(signals):
    # 모든 신호등 주기의 최소공배수 구하기
    limit = 1

    for green, yellow, red in signals:
        cycle = green + yellow + red
        limit = limit * cycle // gcd(limit, cycle)

    # 1초부터 전체 상태가 반복되는 주기까지 확인
    for time in range(1, limit + 1):
        all_yellow = True

        # 현재 시각에 각 신호등이 노란불인지 확인
        for green, yellow, red in signals:
            cycle = green + yellow + red
            position = (time - 1) % cycle

            # 노란불이 아닌 신호등을 하나라도 발견하면 중단
            if not (green <= position < green + yellow):
                all_yellow = False
                break

        # 모든 신호등이 노란불이면 현재 시각이 정답
        if all_yellow:
            return time

    # 한 주기 전체를 확인해도 없다면 불가능
    return -1