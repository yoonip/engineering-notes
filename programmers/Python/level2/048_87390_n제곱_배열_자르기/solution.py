def solution(n, left, right):
    answer = []
    for index in range(left, right + 1):
        # 전체 배열 없이 펼친 위치를 행·열로 바꾼다.
        row, column = divmod(index, n)
        # 행과 열을 모두 포함한 첫 정사각형 단계가 이 칸의 값이다.
        answer.append(max(row, column) + 1)
    return answer
