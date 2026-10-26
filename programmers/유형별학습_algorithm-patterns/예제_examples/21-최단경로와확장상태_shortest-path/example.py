import sys  # 표준 입력 전체를 토큰으로 읽기

def main():  # 입력 한 건을 계산하고 결과 출력
    tokens = iter(sys.stdin.read().split())  # 공백과 줄바꿈을 같은 구분자로 처리
    n, m, start = int(next(tokens)), int(next(tokens)), int(next(tokens))  # 그래프 크기와 출발점
    inf = 10 ** 9  # 가능한 최단 거리보다 큰 표시값
    weight = [[inf] * n for _ in range(n)]  # 방향 간선의 최소 비용 행렬
    for _ in range(m):  # 비음수 간선 입력
        a, b, cost = int(next(tokens)), int(next(tokens)), int(next(tokens))  # 출발·도착·비용
        weight[a][b] = min(weight[a][b], cost)  # 평행 간선 중 최솟값만 저장
    distance = [inf] * n  # 미도달 거리 초기화
    used = [False] * n  # 확정 여부
    distance[start] = 0  # 출발 비용 0
    for _ in range(n):  # 정점을 하나씩 확정
        u = -1  # 다음 최소 후보
        for v in range(n):  # 미확정 정점의 현재 거리 비교
            if not used[v] and (u == -1 or distance[v] < distance[u]):  # 더 작은 후보 확인
                u = v  # 이번 확정 후보 갱신
        if u == -1 or distance[u] == inf:  # 남은 정점이 미도달이면
            break  # 불필요한 확정 생략
        used[u] = True  # 비음수 간선 조건으로 거리 확정
        for v in range(n):  # 현재 정점에서 나가는 간선 확인
            if weight[u][v] != inf:  # 실제 간선만 사용
                distance[v] = min(distance[v], distance[u] + weight[u][v])  # 더 짧은 경로 완화
    print(*(-1 if value == inf else value for value in distance))  # 미도달을 구분해 출력

if __name__ == "__main__":  # 직접 실행할 때만 예제 시작
    main()  # 표준 입력 한 건 처리
