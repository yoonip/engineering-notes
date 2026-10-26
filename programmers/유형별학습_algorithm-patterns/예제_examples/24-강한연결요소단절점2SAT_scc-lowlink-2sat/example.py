import sys  # 표준 입력 전체를 토큰으로 읽기

def main():  # 입력 한 건을 계산하고 결과 출력
    tokens = iter(sys.stdin.read().split())  # 공백과 줄바꿈을 같은 구분자로 처리
    variables, clauses = int(next(tokens)), int(next(tokens))  # 변수 수와 두 리터럴 절 수
    vertices = 2 * variables  # 참과 부정을 각각 정점으로 생성
    adj = [[0] * vertices for _ in range(vertices)]  # 함의 그래프의 인접 행렬
    def literal_node(literal):  # 부호 있는 정수를 리터럴 정점으로 변환
        return 2 * (abs(literal) - 1) + (literal < 0)  # 서로 부정인 리터럴 번호는 XOR 1 관계
    for _ in range(clauses):  # OR 절 입력
        a, b = literal_node(int(next(tokens))), literal_node(int(next(tokens)))  # 절을 이루는 두 정점
        adj[a ^ 1][b] = adj[b ^ 1][a] = 1  # 두 방향의 함의 추가
    seen = [False] * vertices  # 첫 DFS의 방문 여부
    order = []  # 첫 DFS의 종료 순서
    def dfs_order(u):  # 원래 그래프의 후위 순서 계산
        seen[u] = True  # 재귀 중복 방문 방지
        for v in range(vertices):  # 후속 함의 확인
            if adj[u][v] and not seen[v]:  # 미방문 이웃만 탐색
                dfs_order(v)  # 이웃 종료를 먼저 기록
        order.append(u)  # 모든 이웃 처리를 마친 정점
    for u in range(vertices):  # 고립 리터럴도 탐색에 포함
        if not seen[u]:  # 아직 시작하지 않은 DFS
            dfs_order(u)  # 종료 순서 확장
    component = [-1] * vertices  # 두 번째 DFS의 SCC 번호
    def dfs_component(u, label):  # 역그래프에서 SCC 한 개 분리
        component[u] = label  # 현재 소속 기록
        for v in range(vertices):  # u로 들어오던 간선을 역방향으로 사용
            if adj[v][u] and component[v] == -1:  # 아직 SCC가 없는 역방향 이웃
                dfs_component(v, label)  # 같은 SCC에 포함
    count = 0  # 다음 SCC 번호
    for u in reversed(order):  # 종료 순서가 늦은 정점부터 시작
        if component[u] == -1:  # 이전 SCC에 포함되지 않은 정점
            dfs_component(u, count)  # 새로운 SCC 탐색
            count += 1  # 다음 SCC 번호로 이동
    possible = all(component[2 * x] != component[2 * x + 1] for x in range(variables))  # 변수와 부정의 동시 함의 모순 검사
    print("SAT" if possible else "UNSAT")  # 만족 가능성만 출력

if __name__ == "__main__":  # 직접 실행할 때만 예제 시작
    main()  # 표준 입력 한 건 처리
