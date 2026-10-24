# 가짜 해밀토니안 — Python 재풀이

[문제 원문](<https://school.programmers.co.kr/learn/courses/30/lessons/70132>) · [재풀이 목록](<../README.md>)

정답률 2%와 풀이 인원 140명은 이번 목록 확인 시점의 값입니다. 전체 6순위로 진행했습니다.

## 사이트 채점

사이트 채점 합계 100점과 이번 재풀이 이후의 Python3 정답 100점 제출 내역을 확인했습니다. 정답은 실제 1번째 제출이며, 총 1회 제출했습니다.

| 제출 | 결과 | 합계 점수 | 입력 코드 | 채점 기록 |
| --- | --- | ---: | --- | --- |
| 1 | 정답 | 100 | [코드](<solution.py>) | [채점 결과 발췌](<attempts/attempt1_grading.txt>) |

[채점·제출 내역 JSON](<grading.json>)에는 실제 제출 시각, 합계, 테스트별 결과와 시간, 메모리, 입력 SHA256 및 새 제출 내역을 기록합니다. 제출한 입력 파일은 원본 바이트를 보관하며, 화면에 넣을 때의 LF 정규화 해시를 별도 기록합니다.

## 로컬 검증

[제출 전 후보 검증 원본](<local_checks.json>)은 사이트 채점과 별도인 로컬 비교·성능 기록입니다. 로컬 검증에 기록한 코드 해시는 정답 제출 입력과 같습니다.

## 풀이 요약

선택 정점이 둘 이상이면 시작·끝을 다르게 잡을 수 있음. 그 사이 중심 경로의 간선은 한 번, 나머지 간선은 왕복해서 모든 정점 방문.
선택 차수를 d라 하면 중심 경로 내부점은 d-1번, 양끝과 경로 밖 정점은 d번 방문. 중심 경로 옆에 붙이는 가지는 갈라지지 않는 한 줄이어야 함.
line은 아래 단순 경로, stem은 부모가 중심 경로인 상태, branch는 부모를 통해 왕복 접근하는 상태. 자식 조합은 가지 하나·둘과 옆 경로의 최댓값만 추적하면 됨.
큰 조합부터 갱신한 뒤 자식 한 개의 최댓값을 갱신해 같은 자식을 두 역할에 쓰지 않기. 역순 순회로 재귀 없이 시간 O(N), 공간 O(N).

## 정답 제출 코드

실제 1번째 정답 제출 입력의 전체 내용입니다. 원본 파일의 줄바꿈 바이트는 그대로 두며, 아래 표시는 LF로 정규화합니다.

```python
def solution(t):
    n = len(t) + 1
    adjacent = [[] for _ in range(n)]
    for a, b in t:
        adjacent[a].append(b)
        adjacent[b].append(a)
    parent = [-1] * n
    parent[0] = 0
    order = [0]
    for node in order:
        for child in adjacent[node]:
            if child != parent[node]:
                parent[child] = node
                order.append(child)
    line = [1] * n
    stem = [1] * n
    branch = [1] * n
    answer = 1
    for node in reversed(order):
        longest_line = longest_stem = two_stems = 0
        stem_and_line = two_stems_and_line = 0
        best_branch = branch_and_line = 0
        for child in adjacent[node]:
            if child == parent[node]:
                continue
            child_line, child_stem, child_branch = line[child], stem[child], branch[child]
            two_stems_and_line = max(two_stems_and_line, two_stems + child_line, stem_and_line + child_stem)
            branch_and_line = max(branch_and_line, best_branch + child_line, longest_line + child_branch)
            stem_and_line = max(stem_and_line, longest_stem + child_line, longest_line + child_stem)
            two_stems = max(two_stems, longest_stem + child_stem)
            longest_line = max(longest_line, child_line)
            longest_stem = max(longest_stem, child_stem)
            best_branch = max(best_branch, child_branch)
        line[node] = 1 + longest_line
        stem[node] = 1 + stem_and_line
        branch[node] = 1 + max(best_branch, two_stems)
        answer = max(answer, 1 + two_stems_and_line, 1 + branch_and_line)
    return answer

# 전체 코드 줄별 설명
# def solution(t):  # 방문 횟수가 두 번 이하인 가장 큰 부분 트리의 정점 수
#     n = len(t) + 1  # 트리의 정점 수는 간선 수에 1을 더한 값
#     adjacent = [[] for _ in range(n)]  # 각 정점의 양방향 이웃 목록
#     for a, b in t:  # 입력 간선의 양끝을 꺼내기
#         adjacent[a].append(b)  # a에서 b로 이동 가능
#         adjacent[b].append(a)  # 반대 방향도 등록
#     parent = [-1] * n  # 부모 정점이 아직 정해지지 않았다는 표시
#     parent[0] = 0  # 계산용 루트 0의 부모는 자기 자신
#     order = [0]  # 부모가 자식보다 먼저 나오는 방문 순서
#     for node in order:  # 뒤에 자식을 추가하면서 전체 트리 순회
#         for child in adjacent[node]:  # 현재 정점에 연결된 이웃 확인
#             if child != parent[node]:  # 부모로 돌아가는 간선은 제외
#                 parent[child] = node  # 자식의 부모 기록
#                 order.append(child)  # 자식은 부모 뒤에 방문
#     line = [1] * n  # 현재 정점에서 아래로 뻗는 가장 긴 단순 경로 크기
#     stem = [1] * n  # 부모에서 중심 경로가 들어오는 부분 트리의 최대 크기
#     branch = [1] * n  # 부모 간선은 왕복하고 중심 경로는 아래에 있는 상태의 최대 크기
#     answer = 1  # 한 정점만 남기는 경우부터 시작
#     for node in reversed(order):  # 자식 상태를 먼저 구하고 부모로 올라가기
#         longest_line = longest_stem = two_stems = 0  # 앞서 처리한 자식 중 한 줄·중심 경로 가지 하나·둘의 최댓값
#         stem_and_line = two_stems_and_line = 0  # 중심 경로 가지와 옆 경로를 서로 다른 자식에서 고른 최댓값
#         best_branch = branch_and_line = 0  # 접근 가지 하나와 그 반대편 단순 경로 조합의 최댓값
#         for child in adjacent[node]:  # 현재 정점에 붙일 자식을 하나씩 추가
#             if child == parent[node]:  # 부모 쪽은 아래 부분 트리에 포함하지 않기
#                 continue  # 다음 자식으로 이동
#             child_line, child_stem, child_branch = line[child], stem[child], branch[child]  # 이미 계산한 자식의 세 상태
#             two_stems_and_line = max(two_stems_and_line, two_stems + child_line, stem_and_line + child_stem)  # 중심 경로 둘과 옆 경로 하나의 조합을 기존 값으로 먼저 갱신해 자식 중복 방지
#             branch_and_line = max(branch_and_line, best_branch + child_line, longest_line + child_branch)  # 중심 경로를 포함한 가지와 반대편 단순 경로를 다른 자식에서 선택
#             stem_and_line = max(stem_and_line, longest_stem + child_line, longest_line + child_stem)  # 부모에서 내려온 중심 경로 하나와 옆 경로 하나의 조합
#             two_stems = max(two_stems, longest_stem + child_stem)  # 중심 경로의 두 방향으로 연결할 서로 다른 자식 선택
#             longest_line = max(longest_line, child_line)  # 단순 경로는 가장 긴 자식 하나만 사용
#             longest_stem = max(longest_stem, child_stem)  # 다음 자식을 조합할 때 쓸 가장 좋은 중심 경로 가지
#             best_branch = max(best_branch, child_branch)  # 부모의 왕복 접근 경로를 이어 줄 가장 좋은 자식
#         line[node] = 1 + longest_line  # 현재 정점 하나와 가장 긴 아래 경로를 연결
#         stem[node] = 1 + stem_and_line  # 부모가 중심 경로 한 방향을 쓰므로 자식 방향 하나와 옆 경로 하나만 허용
#         branch[node] = 1 + max(best_branch, two_stems)  # 접근 경로를 자식 하나로 연장하거나 현재 점에서 중심 경로 두 방향으로 갈라지기
#         answer = max(answer, 1 + two_stems_and_line, 1 + branch_and_line)  # 부분 트리의 맨 위가 중심 경로 위·밖인 두 경우를 모두 비교
#     return answer  # 모든 정점에서 찾은 최대 부분 트리 크기

# 풀이 요약
# 선택 정점이 둘 이상이면 시작·끝을 다르게 잡을 수 있음. 그 사이 중심 경로의 간선은 한 번, 나머지 간선은 왕복해서 모든 정점 방문.
# 선택 차수를 d라 하면 중심 경로 내부점은 d-1번, 양끝과 경로 밖 정점은 d번 방문. 중심 경로 옆에 붙이는 가지는 갈라지지 않는 한 줄이어야 함.
# line은 아래 단순 경로, stem은 부모가 중심 경로인 상태, branch는 부모를 통해 왕복 접근하는 상태. 자식 조합은 가지 하나·둘과 옆 경로의 최댓값만 추적하면 됨.
# 큰 조합부터 갱신한 뒤 자식 한 개의 최댓값을 갱신해 같은 자식을 두 역할에 쓰지 않기. 역순 순회로 재귀 없이 시간 O(N), 공간 O(N).

```
