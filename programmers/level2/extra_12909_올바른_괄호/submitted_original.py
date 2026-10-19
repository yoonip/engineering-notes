def solution(s):
    balance = 0
    for ch in s:
        balance += 1 if ch == '(' else -1
        if balance < 0:
            return False
    return balance == 0

# 전체 코드 줄별 설명
# def solution(s):  # def는 함수 정의. 소괄호 문자열 입력.
#     balance = 0  # 아직 닫히지 않은 여는 괄호 개수.
#     for ch in s:  # for로 글자를 왼쪽부터 순회.
#         balance += 1 if ch == '(' else -1  # 조건부 표현식. ==는 같음. 여는 괄호면 +1, 닫는 괄호면 -1을 더해 저장.
#         if balance < 0:  # 닫는 괄호가 먼저 나와 짝지을 여는 괄호가 부족한 경우.
#             return False  # False는 거짓. 뒤에서 괄호가 더 와도 앞의 잘못된 순서를 고칠 수 없음.
#     return balance == 0  # 끝에 미완성 여는 괄호도 없어야 참(True). 비교식 결과를 그대로 반환.

# 풀이 요약
# 모든 앞부분에서 여는 괄호 수≥닫는 괄호 수이고, 전체 개수가 같으면 올바른 괄호다.
# 예: )()(는 첫 글자에서 바로 실패하고, (()(는 끝에 balance=2가 남아 실패한다. 시간 O(N), 공간 O(1).
# 