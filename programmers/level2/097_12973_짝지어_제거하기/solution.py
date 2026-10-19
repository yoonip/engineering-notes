def solution(s):
    stack = []
    # 문자를 왼쪽부터 순회.
    for character in s:
        if stack and stack[-1] == character:
            stack.pop()
        else:
            # append로 새 문자를 스택 끝에 추가.
            stack.append(character)
    return int(not stack)
