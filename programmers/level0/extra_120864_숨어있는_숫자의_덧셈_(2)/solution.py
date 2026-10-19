def solution(my_string):
    separated = ''.join(char if char.isdigit() else ' ' for char in my_string)
    return sum(map(int, separated.split()))

# 전체 코드 줄별 설명
# def solution(my_string):  # def는 함수 정의. 문자와 여러 자리 숫자가 섞인 문자열 입력.
#     separated = ''.join(char if char.isdigit() else ' ' for char in my_string)  # isdigit은 숫자 문자 검사. 조건 표현식으로 문자만 공백으로 바꿔 숫자 구간을 분리.
#     return sum(map(int, separated.split()))  # split은 공백 기준 숫자 묶음 분리, map(int, ...)는 각 묶음을 정수 변환, sum은 합계.

# 풀이 요약
# 연속된 숫자는 유지하고 글자만 공백으로 바꿔 여러 자리 자연수 단위로 더합니다.
# 