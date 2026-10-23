def solution(p):
    if not p:
        return ''
    balance = 0
    # 최소 균형 접두부가 올바른지 저장.
    correct = True
    for index, character in enumerate(p, 1):
        # 여는 괄호면 +1, 닫는 괄호면 -1을 +=로 누적.
        balance += 1 if character == '(' else -1
        if balance < 0:
            # 현재 u의 위반 여부 기록.
            correct = False
        if balance == 0:
            # 끝은 미포함.
            u, v = p[:index], p[index:]
            if correct:
                return u + solution(v)
            flipped = ''.join(')' if ch == '(' else '(' for ch in u[1:-1])
            return '(' + solution(v) + ')' + flipped
