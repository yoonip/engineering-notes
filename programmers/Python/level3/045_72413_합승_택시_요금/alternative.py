# 모든 지점 쌍의 최단요금을 계산한 뒤 합승 종료 지점을 모두 비교합니다. 세 번의 다익스트라보다 밀집 그래프에서 구현이
# 단순하지만 O(N³)입니다.
def solution(n,s,a,b,fares):
    d=[[float('inf')]*n for _ in range(n)]
    for i in range(n):d[i][i]=0
    for u,v,w in fares:d[u-1][v-1]=d[v-1][u-1]=w
    for k in range(n):
        for i in range(n):
            for j in range(n):d[i][j]=min(d[i][j],d[i][k]+d[k][j])
    return min(d[s-1][k]+d[k][a-1]+d[k][b-1] for k in range(n))
