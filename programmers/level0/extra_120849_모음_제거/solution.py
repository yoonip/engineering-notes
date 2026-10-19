def solution(my_string):
    return ''.join(char for char in my_string if char not in 'aeiou')

# 전체 코드 줄별 설명
# def solution(my_string):  # def는 함수 정의. 소문자와 공백 문자열 입력.
#     return ''.join(char for char in my_string if char not in 'aeiou')  # not in은 모음 목록에 없음 검사. 생성기 표현식에서 모음을 제외하고 join으로 연결.

# 풀이 요약
# 다섯 모음에 속하지 않은 문자와 공백만 유지합니다.
# 