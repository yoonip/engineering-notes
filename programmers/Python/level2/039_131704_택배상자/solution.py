def solution(order):
    stack = []
    answer = 0
    for box in range(1, len(order) + 1):
        stack.append(box)
        # 보조 벨트 맨 위가 필요한 상자이면 바로 싣는다.
        while stack and stack[-1] == order[answer]:
            stack.pop()
            answer += 1
    return answer
