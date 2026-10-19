def solution(my_strings, parts):
    return ''.join(text[start:end + 1] for text, (start, end) in zip(my_strings, parts))

# 전체 코드 줄별 설명
# def solution(my_strings, parts):  # def는 함수 정의. 문자열 리스트와 각 부분 범위 입력.
#     return ''.join(text[start:end + 1] for text, (start, end) in zip(my_strings, parts))  # zip은 같은 위치 원소를 묶음, 튜플 분해로 범위를 받음. 슬라이싱 후 join으로 연결.

# 풀이 요약
# 문자열과 해당 범위를 짝지어 부분 문자열들을 순서대로 이어 붙입니다.
# 