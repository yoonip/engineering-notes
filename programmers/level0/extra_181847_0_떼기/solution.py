def solution(n_str):
    return n_str.lstrip('0')

# 전체 코드 줄별 설명
# def solution(n_str):  # def는 함수 정의. 앞쪽에 0이 있을 수 있는 문자열 입력.
#     return n_str.lstrip('0')  # lstrip(문자)는 왼쪽 끝에서 해당 문자가 반복되는 동안 제거. 중간·뒤의 0은 유지.

# 풀이 요약
# 문자열 왼쪽의 연속된 0만 제거합니다.
# 