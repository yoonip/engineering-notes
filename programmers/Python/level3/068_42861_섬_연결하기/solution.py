# 섬 수와 [섬1,섬2,건설비] 목록을 받음.
def solution(n, costs):
    # 처음에는 각 섬이 자기 연결 집합의 대표.
    parent = list(range(n))
    # 대표별 집합 크기를 저장하는 서로소 집합(유니온 파인드) 자료구조.
    size = [1] * n
    # 현재 섬이 속한 연결 집합의 대표를 찾는 내부 함수.
    def find(node):
        # 자기 자신이 대표일 때까지 올라감.
        while parent[node] != node:
            # 부모를 조부모로 바꿔 다음 탐색을 빠르게 함.
            parent[node] = parent[parent[node]]
            # 더 위의 대표 후보로 이동.
            node = parent[node]
        # 최종 대표 반환.
        return node
    # 전체 건설비와 선택한 다리 수를 언패킹 대입.
    answer, used = 0, 0
    # 비용이 싼 다리부터 확인하는 크루스칼 알고리즘.
    for first, second, cost in sorted(costs, key=lambda edge: edge[2]):
        # 두 섬의 연결 집합 대표 조회.
        root_a, root_b = find(first), find(second)
        # 이미 연결된 두 섬을 잇는 다리는 순환만 만들므로 제외.
        if root_a == root_b:
            # 이번 다리 건너뜀.
            continue
        # 작은 집합을 큰 집합에 붙이기 위해 크기 비교.
        if size[root_a] < size[root_b]:
            # 두 변수의 값 교환.
            root_a, root_b = root_b, root_a
        # 두 연결 집합을 하나로 합침.
        parent[root_b] = root_a
        # 합쳐진 집합 크기 갱신.
        size[root_a] += size[root_b]
        # 선택한 다리 비용 합산.
        answer += cost
        used += 1
        # 모든 섬을 연결하는 트리에는 n-1개 다리면 충분.
        if used == n - 1:
            break
    # 최소 신장 트리(MST), 즉 모든 섬을 잇는 최소 비용 트리의 비용 반환.
    return answer
