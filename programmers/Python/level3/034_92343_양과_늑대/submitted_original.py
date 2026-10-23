from functools import lru_cache

def solution(info, edges):
    n = len(info)
    children = [0] * n
    for parent, child in edges:
        children[parent] |= 1 << child
    sheep_mask = sum(1 << node for node in range(n) if info[node] == 0)

    @lru_cache(None)
    def dfs(visited):
        sheep = (visited & sheep_mask).bit_count()
        wolves = visited.bit_count() - sheep
        if wolves >= sheep:
            return 0
        answer = sheep
        available = 0
        for node in range(n):
            if visited & (1 << node):
                available |= children[node]
        available &= ~visited
        while available:
            bit = available & -available
            available ^= bit
            answer = max(answer, dfs(visited | bit))
        return answer

    return dfs(1)

# 전체 코드 줄별 설명
# from functools import lru_cache  # functools에서 lru_cache를 import. 같은 방문 노드 집합의 결과를 캐시해 중복 순서 탐색 방지.
# 
# def solution(info, edges):  # def는 함수 정의. info는 양 0·늑대 1, edges는 부모·자식 연결.
#     n = len(info)  # len은 노드 개수.
#     children = [0] * n  # [] 리스트와 * 반복. 노드별 자식 집합을 정수 비트마스크로 저장.
#     for parent, child in edges:  # for~in으로 부모와 자식을 언패킹.
#         children[parent] |= 1 << child  # <<는 비트 이동, |=는 OR 후 저장. 부모의 자식 집합에 해당 비트 추가.
#     sheep_mask = sum(1 << node for node in range(n) if info[node] == 0)  # 생성식과 sum으로 양이 있는 노드 비트만 합침. ==는 같음 비교.
# 
#     @lru_cache(None)  # @는 데코레이터 적용. None은 캐시 용량 제한 없음.
#     def dfs(visited):  # 지금까지 방문한 집합에서 최대로 모을 수 있는 양 수를 구하는 깊이 우선 재귀 탐색.
#         sheep = (visited & sheep_mask).bit_count()  # &는 교집합 비트 AND, bit_count는 1비트 수. 방문한 양의 수 계산.
#         wolves = visited.bit_count() - sheep  # 전체 방문 노드 수에서 양을 빼 늑대 수 계산.
#         if wolves >= sheep:  # if는 조건문, >=는 이상. 늑대가 양 이상이면 즉시 잡아먹힌 불가능 상태.
#             return 0  # return으로 이 잘못된 선택의 결과 0 반환.
#         answer = sheep  # 여기서 더 탐색하지 않고 돌아오는 선택의 양 수.
#         available = 0  # 다음에 새로 방문할 수 있는 노드 집합 초기화.
#         for node in range(n):  # range는 0~n-1. 지금까지 방문한 부모들을 순회.
#             if visited & (1 << node):  # 해당 노드 방문 비트가 켜져 있는지 검사.
#                 available |= children[node]  # 방문한 노드의 자식들을 다음 후보 집합에 합침.
#         available &= ~visited  # ~는 비트 반전, &=는 AND 후 저장. 이미 방문한 노드는 새 후보에서 제거.
#         while available:  # while은 후보 비트가 남아 있는 동안 반복.
#             bit = available & -available  # 정수와 그 음수의 AND는 가장 오른쪽 1비트만 추출.
#             available ^= bit  # ^는 XOR. 꺼낸 후보 비트를 제거.
#             answer = max(answer, dfs(visited | bit))  # max는 큰 값, |는 OR. 해당 노드를 새로 방문한 경우와 비교.
#         return answer  # 현재 방문 집합에서 가능한 최대 양 수 반환.
# 
#     return dfs(1)  # 루트 0번의 비트만 켠 정수 1로 시작. 루트에는 항상 양이 있음.

# 풀이 요약
# 방문했던 노드 사이를 다시 이동해도 양·늑대 수는 변하지 않으므로, 현재 위치 대신 방문 집합만 상태로 사용합니다.
# 방문한 부모들의 아직 안 간 자식 중 하나를 고릅니다. 늑대≥양이 되는 선택은 즉시 버리고, 같은 방문 집합은 캐시합니다. 시간 O(N2^N), 공간 O(2^N).
# 예: 양이 두 마리·늑대가 한 마리일 때 늑대를 먼저 더 방문하면 즉시 실패합니다. 다른 가지의 양을 먼저 모으면 그 늑대도 나중에 안전하게 방문할 수 있습니다.
# 