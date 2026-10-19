# 문제: 뒤에 있는 큰 수 찾기
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/154539
# 풀이: 아직 답을 못 찾은 인덱스를 단조 스택에 둔다. 더 큰 수가 나타나면 작은 원소의 답을 확정해 반복적인 뒤쪽 탐색을 줄인다.
# 복잡도: 원소 N개: 시간 O(N), 추가 공간 O(N). 각 인덱스는 한 번씩 삽입·제거한다.

def solution(numbers):
    answer = [-1] * len(numbers)
    stack = []
    for index, value in enumerate(numbers):
        while stack and numbers[stack[-1]] < value:
            previous = stack.pop()
            answer[previous] = value
        stack.append(index)
    return answer
