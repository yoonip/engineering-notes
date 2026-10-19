def solution(num_list):
    if len(num_list) >= 11:
        return sum(num_list)
    product = 1
    for value in num_list:
        product *= value
    return product

# 전체 코드 줄별 설명
# def solution(num_list):  # def는 함수 정의. 정수 리스트 입력.
#     if len(num_list) >= 11:  # len은 길이, >=는 이상 비교. 원소 개수가 11 이상인지 확인.
#         return sum(num_list)  # sum은 원소의 합계, return은 결과 반환.
#     product = 1  # 곱셈 누적의 시작값은 1.
#     for value in num_list:  # 각 정수 순회.
#         product *= value  # *=는 곱해 저장. 원소들의 곱 누적.
#     return product  # 길이가 10 이하인 경우 전체 곱 반환.

# 풀이 요약
# 길이에 따라 합계 또는 곱을 선택합니다.
# 