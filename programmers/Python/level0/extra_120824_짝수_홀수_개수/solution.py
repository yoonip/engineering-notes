def solution(num_list):
    even = sum(value % 2 == 0 for value in num_list)
    return [even, len(num_list) - even]

# 전체 코드 줄별 설명
# def solution(num_list):  # def는 함수 정의. 정수 리스트 입력.
#     even = sum(value % 2 == 0 for value in num_list)  # %는 나머지, ==는 같음 비교. sum은 짝수 조건의 참을 1로 합산.
#     return [even, len(num_list) - even]  # []는 리스트. len은 전체 개수. 전체에서 짝수 개수를 빼 홀수 개수 계산.

# 풀이 요약
# 짝수 개수를 먼저 세고 나머지를 홀수 개수로 계산합니다.
# 