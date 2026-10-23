def solution(p):
    output = []
    tasks = [('convert', p)]
    while tasks:
        action, text = tasks.pop()
        if action == 'literal':
            output.append(text)
            continue
        if not text:
            continue
        balance, valid = 0, True
        for end, ch in enumerate(text, 1):
            balance += 1 if ch == '(' else -1
            valid &= balance >= 0
            if balance == 0:
                break
        u, v = text[:end], text[end:]
        if valid:
            output.append(u)
            tasks.append(('convert', v))
        else:
            output.append('(')
            flipped = ''.join(')' if ch == '(' else '(' for ch in u[1:-1])
            # 나중에 출력할 조각부터 넣어야 원하는 순서로 꺼낸다.
            tasks.append(('literal', ')' + flipped))
            tasks.append(('convert', v))
    return ''.join(output)
