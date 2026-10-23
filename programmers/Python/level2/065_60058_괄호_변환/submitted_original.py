def solution(p):
    if not p:
        return ''
    balance = 0
    correct = True
    for index, character in enumerate(p, 1):
        balance += 1 if character == '(' else -1
        if balance < 0:
            correct = False
        if balance == 0:
            u, v = p[:index], p[index:]
            if correct:
                return u + solution(v)
            flipped = ''.join(')' if ch == '(' else '(' for ch in u[1:-1])
            return '(' + solution(v) + ')' + flipped

# 전체 코드 줄별 설명
# def solution(p):  # def는 함수 정의. p는 균형잡힌 괄호 문자열 입력.
#     if not p:  # not은 참·거짓 반전. 빈 문자열은 거짓이므로 종료 조건.
#         return ''  # return으로 빈 문자열 반환.
#     balance = 0  # =는 대입. 여는 괄호 수-닫는 괄호 수 초기화.
#     correct = True  # True는 참. 최소 균형 접두부가 올바른지 저장.
#     for index, character in enumerate(p, 1):  # enumerate(문자열,1)은 1부터 번호 부여. 자를 길이와 문자를 언패킹.
#         balance += 1 if character == '(' else -1  # 조건 표현식. ==는 같음. 여는 괄호면 +1, 닫는 괄호면 -1을 +=로 누적.
#         if balance < 0:  # <는 작음. 닫는 괄호가 먼저 많아지면 올바르지 않음.
#             correct = False  # False는 거짓. 현재 u의 위반 여부 기록.
#         if balance == 0:  # 최초로 균형이 맞으면 더 분리할 수 없는 u 완성.
#             u, v = p[:index], p[index:]  # 슬라이스 [시작:끝]으로 u·v 분리. 끝은 미포함.
#             if correct:  # if는 조건 분기. u가 올바르면 그대로 보존.
#                 return u + solution(v)  # +로 문자열 연결. v를 같은 함수로 재귀 변환해 뒤에 붙임.
#             flipped = ''.join(')' if ch == '(' else '(' for ch in u[1:-1])  # [1:-1]은 양끝 제외. 생성식으로 괄호 방향을 바꾸고 join으로 연결.
#             return '(' + solution(v) + ')' + flipped  # 지정 절차대로 변환한 v를 감싸고 뒤집은 u 내부를 붙여 반환.

# 풀이 요약
# 가장 짧은 균형 접두부 u를 찾습니다. u가 올바르면 u+변환(v), 아니면 '('+변환(v)+')'+방향을 뒤집은 u 내부를 반환합니다.
# 예: '()))((()'는 '()(())()'. 문자열 복사·연결을 포함한 시간·공간 상한 O(N²), 재귀 깊이 O(N).
