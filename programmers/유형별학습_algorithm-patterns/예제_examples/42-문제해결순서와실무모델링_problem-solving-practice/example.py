import sys  # 표준 입력 전체를 토큰으로 읽기

def main():  # 입력 한 건을 계산하고 결과 출력
    tokens = iter(sys.stdin.read().split())  # 공백과 줄바꿈을 같은 구분자로 처리
    n, m, checkpoint, target = (int(next(tokens)) for _ in range(4))  # 위치 수·도로 수·필수 지점·목표
    adj = [[0] * n for _ in range(n)]  # 단위 비용 도로의 인접 행렬
    for _ in range(m):  # 양방향 도로 입력
        a, b = int(next(tokens)), int(next(tokens))  # 도로 양끝
        adj[a][b] = adj[b][a] = 1  # 두 방향 이동 허용
    def bfs_distance(start, goal):  # 위치만으로 충분한 최소 이동 계산
        distance = [-1] * n  # 아직 도달하지 않은 위치
        queue = [start]  # FIFO 탐색 목록
        distance[start] = 0  # 출발점을 거리 0으로 발견
        head = 0  # 다음에 읽을 큐 인덱스
        while head < len(queue):  # 가까운 위치부터 확인
            u = queue[head]  # 현재 위치
            head += 1  # 읽는 위치 전진
            for v in range(n):  # 이어진 도로 후보
                if adj[u][v] and distance[v] == -1:  # 새로 도달하는 위치
                    distance[v] = distance[u] + 1  # 한 도로 더 이동한 거리
                    queue.append(v)  # 다음 탐색 대상 추가
        return distance[goal]  # 미도달이면 -1
    first = bfs_distance(0, checkpoint)  # 필수 지점까지의 최소 이동
    second = bfs_distance(checkpoint, target)  # 필수 지점 이후의 최소 이동
    print(-1 if first < 0 or second < 0 else first + second)  # 두 구간의 도달 여부를 먼저 확인

if __name__ == "__main__":  # 직접 실행할 때만 예제 시작
    main()  # 표준 입력 한 건 처리
