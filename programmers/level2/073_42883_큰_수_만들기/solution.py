def solution(number, k):
    stack = []
    # 숫자 문자를 왼쪽부터 순회.
    for digit in number:
        while k > 0 and stack and stack[-1] < digit:
            stack.pop()
            k -= 1
        # 같은 자리 문자 비교는 숫자 크기 순서와 같음.
        stack.append(digit)
    if k > 0:
        stack = stack[:-k]
    return ''.join(stack)
