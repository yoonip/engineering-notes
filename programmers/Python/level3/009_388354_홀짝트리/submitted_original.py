def solution(nodes, edges):
    n = len(nodes)
    index = {node: i for i, node in enumerate(nodes)}
    parent = list(range(n))
    sizes = [1] * n
    degrees = [0] * n

    def find(node):
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    for a, b in edges:
        a, b = index[a], index[b]
        degrees[a] += 1
        degrees[b] += 1
        first, second = find(a), find(b)
        if first != second:
            if sizes[first] < sizes[second]:
                first, second = second, first
            parent[second] = first
            sizes[first] += sizes[second]
    matches = [0] * n
    for i, node in enumerate(nodes):
        if node % 2 == degrees[i] % 2:
            matches[find(i)] += 1
    answer = [0, 0]
    for root in range(n):
        if parent[root] == root:
            answer[0] += int(matches[root] == 1)
            answer[1] += int(matches[root] == sizes[root] - 1)
    return answer

# 전체 코드 줄별 설명
# def solution(nodes, edges):  # def는 함수 정의. nodes는 노드 번호, edges는 무방향 연결 목록.
#     n = len(nodes)  # len은 원소 개수. 실제 노드 수.
#     index = {node: i for i, node in enumerate(nodes)}  # {} 딕셔너리 내포. enumerate의 (순번,값)으로 큰 노드 번호를 0 기반 인덱스로 압축.
#     parent = list(range(n))  # range는 0~n-1, list는 목록 생성. 서로소 집합의 부모를 자기 자신으로 초기화.
#     sizes = [1] * n  # [] 리스트와 * 반복으로 각 연결 집합의 크기 초기화.
#     degrees = [0] * n  # 노드별 연결된 간선 수인 차수 초기화.
# 
#     def find(node):  # 연결 집합의 대표를 찾는 중첩 함수 정의.
#         while parent[node] != node:  # while은 반복, !=는 다름. 대표에 도달할 때까지 부모를 따라감.
#             parent[node] = parent[parent[node]]  # 경로 압축. 다음 대표 탐색이 빨라지도록 조상으로 바로 연결.
#             node = parent[node]  # 상위 노드로 이동.
#         return node  # return으로 대표 인덱스 반환.
# 
#     for a, b in edges:  # for~in으로 간선 두 끝 번호를 언패킹.
#         a, b = index[a], index[b]  # 딕셔너리 [키] 조회로 압축 인덱스로 변환.
#         degrees[a] += 1  # +=는 더해 저장. a의 차수 증가.
#         degrees[b] += 1  # 무방향 간선이므로 b의 차수도 증가.
#         first, second = find(a), find(b)  # 두 노드의 연결 집합 대표 조회.
#         if first != second:  # if는 조건문. 이미 같은 집합이면 다시 합치지 않음.
#             if sizes[first] < sizes[second]:  # 작은 집합을 큰 집합에 붙이기 위해 순서 조정.
#                 first, second = second, first  # 두 변수 값을 튜플 대입으로 교환.
#             parent[second] = first  # 두 집합을 하나로 합침.
#             sizes[first] += sizes[second]  # 대표가 보관하는 트리 크기 갱신.
#     matches = [0] * n  # 각 트리에서 번호와 차수의 홀짝이 같은 노드 수 저장.
#     for i, node in enumerate(nodes):  # 원래 번호와 압축 인덱스를 함께 순회.
#         if node % 2 == degrees[i] % 2:  # %는 나머지, ==는 같음. 번호와 차수의 홀짝 일치 여부.
#             matches[find(i)] += 1  # 해당 연결 집합의 일치 수 증가.
#     answer = [0, 0]  # 홀짝 트리 수·역홀짝 트리 수를 담은 리스트.
#     for root in range(n):  # 모든 인덱스를 순회해 집합 대표만 처리.
#         if parent[root] == root:  # 부모가 자기 자신이면 한 트리의 대표.
#             answer[0] += int(matches[root] == 1)  # int는 참을 1로 변환. 홀짝 일치 노드가 정확히 하나여야 그 노드를 루트로 삼을 수 있음.
#             answer[1] += int(matches[root] == sizes[root] - 1)  # 불일치 노드가 정확히 하나이면 그 노드를 루트로 삼아 역홀짝 트리 가능.
#     return answer  # 두 종류의 가능한 트리 개수를 반환.

# 풀이 요약
# 루트의 자식 수는 차수와 같고, 나머지 노드의 자식 수는 차수-1이라 홀짝이 뒤집힙니다.
# 따라서 번호·차수 홀짝 일치 노드가 정확히 하나면 홀짝 트리, 불일치가 정확히 하나면 역홀짝 트리입니다. 서로소 집합으로 트리를 묶어 개수만 셉니다. 시간 O((N+E)α(N)), 공간 O(N). α는 매우 느리게 증가하는 역 아커만 함수입니다.
# 예: 고립된 짝수 노드는 자식 0개이므로 홀짝 트리, 고립된 홀수 노드는 역홀짝 트리입니다. 루트 선택 수가 아니라 가능한 트리 수를 셉니다.
