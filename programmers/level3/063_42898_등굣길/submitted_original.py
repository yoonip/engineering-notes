def solution(m, n, puddles):
    blocked = {tuple(point) for point in puddles}
    dp = [0] * (m + 1)
    dp[1] = 1
    for y in range(1, n + 1):
        for x in range(1, m + 1):
            if (x, y) in blocked:
                dp[x] = 0
            else:
                dp[x] = (dp[x] + dp[x - 1]) % 1000000007
    return dp[m]

# 전체 코드 줄별 설명
# def solution(m, n, puddles):  # def는 함수 정의. m은 가로, n은 세로, puddles는 물웅덩이의 (x,y) 좌표 목록.
#     blocked = {tuple(point) for point in puddles}  # {}는 집합 컴프리헨션. tuple은 리스트 좌표를 집합에 넣을 수 있는 변경 불가 묶음으로 변환.
#     dp = [0] * (m + 1)  # []는 리스트, *는 반복. 한 행의 경로 수를 저장하는 동적 계획법(DP) 배열. 0번은 경계용.
#     dp[1] = 1  # 집에서 시작하는 방법은 한 가지.
#     for y in range(1, n + 1):  # range의 끝은 제외. 위에서 아래로 행을 순회.
#         for x in range(1, m + 1):  # 왼쪽에서 오른쪽으로 열을 순회.
#             if (x, y) in blocked:  # ()는 튜플, in은 집합에 포함되는지 확인. 웅덩이면 통과 불가.
#                 dp[x] = 0  # 위에서 내려오던 경로도 모두 막히므로 0으로 초기화.
#             else:  # 웅덩이가 아닌 칸.
#                 dp[x] = (dp[x] + dp[x - 1]) % 1000000007  # dp[x]는 이전 행(위), dp[x-1]은 현재 행(왼쪽)의 경로 수. %는 나머지 연산.
#     return dp[m]  # 마지막 행의 마지막 칸, 즉 학교까지 가는 경로 수 반환.

# 풀이 요약
# 오른쪽·아래로만 이동하므로 현재 칸에 도달하는 경로 수는 위 칸과 왼쪽 칸의 경로 수 합이다. 웅덩이는 0으로 만든다.
# 예: 가로 4·세로 3에서 (2,2)가 막히면 학교까지 4가지다. 입력 좌표는 행·열이 아니라 가로 x·세로 y 순서임에 주의한다.
# 시간 O(MN), 추가 공간 O(M + 웅덩이 수). 모든 경로의 이동 횟수는 같으므로 따로 최단 거리를 계산할 필요가 없다.
# 