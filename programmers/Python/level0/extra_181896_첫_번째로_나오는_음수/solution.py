def solution(num_list):
    for index, value in enumerate(num_list):
        if value < 0:
            return index
    return -1

# 전체 코드 줄별 설명
# def solution(num_list):  # def는 함수 정의. 정수 리스트 입력.
#     for index, value in enumerate(num_list):  # enumerate는 원소 위치와 값을 함께 제공.
#         if value < 0:  # if는 조건, <는 미만 비교. 음수인지 검사.
#             return index  # 처음 발견한 음수의 인덱스를 반환하고 종료.
#     return -1  # 음수가 없으면 -1 반환.

# 풀이 요약
# 앞에서부터 검사하면 처음 찾은 음수가 가장 먼저 등장한 음수입니다.
# 