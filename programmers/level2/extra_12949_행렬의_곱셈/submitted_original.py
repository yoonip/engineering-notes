def solution(arr1, arr2):
    columns = list(zip(*arr2))
    answer = []
    for row in arr1:
        result_row = []
        for column in columns:
            value = sum(a * b for a, b in zip(row, column))
            result_row.append(value)
        answer.append(result_row)
    return answer

# 전체 코드 줄별 설명
# def solution(arr1, arr2):  # def는 함수 정의. 곱할 두 행렬을 중첩 리스트로 받음.
#     columns = list(zip(*arr2))  # *는 각 행을 별도 인자로 풀기, zip은 같은 위치를 묶기. arr2의 열들을 튜플로 모아 list로 변환.
#     answer = []  # []는 빈 리스트. 결과 행렬을 저장.
#     for row in arr1:  # for로 왼쪽 행렬의 행을 하나씩 순회.
#         result_row = []  # 현재 결과 행을 담는 리스트.
#         for column in columns:  # 오른쪽 행렬의 열을 하나씩 순회.
#             value = sum(a * b for a, b in zip(row, column))  # zip으로 행·열의 같은 위치끼리 묶어 곱함. sum은 생성식의 곱들을 모두 합산하는 내적 계산.
#             result_row.append(value)  # append는 리스트 끝에 추가. 결과 행의 한 칸 저장.
#         answer.append(result_row)  # 완성된 한 행을 결과 행렬에 추가.
#     return answer  # return은 결과 반환.

# 풀이 요약
# 결과의 (i,j) 값은 왼쪽 행렬의 i행과 오른쪽 행렬의 j열을 같은 위치끼리 곱한 합이다.
# 예: [1,4]와 [3,3]은 1×3+4×3=15. 왼쪽 R×K, 오른쪽 K×C라면 시간 O(RKC), 공간 O(KC+RC).
# 