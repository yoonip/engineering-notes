def solution(order):
    return sum(char in '369' for char in str(order))

# 전체 코드 줄별 설명
# def solution(order):  # def는 함수 정의. 말해야 하는 정수 입력.
#     return sum(char in '369' for char in str(order))  # str은 문자열 변환, in은 3·6·9 중 하나인지 검사. sum은 참을 1로 세어 합산.

# 풀이 요약
# 각 자릿수가 3·6·9인지 검사해 박수 횟수를 셉니다.
# 