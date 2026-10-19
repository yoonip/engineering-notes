def solution(s):
    return ''.join(sorted(s, reverse=True))

# 전체 코드 줄별 설명
# def solution(s):  # def는 함수 정의. 영문 대소문자 문자열 입력.
#     return ''.join(sorted(s, reverse=True))  # sorted는 문자 정렬, reverse=True는 내림차순, join은 문자열 연결. 문자 코드상 소문자가 대문자보다 큼.

# 풀이 요약
# 파이썬 문자 정렬 순서가 문제의 대소문자 크기 정의와 같으므로 내림차순 정렬합니다.
# 