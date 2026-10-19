def solution(info, n, m):
    dp = [n] * m
    dp[0] = 0
    for a_trace, b_trace in info:
        next_dp = [n] * m
        for b_used, a_used in enumerate(dp):
            if a_used == n:
                continue
            if a_used + a_trace < n:
                next_dp[b_used] = min(next_dp[b_used], a_used + a_trace)
            if b_used + b_trace < m:
                next_dp[b_used + b_trace] = min(next_dp[b_used + b_trace], a_used)
        dp = next_dp
    answer = min(dp)
    return answer if answer < n else -1

# 전체 코드 줄별 설명 (아래는 모두 실행되지 않는 주석입니다.)
# def solution(info, n, m):  # def는 함수 정의. info는 물건 정보, n·m은 체포 기준 입력.
#     dp = [n] * m  # [n]은 리스트, * m은 반복. dp[b]에는 B 흔적 b일 때 최소 A 흔적 저장, n은 불가능 표시.
#     dp[0] = 0  # []는 인덱싱. 아무것도 훔치기 전 B=0, A=0 상태 설정.
#     for a_trace, b_trace in info:  # for로 물건 순회. 쉼표는 두 흔적 값을 변수 두 개로 푸는 언패킹.
#         next_dp = [n] * m  # 이번 물건 처리 후 상태를 담을 새 리스트 초기화.
#         for b_used, a_used in enumerate(dp):  # enumerate는 (인덱스,값)을 차례로 제공. B 흔적과 최소 A 흔적을 읽음.
#             if a_used == n:  # if는 조건문, ==는 같음 비교. 불가능 상태인지 확인.
#                 continue  # continue로 이번 불가능 상태를 건너뜀.
#             if a_used + a_trace < n:  # <는 미만. A가 맡아도 체포 기준 미만인 경우만 허용.
#                 next_dp[b_used] = min(next_dp[b_used], a_used + a_trace)  # min은 작은 값 선택. B 흔적은 유지하고 최소 A 흔적 갱신.
#             if b_used + b_trace < m:  # B가 맡아도 B의 흔적이 기준 미만인지 확인.
#                 next_dp[b_used + b_trace] = min(next_dp[b_used + b_trace], a_used)  # B 흔적을 늘린 칸에 기존 A 흔적을 최소값으로 반영.
#         dp = next_dp  # 다음 상태 목록을 현재 dp로 교체. =는 대입.
#     answer = min(dp)  # min(dp)는 모든 B 흔적 상태 중 가장 작은 A 흔적.
#     return answer if answer < n else -1  # a if 조건 else b는 조건 표현식. 가능하면 answer, 전부 불가능하면 -1을 반환.

# 풀이 요약
# DP(작은 상태의 최적값을 저장하는 방법)로 B 흔적마다 최소 A 흔적만 유지합니다.
# 각 물건을 A 또는 B에게 배정하되 흔적이 n,m 이상이 되는 선택은 버립니다. 시간 O(물건 수*m), 공간 O(m).
# 예: info=[[1,2],[2,3],[2,1]], n=4,m=4이면 가능한 최소 A 흔적은 2입니다.
