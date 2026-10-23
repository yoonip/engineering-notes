# 연결된 컴퓨터의 집합을 합치고 서로 다른 대표의 개수를 셉니다. DFS 대신 연결 관계를 하나씩 처리하는 방식입니다.
def solution(n,computers):
    parent=list(range(n))
    def find(x):
        while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
        return x
    for i in range(n):
        for j in range(i):
            if computers[i][j]:parent[find(i)]=find(j)
    return len({find(i) for i in range(n)})
