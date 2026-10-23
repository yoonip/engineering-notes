def solution(m, n, s, time_map):
    size = m * n  # *는 곱셈. 전체 칸 수를 구함.
    infinity = s + 1  # 허용 시간을 넘는 값으로 도달 불가능 상태 표시.
    current = [infinity] * size  # []는 리스트. 현재 이동 횟수로 각 칸에 도착하는 최소 대화 시간 저장.
    current[0] = 0  # 시작 칸에는 이동 없이 대화 시간 0으로 도착.
    for steps in range(1, size):
        next_cost = [infinity] * size  # 다음 이동 횟수의 최소 대화 시간 리스트 초기화.
        for r in range(m):  # 현재 칸의 행을 순회.
            for c in range(n):  # 현재 칸의 열을 순회.
                cost = current[r * n + c]  # 2차원 좌표를 1차원 번호로 변환해 현재 최소 시간 조회.
                if cost > s:
                    continue  # continue는 이번 칸을 건너뜀.
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):  # ()는 튜플. 상하좌우 네 방향 이동 검사.
                    nr, nc = r + dr, c + dc  # 이웃 칸 좌표 계산.
                    if 0 <= nr < m and 0 <= nc < n and time_map[nr][nc] != -1:  # 연속 비교·and로 격자 내부이며 테이블 장애물이 아닌 칸만 선택.
                        candidate = cost + time_map[nr][nc]  # 이웃 칸에서 필요한 대화 시간을 더함.
                        index = nr * n + nc  # 이웃의 1차원 칸 번호 계산.
                        if candidate <= s and candidate < next_cost[index]:  # 제한을 만족하고 같은 이동 횟수의 기존 경로보다 대화 시간이 적으면 갱신.
                            next_cost[index] = candidate  # 이웃 칸의 최소 대화 시간 저장.
        current = next_cost  # 한 번 더 이동한 결과로 현재 상태 교체.
        if current[-1] <= s:  # [-1]은 마지막 칸. 도착 가능한 첫 이동 횟수인지 검사.
            return [steps, current[-1]]  # return으로 최소 이동 횟수와 그중 최소 대화 시간 반환.
    return [-1, -1]  # 조건을 만족하는 경로가 없을 때 기본값. 문제에서는 경로 존재 보장.
