# 크레인 인형뽑기 게임
# 분류: 열별 스택 / 시뮬레이션
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/64061
# 선택 이유: 열마다 아래 인형부터 스택으로 저장하면 집을 때 위에서 다시 찾지 않고 pop할 수 있다.
# 비용: N×N 보드, 이동 M개: 시간 O(N²+M), 추가 공간 O(N²). 입력 보드는 바꾸지 않는다.

def solution(board, moves):
    n = len(board)
    columns = [[] for _ in range(n)]
    for row in reversed(board):
        for col, doll in enumerate(row):
            if doll:
                columns[col].append(doll)

    basket = []
    answer = 0
    for move in moves:
        column = columns[move - 1]
        if not column:
            continue
        doll = column.pop()
        if basket and basket[-1] == doll:
            basket.pop()
            answer += 2
        else:
            basket.append(doll)
    return answer
