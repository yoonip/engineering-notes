# 붕대 감기
# 분류: 공격 간격 일괄 회복
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/250137
# 선택 이유: 공격 사이에는 회복만 일어나므로 간격과 완주 횟수로 한꺼번에 계산한다. 공격 뒤 연속 회복은 초기화된다.
# 비용: 공격 A개: 시간 O(A), 추가 공간 O(1). 공격 시각은 오름차순이며 중복되지 않는다.

def solution(bandage, health, attacks):
    duration, heal, bonus = bandage
    current = health
    previous_attack = 0

    for time, damage in attacks:
        gap = time - previous_attack - 1
        # 공격이 없는 초에만 회복하며, 공격 시각에는 회복하지 않는다.
        recovered = gap * heal + (gap // duration) * bonus
        current = min(health, current + recovered) - damage
        if current <= 0:
            return -1
        previous_attack = time

    return current
