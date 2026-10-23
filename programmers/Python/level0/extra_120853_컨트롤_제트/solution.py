def solution(s):
    stack = []
    for token in s.split():
        if token == 'Z':
            stack.pop()
        else:
            stack.append(int(token))
    return sum(stack)

# 전체 코드 줄별 설명
# def solution(s):  # def는 함수 정의. 숫자와 취소 명령 Z의 문자열 입력.
#     stack = []  # []는 빈 리스트. 아직 취소되지 않은 숫자들을 스택으로 저장.
#     for token in s.split():  # split은 공백으로 나누기, for는 각 항목 순회.
#         if token == 'Z':  # if는 조건, ==는 같음 비교. 취소 명령인지 확인.
#             stack.pop()  # pop은 마지막 숫자 제거. 가장 최근 더한 수를 취소.
#         else:  # 숫자 문자열인 경우.
#             stack.append(int(token))  # int는 정수 변환, append는 끝에 추가.
#     return sum(stack)  # sum으로 취소되지 않은 숫자 합계 반환.

# 풀이 요약
# Z를 만나면 스택의 마지막 숫자를 제거하고 남은 값만 합산합니다.
# 