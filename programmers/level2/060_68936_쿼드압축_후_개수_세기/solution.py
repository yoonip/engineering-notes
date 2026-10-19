# 문제: 쿼드압축 후 개수 세기
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/68936
# 풀이: 영역이 한 값이면 한 개로 세고, 다르면 네 사분면에 같은 규칙을 적용한다. 배열을 복사하지 않고 좌표와 크기를 전달한다.
# 복잡도: 정사각형 한 변 N: 시간 상한 O(N² log N), 재귀 추가 공간 O(log N).

def solution(arr):
    answer = [0, 0]
    def compress(row, column, size):
        value = arr[row][column]
        if all(arr[r][c] == value for r in range(row, row + size) for c in range(column, column + size)):
            answer[value] += 1
            return
        half = size // 2
        compress(row, column, half)
        compress(row, column + half, half)
        compress(row + half, column, half)
        compress(row + half, column + half, half)
    compress(0, 0, len(arr))
    return answer
