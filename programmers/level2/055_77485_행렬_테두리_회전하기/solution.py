def solution(rows, columns, queries):
    board = [[r * columns + c + 1 for c in range(columns)] for r in range(rows)]
    answer = []
    for query in queries:
        top, left, bottom, right = [value - 1 for value in query]
        path = [(top, c) for c in range(left, right)]
        path.extend((r, right) for r in range(top, bottom))
        path.extend((bottom, c) for c in range(right, left, -1))
        path.extend((r, left) for r in range(bottom, top, -1))
        values = [board[r][c] for r, c in path]
        for index, (r, c) in enumerate(path):
            board[r][c] = values[index - 1]
        answer.append(min(values))
    return answer

# 전체 코드 줄별 설명
# def solution(rows, columns, queries):  # def는 함수 정의. 행 수·열 수·회전 영역 목록 입력.
#     board = [[r * columns + c + 1 for c in range(columns)] for r in range(rows)]  # 중첩 리스트 내포로 1부터 행 순서의 숫자 행렬 생성. range는 끝 미포함.
#     answer = []  # []는 결과 리스트. 회전별 최솟값 저장.
#     for query in queries:  # for~in으로 회전 영역을 주어진 순서대로 순회.
#         top, left, bottom, right = [value - 1 for value in query]  # 리스트 내포로 1부터인 좌표를 0부터로 바꾸고 네 변수에 언패킹.
#         path = [(top, c) for c in range(left, right)]  # ()는 좌표 튜플. 위쪽 변을 오른쪽으로 순회하되 끝 꼭짓점 제외.
#         path.extend((r, right) for r in range(top, bottom))  # extend는 여러 원소 추가. 오른쪽 변을 아래 방향으로 연결.
#         path.extend((bottom, c) for c in range(right, left, -1))  # range 간격 -1로 아래쪽 변을 왼쪽 방향으로 연결.
#         path.extend((r, left) for r in range(bottom, top, -1))  # 왼쪽 변을 위쪽으로 연결해 모서리 중복 없는 시계 방향 경로 완성.
#         values = [board[r][c] for r, c in path]  # [][]는 행·열 접근. 변경 전에 테두리의 기존 값들 복사.
#         for index, (r, c) in enumerate(path):  # enumerate는 인덱스·좌표 제공. 괄호로 중첩 튜플 언패킹.
#             board[r][c] = values[index - 1]  # 이전 위치의 값을 현재 위치로 대입. -1 인덱스는 마지막 값이라 원형 회전 처리.
#         answer.append(min(values))  # min은 최솟값. 이동한 숫자들 중 최소를 append로 추가.
#     return answer  # return으로 회전별 결과 목록 반환.

# 풀이 요약
# 테두리 좌표를 시계 방향으로 모은 뒤 각 칸에 직전 칸의 기존 값을 넣습니다. 안쪽 값은 경로에 포함되지 않습니다.
# 예: 첫 6×6 예제의 회전별 최솟값은 [8,10,25]. 회전 Q개일 때 시간 O(행*열+Q(행+열)), 공간 O(행*열+Q).
