# 문제: 택배상자
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/131704
# 풀이: 보조 컨베이어를 스택으로 표현한다. 다음 요청 상자가 스택 위에 오면 즉시 꺼내 각 상자를 한 번씩 넣고 뺀다.
# 복잡도: 상자 N개: 시간 O(N), 추가 공간 O(N).

def solution(order):
    stack = []
    answer = 0
    for box in range(1, len(order) + 1):
        stack.append(box)
        while stack and stack[-1] == order[answer]:
            stack.pop()
            answer += 1
    return answer
