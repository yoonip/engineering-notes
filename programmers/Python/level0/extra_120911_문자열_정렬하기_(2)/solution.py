def solution(my_string):
    return ''.join(sorted(my_string.lower()))

# 전체 코드 줄별 설명
# def solution(my_string):  # def는 함수 정의. 알파벳 문자열 입력.
#     return ''.join(sorted(my_string.lower()))  # lower는 소문자 변환, sorted는 문자들을 사전순 정렬한 리스트 반환, join은 문자열 연결.

# 풀이 요약
# 소문자로 통일한 후 각 문자를 정렬해 다시 연결합니다.
# 