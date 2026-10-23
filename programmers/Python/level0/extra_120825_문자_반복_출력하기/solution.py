def solution(my_string, n):
    return ''.join(char * n for char in my_string)

# 전체 코드 줄별 설명
# def solution(my_string, n):  # def는 함수 정의. 문자열과 각 문자 반복 횟수 입력.
#     return ''.join(char * n for char in my_string)  # 문자 * 정수는 문자 반복. 생성기 표현식으로 각 글자를 반복하고 join으로 연결.

# 풀이 요약
# 문자열 전체가 아닌 각 글자를 n번씩 반복합니다.
# 