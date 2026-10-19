def solution(n, wires):
    graph = [[] for _ in range(n + 1)]
    for a, b in wires:
        graph[a].append(b)
        graph[b].append(a)
    answer = n
    def dfs(node, parent):
        nonlocal answer
        size = 1
        for neighbor in graph[node]:
            if neighbor == parent:
                continue
            child_size = dfs(neighbor, node)
            answer = min(answer, abs(n - 2 * child_size))
            size += child_size
        return size
    dfs(1, 0)
    return answer

# 전체 코드 줄별 설명
# def solution(n, wires):  # def는 함수 정의. n은 송전탑 수, wires는 트리 간선 목록.
#     graph = [[] for _ in range(n + 1)]  # 리스트 내포로 정점별 독립된 인접 리스트 생성. _는 안 쓰는 변수.
#     for a, b in wires:  # for~in으로 간선 양 끝 번호 언패킹.
#         graph[a].append(b)  # [a]는 a번 인접 목록. append로 이웃 추가.
#         graph[b].append(a)  # 양방향 전선이므로 반대쪽도 연결.
#     answer = n  # =는 대입. 최소 차이를 큰 값으로 초기화.
#     def dfs(node, parent):  # 중첩 함수. 현재 정점 아래 부분 트리 크기를 재귀 계산.
#         nonlocal answer  # nonlocal은 바깥 함수의 answer를 이 함수에서 변경하도록 지정.
#         size = 1  # 자기 자신을 포함한 부분 트리 크기 초기화.
#         for neighbor in graph[node]:  # 인접한 송전탑 순회.
#             if neighbor == parent:  # ==는 같음. 방금 온 부모로 되돌아가는 간선 검사.
#                 continue  # continue로 부모 간선 건너뜀.
#             child_size = dfs(neighbor, node)  # 자식 부분 트리의 정점 수를 재귀 호출로 얻음.
#             answer = min(answer, abs(n - 2 * child_size))  # min은 최솟값, abs는 절댓값. 간선을 끊었을 때 s와 n-s의 차이 비교.
#             size += child_size  # +=는 더해 저장. 자식 부분 트리 크기 누적.
#         return size  # 현재 부분 트리 크기를 호출한 부모에게 반환.
#     dfs(1, 0)  # 1번을 루트로 탐색. 0은 실제 정점이 아닌 부모 표시.
#     return answer  # return으로 모든 전선 절단 중 최소 차이 반환.

# 풀이 요약
# 자식으로 가는 전선을 끊으면 자식 부분 트리 s개와 나머지 n-s개로 나뉩니다. 모든 간선의 |n-2s|를 비교합니다.
# 예: 일자형 4개 송전탑은 가운데 전선을 끊어 2:2, 차이 0. 시간·공간 O(N).
