# 실외·쾌적 온도, 온도 변경·유지 비용, 시간별 탑승 여부 입력.
def solution(temperature, t1, t2, a, b, onboard):
    # -10~40도를 리스트 인덱스 0~50으로 옮김.
    outside = temperature + 10
    # 쾌적 온도 범위도 같은 좌표로 변환하는 언패킹.
    low, high = t1 + 10, t2 + 10
    # 도달 불가능 상태의 충분히 큰 비용.
    infinity = 10 ** 9
    # dp[온도]는 현재 시각에 그 온도로 도착하는 최소 소비전력.
    dp = [infinity] * 51
    # 0분의 실내온도는 실외와 같고 소비전력은 아직 0.
    dp[outside] = 0
    # for~in의 passenger는 그 시각 탑승 여부.
    for passenger in onboard[1:]:
        # 다음 1분의 온도별 최소 비용 표를 따로 생성.
        next_dp = [infinity] * 51
        # 현재 온도와 그 온도까지의 최소 비용.
        for current, cost in enumerate(dp):
            # 도달 불가능한 온도는 확장하지 않음.
            if cost == infinity:
                # 해당 온도 후보 제외.
                continue
            # 전원을 끄면 실외온도 쪽으로 1도 이동.
            natural = current + (current < outside) - (current > outside)
            # () 튜플들로 끄기·유지·냉방·난방 네 행동의 다음 온도와 추가 비용을 순회.
            for target, added in ((natural, 0), (current, b), (current - 1, a), (current + 1, a)):
                # 정리한 온도 범위 밖의 후보 제외.
                if not 0 <= target <= 50:
                    # 해당 온도 후보 제외.
                    continue
                # 탑승 시각인데 쾌적 범위 밖이면 허용하지 않음.
                if passenger and not low <= target <= high:
                    # 해당 온도 후보 제외.
                    continue
                # 같은 다음 온도에 도착하는 행동 중 최소 비용 저장.
                next_dp[target] = min(next_dp[target], cost + added)
        # 현재 표와 분리해 한 분에 여러 번 이동하는 오류 방지.
        dp = next_dp
    # return으로 마지막 시각의 가능한 모든 온도 중 최소 소비전력 반환.
    return min(dp)
