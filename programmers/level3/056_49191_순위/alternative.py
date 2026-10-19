# 각 선수에서 승리 방향과 패배 방향으로 각각 그래프 탐색합니다. 승자·패자 관계가 모두 합해 N−1명인 선수를 셉니다.
# Floyd 전파와 달리 인접 리스트를 사용합니다.
def solution(n,results):
    win=[set() for _ in range(n)];lose=[set() for _ in range(n)]
    for a,b in results:win[a-1].add(b-1);lose[b-1].add(a-1)
    def reachable(start,graph):
        seen=set();stack=list(graph[start])
        while stack:
            v=stack.pop()
            if v not in seen:seen.add(v);stack.extend(graph[v]-seen)
        return seen
    return sum(len(reachable(i,win)|reachable(i,lose))==n-1 for i in range(n))
