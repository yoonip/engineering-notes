def solution(n, costs):
    parent = list(range(n))
    size = [1] * n
    def find(node):
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node
    answer, used = 0, 0
    for first, second, cost in sorted(costs, key=lambda edge: edge[2]):
        root_a, root_b = find(first), find(second)
        if root_a == root_b:
            continue
        if size[root_a] < size[root_b]:
            root_a, root_b = root_b, root_a
        parent[root_b] = root_a
        size[root_a] += size[root_b]
        answer += cost
        used += 1
        if used == n - 1:
            break
    return answer

# 전체 코드 줄별 설명
# def solution(n, costs):  # def는 함수 정의. 섬 수와 [섬1,섬2,건설비] 목록을 받음.
#     parent = list(range(n))  # range(n)은 0~n-1, list는 리스트 변환. 처음에는 각 섬이 자기 연결 집합의 대표.
#     size = [1] * n  # []는 리스트, *는 반복. 대표별 집합 크기를 저장하는 서로소 집합(유니온 파인드) 자료구조.
#     def find(node):  # 현재 섬이 속한 연결 집합의 대표를 찾는 내부 함수.
#         while parent[node] != node:  # while은 조건 반복, !=는 다름. 자기 자신이 대표일 때까지 올라감.
#             parent[node] = parent[parent[node]]  # 경로 압축. 부모를 조부모로 바꿔 다음 탐색을 빠르게 함.
#             node = parent[node]  # 더 위의 대표 후보로 이동.
#         return node  # 최종 대표 반환.
#     answer, used = 0, 0  # 전체 건설비와 선택한 다리 수를 언패킹 대입.
#     for first, second, cost in sorted(costs, key=lambda edge: edge[2]):  # sorted는 정렬, lambda는 짧은 익명 함수. 비용이 싼 다리부터 확인하는 크루스칼 알고리즘.
#         root_a, root_b = find(first), find(second)  # 두 섬의 연결 집합 대표 조회.
#         if root_a == root_b:  # ==는 같음. 이미 연결된 두 섬을 잇는 다리는 순환만 만들므로 제외.
#             continue  # 이번 다리 건너뜀.
#         if size[root_a] < size[root_b]:  # 작은 집합을 큰 집합에 붙이기 위해 크기 비교.
#             root_a, root_b = root_b, root_a  # 두 변수의 값 교환.
#         parent[root_b] = root_a  # 두 연결 집합을 하나로 합침.
#         size[root_a] += size[root_b]  # +=는 더해 저장. 합쳐진 집합 크기 갱신.
#         answer += cost  # 선택한 다리 비용 합산.
#         used += 1  # 다리 수 증가.
#         if used == n - 1:  # 모든 섬을 연결하는 트리에는 n-1개 다리면 충분.
#             break  # 더 이상 다리를 확인하지 않음.
#     return answer  # 최소 신장 트리(MST), 즉 모든 섬을 잇는 최소 비용 트리의 비용 반환.

# 풀이 요약
# 싼 다리부터 선택하되 이미 이어진 집합 내부의 다리는 버린다. 연결되지 않은 두 집합 사이의 가장 싼 간선은 최적 해에도 포함시킬 수 있다.
# 예제는 0-1(1), 1-3(1), 0-2(2)를 골라 총 4. 유니온 파인드로 이미 연결되었는지 빠르게 확인한다.
# 다리 M개일 때 정렬이 주된 비용으로 시간 O(M log M), 공간 O(N+M).
# 