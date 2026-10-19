# 필요한 금·은과 도시별 보유량·적재량·편도 시간 입력.
def solution(a, b, g, s, w, t):
    # 최악의 총 20억 kg·용량 1·편도 10만도 포함하는 상한.
    left, right = 0, 4 * 10 ** 14
    # 가능한 최소 시간을 찾음.
    while left < right:
        # 현재 시간 범위의 중간값.
        middle = (left + right) // 2
        # 연쇄 대입으로 금·은·합계의 최대 운반량 초기화.
        total_gold = total_silver = total = 0
        # for로 도시별 네 정보를 언패킹.
        for gold, silver, weight, travel in zip(g, s, w, t):
            # 마지막에는 돌아오지 않아도 되므로 이 식으로 운반 횟수×적재량 계산.
            capacity = ((middle + travel) // (2 * travel)) * weight
            # 금만 실었을 때의 최대 운반량.
            total_gold += min(gold, capacity)
            # 은만 실었을 때의 최대 운반량.
            total_silver += min(silver, capacity)
            # 금·은이 같은 적재 용량을 나눠 쓰므로 총량 조건도 별도로 계산.
            total += min(gold + silver, capacity)
            # 금·은 개별량과 합계량이 모두 충분해야 실제 배분 가능.
            if total_gold >= a and total_silver >= b and total >= a + b:
                break
        # 금·은 개별량과 합계량이 모두 충분해야 실제 배분 가능.
        if total_gold >= a and total_silver >= b and total >= a + b:
            # 가능한 시간이므로 더 짧은 시간에서 최소값 탐색.
            right = middle
        else:
            # 불가능한 중간 시간을 제외한 오른쪽 범위로 이동.
            left = middle + 1
    # return으로 가능한 최소 시간 반환.
    return left
