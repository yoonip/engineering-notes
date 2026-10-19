# 행렬의 덧셈
# 분류: 중첩 반복
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/12950
# AI 작성 학습 풀이입니다. 온라인 채점 통과를 확인한 제출물이 아닙니다.

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


# 같은 코드의 문법 설명: 아래 부분은 전체 주석입니다.
# def solution(arr1, arr2):  # def로 함수를 정의합니다. 두 행렬을 2차원 리스트로 받습니다.
#     rows = len(arr1)  # len()은 원소 수입니다. arr1의 원소는 각 행이므로 전체 행 수입니다.
#     cols = len(arr1[0])  # arr1[0]은 첫 번째 행입니다. 그 행의 원소 수가 열 수입니다.
#     answer = []  # 완성된 행들을 저장할 빈 리스트입니다.
#
#     for r in range(rows):  # range(rows)는 0부터 rows-1까지입니다. r은 행 번호입니다.
#         row = []  # 이번 행의 결과를 담을 새 리스트입니다. 행이 바뀔 때마다 새로 만듭니다.
#         for c in range(cols):  # c는 0부터 시작하는 열 번호입니다. 각 행에서 모든 열을 반복합니다.
#             row.append(arr1[r][c] + arr2[r][c])  # [행][열]로 같은 위치의 두 값을 읽어 더하고 append()로 이번 행 뒤에 추가합니다.
#         answer.append(row)  # 열 반복문이 끝난 뒤 완성한 행 전체를 결과에 추가합니다. answer는 리스트 안에 리스트가 있는 2차원 리스트입니다.
#
#     return answer  # 모든 행을 처리한 뒤 결과 행렬을 반환하고 함수를 종료합니다.
#
