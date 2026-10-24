# 중요한 도로 — Python 재풀이

[문제 원문](<https://school.programmers.co.kr/learn/courses/30/lessons/214293>) · [재풀이 목록](<../README.md>)

정답률 3%와 풀이 인원 107명은 이번 목록 확인 시점의 값입니다. 전체 5순위로 진행했습니다.

## 사이트 채점

사이트 채점 합계 100점과 이번 재풀이 이후의 Python3 정답 100점 제출 내역을 확인했습니다. 정답은 실제 1번째 제출이며, 총 1회 제출했습니다.

| 제출 | 결과 | 합계 점수 | 입력 코드 | 채점 기록 |
| --- | --- | ---: | --- | --- |
| 1 | 정답 | 100 | [코드](<solution.py>) | [채점 결과 발췌](<attempts/attempt1_grading.txt>) |

[채점·제출 내역 JSON](<grading.json>)에는 실제 제출 시각, 합계, 테스트별 결과와 시간, 메모리, 입력 SHA256 및 새 제출 내역을 기록합니다. 제출한 입력 파일은 원본 바이트를 보관하며, 화면에 넣을 때의 LF 정규화 해시를 별도 기록합니다.

## 로컬 검증

[제출 전 후보 검증 원본](<local_checks.json>)은 사이트 채점과 별도인 로컬 비교·성능 기록입니다. 로컬 검증에 기록한 코드 해시는 정답 제출 입력과 같습니다.

## 풀이 요약

1번과 N번에서 다익스트라를 한 번씩 실행해 모든 도로 앞뒤의 최단 거리 확보
교통량을 0으로 바꾼 도로를 거치는 경로가 기존 최단 거리보다 짧으면 감소에 민감한 도로
현재 최단 경로에 속하는 도로만 모으면 그 그래프의 단절 간선은 모든 최단 경로가 사용하는 도로이므로 증가에 민감
최단 경로 밖의 도로는 증가해도 답을 바꾸지 않고, 최단 경로 그래프의 비단절 도로는 다른 최단 경로로 우회 가능
단절 간선 DFS는 방문 순서·복귀 순서·스택으로 처리해 50000개 정점의 깊은 경로도 재귀 없이 검사
정점 N개와 도로 M개에서 시간 O((N+M) log N), 공간 O(N+M)

## 정답 제출 코드

실제 1번째 정답 제출 입력의 전체 내용입니다. 원본 파일의 줄바꿈 바이트는 그대로 두며, 아래 표시는 LF로 정규화합니다.

```python
from heapq import heappop, heappush


def solution(n, roads):
    graph = [[] for _ in range(n + 1)]
    for edge_id, (a, b, length, traffic) in enumerate(roads):
        weight = length + traffic
        graph[a].append((b, weight, edge_id))
        graph[b].append((a, weight, edge_id))

    def shortest(start):
        distance = [10 ** 30] * (n + 1)
        distance[start] = 0
        heap = [(0, start)]
        while heap:
            current, node = heappop(heap)
            if current != distance[node]:
                continue
            for target, weight, _ in graph[node]:
                candidate = current + weight
                if candidate < distance[target]:
                    distance[target] = candidate
                    heappush(heap, (candidate, target))
        return distance

    forward = shortest(1)
    backward = shortest(n)
    best = forward[n]
    important = bytearray(len(roads))
    tight = [[] for _ in range(n + 1)]
    for edge_id, (a, b, length, traffic) in enumerate(roads):
        important[edge_id] = forward[a] + length + backward[b] < best or forward[b] + length + backward[a] < best
        weight = length + traffic
        if forward[a] + weight + backward[b] == best or forward[b] + weight + backward[a] == best:
            tight[a].append((b, edge_id))
            tight[b].append((a, edge_id))
    entered = [0] * (n + 1)
    low = [0] * (n + 1)
    parent = [0] * (n + 1)
    parent_edge = [-1] * (n + 1)
    position = [0] * (n + 1)
    timer = 1
    entered[1] = low[1] = 1
    stack = [1]
    while stack:
        node = stack[-1]
        if position[node] == len(tight[node]):
            stack.pop()
            previous = parent[node]
            if previous:
                if low[node] > entered[previous]:
                    important[parent_edge[node]] = 1
                low[previous] = min(low[previous], low[node])
            continue
        target, edge_id = tight[node][position[node]]
        position[node] += 1
        if edge_id == parent_edge[node]:
            continue
        if not entered[target]:
            parent[target], parent_edge[target] = node, edge_id
            timer += 1
            entered[target] = low[target] = timer
            stack.append(target)
        else:
            low[node] = min(low[node], entered[target])
    return [edge_id + 1 for edge_id, flag in enumerate(important) if flag] or [-1]

# 전체 코드 줄별 설명
# from heapq import heappop, heappush  # 다음 최단 거리 후보를 고를 최소 힙 연산


# def solution(n, roads):  # 교통량 하나의 변화로 최단 도착 시간이 바뀔 수 있는 도로 번호 찾기
#     graph = [[] for _ in range(n + 1)]  # 정점별 도착점·통과 시간·원래 도로 번호의 인접 목록
#     for edge_id, (a, b, length, traffic) in enumerate(roads):  # 각 무방향 도로를 입력 순서의 번호와 함께 등록
#         weight = length + traffic  # 현재 도로 통과 시간은 길이와 교통량의 합
#         graph[a].append((b, weight, edge_id))  # a에서 b로 이동하는 방향 추가
#         graph[b].append((a, weight, edge_id))  # b에서 a로 이동하는 반대 방향 추가

#     def shortest(start):  # 한 출발점에서 모든 정점까지의 현재 최단 시간 계산
#         distance = [10 ** 30] * (n + 1)  # 아직 도달하지 않은 정점에 충분히 큰 정수 거리 지정
#         distance[start] = 0  # 출발점까지 걸리는 시간은 0
#         heap = [(0, start)]  # 출발점을 첫 최소 힙 후보로 준비
#         while heap:  # 도착 시간 후보가 남아 있는 동안 거리 완화
#             current, node = heappop(heap)  # 가장 작은 도착 시간 후보부터 꺼내기
#             if current != distance[node]:  # 이미 더 짧은 거리가 나온 오래된 후보인지 확인
#                 continue  # 오래된 후보로 인접 도로를 중복 검사하지 않음
#             for target, weight, _ in graph[node]:  # 현재 정점에서 바로 갈 수 있는 모든 도로 확인
#                 candidate = current + weight  # 이 도로를 지나 이웃에 도착하는 새 시간
#                 if candidate < distance[target]:  # 기존 경로보다 빠를 때만 후보 갱신
#                     distance[target] = candidate  # 이웃까지의 최단 시간 줄이기
#                     heappush(heap, (candidate, target))  # 더 짧아진 이웃을 최소 힙에 추가
#         return distance  # 모든 정점까지의 최단 시간 반환

#     forward = shortest(1)  # 출발점 1에서 각 도로의 앞쪽까지 걸리는 최단 시간
#     backward = shortest(n)  # 각 도로의 뒤쪽에서 목적지 n까지 걸리는 최단 시간
#     best = forward[n]  # 교통량을 바꾸기 전의 최소 도착 시간
#     important = bytearray(len(roads))  # 교통량 증가 또는 감소가 영향을 줄 수 있는 도로 표시
#     tight = [[] for _ in range(n + 1)]  # 현재 최단 경로 중 하나에 속하는 도로만 모을 그래프
#     for edge_id, (a, b, length, traffic) in enumerate(roads):  # 각 도로의 감소 가능성과 현재 최단 경로 포함 여부 확인
#         important[edge_id] = forward[a] + length + backward[b] < best or forward[b] + length + backward[a] < best  # 교통량을 0까지 줄여 더 빠른 경로를 만들 수 있으면 표시
#         weight = length + traffic  # 이 도로의 현재 통과 시간 복원
#         if forward[a] + weight + backward[b] == best or forward[b] + weight + backward[a] == best:  # 어느 방향으로든 현재 최단 경로에 들어가는 도로인지 확인
#             tight[a].append((b, edge_id))  # 최단 경로 그래프에 정방향 연결 추가
#             tight[b].append((a, edge_id))  # 단절 간선 검사를 위해 반대 방향도 추가
#     entered = [0] * (n + 1)  # 반복 DFS에서 각 정점을 처음 방문한 순서
#     low = [0] * (n + 1)  # DFS 자손에서 부모 간선을 쓰지 않고 돌아갈 수 있는 최소 방문 순서
#     parent = [0] * (n + 1)  # DFS 트리에서 각 정점의 부모
#     parent_edge = [-1] * (n + 1)  # 부모와 연결된 도로 번호로 반대 방향 간선만 제외
#     position = [0] * (n + 1)  # 재귀 호출 대신 정점별 다음 인접 간선 위치 저장
#     timer = 1  # DFS 방문 순서의 다음 기준값
#     entered[1] = low[1] = 1  # 출발 정점을 첫 방문 정점으로 지정
#     stack = [1]  # 아직 자식 처리가 끝나지 않은 DFS 경로
#     while stack:  # 깊은 그래프도 파이썬 재귀 없이 단절 간선 탐색
#         node = stack[-1]  # 현재 DFS 경로의 마지막 정점
#         if position[node] == len(tight[node]):  # 모든 인접 최단 경로 도로를 확인했으면 복귀
#             stack.pop()  # 처리가 끝난 정점을 DFS 경로에서 제거
#             previous = parent[node]  # 자손 정보를 전달할 부모 정점
#             if previous:  # 시작 정점이 아니면 부모 간선의 단절 여부 판정
#                 if low[node] > entered[previous]:  # 자손에서 부모 이전으로 돌아갈 우회 도로가 없으면
#                     important[parent_edge[node]] = 1  # 모든 최단 경로가 쓰는 이 도로의 교통량 증가는 도착 시간을 바꿈
#                 low[previous] = min(low[previous], low[node])  # 자손이 찾은 가장 빠른 복귀 위치를 부모에 전달
#             continue  # 복귀한 부모의 다음 간선 처리로 넘어가기
#         target, edge_id = tight[node][position[node]]  # 현재 정점에서 아직 확인하지 않은 도로 하나 선택
#         position[node] += 1  # 같은 도로를 다음 반복에 다시 처리하지 않도록 위치 이동
#         if edge_id == parent_edge[node]:  # DFS에서 방금 내려온 도로의 반대 방향인지 확인
#             continue  # 부모 간선 자체는 우회 경로로 세지 않음
#         if not entered[target]:  # 처음 만난 정점이면 DFS 자식으로 내려가기
#             parent[target], parent_edge[target] = node, edge_id  # 복귀할 부모와 내려온 도로 번호 기록
#             timer += 1  # 새 정점의 방문 순서 증가
#             entered[target] = low[target] = timer  # 아직 우회 경로가 없는 새 정점의 초기 복귀 순서
#             stack.append(target)  # 새 자식 정점의 인접 간선을 다음에 처리
#         else:  # 이미 방문한 정점으로 이어지는 우회 간선을 만난 경우
#             low[node] = min(low[node], entered[target])  # 이 간선으로 돌아갈 수 있는 방문 순서를 반영
#     return [edge_id + 1 for edge_id, flag in enumerate(important) if flag] or [-1]  # 영향을 주는 도로를 입력 번호 순서대로 반환하고 없으면 -1

# 풀이 요약
# 1번과 N번에서 다익스트라를 한 번씩 실행해 모든 도로 앞뒤의 최단 거리 확보
# 교통량을 0으로 바꾼 도로를 거치는 경로가 기존 최단 거리보다 짧으면 감소에 민감한 도로
# 현재 최단 경로에 속하는 도로만 모으면 그 그래프의 단절 간선은 모든 최단 경로가 사용하는 도로이므로 증가에 민감
# 최단 경로 밖의 도로는 증가해도 답을 바꾸지 않고, 최단 경로 그래프의 비단절 도로는 다른 최단 경로로 우회 가능
# 단절 간선 DFS는 방문 순서·복귀 순서·스택으로 처리해 50000개 정점의 깊은 경로도 재귀 없이 검사
# 정점 N개와 도로 M개에서 시간 O((N+M) log N), 공간 O(N+M)
```
