def solution(myString, pat):
    return int(pat.lower() in myString.lower())

# 전체 코드 줄별 설명
# def solution(myString, pat):  # def는 함수 정의. 원본과 찾을 문자열 입력.
#     return int(pat.lower() in myString.lower())  # lower는 소문자 변환, in은 부분 문자열 포함 검사, int는 참·거짓을 1·0으로 변환.

# 풀이 요약
# 양쪽 문자열을 모두 소문자로 바꿔 대소문자를 구분하지 않고 찾습니다.
# 