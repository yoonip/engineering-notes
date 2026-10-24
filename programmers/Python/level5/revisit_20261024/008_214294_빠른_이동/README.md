# 빠른 이동 — Python 재풀이

[문제 원문](<https://school.programmers.co.kr/learn/courses/30/lessons/214294>) · [재풀이 목록](<../README.md>)

정답률 2%와 풀이 인원 96명은 이번 목록 확인 시점의 값입니다. 전체 8순위로 진행했습니다.

## 사이트 채점

사이트 채점 합계 100점과 이번 재풀이 이후의 Python3 정답 100점 제출 내역을 확인했습니다. 정답은 실제 1번째 제출이며, 총 1회 제출했습니다.

| 제출 | 결과 | 합계 점수 | 입력 코드 | 채점 기록 |
| --- | --- | ---: | --- | --- |
| 1 | 정답 | 100 | [코드](<solution.py>) | [채점 결과 발췌](<attempts/attempt1_grading.txt>) |

[채점·제출 내역 JSON](<grading.json>)에는 실제 제출 시각, 합계, 테스트별 결과와 시간, 메모리, 입력 SHA256 및 새 제출 내역을 기록합니다. 제출한 입력 파일은 원본 바이트를 보관하며, 화면에 넣을 때의 LF 정규화 해시를 별도 기록합니다.

## 로컬 검증

[제출 전 후보 검증 원본](<local_checks.json>)은 사이트 채점과 별도인 로컬 비교·성능 기록입니다. 로컬 검증에 기록한 코드 해시는 정답 제출 입력과 같습니다.

## 풀이 요약

도달 여부를 파이썬 정수 비트셋으로 저장하고 Warshall의 행 합치기를 정수 OR로 처리
서로 왕복 가능한 정점들을 강한 연결 요소로 묶으면, 요소 안에서는 도로만으로 모두 방문하고 원하는 출구로 나갈 수 있음
서로 다른 요소 사이의 전체 도달 관계를 이분 그래프로 만들고 Hopcroft–Karp 최대 매칭 계산
강한 연결 요소 K개와 최대 매칭 M개에서 최소 도달 사슬 덮개는 K−M개, 필요한 빠른 이동은 K−M−1번
1번에서 모든 지점에 갈 수 있으므로 다음 사슬로 넘어갈 때 이미 방문한 1번으로 빠른 이동한 뒤 사슬 시작점까지 도로로 이동 가능
비트셋 한 워드의 비트 수 W와 이분 간선 수 E에 대해 전처리 O(N²⌈N/W⌉), 매칭 O(E√K), 보조 공간 O(N²)

## 정답 제출 코드

실제 1번째 정답 제출 입력의 전체 내용입니다. 원본 파일의 줄바꿈 바이트는 그대로 두며, 아래 표시는 LF로 정규화합니다.

```python
from collections import deque


def solution(n, roads):
    reach = [1 << node for node in range(n)]
    for source, target in roads:
        reach[source - 1] |= 1 << (target - 1)
    for middle in range(n):
        bit, through = 1 << middle, reach[middle]
        for source, row in enumerate(reach):
            if row & bit:
                reach[source] = row | through
    component = [-1] * n
    representatives = []
    for node in range(n):
        if component[node] != -1:
            continue
        number = len(representatives)
        representatives.append(node)
        for other in range(n):
            if reach[node] & (1 << other) and reach[other] & (1 << node):
                component[other] = number
    count = len(representatives)
    neighbors = [[] for _ in range(count)]
    for left, source in enumerate(representatives):
        for right, target in enumerate(representatives):
            if left != right and reach[source] & (1 << target):
                neighbors[left].append(right)
    pair_left = [count] * count
    pair_right = [count] * count
    distance = [0] * (count + 1)
    infinity = count + 1

    def layers():
        queue = deque()
        for left in range(count):
            if pair_left[left] == count:
                distance[left] = 0; queue.append(left)
            else:
                distance[left] = infinity
        distance[count] = infinity
        while queue:
            left = queue.popleft()
            if distance[left] >= distance[count]:
                continue
            for right in neighbors[left]:
                partner = pair_right[right]
                if distance[partner] == infinity:
                    distance[partner] = distance[left] + 1
                    if partner != count:
                        queue.append(partner)
        return distance[count] != infinity

    def augment(left):
        if left == count:
            return True
        for right in neighbors[left]:
            partner = pair_right[right]
            if distance[partner] == distance[left] + 1 and augment(partner):
                pair_left[left], pair_right[right] = right, left
                return True
        distance[left] = infinity
        return False

    matches = 0
    while layers():
        for left in range(count):
            if pair_left[left] == count and augment(left):
                matches += 1
    return count - matches - 1

# 전체 코드 줄별 설명
# from collections import deque  # 이분 매칭의 증가 경로 층을 찾을 BFS 큐


# def solution(n, roads):  # 모든 지점 스탬프를 모으는 최소 빠른 이동 횟수 계산
#     reach = [1 << node for node in range(n)]  # 출발 정점별 도달 여부를 하나의 파이썬 정수 비트셋에 저장
#     for source, target in roads:  # 입력의 모든 단방향 도로 확인
#         reach[source - 1] |= 1 << (target - 1)  # 도로 하나로 갈 수 있는 도착 정점 비트 표시
#     for middle in range(n):  # 중간 정점을 하나씩 허용하는 Warshall 도달 폐쇄
#         bit, through = 1 << middle, reach[middle]  # 중간 정점 비트와 그 정점에서 갈 수 있는 전체 비트셋
#         for source, row in enumerate(reach):  # 각 출발점이 현재 중간 정점까지 갈 수 있는지 확인
#             if row & bit:  # 중간 정점까지 갈 수 있으면 그 뒤의 도달 관계도 사용 가능
#                 reach[source] = row | through  # 여러 도로를 거쳐 갈 수 있는 정점을 정수 OR로 한꺼번에 합치기
#     component = [-1] * n  # 원래 정점이 속한 강한 연결 요소 번호
#     representatives = []  # 각 강한 연결 요소에서 도달 관계를 읽을 대표 정점
#     for node in range(n):  # 아직 묶이지 않은 정점에서 새 강한 연결 요소 찾기
#         if component[node] != -1:  # 이전 대표와 서로 도달해 이미 분류된 정점이면
#             continue  # 같은 강한 연결 요소를 다시 만들지 않음
#         number = len(representatives)  # 이번에 만들 강한 연결 요소 번호
#         representatives.append(node)  # 이번 요소의 대표 정점 기록
#         for other in range(n):  # 대표와 왕복할 수 있는 모든 정점 검사
#             if reach[node] & (1 << other) and reach[other] & (1 << node):  # 두 방향 모두 도달 가능하면 같은 강한 연결 요소
#                 component[other] = number  # 도로 이동만으로 함께 훑을 수 있는 정점들을 한 요소로 묶기
#     count = len(representatives)  # 사이클을 접은 DAG의 강한 연결 요소 수
#     neighbors = [[] for _ in range(count)]  # 도달 가능한 서로 다른 요소를 이분 매칭의 다음 후보로 저장
#     for left, source in enumerate(representatives):  # 각 요소가 앞부분이 되는 도달 사슬 연결 확인
#         for right, target in enumerate(representatives):  # 뒤에 이어 붙일 요소의 대표 정점 확인
#             if left != right and reach[source] & (1 << target):  # 같은 요소를 제외하고 도로를 따라 이어 갈 수 있으면
#                 neighbors[left].append(right)  # 도달 관계를 이분 매칭 간선으로 추가
#     pair_left = [count] * count  # 각 왼쪽 요소의 오른쪽 매칭 상대; count는 빈 상대 표시
#     pair_right = [count] * count  # 각 오른쪽 요소의 왼쪽 매칭 상대
#     distance = [0] * (count + 1)  # 증가 경로 BFS 층과 빈 상대의 최단 층 저장
#     infinity = count + 1  # 증가 경로 층에서 아직 도달하지 못했다는 표시

#     def layers():  # 가장 짧은 증가 경로의 층 구조 만들기
#         queue = deque()  # 아직 상대가 없는 왼쪽 요소부터 시작할 BFS 큐
#         for left in range(count):  # 각 왼쪽 요소의 이번 BFS 시작 상태 초기화
#             if pair_left[left] == count:  # 매칭되지 않은 요소는 증가 경로의 시작점
#                 distance[left] = 0; queue.append(left)  # 모든 빈 왼쪽 요소를 같은 첫 층에 넣기
#             else:  # 이미 매칭된 요소는 다른 증가 경로를 통해 도달해야 함
#                 distance[left] = infinity  # 아직 도달하지 않은 층으로 초기화
#         distance[count] = infinity  # 빈 오른쪽 상대까지의 최단 층을 아직 모르는 상태
#         while queue:  # 빈 상대를 만나는 가장 짧은 층까지 이분 그래프 탐색
#             left = queue.popleft()  # 다음 왼쪽 요소를 가까운 층부터 꺼내기
#             if distance[left] >= distance[count]:  # 이미 찾은 최단 증가 경로보다 깊은 층이면
#                 continue  # 이번 단계에서 더 긴 증가 경로는 탐색하지 않음
#             for right in neighbors[left]:  # 도달 관계로 연결할 수 있는 오른쪽 요소 확인
#                 partner = pair_right[right]  # 현재 오른쪽 요소와 연결된 왼쪽 상대 또는 빈 상대
#                 if distance[partner] == infinity:  # 아직 이번 BFS에서 도달하지 못한 상대면
#                     distance[partner] = distance[left] + 1  # 교대 경로를 따라 다음 층으로 방문
#                     if partner != count:  # 빈 상대는 도착점이므로 큐에 넣지 않음
#                         queue.append(partner)  # 기존 매칭 상대에서 이어질 교대 경로를 나중에 확인
#         return distance[count] != infinity  # 빈 상대까지 가는 증가 경로가 있는지 반환

#     def augment(left):  # BFS 층을 지키면서 매칭 수를 하나 늘릴 증가 경로 찾기
#         if left == count:  # 빈 오른쪽 상대에 도착한 경우
#             return True  # 매칭 수를 하나 늘릴 자리를 찾음
#         for right in neighbors[left]:  # 현재 요소 뒤에 연결할 수 있는 오른쪽 후보 확인
#             partner = pair_right[right]  # 이 후보를 쓰기 위해 옮겨야 할 기존 왼쪽 상대
#             if distance[partner] == distance[left] + 1 and augment(partner):  # 다음 BFS 층으로 이어지는 증가 경로가 있으면
#                 pair_left[left], pair_right[right] = right, left  # 경로의 현재 연결을 새 상대 쌍으로 뒤집기
#                 return True  # 증가 경로 하나를 완성했음을 반환
#         distance[left] = infinity  # 이번 층 구조에서 실패한 요소는 다시 탐색하지 않도록 제외
#         return False  # 현재 요소에서는 최단 증가 경로를 만들 수 없음

#     matches = 0  # 서로 다른 도달 사슬을 이어 붙인 최대 연결 수
#     while layers():  # 증가 경로가 남아 있는 동안 Hopcroft–Karp 단계 반복
#         for left in range(count):  # 빈 왼쪽 요소마다 이번 층의 증가 경로 시도
#             if pair_left[left] == count and augment(left):  # 아직 빈 요소에서 매칭을 하나 늘렸으면
#                 matches += 1  # 사슬 덮개의 개수를 하나 줄이는 연결 수 증가
#     return count - matches - 1  # 최소 도달 사슬 수에서 빠른 이동 없이 시작하는 첫 사슬 하나 제외

# 풀이 요약
# 도달 여부를 파이썬 정수 비트셋으로 저장하고 Warshall의 행 합치기를 정수 OR로 처리
# 서로 왕복 가능한 정점들을 강한 연결 요소로 묶으면, 요소 안에서는 도로만으로 모두 방문하고 원하는 출구로 나갈 수 있음
# 서로 다른 요소 사이의 전체 도달 관계를 이분 그래프로 만들고 Hopcroft–Karp 최대 매칭 계산
# 강한 연결 요소 K개와 최대 매칭 M개에서 최소 도달 사슬 덮개는 K−M개, 필요한 빠른 이동은 K−M−1번
# 1번에서 모든 지점에 갈 수 있으므로 다음 사슬로 넘어갈 때 이미 방문한 1번으로 빠른 이동한 뒤 사슬 시작점까지 도로로 이동 가능
# 비트셋 한 워드의 비트 수 W와 이분 간선 수 E에 대해 전처리 O(N²⌈N/W⌉), 매칭 O(E√K), 보조 공간 O(N²)
```
