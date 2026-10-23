from collections import defaultdict, deque

def solution(city, road):
    graph, cameras = defaultdict(set), {}
    for x1, y1, x2, y2, limit in road:
        point = ((x1 + x2) // 2, (y1 + y2) // 2)
        cameras[point] = min(limit, cameras.get(point, limit))
        dx, dy = int(x2 > x1), int(y2 > y1)
        length = x2 - x1 + y2 - y1
        for step in range(length):
            a = (x1 + step * dx, y1 + step * dy)
            b = (a[0] + dx, a[1] + dy)
            graph[a].add(b)
            graph[b].add(a)
    def reachable(speed):
        seen, queue = {tuple(city[0])}, deque([tuple(city[0])])
        while queue:
            node = queue.popleft()
            for nxt in graph[node]:
                if nxt not in seen and cameras.get(nxt, float('inf')) >= speed:
                    seen.add(nxt)
                    queue.append(nxt)
        return seen
    unrestricted = reachable(float('inf'))
    answer = [0] * (len(city) - 1)
    for speed in sorted(set(cameras.values())):
        seen = reachable(speed)
        for i, target in enumerate(city[1:]):
            if tuple(target) in seen and tuple(target) not in unrestricted:
                answer[i] = speed
    return answer
