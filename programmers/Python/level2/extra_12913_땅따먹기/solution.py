def solution(land):
    # 직전 행의 0~3열에 도착한 최대 점수 네 개를 저장하는 동적 계획법(DP) 상태.
    a = b = c = d = 0
    for first, second, third, fourth in land:
        # 오른쪽 네 식을 전부 이전 값으로 계산한 뒤 동시에 갱신.
        a, b, c, d = (
            first + max(b, c, d),
            # 쉼표는 튜플 원소 구분.
            second + max(a, c, d),
            third + max(a, b, d),
            # 고정된 네 계산으로 내부 반복 비용 절감.
            fourth + max(a, b, c),
        )
    return max(a, b, c, d)
