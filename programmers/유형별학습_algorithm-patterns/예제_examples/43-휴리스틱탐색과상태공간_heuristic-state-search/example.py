import sys  # 표준 입력 전체를 토큰으로 읽기

def main():  # 입력 한 건을 계산하고 결과 출력
    tokens = iter(sys.stdin.read().split())  # 공백과 줄바꿈을 같은 구분자로 처리
    rows, cols = int(next(tokens)), int(next(tokens))  # 격자 크기
    grid = [next(tokens) for _ in range(rows)]  # 벽과 통로 문자열
    if grid[0][0] == "#" or grid[-1][-1] == "#":  # 출발점이나 목표가 벽이면
        print(-1)  # 경로 없음 표시
        return  # 탐색을 시작하지 않기
    vertices = rows * cols  # 격자 칸을 일차원 상태로 표현
    inf = 10 ** 6  # 가능한 이동 수보다 큰 미도달 값
    distance = [inf] * vertices  # 상태별 최선 g
    closed = [False] * vertices  # 확정한 상태 표시
    distance[0] = 0  # 출발점 실제 비용
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # 상·우·하·좌 순서
    answer = -1  # 아직 경로를 찾지 못한 상태
    for _ in range(vertices):  # 상태별 최대 한 번 확장
        u, best = -1, inf  # 다음 최소 f 후보
        for v in range(vertices):  # 열린 상태의 우선순위 직접 비교
            if closed[v] or distance[v] == inf:  # 닫혔거나 미발견인 칸
                continue  # 후보에서 제외
            h = rows - 1 - v // cols + cols - 1 - v % cols  # Manhattan 거리 하한
            score = distance[v] + h  # A*의 g+h
            if score < best:  # 작은 f를 우선하며 동률은 먼저 본 번호 유지
                best, u = score, v  # 이번 확장 후보 갱신
        if u == -1:  # 열린 후보가 더 없으면
            break  # 경로 탐색 실패
        if u == vertices - 1:  # 목표를 유효한 최소 f로 꺼낸 경우
            answer = distance[u]  # 최단 이동 수 확정
            break  # 생성 시점보다 늦게 종료
        closed[u] = True  # 일관성에 따라 재확장 없이 확정
        row, col = divmod(u, cols)  # 현재 칸의 행·열
        for dr, dc in directions:  # 네 방향 이웃 확인
            nr, nc = row + dr, col + dc  # 이웃 좌표
            if not (0 <= nr < rows and 0 <= nc < cols) or grid[nr][nc] == "#":  # 범위와 벽 먼저 검사
                continue  # 이동할 수 없는 칸 제외
            v = nr * cols + nc  # 이웃의 상태 번호
            if not closed[v] and distance[u] + 1 < distance[v]:  # 더 짧은 열린 경로 확인
                distance[v] = distance[u] + 1  # 최선 실제 비용 갱신
    print(answer)  # 최단 거리 또는 미도달 -1

if __name__ == "__main__":  # 직접 실행할 때만 예제 시작
    main()  # 표준 입력 한 건 처리
