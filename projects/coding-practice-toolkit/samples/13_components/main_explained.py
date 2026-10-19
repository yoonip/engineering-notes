# 무방향 그래프에서 간선을 따라 서로 갈 수 있는 정점 묶음의 수를 센다.
# 미방문 정점 하나에서 BFS를 시작할 때마다 새로운 연결요소가 하나 발견된다.
# 간선이 전혀 없는 고립 정점도 자기 자신만으로 연결요소 하나다.
# 입력 제한과 실행 비용: 인접행렬 버전: 시간 O(N²+M), 공간 O(N²). 인접리스트로 구현하면 시간·공간 O(N+M) 가능.

# adj[u][v]는 두 정점 사이 간선의 유무, seen[v]는 정점 v를 이미 방문했는지다.
# answer는 발견한 연결요소 개수다. 정점 번호는 0부터 N-1까지다.
# N<=100이어서 인접행렬이 간단하다. 큰 희소 그래프에는 인접리스트가 더 알맞을 수 있다.

# sys.stdin.buffer는 입력을 바이트로 읽는다. read는 전체 입력을 메모리에 올린다는 점을 고려한다.
# 문자열이 필요하면 decode하고 숫자가 필요하면 int로 바꾼다. 정수는 큰 값도 자동 확장된다.

import sys
from collections import deque
it=iter(map(int,sys.stdin.buffer.read().split()))
n,m=next(it),next(it)
adj=[[0]*n for _ in range(n)]
for _ in range(m):
    u,v=next(it),next(it)
    # 무방향 간선은 u에서 v로도, v에서 u로도 갈 수 있다.
    # 따라서 인접행렬의 대칭 두 칸을 모두 1로 표시한다.
    adj[u][v]=adj[v][u]=1
seen=[False]*n
answer=0
# 아직 방문하지 않은 정점만 새 BFS의 출발점으로 삼는다.
# 이미 방문한 정점은 앞의 BFS가 찾은 묶음에 속하므로 새로 세지 않는다.
for start in range(n):
    if seen[start]: continue # 앞서 센 연결요소에 포함된 정점은 건너뛴다.
    # 이 출발점의 연결요소를 하나 센다.
    # BFS가 이 묶음의 모든 정점을 방문한 뒤 바깥 반복이 다음 미방문 정점을 찾는다.
    answer+=1
    seen[start]=True
    q=deque([start])
    # 큐 앞 정점을 꺼내 그 정점에 연결된 이웃을 확인한다.
    # 행렬 한 행의 N칸을 확인하므로 전체 BFS는 O(N²)다.
    while q:
        u=q.popleft()
        for v in range(n):
            if adj[u][v] and not seen[v]:
                # 이웃을 큐에 넣는 순간 방문 표시를 한다.
                # 같은 이웃을 다른 정점이 다시 넣지 않으므로 한 정점은 전체 탐색에서 한 번만 큐에 들어간다.
                seen[v]=True
                q.append(v)
print(answer)

# 손으로 확인: 0에서 BFS → 0,1,2 방문 → 첫 연결요소
# 손으로 확인: 1,2는 이미 방문했으므로 시작하지 않음
# 손으로 확인: 3에서 BFS → 3,4 방문 → 둘째 연결요소
# 손으로 확인: 5에서 BFS → 5만 방문 → 셋째 연결요소
# 완성 후 확인: 무방향 간선은 adj[u][v]와 adj[v][u] 두 곳에 표시한다.
# 완성 후 확인: 큐에 넣을 때 visited를 표시해 중복 삽입을 막는다.
# 완성 후 확인: 고립된 정점을 빠뜨리지 않는다.
# 완성 후 확인: 한 번 BFS한 후에도 다른 연결요소를 찾도록 바깥 반복을 계속한다.
