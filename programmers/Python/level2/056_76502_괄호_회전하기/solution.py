def solution(s):
    pairs = {')': '(', ']': '[', '}': '{'}
    answer = 0
    for offset in range(len(s)):
        stack = []
        for character in s[offset:] + s[:offset]:
            # 가장 최근의 여는 괄호부터 닫혀야 한다.
            if character in '([{':
                stack.append(character)
            # 짝이 맞지 않거나 여는 괄호가 없으면 이 회전은 실패다.
            elif not stack or stack.pop() != pairs[character]:
                break
        else:
            if not stack:
                answer += 1
    return answer
