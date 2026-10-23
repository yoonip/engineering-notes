# 현재 시각과 거점을 상태로 두고 머물기·인접 이동을 모두 재귀 탐색합니다. 끝 기록은 고정합니다. 반복 DP와 달리 뒤에서
# 필요한 값만 계산합니다.
from functools import lru_cache

def solution(n,m,edge_list,k,gps_log):
    graph=[{i} for i in range(n+1)]
    for a,b in edge_list:graph[a].add(b);graph[b].add(a)
    @lru_cache(None)
    def solve(time,node):
        if time==k-1:return 0 if node==gps_log[-1] else float('inf')
        return min((nxt!=gps_log[time+1])+solve(time+1,nxt) for nxt in graph[node])
    result=solve(0,gps_log[0])
    return result if result<float('inf') else -1
