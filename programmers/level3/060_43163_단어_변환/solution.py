# deque는 먼저 넣은 원소를 앞에서 빠르게 꺼내는 BFS용 큐.
from collections import deque

# 시작 단어·목표 단어·사용 가능한 단어 목록을 받음.
def solution(begin, target, words):
    # 목표가 목록에 없으면 변환 불가능.
    if target not in words:
        # 큐가 빌 때까지 목표에 도달하지 못하면 불가능.
        return 0
    # (단어,변환 횟수)를 담은 선입선출 큐 생성.
    queue = deque([(begin, 0)])
    # 이미 발견한 단어를 저장.
    visited = {begin}
    # 큐가 비어 있지 않은 동안 너비 우선 탐색(BFS).
    while queue:
        # 두 값을 언패킹.
        word, steps = queue.popleft()
        # 목표 단어에 도달했는지 검사.
        if word == target:
            # BFS는 적은 변환 횟수부터 방문하므로 처음 도착한 횟수가 최소.
            return steps
        # for로 다음 변환 후보 단어 순회.
        for candidate in words:
            # sum은 다른 글자의 수를 합산해 정확히 하나인지 검사.
            if candidate not in visited and sum(a != b for a, b in zip(word, candidate)) == 1:
                # 큐에 넣을 때 방문 표시해 중복 탐색 방지.
                visited.add(candidate)
                # 한 번 변환한 다음 단어를 큐에 넣음.
                queue.append((candidate, steps + 1))
    # 큐가 빌 때까지 목표에 도달하지 못하면 불가능.
    return 0
