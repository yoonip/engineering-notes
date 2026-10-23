def solution(bandage, health, attacks):
    # 붕대 감기 기술의 정보
    duration, heal, bonus = bandage

    current = health       # 현재 체력
    success = 0            # 연속으로 붕대를 감은 시간
    attack_index = 0       # 다음에 처리할 공격의 위치
    last_time = attacks[-1][0]  # 마지막 공격 시각

    # 1초부터 마지막 공격 시각까지 진행
    for time in range(1, last_time + 1):

        # 현재 시각에 공격을 받는 경우
        if time == attacks[attack_index][0]:
            damage = attacks[attack_index][1]
            current -= damage
            success = 0
            attack_index += 1

            # 체력이 0 이하이면 즉시 종료
            if current <= 0:
                return -1

        # 공격을 받지 않는 경우
        else:
            current += heal
            success += 1

            # 정해진 시간 동안 연속 성공하면 추가 회복
            if success == duration:
                current += bonus
                success = 0

            # 최대 체력을 넘지 않도록 제한
            current = min(health, current)

    return current