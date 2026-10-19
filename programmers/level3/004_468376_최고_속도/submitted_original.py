from bisect import bisect_left, bisect_right
from heapq import heappush, heappop

def solution(city, road):
    cameras = {}
    for x1, y1, x2, y2, limit in road:
        point = ((x1 + x2) // 2, (y1 + y2) // 2)
        cameras[point] = min(cameras.get(point, limit), limit)
    camera_points = list(cameras)
    cuts = []
    bases = []
    parent = []
    links = []
    for x1, y1, x2, y2, limit in road:
        positions = [(x + y, i) for i, (x, y) in enumerate(camera_points) if x1 <= x <= x2 and y1 <= y <= y2]
        boundaries = sorted({x1 + y1, x2 + y2} | {position for position, _ in positions})
        base = len(parent)
        parent.extend(range(base, base + len(boundaries) - 1))
        cuts.append(boundaries)
        bases.append(base)
        for position, camera in positions:
            index = bisect_left(boundaries, position)
            if index > 0:
                links.append((base + index - 1, camera))
            if index + 1 < len(boundaries):
                links.append((base + index, camera))
    sizes = [1] * len(parent)

    def find(node):
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    def piece(index, x, y):
        offset = min(bisect_right(cuts[index], x + y) - 1, len(cuts[index]) - 2)
        return bases[index] + offset

    for i, (x1, y1, x2, y2, _) in enumerate(road):
        for j in range(i):
            a, b, c, d, _ = road[j]
            x, y = max(x1, a), max(y1, b)
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

# 전체 코드 줄별 설명
# from bisect import bisect_left, bisect_right  # bisect 모듈의 이진 탐색 함수 import. 정렬 배열에서 값의 왼쪽·오른쪽 삽입 위치를 반환.
# from heapq import heappush, heappop  # heapq의 힙 삽입·최솟값 제거 함수. 음수 속도를 넣어 가장 큰 속도를 먼저 처리.
# 
# def solution(city, road):  # def는 함수 정의. city는 도시 좌표, road는 양 끝 좌표와 카메라 제한 목록.
#     cameras = {}  # {}는 빈 딕셔너리. 좌표를 키로 해당 지점의 최소 제한 속도 저장.
#     for x1, y1, x2, y2, limit in road:  # for로 도로 순회. 한 행의 다섯 값을 변수로 나눠 받는 언패킹.
#         point = ((x1 + x2) // 2, (y1 + y2) // 2)  # ()는 좌표 튜플, //는 정수 나눗셈. 도로 정중앙 좌표.
#         cameras[point] = min(cameras.get(point, limit), limit)  # get은 없는 키의 기본값, min은 작은 값. 같은 위치의 가장 엄격한 제한만 남김.
#     camera_points = list(cameras)  # list(dict)는 키 목록 생성. 서로 다른 카메라 좌표들을 번호로 관리.
#     cuts = []  # 각 도로가 카메라에서 나뉘는 경계 위치 목록.
#     bases = []  # 도로별 첫 조각의 정점 번호 저장.
#     parent = []  # 서로 연결된 조각을 합칠 서로소 집합의 부모 목록.
#     links = []  # 카메라 번호와 그 카메라에 닿는 조각 번호의 연결 목록.
#     for x1, y1, x2, y2, limit in road:  # 도로별로 카메라 없는 조각을 생성.
#         positions = [(x + y, i) for i, (x, y) in enumerate(camera_points) if x1 <= x <= x2 and y1 <= y <= y2]  # 리스트 내포로 이 도로 위의 모든 카메라 수집. 축 평행 선분에서는 x+y가 위치 순서를 나타냄.
#         boundaries = sorted({x1 + y1, x2 + y2} | {position for position, _ in positions})  # {} 집합은 중복 제거, |는 합집합. 끝점·카메라 위치를 sorted로 정렬.
#         base = len(parent)  # len은 개수. 새 조각에 붙일 첫 정점 번호.
#         parent.extend(range(base, base + len(boundaries) - 1))  # range는 끝 제외 정수 범위, extend는 여러 원소 추가. 인접 경계 사이마다 조각 하나.
#         cuts.append(boundaries)  # append는 원소 하나 추가. 이 도로의 경계 목록 저장.
#         bases.append(base)  # 이 도로 조각 번호의 시작값 저장.
#         for position, camera in positions:  # 카메라가 있는 경계를 순회.
#             index = bisect_left(boundaries, position)  # 카메라가 몇 번째 경계인지 이진 탐색.
#             if index > 0:  # if는 조건문. 카메라 왼쪽/아래쪽에 조각이 있는 경우.
#                 links.append((base + index - 1, camera))  # 카메라 앞 조각과 카메라의 연결을 튜플로 저장.
#             if index + 1 < len(boundaries):  # 카메라 뒤에도 조각이 있는지 확인.
#                 links.append((base + index, camera))  # 카메라 뒤 조각의 연결 저장.
#     sizes = [1] * len(parent)  # [1]*개수는 반복 초기화. 작은 연결 집합을 큰 집합에 붙이는 데 사용.
# 
#     def find(node):  # 서로소 집합에서 대표 정점을 찾는 중첩 함수.
#         while parent[node] != node:  # while은 반복, !=는 다름. 자기 자신이 부모이면 대표.
#             parent[node] = parent[parent[node]]  # 경로 압축으로 부모를 조상에 바로 연결해 다음 탐색 단축.
#             node = parent[node]  # 부모 방향으로 이동.
#         return node  # return은 대표 정점 반환.
# 
#     def piece(index, x, y):  # 도로 index 위 좌표가 포함된 카메라 없는 조각의 정점 번호 계산.
#         offset = min(bisect_right(cuts[index], x + y) - 1, len(cuts[index]) - 2)  # 오른쪽 삽입 위치로 구간을 찾고 마지막 끝점은 마지막 조각에 배정.
#         return bases[index] + offset  # 도로의 첫 정점 번호에 구간 번호를 더해 반환.
# 
#     for i, (x1, y1, x2, y2, _) in enumerate(road):  # enumerate는 번호·값 제공. _는 여기서 사용하지 않는 제한 값.
#         for j in range(i):  # 도로 쌍을 중복 없이 한 번씩 비교.
#             a, b, c, d, _ = road[j]  # 다른 도로의 양 끝 좌표를 언패킹.
#             x, y = max(x1, a), max(y1, b)  # 두 선분 범위가 만난다면 그 유일한 교점의 좌표.
#             if x > min(x2, c) or y > min(y2, d) or (x, y) in cameras:  # or는 하나라도 참. 교점이 없거나 카메라 위치이면 무료 연결을 하지 않음.
#                 continue  # continue는 이번 도로 쌍을 건너뜀.
#             first, second = find(piece(i, x, y)), find(piece(j, x, y))  # 교점 양쪽 도로 조각의 대표를 조회.
#             if first != second:  # 이미 연결된 집합이 아닐 때만 합침.
#                 if sizes[first] < sizes[second]:  # 작은 집합을 큰 집합에 붙이도록 순서 조정.
#                     first, second = second, first  # 두 변수의 값을 튜플 대입으로 교환.
#                 parent[second] = first  # 두 카메라 없는 조각을 같은 연결 집합으로 합침.
#                 sizes[first] += sizes[second]  # +=는 더해 저장. 합쳐진 집합 크기 갱신.
#     offset = len(parent)  # 조각 정점 다음 번호부터 카메라 정점으로 사용.
#     graph = [[] for _ in range(offset + len(cameras))]  # 인접 리스트 생성. 각 정점에 (이웃, 제한 속도)를 저장.
#     for node, camera in links:  # 카메라와 주변 조각 연결을 그래프 간선으로 변환.
#         node = find(node)  # 조각 대신 합쳐진 연결 집합의 대표 사용.
#         limit = cameras[camera_points[camera]]  # 카메라 위치에서의 제한 속도 조회.
#         graph[node].append((offset + camera, limit))  # 조각에서 카메라로 가는 간선 추가.
#         graph[offset + camera].append((node, limit))  # 반대 방향도 추가해 양방향 이동 표현.
#     cities = []  # 도시가 속한 연결 집합 번호 목록.
#     for x, y in city:  # 각 도시 좌표 순회.
#         for i, (x1, y1, x2, y2, _) in enumerate(road):  # 도시가 놓인 도로를 찾음.
#             if x1 <= x <= x2 and y1 <= y <= y2:  # and는 모두 참. 좌표가 선분의 범위 안인지 검사.
#                 cities.append(find(piece(i, x, y)))  # 도시는 카메라와 겹치지 않으므로 조각 대표만 저장.
#                 break  # break는 안쪽 반복 종료. 교점의 다른 도로도 이미 같은 집합.
#     infinity = 1000001  # 모든 제한 속도보다 큰 값으로 무제한을 표현.
#     best = [0] * len(graph)  # best[v]는 그 정점까지 가능한 최고 속도.
#     best[cities[0]] = infinity  # 시작 도시는 아직 카메라를 지나지 않았으므로 무제한.
#     heap = [(-infinity, cities[0])]  # 최소 힙에 음수 속도를 넣어 큰 속도부터 꺼내는 최대 힙처럼 사용.
#     while heap:  # 빈 힙은 거짓. 처리할 후보가 남아 있는 동안 반복.
#         negative, node = heappop(heap)  # heappop은 가장 작은 항목을 제거·반환. 튜플은 첫 값부터 비교.
#         speed = -negative  # 부호를 되돌려 실제 속도 복원.
#         if speed != best[node]:  # 더 좋은 경로가 나중에 등록된 낡은 후보인지 확인.
#             continue  # 낡은 후보를 건너뜀.
#         for neighbor, limit in graph[node]:  # 현재 정점의 이웃과 제한 속도 순회.
#             candidate = min(speed, limit)  # 경로에서 지나친 카메라 제한의 최솟값이 유지 가능한 속도.
#             if candidate > best[neighbor]:  # 기존 경로보다 더 빠른 경로를 찾았는지 검사.
#                 best[neighbor] = candidate  # 이웃의 최고 속도 갱신.
#                 heappush(heap, (-candidate, neighbor))  # heappush로 갱신한 후보 추가.
#     return [0 if best[node] == infinity else best[node] for node in cities[1:]]  # [1:]은 시작 도시 제외. 무제한은 문제 규칙대로 0으로 변환해 반환.

# 풀이 요약
# 모든 카메라 지점에서 도로를 자르고, 카메라가 없는 교점으로 이어진 조각은 서로소 집합으로 합칩니다. 카메라가 교점에 있어도 우회해 무료 통과하지 않도록 그 지점은 합치지 않습니다.
# 카메라 간선만 남은 그래프에서 경로의 최소 제한을 최대화하는 우선순위 탐색을 합니다. 도로 수 M에 대해 전처리 O(M² log M), 압축 그래프 공간 O(M).
# 예: 제한 80·70을 지나는 경로는 70까지 가능하며, 제한 45를 지나는 경로보다 좋습니다. 카메라 없는 연결 집합에 목적 도시가 있으면 0입니다.
