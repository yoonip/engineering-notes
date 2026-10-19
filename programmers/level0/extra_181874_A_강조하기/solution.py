def solution(myString):
    return myString.lower().replace('a', 'A')

# 전체 코드 줄별 설명
# def solution(myString):  # def는 함수 정의. 문자열 입력.
#     return myString.lower().replace('a', 'A')  # lower로 전체 소문자 변환 후 replace(이전,새값)로 a만 대문자 A로 바꿈.

# 풀이 요약
# 모두 소문자로 바꾼 다음 a만 다시 대문자로 바꾸면 A만 강조됩니다.
# 