def solution(wallpaper):
    lux = len(wallpaper)
    luy = len(wallpaper[0])
    rdx = 0
    rdy = 0

    for r, row in enumerate(wallpaper):
        for c, cell in enumerate(row):
            if cell == "#":
                lux = min(lux, r)
                luy = min(luy, c)
                rdx = max(rdx, r + 1)
                rdy = max(rdy, c + 1)

    return [lux, luy, rdx, rdy]


# ============================================================
# 학습용: 위와 같은 코드 + 각 줄의 설명
# 아래는 전체가 주석이므로 실행되지 않음
#
# 좌표는 [행, 열] 순서이며, 둘 다 0부터 시작함.
# 행 번호가 작을수록 위쪽, 열 번호가 작을수록 왼쪽임.
# ============================================================

# def solution(wallpaper):  # wallpaper: 각 행을 문자열로 저장한 리스트
#     lux = len(wallpaper)  # 시작 행: 전체 행 수로 초기화한 뒤 더 작은 파일 행을 찾음
#     luy = len(wallpaper[0])  # 시작 열: 첫 행의 길이, 즉 전체 열 수로 초기화
#     rdx = 0  # 끝 행: 파일을 찾을 때마다 필요한 아래쪽 경계로 갱신
#     rdy = 0  # 끝 열: 파일을 찾을 때마다 필요한 오른쪽 경계로 갱신
#
#     for r, row in enumerate(wallpaper):  # 행 번호 r과 해당 행의 문자열을 함께 꺼냄
#         for c, cell in enumerate(row):  # 그 행에서 열 번호 c와 문자 하나를 함께 꺼냄
#             if cell == "#":  # 파일이 있는 칸만 처리. 빈칸 "."은 건너뜀
#                 lux = min(lux, r)  # 기존 시작 행과 현재 행 중 작은 값 → 가장 위쪽
#                 luy = min(luy, c)  # 기존 시작 열과 현재 열 중 작은 값 → 가장 왼쪽
#                 rdx = max(rdx, r + 1)  # 현재 파일 칸의 아래쪽 경계까지 포함
#                 rdy = max(rdy, c + 1)  # 현재 파일 칸의 오른쪽 경계까지 포함
#
#     return [lux, luy, rdx, rdy]  # [시작 행, 시작 열, 끝 행, 끝 열]을 반환
#
# 예: 파일 하나가 행 2, 열 3에 있다면
# 해당 칸은 행 방향으로 2~3, 열 방향으로 3~4를 차지함.
# 따라서 그 칸 전체를 선택하는 좌표는 [2, 3, 3, 4].
# 이것이 끝점 계산에 r + 1, c + 1을 사용하는 이유임.