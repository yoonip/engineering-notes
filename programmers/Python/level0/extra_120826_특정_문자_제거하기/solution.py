def solution(my_string, letter):
    return my_string.replace(letter, '')

# 전체 코드 줄별 설명
# def solution(my_string, letter):  # def는 함수 정의. 원본 문자열과 제거할 한 문자 입력.
#     return my_string.replace(letter, '')  # replace(이전,새값)는 모든 해당 문자를 치환. 빈 문자열로 바꾸면 제거.

# 풀이 요약
# 대소문자를 구분하여 지정 문자만 모두 제거합니다.
# 