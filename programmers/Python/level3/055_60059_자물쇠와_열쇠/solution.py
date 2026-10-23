# 열쇠와 자물쇠의 0·1 격자를 입력받음.
def solution(key, lock):
    # 열쇠와 자물쇠 한 변의 칸 수를 언패킹 대입.
    m, n = len(key), len(lock)
    # 자물쇠의 모든 홈 좌표를 중복 없는 집합으로 생성.
    holes = {(row, col) for row in range(n) for col in range(n) if lock[row][col] == 0}
    # 자물쇠에 홈이 없으면 열쇠를 바깥으로 치워도 열림.
    if not holes:
        # 한 배치라도 성공하면 참 반환.
        return True
    # 열쇠의 돌기 좌표만 모음.
    points = [(row, col) for row in range(m) for col in range(m) if key[row][col] == 1]
    # 0·90·180·270도 회전 검사.
    for _ in range(4):
        # 열쇠가 한 칸이라도 자물쇠와 겹칠 수 있는 모든 세로 이동량.
        for dr in range(1 - m, n):
            # 가능한 모든 가로 이동량.
            for dc in range(1 - m, n):
                # 자물쇠 영역 안에 들어온 열쇠 돌기만 집합으로 생성.
                inside = {(row + dr, col + dc) for row, col in points if 0 <= row + dr < n and 0 <= col + dc < n}
                # 돌기 집합과 홈 집합이 정확히 같으면 미충족 홈도 돌기 충돌도 없음.
                if inside == holes:
                    # 한 배치라도 성공하면 참 반환.
                    return True
        # 반사는 하지 않음.
        points = [(col, m - 1 - row) for row, col in points]
    # 모든 회전·이동이 실패하면 거짓 반환.
    return False
