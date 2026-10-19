def solution(my_string):
    return ''.join(dict.fromkeys(my_string))

# 전체 코드 줄별 설명
# def solution(my_string):  # def는 함수 정의. 공백과 대소문자를 포함한 문자열 입력.
#     return ''.join(dict.fromkeys(my_string))  # dict.fromkeys는 문자를 키로 만드는 딕셔너리 생성. 중복은 제거하고 첫 등장 순서 유지. join으로 연결.

# 풀이 요약
# 딕셔너리의 키는 중복되지 않고 삽입 순서가 유지되므로 첫 문자만 남길 수 있습니다.
# 