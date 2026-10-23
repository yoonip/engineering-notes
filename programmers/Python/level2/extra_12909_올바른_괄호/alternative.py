def solution(s):
    stack = []
    for ch in s:
        if ch == '(':
            stack.append(ch)
        elif not stack:
            return False
        else:
            stack.pop()
    return not stack
