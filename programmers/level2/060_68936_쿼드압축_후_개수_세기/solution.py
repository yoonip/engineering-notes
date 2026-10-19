def solution(arr):
    answer = [0, 0]
    def compress(row, column, size):
        value = arr[row][column]
        # 전부 같은 값이면 이 구역 하나로 압축하고 종료한다.
        if all(arr[r][c] == value for r in range(row, row + size) for c in range(column, column + size)):
            answer[value] += 1
            return
        # 섞인 구역만 같은 크기의 네 부분으로 나눈다.
        half = size // 2
        compress(row, column, half)
        compress(row, column + half, half)
        compress(row + half, column, half)
        compress(row + half, column + half, half)
    compress(0, 0, len(arr))
    return answer
