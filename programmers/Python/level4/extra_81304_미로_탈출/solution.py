from heapq import heappush, heappop  # from A import B는 모듈에서 함수 가져오기. heapq는 최솟값을 빠르게 꺼내는 힙 구현.

def solution(n, start, end, roads, traps):
    bits = [0] * (n + 1)  # []는 리스트, *는 반복. 일반 방은 비트 0으로 표시.
    for index, node in enumerate(traps):  # enumerate는 인덱스와 값을 함께 제공. 함정에 비트 위치 부여.
        bits[node] = 1 << index  # <<는 비트 왼쪽 이동. 각 함정을 서로 다른 2의 거듭제곱으로 표시.
    graph = [[] for _ in range(n + 1)]  # 리스트 내포로 각 방의 독립적인 이웃 목록 생성.
    for a, b, cost in roads:  # 각 도로의 출발 방·도착 방·이동 시간을 나눠 받음.
        graph[a].append((b, cost, False))  # append는 끝에 추가. 원래 방향의 통로를 튜플로 저장.
        graph[b].append((a, cost, True))  # 역방향 후보도 저장. 뒤집힌 상태에서만 사용 가능.
    distance = [[10**18] * (1 << len(traps)) for _ in range(n + 1)]
    distance[start][0] = 0  # 모든 함정이 꺼진 출발 상태의 거리는 0.
    heap = [(0, start, 0)]  # 최소 힙에 (거리, 방, 활성 비트)를 저장. 튜플의 첫 값이 작은 순서로 꺼냄.
    while heap:  # while은 조건이 참인 동안 반복. 처리할 경로가 남아 있으면 실행.
        cost, node, mask = heappop(heap)  # heappop은 힙의 최솟값을 제거·반환. 가장 짧은 후보 경로 선택.
        if cost != distance[node][mask]:  # !=는 다름 비교. 이미 더 짧은 경로를 찾은 오래된 후보는 제외.
            continue  # continue는 이번 반복을 건너뛰고 다음 후보 처리.
        if node == end:  # ==는 같음 비교. 도착 방의 최단 거리를 확정한 경우.
            return cost
        active = bool(mask & bits[node])  # &는 비트 AND, bool은 참·거짓 변환. 현재 방 함정의 활성 여부.
        for neighbor, weight, backwards in graph[node]:  # 인접 통로의 도착 방·시간·원래 역방향 여부를 순회.
            flipped = active != bool(mask & bits[neighbor])  # 양 끝 함정 활성 여부가 다를 때만 통로 방향이 뒤집힘.
            if flipped != backwards:  # 통로의 실제 방향으로 현재 방에서 갈 수 없는 경우.
                continue  # 이 통로를 건너뛰고 다른 이웃 검사.
            next_mask = mask ^ bits[neighbor]  # ^는 비트 XOR. 도착 방이 함정이면 활성 비트를 반전, 일반 방이면 그대로.
            next_cost = cost + weight  # 지금까지 시간에 통로 이동 시간을 더함.
            if next_cost < distance[neighbor][next_mask]:  # 같은 도착 방·함정 상태에 더 짧게 도달할 수 있으면 실행.
                distance[neighbor][next_mask] = next_cost  # 최단 거리 갱신.
                heappush(heap, (next_cost, neighbor, next_mask))  # heappush는 최소 힙에 후보를 추가하고 힙 구조 유지.
    return -1  # 도달 불가능한 경우의 기본 반환값. 문제에서는 항상 탈출 가능.
