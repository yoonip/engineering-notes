def solution(keyinput, board):
    moves = {'up': (0, 1), 'down': (0, -1), 'left': (-1, 0), 'right': (1, 0)}
    x, y = 0, 0
    limit_x, limit_y = board[0] // 2, board[1] // 2
    for key in keyinput:
        dx, dy = moves[key]
        nx, ny = x + dx, y + dy
        if abs(nx) <= limit_x and abs(ny) <= limit_y:
            x, y = nx, ny
    return [x, y]

# 전체 코드 줄별 설명
# def solution(keyinput, board):  # def는 함수 정의. 방향키 목록과 지도 가로·세로 크기 입력.
#     moves = {'up': (0, 1), 'down': (0, -1), 'left': (-1, 0), 'right': (1, 0)}  # {}는 딕셔너리, ()는 좌표 변화 튜플. 방향 이름을 이동량에 연결.
#     x, y = 0, 0  # 시작 좌표 초기화.
#     limit_x, limit_y = board[0] // 2, board[1] // 2  # []는 인덱스 접근, //는 정수 나눗셈. 중앙에서 각 축으로 갈 수 있는 최대 거리.
#     for key in keyinput:  # for로 방향키를 입력 순서대로 처리.
#         dx, dy = moves[key]  # 딕셔너리에서 이동량을 조회해 두 변수로 나누어 받음.
#         nx, ny = x + dx, y + dy  # 이동 후보 좌표 계산.
#         if abs(nx) <= limit_x and abs(ny) <= limit_y:  # abs는 절댓값, <=는 이하, and는 모두 만족. 지도 범위 안인지 검사.
#             x, y = nx, ny  # 유효한 이동일 때만 좌표 갱신.
#     return [x, y]  # []는 리스트. 최종 x·y 좌표 반환.

# 풀이 요약
# 이동할 후보 좌표를 먼저 만들고 지도 경계 안에 있을 때만 반영합니다.
# 