def solution(my_string, n):
    return my_string[-n:]

# 전체 코드 줄별 설명
# def solution(my_string, n):  # def는 함수 정의. 문자열과 가져올 글자 수 입력.
#     return my_string[-n:]  # 음수 인덱스 -n은 뒤에서 n번째 위치. [시작:] 슬라이싱으로 그 위치부터 끝까지 반환.

# 풀이 요약
# 뒤에서 n번째 글자부터 끝까지 잘라냅니다.
# 