def solution(temperature, t1, t2, a, b, onboard):
    outside = temperature + 10
    low, high = t1 + 10, t2 + 10
    infinity = 10 ** 9
    dp = [infinity] * 51
    dp[outside] = 0
    for passenger in onboard[1:]:
        next_dp = [infinity] * 51
        for current, cost in enumerate(dp):
            if cost == infinity:
                continue
            natural = current + (current < outside) - (current > outside)
            for target, added in ((natural, 0), (current, b), (current - 1, a), (current + 1, a)):
                if not 0 <= target <= 50:
                    continue
                if passenger and not low <= target <= high:
                    continue
                next_dp[target] = min(next_dp[target], cost + added)
        dp = next_dp
    return min(dp)

# 전체 코드 줄별 설명
# def solution(temperature, t1, t2, a, b, onboard):  # def는 함수 정의. 실외·쾌적 온도, 온도 변경·유지 비용, 시간별 탑승 여부 입력.
#     outside = temperature + 10  # -10~40도를 리스트 인덱스 0~50으로 옮김.
#     low, high = t1 + 10, t2 + 10  # 쾌적 온도 범위도 같은 좌표로 변환하는 언패킹.
#     infinity = 10 ** 9  # **는 거듭제곱. 도달 불가능 상태의 충분히 큰 비용.
#     dp = [infinity] * 51  # []는 리스트, *는 반복 초기화. dp[온도]는 현재 시각에 그 온도로 도착하는 최소 소비전력.
#     dp[outside] = 0  # 0분의 실내온도는 실외와 같고 소비전력은 아직 0.
#     for passenger in onboard[1:]:  # [1:] 슬라이스로 1분부터 순회. for~in의 passenger는 그 시각 탑승 여부.
#         next_dp = [infinity] * 51  # 다음 1분의 온도별 최소 비용 표를 따로 생성.
#         for current, cost in enumerate(dp):  # enumerate는 (인덱스,값) 제공. 현재 온도와 그 온도까지의 최소 비용.
#             if cost == infinity:  # if는 조건문, ==는 같음. 도달 불가능한 온도는 확장하지 않음.
#                 continue  # continue는 다음 현재 온도로 진행.
#             natural = current + (current < outside) - (current > outside)  # 비교의 참·거짓은 계산에서 1·0. 전원을 끄면 실외온도 쪽으로 1도 이동.
#             for target, added in ((natural, 0), (current, b), (current - 1, a), (current + 1, a)):  # () 튜플들로 끄기·유지·냉방·난방 네 행동의 다음 온도와 추가 비용을 순회.
#                 if not 0 <= target <= 50:  # not은 부정. 정리한 온도 범위 밖의 후보 제외.
#                     continue  # 다음 행동 후보로 진행.
#                 if passenger and not low <= target <= high:  # and는 모두 참. 탑승 시각인데 쾌적 범위 밖이면 허용하지 않음.
#                     continue  # 해당 온도 후보 제외.
#                 next_dp[target] = min(next_dp[target], cost + added)  # min은 작은 값. 같은 다음 온도에 도착하는 행동 중 최소 비용 저장.
#         dp = next_dp  # 다음 시각의 표로 갱신. 현재 표와 분리해 한 분에 여러 번 이동하는 오류 방지.
#     return min(dp)  # return으로 마지막 시각의 가능한 모든 온도 중 최소 소비전력 반환.

# 풀이 요약
# DP 상태는 현재 시각의 온도별 최소 소비전력입니다. 매 분 전원 끄기(무료 자연 변화), 유지(b), 1도 상승·하강(a)을 모두 비교합니다.
# 탑승 시각의 다음 온도가 쾌적 범위 밖이면 제외합니다. 마지막 시각 이후의 비용은 더하지 않습니다. 시간 O(51T), 공간 O(51).
# 예: 28도에서 26도까지 두 번 냉방한 뒤 계속 유지할 수도 있지만, 24도까지 더 냉방하고 전원을 꺼 자연 상승시키면 첫 예제에서 총 40이 됩니다.
