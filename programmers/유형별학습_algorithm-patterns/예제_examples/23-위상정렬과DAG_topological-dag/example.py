import sys  # 표준 입력 전체를 토큰으로 읽기

def main():  # 입력 한 건을 계산하고 결과 출력
    tokens = iter(sys.stdin.read().split())  # 공백과 줄바꿈을 같은 구분자로 처리
    n, m = int(next(tokens)), int(next(tokens))  # 작업 수와 선행 관계 수
    duration = [int(next(tokens)) for _ in range(n)]  # 각 작업의 소요 시간
    finish = duration[:]  # 선행 조건이 없을 때의 완료 시각
    degree = [0] * n  # 아직 남은 선행 관계 수
    adj = [[0] * n for _ in range(n)]  # 선행 관계의 인접 행렬
    for _ in range(m):  # 선행 간선 입력
        u, v = int(next(tokens)), int(next(tokens))  # u가 v보다 먼저 끝나야 함
        if not adj[u][v]:  # 중복 관계는 한 번만 저장
            adj[u][v] = 1  # 방향 간선 표시
            degree[v] += 1  # 남은 선행 조건 추가
    queue = [u for u in range(n) if degree[u] == 0]  # 바로 처리 가능한 작업
    head = processed = 0  # 큐 위치와 처리 수
    while head < len(queue):  # 준비 작업이 남은 동안 반복
        u = queue[head]  # 다음 완료 작업
        head += 1  # 읽는 위치 이동
        processed += 1  # 사이클 판정용 처리 수
        for v in range(n):  # 후속 작업 후보 확인
            if not adj[u][v]:  # 관계없는 작업
                continue  # 갱신 생략
            finish[v] = max(finish[v], finish[u] + duration[v])  # 가장 늦은 선행 완료 시각
            degree[v] -= 1  # 끝난 선행 작업 하나 제거
            if degree[v] == 0:  # 남은 선행 조건이 없으면
                queue.append(v)  # 이후 처리할 작업에 추가
    if processed != n:  # 전체 작업을 처리하지 못한 경우
        print("CYCLE")  # 순환 의존 표시
    else:  # 모든 작업이 위상 순서로 처리된 경우
        print(*finish)  # 정점별 최소 완료 시각

if __name__ == "__main__":  # 직접 실행할 때만 예제 시작
    main()  # 표준 입력 한 건 처리
