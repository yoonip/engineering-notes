def solution(my_string):
    return sum(int(char) for char in my_string if char.isdigit())

# 전체 코드 줄별 설명
# def solution(my_string):  # def는 함수 정의. 문자와 한 자리 숫자가 섞인 문자열 입력.
#     return sum(int(char) for char in my_string if char.isdigit())  # isdigit은 숫자 문자 검사. 생성기에서 숫자만 int로 변환하고 sum으로 합산.

# 풀이 요약
# 이 문제는 연속된 숫자도 자릿수 하나씩 따로 더합니다.
# 