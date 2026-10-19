def solution(my_string, is_suffix):
    return int(my_string.endswith(is_suffix))

# 전체 코드 줄별 설명
# def solution(my_string, is_suffix):  # def는 함수 정의. 원본 문자열과 접미사 후보 입력.
#     return int(my_string.endswith(is_suffix))  # endswith는 지정 문자열로 끝나는지 검사. int는 True를 1, False를 0으로 변환.

# 풀이 요약
# 문자열 끝이 후보 문자열과 일치하는지 검사합니다.
# 