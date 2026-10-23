def solution(n, info):
    # 뒤집은 배열로 낮은 점수 화살부터 동률을 비교한다.
    best_key = (0, [])
    answer = [-1]
    # 각 득점 과녁을 이길지 포기할지 선택한다.
    for mask in range(1 << 10):
        shots = [0] * 11
        remaining = n
        for index in range(10):
            if mask & (1 << index):
                shots[index] = info[index] + 1
                remaining -= shots[index]
        if remaining < 0:
            continue
        # 득점에 도움이 되지 않는 남은 화살은 0점에 몰아 동률 우선순위를 높인다.
        shots[10] = remaining
        difference = 0
        for index in range(10):
            if shots[index] > info[index]:
                difference += 10 - index
            elif info[index] > 0:
                difference -= 10 - index
        key = (difference, shots[::-1])
        if difference > 0 and key > best_key:
            best_key, answer = key, shots
    return answer
