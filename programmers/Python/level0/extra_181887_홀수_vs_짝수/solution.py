def solution(num_list):
    return max(sum(num_list[::2]), sum(num_list[1::2]))

# 전체 코드 줄별 설명
# def solution(num_list):  # def는 함수 정의. 정수 리스트 입력.
#     return max(sum(num_list[::2]), sum(num_list[1::2]))  # [::2]는 홀수 번째, [1::2]는 짝수 번째 원소. sum은 합계, max는 큰 값 선택.

# 풀이 요약
# 원소의 값이 홀수인지가 아니라 원소의 순번이 홀수·짝수인지 구분합니다.
# 