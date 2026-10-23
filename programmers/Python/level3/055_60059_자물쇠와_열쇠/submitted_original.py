def solution(key, lock):
    m, n = len(key), len(lock)
    holes = {(row, col) for row in range(n) for col in range(n) if lock[row][col] == 0}
    if not holes:
        return True
    points = [(row, col) for row in range(m) for col in range(m) if key[row][col] == 1]
    for _ in range(4):
        for dr in range(1 - m, n):
            for dc in range(1 - m, n):
                inside = {(row + dr, col + dc) for row, col in points if 0 <= row + dr < n and 0 <= col + dc < n}
                if inside == holes:
                    return True
        points = [(col, m - 1 - row) for row, col in points]
    return False

# 전체 코드 줄별 설명
# def solution(key, lock):  # def는 함수 정의. 열쇠와 자물쇠의 0·1 격자를 입력받음.
#     m, n = len(key), len(lock)  # len은 길이. 열쇠와 자물쇠 한 변의 칸 수를 언패킹 대입.
#     holes = {(row, col) for row in range(n) for col in range(n) if lock[row][col] == 0}  # {}의 집합 컴프리헨션. 자물쇠의 모든 홈 좌표를 중복 없는 집합으로 생성.
#     if not holes:  # not은 부정. 빈 집합이면 참. 자물쇠에 홈이 없으면 열쇠를 바깥으로 치워도 열림.
#         return True  # True는 참을 뜻하는 불리언 값.
#     points = [(row, col) for row in range(m) for col in range(m) if key[row][col] == 1]  # []는 리스트 컴프리헨션. 열쇠의 돌기 좌표만 모음.
#     for _ in range(4):  # range(4)는 네 번 반복, _는 쓰지 않는 변수. 0·90·180·270도 회전 검사.
#         for dr in range(1 - m, n):  # 열쇠가 한 칸이라도 자물쇠와 겹칠 수 있는 모든 세로 이동량.
#             for dc in range(1 - m, n):  # 가능한 모든 가로 이동량.
#                 inside = {(row + dr, col + dc) for row, col in points if 0 <= row + dr < n and 0 <= col + dc < n}  # and는 모두 참. 자물쇠 영역 안에 들어온 열쇠 돌기만 집합으로 생성.
#                 if inside == holes:  # ==는 같음. 돌기 집합과 홈 집합이 정확히 같으면 미충족 홈도 돌기 충돌도 없음.
#                     return True  # 한 배치라도 성공하면 참 반환.
#         points = [(col, m - 1 - row) for row, col in points]  # 각 돌기의 좌표를 시계 방향 90도 회전. 반사는 하지 않음.
#     return False  # 모든 회전·이동이 실패하면 거짓 반환.

# 풀이 요약
# 열쇠 돌기를 네 방향으로 회전하고 모든 겹치는 위치로 이동시킨다. 자물쇠 안에 들어온 돌기 좌표 집합이 홈 좌표 집합과 같으면 열린다.
# 예제는 90도 회전 후 오른쪽·아래 한 칸씩 옮기면 두 홈을 채운다. 자물쇠 밖의 돌기는 비교에서 제외한다.
# 시간 O((N+M)²·M² + N²), 공간 O(N²+M²). N,M≤20이므로 모든 배치를 검사해도 충분하다.
# 