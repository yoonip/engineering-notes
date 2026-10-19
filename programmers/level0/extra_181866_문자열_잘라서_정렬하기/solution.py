def solution(myString):
    return sorted(part for part in myString.split('x') if part)

# 전체 코드 줄별 설명
# def solution(myString):  # def는 함수 정의. x로 나눌 문자열 입력.
#     return sorted(part for part in myString.split('x') if part)  # split은 분리, if part는 빈 문자열 제외, sorted는 사전순 정렬.

# 풀이 요약
# x로 나눈 뒤 빈 조각은 버리고 남은 문자열을 정렬합니다.
# 