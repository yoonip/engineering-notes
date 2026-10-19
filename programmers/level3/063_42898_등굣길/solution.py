# m은 가로, n은 세로, puddles는 물웅덩이의 (x,y) 좌표 목록.
def solution(m, n, puddles):
    # tuple은 리스트 좌표를 집합에 넣을 수 있는 변경 불가 묶음으로 변환.
    blocked = {tuple(point) for point in puddles}
    dp = [0] * (m + 1)
    # 집에서 시작하는 방법은 한 가지.
    dp[1] = 1
    # 위에서 아래로 행을 순회.
    for y in range(1, n + 1):
        # 왼쪽에서 오른쪽으로 열을 순회.
        for x in range(1, m + 1):
            # 웅덩이면 통과 불가.
            if (x, y) in blocked:
                # 위에서 내려오던 경로도 모두 막히므로 0으로 초기화.
                dp[x] = 0
            else:
                # %는 나머지 연산.
                dp[x] = (dp[x] + dp[x - 1]) % 1000000007
    # 마지막 행의 마지막 칸, 즉 학교까지 가는 경로 수 반환.
    return dp[m]
