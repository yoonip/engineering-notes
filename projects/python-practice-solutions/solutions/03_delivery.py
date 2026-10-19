# 배달
# 분류: Dijkstra / 최소 힙
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/12978
# AI 작성 학습 풀이입니다. 온라인 채점 통과를 확인한 제출물이 아닙니다.

import heapq


def solution(N, road, K):
    graph = [[] for _ in range(N + 1)]
    for a, b, cost in road:
        graph[a].append((b, cost))
        graph[b].append((a, cost))

    distance = [float("inf")] * (N + 1)
    distance[1] = 0
    heap = [(0, 1)]

    while heap:
        current_distance, village = heapq.heappop(heap)

        if current_distance > distance[village]:
            continue

        for next_village, cost in graph[village]:
            next_distance = current_distance + cost

            if next_distance < distance[next_village]:
                distance[next_village] = next_distance
                heapq.heappush(heap, (next_distance, next_village))

    answer = 0
    for village in range(1, N + 1):
        if distance[village] <= K:
            answer += 1

    return answer


# 같은 코드의 문법 설명: 아래 부분은 전체 주석입니다.
# import heapq  # import는 모듈을 가져옵니다. heapq는 가장 작은 항목을 먼저 꺼내는 최소 힙 기능입니다.
#
#
# def solution(N, road, K):  # def로 함수를 정의합니다. N은 마을 수, road는 도로 리스트, K는 제한 시간입니다.
#     graph = [[] for _ in range(N + 1)]  # 리스트 컴프리헨션으로 독립된 빈 리스트들을 만듭니다. 마을 번호 1~N을 사용하기 위해 N+1개입니다.
#     for a, b, cost in road:  # 도로의 세 값을 출발 마을, 연결 마을, 시간에 각각 언패킹합니다.
#         graph[a].append((b, cost))  # a번 리스트에 (이웃 마을, 시간) 튜플을 추가합니다.
#         graph[b].append((a, cost))  # 양방향 도로이므로 반대 방향도 추가합니다.
#
#     distance = [float("inf")] * (N + 1)  # float("inf")는 양의 무한대입니다. 아직 거리를 모른다는 초기값으로 사용합니다.
#     distance[1] = 0  # 시작 마을에서 자기 자신까지의 시간은 0입니다.
#     heap = [(0, 1)]  # 리스트에 (누적 시간, 마을 번호) 튜플을 넣습니다. 힙은 우선 첫 원소인 시간으로 비교합니다.
#
#     while heap:  # 힙 리스트가 비어 있지 않은 동안 반복합니다.
#         current_distance, village = heapq.heappop(heap)  # 모듈.함수 형식으로 호출합니다. heappop은 최소 항목을 꺼내며 두 값을 언패킹합니다.
#
#         if current_distance > distance[village]:  # >는 크다는 비교입니다. 기록된 최단 시간보다 오래 걸리는 낡은 항목인지 확인합니다.
#             continue  # 현재 반복의 남은 코드를 건너뛰고 가장 가까운 반복문의 다음 반복으로 갑니다.
#
#         for next_village, cost in graph[village]:  # 현재 마을의 이웃 리스트를 반복하며 각 튜플을 두 변수에 언패킹합니다.
#             next_distance = current_distance + cost  # 현재까지의 시간에 다음 도로 시간을 더하여 후보 시간을 계산합니다.
#
#             if next_distance < distance[next_village]:  # <는 작다는 비교입니다. 새 경로가 기존 기록보다 빠르면 실행합니다.
#                 distance[next_village] = next_distance  # 대입 연산 =로 더 짧은 시간을 기록합니다.
#                 heapq.heappush(heap, (next_distance, next_village))  # 힙에 (시간, 마을) 튜플을 넣습니다. 최소 항목을 꺼낼 수 있도록 힙 순서를 유지합니다.
#
#     answer = 0  # 조건에 맞는 마을 수를 0으로 시작합니다.
#     for village in range(1, N + 1):  # range(시작,끝)은 끝을 제외하므로 마을 번호 1부터 N까지 반복합니다.
#         if distance[village] <= K:  # <=는 작거나 같다는 비교입니다. 제한 시간과 정확히 같아도 포함합니다.
#             answer += 1  # += 1은 기존 값에 1을 더하여 다시 저장합니다.
#
#     return answer  # 계산한 정수를 반환하고 함수 전체를 종료합니다.
