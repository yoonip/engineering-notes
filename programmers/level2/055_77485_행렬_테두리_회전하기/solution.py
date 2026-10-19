# 문제: 행렬 테두리 회전하기
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/77485
# 풀이: 테두리 좌표와 기존 값을 따로 모아 시계 방향으로 한 칸 옮긴다. 값을 먼저 보존해 덮어쓰기로 다음 값이 바뀌지 않게 한다.
# 복잡도: 행 R·열 C·질의 Q개: 시간 O(RC+Q(R+C)), 반환값 외 추가 공간 O(RC+R+C).

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
