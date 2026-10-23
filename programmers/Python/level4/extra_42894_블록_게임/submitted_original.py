def solution(board):
    board = [row[:] for row in board]
    n = len(board)
    blocks = {}
    for r in range(n):
        for c in range(n):
            if board[r][c]:
                blocks.setdefault(board[r][c], []).append((r, c))
    holes = {}
    for number, cells in blocks.items():
        top, bottom = min(r for r, c in cells), max(r for r, c in cells)
        left, right = min(c for r, c in cells), max(c for r, c in cells)
        holes[number] = [(r, c) for r in range(top, bottom + 1) for c in range(left, right + 1) if (r, c) not in cells]
    answer = 0
    while True:
        removed = []
        for number, cells in blocks.items():
            empty = holes[number]
            if len(empty) == 2 and all(all(board[up][c] == 0 for up in range(r + 1)) for r, c in empty):
                for r, c in cells:
                    board[r][c] = 0
                removed.append(number)
        if not removed:
            break
        answer += len(removed)
        for number in removed:
            del blocks[number]
    return answer

# 전체 코드 줄별 설명
# def solution(board):  # def는 함수 정의. 번호별로 네 칸을 차지하는 블록이 놓인 격자를 입력받음.
#     board = [row[:] for row in board]  # 리스트 내포와 [:] 복사로 입력 행렬을 바꾸지 않고 작업할 새 행렬 생성.
#     n = len(board)  # len은 길이. 정사각 격자의 한 변 길이.
#     blocks = {}  # {}는 빈 딕셔너리. 블록 번호별 원래 칸 좌표 저장.
#     for r in range(n):  # range(n)은 0부터 n-1까지. 모든 행 순회.
#         for c in range(n):  # 모든 열 순회.
#             if board[r][c]:  # if는 조건문. 0이 아닌 칸에 블록이 있음.
#                 blocks.setdefault(board[r][c], []).append((r, c))  # setdefault는 없으면 빈 리스트 생성. append로 좌표 튜플 추가.
#     holes = {}  # 블록별 바운딩 직사각형에서 채워야 하는 빈 위치 목록 저장.
#     for number, cells in blocks.items():  # items는 딕셔너리의 (키, 값) 쌍 제공. 번호와 네 좌표를 순회.
#         top, bottom = min(r for r, c in cells), max(r for r, c in cells)  # min·max로 블록의 최상단·최하단 행 계산.
#         left, right = min(c for r, c in cells), max(c for r, c in cells)  # 블록의 가장 왼쪽·오른쪽 열 계산.
#         holes[number] = [(r, c) for r in range(top, bottom + 1) for c in range(left, right + 1) if (r, c) not in cells]  # 중첩 리스트 내포. not in은 원래 블록 칸에 속하지 않음을 검사.
#     answer = 0  # 제거한 블록 개수 초기화.
#     while True:  # 더 제거할 블록이 없을 때 break로 종료하는 반복.
#         removed = []  # 이번 반복에서 제거한 블록 번호 목록.
#         for number, cells in blocks.items():  # 아직 남아 있는 모든 블록 순회.
#             empty = holes[number]  # 이 블록의 직사각형을 완성할 위치들을 가져옴.
#             if len(empty) == 2 and all(all(board[up][c] == 0 for up in range(r + 1)) for r, c in empty):  # all은 모든 조건이 참인지 검사. 두 빈칸과 그 위 세로 경로가 전부 비어 있어야 검은 블록 투입 가능.
#                 for r, c in cells:  # 제거할 원래 블록의 네 칸 순회.
#                     board[r][c] = 0  # 블록을 제거해 빈칸으로 변경. 다음 블록의 투입 경로가 열릴 수 있음.
#                 removed.append(number)  # 이번에 제거한 번호를 기록.
#         if not removed:  # not은 부정. 이번에 제거한 블록이 하나도 없으면 실행.
#             break  # 더 이상 상태가 변하지 않으므로 while 종료.
#         answer += len(removed)  # +=는 더한 값 저장. 이번에 제거한 블록 개수 합산.
#         for number in removed:  # 순회 중 딕셔너리를 바꾸지 않도록 제거는 별도 반복에서 처리.
#             del blocks[number]  # del은 지정 항목 삭제. 이미 제거한 블록을 다음 검사에서 제외.
#     return answer  # return으로 제거 가능한 최대 블록 개수 반환.

# 풀이 요약
# 블록을 둘러싼 직사각형의 나머지 두 칸까지 위에서 검은 블록을 떨어뜨릴 수 있으면 제거합니다. 자기 블록이 위를 막는 경우도 불가능합니다.
# 제거는 다른 제거를 방해하지 않고 길만 열어 주므로 가능한 블록부터 없애도 최적입니다. 더 변화가 없을 때까지 반복합니다.
# 블록 수 B, 격자 길이 N에 대해 시간 O(N^2+B^2*N), 공간 O(N^2+B).
# 