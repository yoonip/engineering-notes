def solution(myString):
    return ''.join(max(char, 'l') for char in myString)

# 전체 코드 줄별 설명
# def solution(myString):  # def는 함수 정의. 소문자 문자열 입력.
#     return ''.join(max(char, 'l') for char in myString)  # max는 사전순으로 큰 문자 선택. l보다 작은 문자를 l로 올리고 join으로 연결.

# 풀이 요약
# 각 문자를 l과 비교해 더 큰 쪽을 선택합니다.
# 