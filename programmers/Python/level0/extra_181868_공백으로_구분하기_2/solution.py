def solution(my_string):
    return my_string.split()

# 전체 코드 줄별 설명
# def solution(my_string):  # def는 함수 정의. 여러 공백을 포함할 수 있는 문자열 입력.
#     return my_string.split()  # 인자 없는 split은 연속된 공백을 하나의 구분자로 취급하고 앞뒤 공백도 무시.

# 풀이 요약
# split에 구분자를 지정하지 않으면 여러 공백과 양 끝 공백을 한 번에 처리합니다.
# 