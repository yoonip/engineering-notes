def solution(my_string, target):
    return int(target in my_string)

# 전체 코드 줄별 설명
# def solution(my_string, target):  # def는 함수 정의. 원본과 부분 문자열 후보 입력.
#     return int(target in my_string)  # in은 연속 부분 문자열 포함 검사, int는 참을 1·거짓을 0으로 변환.

# 풀이 요약
# target이 my_string 안에 연속해서 나타나는지 검사합니다.
# 