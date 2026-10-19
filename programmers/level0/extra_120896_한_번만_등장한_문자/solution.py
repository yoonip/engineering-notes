def solution(s):
    return ''.join(sorted(char for char in set(s) if s.count(char) == 1))

# 전체 코드 줄별 설명
# def solution(s):  # def는 함수 정의. 소문자 문자열 입력.
#     return ''.join(sorted(char for char in set(s) if s.count(char) == 1))  # set은 서로 다른 문자, count는 출현 횟수, if는 한 번 나온 문자 필터, sorted는 정렬, join은 문자열 연결.

# 풀이 요약
# 각 문자의 출현 횟수가 1인지 검사한 뒤 사전순으로 연결합니다.
# 