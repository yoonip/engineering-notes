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


# 같은 정답 코드 + 줄별 문법 설명
# 아래는 전체가 주석이므로 실행되지 않습니다.

# def solution(arr1, arr2):  # def로 함수를 정의합니다. 두 행렬을 2차원 리스트로 받습니다.
#     rows = len(arr1)  # len()으로 행 수를 구합니다.
#     cols = len(arr1[0])  # arr1[0]은 첫 행입니다. 그 행의 원소 수가 열 수입니다.
#     answer = []  # 완성된 행들을 담을 빈 리스트입니다.
#
#     for r in range(rows):  # r에 0부터 rows-1까지 넣습니다. r은 행 번호입니다.
#         row = []  # 현재 행의 결과를 담을 새 리스트입니다. 행마다 새로 만듭니다.
#         for c in range(cols):  # c는 열 번호입니다. 현재 행의 모든 열을 확인합니다.
#             row.append(arr1[r][c] + arr2[r][c])  # [행][열]로 같은 위치의 값을 읽고 더해 현재 행에 추가합니다.
#         answer.append(row)  # 안쪽 반복이 끝나면 완성한 행 전체를 결과에 추가합니다.
#
#     return answer  # 모든 행이 완성되면 결과 행렬을 반환합니다.