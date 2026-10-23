def solution(s):
    balance = 0
    for ch in s:
        # 여는 괄호면 +1, 닫는 괄호면 -1을 더해 저장.
        balance += 1 if ch == '(' else -1
        if balance < 0:
            return False
    return balance == 0
