# 문제: 전력망을 둘로 나누기
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/86971
# 풀이: DFS로 자식 부분 트리의 크기 S를 구한다. 그 간선을 끊은 차이는 |N-2S|이므로 간선마다 별도 탐색할 필요가 없다.
# 복잡도: 정점 N개인 트리: 시간 O(N), 인접 목록·재귀 공간 O(N).

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
