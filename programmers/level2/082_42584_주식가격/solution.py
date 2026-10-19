# 문제: 주식가격
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/42584
# 풀이: 가격 하락을 기다리는 인덱스를 스택에 둔다. 낮은 가격이 오면 해당 인덱스의 기간을 확정해 뒤쪽 재탐색을 줄인다.
# 복잡도: 가격 N개: 시간 O(N), 추가 공간 O(N).

def solution(prices):
    n = len(prices)
    answer = [n - index - 1 for index in range(n)]
    stack = []
    for index, price in enumerate(prices):
        while stack and prices[stack[-1]] > price:
            previous = stack.pop()
            answer[previous] = index - previous
        stack.append(index)
    return answer
