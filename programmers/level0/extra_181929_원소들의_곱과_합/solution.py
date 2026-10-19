def solution(num_list):
    product = 1
    for value in num_list:
        product *= value
    return int(product < sum(num_list) ** 2)

# 전체 코드 줄별 설명
# def solution(num_list):  # def는 함수 정의. 정수 리스트 입력.
#     product = 1  # 곱셈의 시작값은 1.
#     for value in num_list:  # for로 각 정수 순회.
#         product *= value  # *=는 곱해 저장. 전체 원소의 곱 누적.
#     return int(product < sum(num_list) ** 2)  # sum은 합계, **는 제곱, <는 미만 비교, int는 참·거짓을 1·0으로 변환.

# 풀이 요약
# 곱과 합의 제곱을 각각 계산한 뒤 비교합니다.
# 