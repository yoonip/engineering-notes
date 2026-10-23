def solution(prices):
    # =는 대입.
    n = len(prices)
    answer = [n - index - 1 for index in range(n)]
    stack = []
    # 현재 시점·가격 언패킹.
    for index, price in enumerate(prices):
        while stack and prices[stack[-1]] > price:
            # pop으로 하락 시점이 확정된 인덱스를 꺼내 삭제.
            previous = stack.pop()
            answer[previous] = index - previous
        # append로 현재 시점을 대기 스택에 추가.
        stack.append(index)
    return answer
