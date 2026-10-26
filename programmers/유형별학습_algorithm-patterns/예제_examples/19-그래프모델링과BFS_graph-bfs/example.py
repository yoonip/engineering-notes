import sys  # 표준 입력 전체를 토큰으로 읽기

def main():  # 입력 한 건을 계산하고 결과 출력
    tokens = iter(sys.stdin.read().split())  # 공백과 줄바꿈을 같은 구분자로 처리
    n, m, start = int(next(tokens)), int(next(tokens)), int(next(tokens))  # 그래프 크기와 출발점
    adj = [[0] * n for _ in range(n)]  # 각 행이 독립인 인접 행렬
    for _ in range(m):  # 무방향 간선 입력
        a, b = int(next(tokens)), int(next(tokens))  # 간선 양끝
        adj[a][b] = adj[b][a] = 1  # 양방향 이동 표시
    distance = [-1] * n  # 아직 발견하지 않은 거리
    queue = [start]  # head로 읽을 FIFO 목록
    distance[start] = 0  # 출발점을 넣는 순간 발견 처리
    head = 0  # 다음에 읽을 큐 위치
    while head < len(queue):  # 발견 순서대로 처리
        u = queue[head]  # 이번 정점
        head += 1  # 읽는 위치 전진
        for v in range(n):  # 현재 행의 모든 이웃 후보
            if adj[u][v] and distance[v] == -1:  # 연결된 미발견 정점만 선택
                distance[v] = distance[u] + 1  # 한 간선 더 이동한 최단 거리
                queue.append(v)  # 다음 층 후보를 뒤에 추가
    print(*distance)  # 번호순 거리 출력

if __name__ == "__main__":  # 직접 실행할 때만 예제 시작
    main()  # 표준 입력 한 건 처리
