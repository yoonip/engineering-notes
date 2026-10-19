# 문제: 프로세스
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/42587
# 풀이: deque로 대기 순서를, Counter로 우선순위별 남은 수를 관리한다. 최댓값을 갱신해 매 회전의 전체 큐 탐색을 없앤다.
# 복잡도: 프로세스 N개·우선순위 종류 P≤9: 시간 O(NP)=O(N), 추가 공간 O(N+P). 큐 회전마다 전체 탐색을 하지 않는다.

from collections import Counter, deque


def solution(priorities, location):
    queue = deque(enumerate(priorities))
    counts = Counter(priorities)
    highest = max(priorities)
    executed = 0
    while queue:
        index, priority = queue.popleft()
        if priority < highest:
            queue.append((index, priority))
            continue
        executed += 1
        counts[priority] -= 1
        if index == location:
            return executed
        # 우선순위가 1~9이므로 최댓값 갱신에 전체 큐 탐색이 필요 없다.
        while highest > 0 and counts[highest] == 0:
            highest -= 1
