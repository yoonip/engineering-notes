def solution(strArr):
    return [text.upper() if i % 2 else text.lower() for i, text in enumerate(strArr)]

# 전체 코드 줄별 설명
# def solution(strArr):  # def는 함수 정의. 문자열 리스트 입력.
#     return [text.upper() if i % 2 else text.lower() for i, text in enumerate(strArr)]  # enumerate는 인덱스와 값 제공. %2가 1인 홀수 인덱스는 upper, 짝수는 lower 적용하는 리스트 내포.

# 풀이 요약
# 0부터 세는 인덱스가 짝수면 소문자, 홀수면 대문자로 변환합니다.
# 