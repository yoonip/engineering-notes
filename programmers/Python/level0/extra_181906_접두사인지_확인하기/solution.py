def solution(my_string, is_prefix):
    return int(my_string.startswith(is_prefix))

# 전체 코드 줄별 설명
# def solution(my_string, is_prefix):  # def는 함수 정의. 문자열과 접두사 후보 입력.
#     return int(my_string.startswith(is_prefix))  # startswith는 지정 문자열로 시작하는지 검사. int는 참을 1, 거짓을 0으로 변환.

# 풀이 요약
# 문자열 시작이 후보 문자열과 일치하는지 검사합니다.
# 