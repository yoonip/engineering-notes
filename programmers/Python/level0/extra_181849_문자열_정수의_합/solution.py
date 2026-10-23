def solution(num_str):
    return sum(map(int, num_str))

# 전체 코드 줄별 설명
# def solution(num_str):  # def는 함수 정의. 숫자 문자열 입력.
#     return sum(map(int, num_str))  # map(int,문자열)은 각 숫자를 정수로 변환. sum은 변환된 자릿수의 합 계산.

# 풀이 요약
# 전체를 하나의 정수로 바꾸지 않고 각 자릿수를 더합니다.
# 