# 행렬의 덧셈
# 분류: 중첩 반복
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/12950
# 선택 이유: 같은 위치의 두 원소를 한 번씩 더해 새 행렬을 만든다.
# 비용: R×C 행렬: 시간 O(RC), 반환 행렬 이외의 추가 공간 O(1).

def solution(arr1, arr2):
    rows = len(arr1)
    cols = len(arr1[0])
    answer = []

    for r in range(rows):
        row = []
        for c in range(cols):
            row.append(arr1[r][c] + arr2[r][c])
        answer.append(row)

    return answer
