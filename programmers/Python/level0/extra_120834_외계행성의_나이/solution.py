def solution(age):
    return ''.join(chr(ord('a') + int(char)) for char in str(age))

# 전체 코드 줄별 설명
# def solution(age):  # def는 함수 정의. 숫자로 표현된 나이 입력.
#     return ''.join(chr(ord('a') + int(char)) for char in str(age))  # str은 숫자 문자열 변환, int는 각 자릿수 변환, ord는 문자 코드, chr은 코드에서 문자 변환, join은 연결.

# 풀이 요약
# 숫자 0~9를 a~j로 대응시켜 각 자릿수를 바꿉니다.
# 