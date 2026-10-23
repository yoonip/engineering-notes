def solution(n):
    answer = []
    def move(count, start, goal, spare):
        # 옮길 원판이 없으면 재귀 종료.
        if count == 0:
            return
        move(count - 1, start, spare, goal)
        # 가장 큰 원판 하나를 목적지로 이동.
        answer.append([start, goal])
        move(count - 1, spare, goal, start)
    # 원판 n개를 1번에서 3번으로 옮기고 2번을 보조로 사용.
    move(n, 1, 3, 2)
    return answer
