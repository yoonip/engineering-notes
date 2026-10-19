def solution(numbers):
    answer = [-1] * len(numbers)
    stack = []
    for index, value in enumerate(numbers):
        # 지금 값이 처음 만난 더 큰 수인 미해결 인덱스를 꺼낸다.
        while stack and numbers[stack[-1]] < value:
            previous = stack.pop()
            answer[previous] = value
        # 현재 인덱스도 이후의 더 큰 수를 기다린다.
        stack.append(index)
    return answer
