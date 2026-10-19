# 문제: 양궁대회
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/92342
# 풀이: 점수 칸별 승리 여부를 비트마스크로 비교한다. 승리에는 상대보다 한 발만 더 쓰고 남은 화살은 0점에 모은다.
# 복잡도: 점수 칸 11개 고정: 시간 O(2^10·11), 추가 공간 O(11).

def solution(n, info):
    best_key = (0, [])
    answer = [-1]
    for mask in range(1 << 10):
        shots = [0] * 11
        remaining = n
        for index in range(10):
            if mask & (1 << index):
                shots[index] = info[index] + 1
                remaining -= shots[index]
        if remaining < 0:
            continue
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
