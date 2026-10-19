# board는 초기 내구도 격자, skill은 직사각형 공격·회복 목록.
def solution(board, skill):
    # 행·열 수를 언패킹.
    n, m = len(board), len(board[0])
    # 범위 끝 다음 칸을 표시하려고 한 행·열 더 확보.
    difference = [[0] * (m + 1) for _ in range(n + 1)]
    # for~in으로 스킬 종류·두 끝 좌표·변화량을 언패킹.
    for kind, r1, c1, r2, c2, degree in skill:
        # 공격은 음수, 회복은 양수.
        change = -degree if kind == 1 else degree
        # 직사각형의 시작 꼭짓점에 변화 시작 표시.
        difference[r1][c1] += change
        # 오른쪽 경계 다음에서 가로 방향 변화 취소.
        difference[r1][c2 + 1] -= change
        # 아래 경계 다음에서 세로 방향 변화 취소.
        difference[r2 + 1][c1] -= change
        # 가로·세로 취소가 겹친 오른쪽 아래 바깥점은 한 번 다시 더함.
        difference[r2 + 1][c2 + 1] += change
    # 실제 격자의 모든 행 순회.
    for r in range(n):
        # 첫 열을 제외한 열들을 왼쪽부터 순회.
        for c in range(1, m):
            # 가로 누적합으로 각 행의 구간 변화 복원.
            difference[r][c] += difference[r][c - 1]
    # 첫 행을 제외한 행들을 위에서부터 순회.
    for r in range(1, n):
        # 모든 실제 열 순회.
        for c in range(m):
            # 세로 누적합으로 직사각형 변화량 전체 복원.
            difference[r][c] += difference[r - 1][c]
    # >0 비교의 참·거짓이 1·0으로 계산되어 최종 생존 건물 수 반환.
    return sum(board[r][c] + difference[r][c] > 0 for r in range(n) for c in range(m))
