import sys  # 표준 입력 전체를 토큰으로 읽기

def main():  # 입력 한 건을 계산하고 결과 출력
    tokens = iter(sys.stdin.read().split())  # 공백과 줄바꿈을 같은 구분자로 처리
    n, queries = int(next(tokens)), int(next(tokens))  # 트리 크기와 질의 수
    adj = [[0] * n for _ in range(n)]  # 작은 트리의 인접 행렬
    for _ in range(n - 1):  # 트리 간선 입력
        a, b = int(next(tokens)), int(next(tokens))  # 간선 양끝
        adj[a][b] = adj[b][a] = 1  # 양방향 연결
    depth = [0] * n  # 루트 기준 깊이
    subtree = [0] * n  # 자기 자신을 포함한 크기
    up = [[0] * n for _ in range(4)]  # 최대 8정점에 충분한 조상 표
    def prepare(u, parent):  # 부모·깊이와 후위 크기 계산
        up[0][u] = parent  # 직계 부모 저장
        subtree[u] = 1  # 자기 자신부터 집계
        for v in range(n):  # 이웃 후보 확인
            if not adj[u][v] or v == parent:  # 없는 간선과 부모 제외
                continue  # 자식만 아래로 탐색
            depth[v] = depth[u] + 1  # 자식 깊이 갱신
            prepare(v, u)  # 자식 결과 계산
            subtree[u] += subtree[v]  # 완성한 크기를 부모에 더하기
    prepare(0, 0)  # 루트의 조상을 자신으로 통일
    for k in range(1, 4):  # 두 번의 절반 점프로 표 확장
        for u in range(n):  # 모든 정점의 같은 크기 점프 계산
            up[k][u] = up[k - 1][up[k - 1][u]]  # 2의 k제곱 번째 조상
    def lca(u, v):  # 깊이 정렬 후 최소 공통 조상 찾기
        if depth[u] < depth[v]:  # 깊은 쪽을 앞에 두기
            u, v = v, u  # 두 정점 교환
        difference = depth[u] - depth[v]  # 먼저 줄일 깊이 차이
        for k in range(4):  # 차이의 켜진 비트만큼 이동
            if (difference >> k) & 1:  # 해당 크기의 점프가 필요하면
                u = up[k][u]  # 조상으로 이동
        if u == v:  # 조상 관계와 같은 정점 질의
            return u  # 부모로 더 올라가지 않기
        for k in range(3, -1, -1):  # 큰 점프부터 함께 이동
            if up[k][u] != up[k][v]:  # 아직 공통 조상 아래인 점프
                u, v = up[k][u], up[k][v]  # 두 정점을 같은 높이로 올리기
        return up[0][u]  # 바로 위의 공통 부모
    print(*subtree)  # 번호순 서브트리 크기
    for _ in range(queries):  # 입력 순서대로 질의
        u, v = int(next(tokens)), int(next(tokens))  # 두 질의 정점
        print(lca(u, v))  # 질의 결과 한 줄

if __name__ == "__main__":  # 직접 실행할 때만 예제 시작
    main()  # 표준 입력 한 건 처리
