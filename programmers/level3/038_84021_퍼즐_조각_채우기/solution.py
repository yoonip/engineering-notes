# Counter는 원소별 개수를 세는 딕셔너리형 자료구조.
from collections import Counter

# 좌표 목록을 같은 기준점으로 옮기는 함수.
def normalize(cells):
    # min은 최솟값, 괄호 안 생성식은 각 좌표의 행만 차례로 꺼냄.
    min_row = min(row for row, col in cells)
    # for의 두 변수는 튜플 언패킹.
    min_col = min(col for row, col in cells)
    # 위치와 탐색 순서의 차이를 제거.
    return tuple(sorted((row - min_row, col - min_col) for row, col in cells))

# 회전해도 같다고 판단할 대표 모양을 만드는 함수.
def shape(cells):
    # 네 방향의 모양을 저장.
    forms = []
    # _는 쓰지 않는 반복 변수.
    for _ in range(4):
        # 현재 방향의 표준 좌표를 저장.
        forms.append(normalize(cells))
        # (행,열)을 90도 회전한 좌표로 변환.
        cells = [(col, -row) for row, col in cells]
    # 네 방향 중 가장 작은 것을 대표값으로 선택.
    return min(forms)

# board에서 target 값으로 연결된 덩어리를 추출.
def components(board, target):
    # 정사각형 한 변의 칸 수.
    n = len(board)
    # False는 아직 방문하지 않았다는 불리언 값.
    visited = [[False] * n for _ in range(n)]
    # 각 덩어리의 대표 모양을 담을 리스트.
    result = []
    # 모든 행을 순회.
    for row in range(n):
        # 각 행의 모든 열을 순회.
        for col in range(n):
            # 이미 방문했거나 대상이 아니면 제외.
            if visited[row][col] or board[row][col] != target:
                # 이번 반복만 건너뛰고 다음 칸으로 이동.
                continue
            # 탐색에 넣는 시점에 방문 처리해 중복 삽입 방지.
            visited[row][col] = True
            # ()는 두 좌표를 묶은 튜플.
            stack = [(row, col)]
            # 현재 덩어리의 모든 좌표를 저장.
            cells = []
            # 리스트가 비어 있지 않은 동안 반복하는 깊이 우선 탐색(DFS).
            while stack:
                # 좌표를 두 변수에 나눠 대입.
                r, c = stack.pop()
                # 현재 칸을 덩어리에 추가.
                cells.append((r, c))
                # 상하좌우 네 방향의 변화량을 순회.
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    # 인접 칸의 행과 열 계산.
                    nr, nc = r + dr, c + dc
                    # 범위·미방문·대상 여부 검사.
                    if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc] and board[nr][nc] == target:
                        # 새 칸을 방문 표시.
                        visited[nr][nc] = True
                        # 스택에 넣어 나중에 탐색.
                        stack.append((nr, nc))
            # 완성된 덩어리를 회전 기준으로 표준화해 저장.
            result.append(shape(cells))
    # 발견한 모든 덩어리의 모양 반환.
    return result

# 프로그래머스가 호출하는 정답 함수.
def solution(game_board, table):
    # 딕셔너리 키에는 튜플 사용 가능.
    pieces = Counter(components(table, 1))
    # 채운 칸 수를 0으로 시작.
    answer = 0
    # 게임 보드의 빈 공간 덩어리를 차례로 확인.
    for hole in components(game_board, 0):
        # Counter는 없는 키의 개수를 0으로 돌려줌.
        if pieces[hole] > 0:
            # 모양이 같으면 빈 공간 전체를 채움.
            answer += len(hole)
            # 사용한 조각 한 개 차감.
            pieces[hole] -= 1
    # 최대한 채운 칸 수 반환.
    return answer
