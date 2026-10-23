def solution(n):
    return sum(int(char) for char in str(n))

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의. 자릿수를 더할 정수 입력.
#     return sum(int(char) for char in str(n))  # str로 정수를 문자열로 변환. 각 문자를 int로 바꾸는 생성기 표현식을 sum으로 합산.

# 풀이 요약
# 정수를 문자열로 바꿔 각 자릿수를 따로 더합니다.
# 