# 같은 방문 노드 집합의 결과를 캐시해 중복 순서 탐색 방지.
from functools import lru_cache

# info는 양 0·늑대 1, edges는 부모·자식 연결.
def solution(info, edges):
    # len은 노드 개수.
    n = len(info)
    # 노드별 자식 집합을 정수 비트마스크로 저장.
    children = [0] * n
    # for~in으로 부모와 자식을 언패킹.
    for parent, child in edges:
        # 부모의 자식 집합에 해당 비트 추가.
        children[parent] |= 1 << child
    # ==는 같음 비교.
    sheep_mask = sum(1 << node for node in range(n) if info[node] == 0)

    # None은 캐시 용량 제한 없음.
    @lru_cache(None)
    # 지금까지 방문한 집합에서 최대로 모을 수 있는 양 수를 구하는 깊이 우선 재귀 탐색.
    def dfs(visited):
        # 방문한 양의 수 계산.
        sheep = (visited & sheep_mask).bit_count()
        # 전체 방문 노드 수에서 양을 빼 늑대 수 계산.
        wolves = visited.bit_count() - sheep
        # 늑대가 양 이상이면 즉시 잡아먹힌 불가능 상태.
        if wolves >= sheep:
            # return으로 이 잘못된 선택의 결과 0 반환.
            return 0
        # 여기서 더 탐색하지 않고 돌아오는 선택의 양 수.
        answer = sheep
        # 다음에 새로 방문할 수 있는 노드 집합 초기화.
        available = 0
        # 지금까지 방문한 부모들을 순회.
        for node in range(n):
            # 해당 노드 방문 비트가 켜져 있는지 검사.
            if visited & (1 << node):
                # 방문한 노드의 자식들을 다음 후보 집합에 합침.
                available |= children[node]
        # 이미 방문한 노드는 새 후보에서 제거.
        available &= ~visited
        # while은 후보 비트가 남아 있는 동안 반복.
        while available:
            # 정수와 그 음수의 AND는 가장 오른쪽 1비트만 추출.
            bit = available & -available
            # 꺼낸 후보 비트를 제거.
            available ^= bit
            # 해당 노드를 새로 방문한 경우와 비교.
            answer = max(answer, dfs(visited | bit))
        # 현재 방문 집합에서 가능한 최대 양 수 반환.
        return answer

    # 루트에는 항상 양이 있음.
    return dfs(1)
