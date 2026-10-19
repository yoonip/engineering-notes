# 중력 작용
# 분류: HLD / implicit treap / 구간 합
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/77887
# 선택 이유: HLD로 경로를 연속 구간으로 나누고 implicit treap에서 구간 이동과 합을 처리한다. 노드를 따라 값을 하나씩 옮기지 않는다.
# 비용: 정점 N, 질의 Q: 초기화 기대 O(N log N), 갱신 기대 O(log² N), 합 질의 기대 O(log N), 추가 공간 O(N+Q).

from random import Random


def solution(values, edges, queries):
    n = len(values)
    graph = [[] for _ in range(n)]
    for a, b in edges:
        graph[a - 1].append(b - 1)
        graph[b - 1].append(a - 1)

    parent = [-1] * n
    order = [0]
    for u in order:
        for v in graph[u]:
            if v != parent[u]:
                parent[v] = u
                order.append(v)

    subtree = [1] * n
    heavy = [-1] * n
    for u in reversed(order):
        p = parent[u]
        if p != -1:
            subtree[p] += subtree[u]
            if heavy[p] == -1 or subtree[u] > subtree[heavy[p]]:
                heavy[p] = u

    head = [0] * n
    position = [0] * n
    stack = [(0, 0)]
    timer = 0
    while stack:
        u, top = stack.pop()
        while u != -1:
            head[u] = top
            position[u] = timer
            timer += 1
            for v in graph[u]:
                if parent[v] == u and v != heavy[u]:
                    stack.append((v, v))
            u = heavy[u]

    left = [0] * (n + 1)
    right = [0] * (n + 1)
    size = [0] + [1] * n
    weight = [0] * (n + 1)
    for u in range(n):
        weight[position[u] + 1] = values[u]
    total = weight.copy()
    rng = Random(77887)
    priority = [rng.getrandbits(64) for _ in range(n + 1)]

    def pull(u):
        size[u] = size[left[u]] + size[right[u]] + 1
        total[u] = total[left[u]] + weight[u] + total[right[u]]

    def merge(a, b):
        if not a or not b:
            return a or b
        if priority[a] < priority[b]:
            right[a] = merge(right[a], b)
            pull(a)
            return a
        left[b] = merge(a, left[b])
        pull(b)
        return b

    def split(u, count):
        if not u:
            return 0, 0
        if count <= 0:
            return 0, u
        if count >= size[u]:
            return u, 0
        if count <= size[left[u]]:
            a, left[u] = split(left[u], count)
            pull(u)
            return a, u
        right[u], b = split(right[u], count - size[left[u]] - 1)
        pull(u)
        return u, b

    def prefix_sum(u, count):
        result = 0
        while u and count > 0:
            left_size = size[left[u]]
            if count <= left_size:
                u = left[u]
            else:
                result += total[left[u]] + weight[u]
                count -= left_size + 1
                u = right[u]
        return result

    root = 0
    for u in range(1, n + 1):
        root = merge(root, u)

    answer = []
    for u, w in queries:
        u -= 1
        if w == -1:
            start = position[u]
            end = start + subtree[u]
            answer.append(prefix_sum(root, end) - prefix_sum(root, start))
        else:
            segments = []
            while u != -1:
                top = head[u]
                segments.append((position[top], position[u]))
                u = parent[top]

            carry = w
            for start, end in reversed(segments):
                before, rest = split(root, start)
                segment, after = split(rest, end - start + 1)
                middle, last = split(segment, end - start)
                carry, weight[last] = weight[last], carry
                pull(last)
                root = merge(merge(before, merge(last, middle)), after)

    return answer
