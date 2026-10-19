# 문제: 큰 수 만들기
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/42883
# 풀이: 뒤에 더 큰 숫자가 나오면 앞의 작은 숫자를 스택에서 제거한다. 각 숫자를 한 번씩 넣고 빼며 삭제 횟수를 맞춘다.
# 복잡도: 숫자 길이 N: 시간 O(N), 추가 공간 O(N).

def solution(number, k):
    stack = []
    for digit in number:
        while k > 0 and stack and stack[-1] < digit:
            stack.pop()
            k -= 1
        stack.append(digit)
    if k > 0:
        stack = stack[:-k]
    return ''.join(stack)
