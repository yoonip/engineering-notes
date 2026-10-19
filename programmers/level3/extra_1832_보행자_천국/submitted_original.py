def solution(m, n, city_map):
    mod = 20170805
    vertical = [0] * n
    vertical[0] = 1
    for row in range(m):
        horizontal = 0
        for col in range(n):
            kind = city_map[row][col]
            if kind == 1:
                vertical[col] = horizontal = 0
            elif kind == 0:
                total = (vertical[col] + horizontal) % mod
                vertical[col] = horizontal = total
    return horizontal

# 전체 코드 줄별 설명
# def solution(m, n, city_map):  # def는 함수 정의. 행·열 수와 도로 상태 표 입력.
#     mod = 20170805  # 문제에서 지정한 나머지 계산 기준.
#     vertical = [0] * n  # []는 리스트, *는 반복. 각 열에서 아래로 내려오는 경로 수.
#     vertical[0] = 1  # 출발점에 도달하는 가상의 경로 하나로 초기화.
#     for row in range(m):  # range는 정수 범위. 위에서 아래로 행 순회.
#         horizontal = 0  # 행의 왼쪽 경계에서는 들어오는 경로가 없음.
#         for col in range(n):  # 왼쪽에서 오른쪽으로 열 순회.
#             kind = city_map[row][col]  # 중첩 []로 현재 칸 통행 조건 조회.
#             if kind == 1:  # ==는 같음. 벽이면 모든 경로 차단.
#                 vertical[col] = horizontal = 0  # 연쇄 대입으로 위·왼쪽 경로 모두 초기화.
#             elif kind == 0:  # elif는 추가 조건. 회전 가능한 칸.
#                 total = (vertical[col] + horizontal) % mod  # %는 나머지. 두 방향으로 온 경로 수 합산.
#                 vertical[col] = horizontal = total  # 아래·오른쪽 모두 합산한 경로로 나갈 수 있음. 직진 전용 2에서는 이 갱신을 생략해 각 방향 유지.
#     return horizontal  # 도착점은 자유 통행 칸이므로 합산된 최종 경로 수 반환.

# 풀이 요약
# vertical[c]는 위에서 내려온 경로 수, horizontal은 왼쪽에서 온 경로 수다. 자유 통행 칸에서는 두 수를 합쳐 어느 방향으로도 출발할 수 있다.
# 벽에서는 두 수를 0으로 만들고, 직진 전용 칸에서는 두 수를 섞지 않고 그대로 전달한다. 예제 2는 방향 전환을 제한하면 두 경로만 남는다.
# 시작점 위에서 경로 하나가 들어온 것으로 초기화한다. 시간 O(MN), 추가 공간 O(N).
# 