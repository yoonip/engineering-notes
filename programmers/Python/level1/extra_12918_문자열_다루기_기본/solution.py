def solution(s):
    return len(s) in (4, 6) and s.isdigit()

# 전체 코드 줄별 설명
# def solution(s):  # def는 함수 정의. 검사할 문자열 입력.
#     return len(s) in (4, 6) and s.isdigit()  # len은 길이, in은 튜플 포함 검사, and는 모두 참, isdigit은 모든 문자가 숫자인지 검사.

# 풀이 요약
# 문자열 길이가 4 또는 6이라는 조건과 숫자로만 구성된 조건을 모두 검사합니다.
# 