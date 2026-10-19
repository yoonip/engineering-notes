from bisect import bisect_left, bisect_right
from heapq import heappush, heappop

def solution(city, road):
    cameras = {}
    # 도로별로 카메라 없는 조각을 생성.
    for x1, y1, x2, y2, limit in road:
        point = ((x1 + x2) // 2, (y1 + y2) // 2)
        # 같은 위치의 가장 엄격한 제한만 남김.
        cameras[point] = min(cameras.get(point, limit), limit)
    camera_points = list(cameras)
    cuts = []
    bases = []
    parent = []
    links = []
    # 도로별로 카메라 없는 조각을 생성.
    for x1, y1, x2, y2, limit in road:
        positions = [(x + y, i) for i, (x, y) in enumerate(camera_points) if x1 <= x <= x2 and y1 <= y <= y2]
        # 끝점·카메라 위치를 sorted로 정렬.
        boundaries = sorted({x1 + y1, x2 + y2} | {position for position, _ in positions})
        base = len(parent)
        # 인접 경계 사이마다 조각 하나.
        parent.extend(range(base, base + len(boundaries) - 1))
        cuts.append(boundaries)
        # 이 도로 조각 번호의 시작값 저장.
        bases.append(base)
        for position, camera in positions:
            # 카메라가 몇 번째 경계인지 이진 탐색.
            index = bisect_left(boundaries, position)
            if index > 0:
                # 카메라 앞 조각과 카메라의 연결을 튜플로 저장.
                links.append((base + index - 1, camera))
            if index + 1 < len(boundaries):
                # 카메라 뒤 조각의 연결 저장.
                links.append((base + index, camera))
    sizes = [1] * len(parent)

    def find(node):
        # 자기 자신이 부모이면 대표.
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            # 부모 방향으로 이동.
            node = parent[node]
        return node

    def piece(index, x, y):
        offset = min(bisect_right(cuts[index], x + y) - 1, len(cuts[index]) - 2)
        return bases[index] + offset

    # 도시가 놓인 도로를 찾음.
    for i, (x1, y1, x2, y2, _) in enumerate(road):
        for j in range(i):
            # 다른 도로의 양 끝 좌표를 언패킹.
            a, b, c, d, _ = road[j]
            x, y = max(x1, a), max(y1, b)
            # 교점이 없거나 카메라 위치이면 무료 연결을 하지 않음.
            if x > min(x2, c) or y > min(y2, d) or (x, y) in cameras:
                continue
            first, second = find(piece(i, x, y)), find(piece(j, x, y))
            if first != second:
                if sizes[first] < sizes[second]:
                    first, second = second, first
                parent[second] = first
                sizes[first] += sizes[second]
    offset = len(parent)
    graph = [[] for _ in range(offset + len(cameras))]
    for node, camera in links:
        node = find(node)
        limit = cameras[camera_points[camera]]
        graph[node].append((offset + camera, limit))
        graph[offset + camera].append((node, limit))
    cities = []
    for x, y in city:
        for i, (x1, y1, x2, y2, _) in enumerate(road):
            if x1 <= x <= x2 and y1 <= y <= y2:
                cities.append(find(piece(i, x, y)))
                break
    infinity = 1000001
    best = [0] * len(graph)
    best[cities[0]] = infinity
    heap = [(-infinity, cities[0])]
    while heap:
        negative, node = heappop(heap)
        speed = -negative
        if speed != best[node]:
            continue
        for neighbor, limit in graph[node]:
            candidate = min(speed, limit)
            if candidate > best[neighbor]:
                best[neighbor] = candidate
                heappush(heap, (-candidate, neighbor))
    return [0 if best[node] == infinity else best[node] for node in cities[1:]]
