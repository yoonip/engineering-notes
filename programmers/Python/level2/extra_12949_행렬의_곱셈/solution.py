def solution(arr1, arr2):
    # arr2의 열들을 튜플로 모아 list로 변환.
    columns = list(zip(*arr2))
    answer = []
    for row in arr1:
        # 현재 결과 행을 담는 리스트.
        result_row = []
        for column in columns:
            # sum은 생성식의 곱들을 모두 합산하는 내적 계산.
            value = sum(a * b for a, b in zip(row, column))
            result_row.append(value)
        # 완성된 한 행을 결과 행렬에 추가.
        answer.append(result_row)
    return answer
