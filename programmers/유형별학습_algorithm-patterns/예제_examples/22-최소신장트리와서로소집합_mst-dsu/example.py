import sys  # 표준 입력 전체를 토큰으로 읽기

def main():  # 입력 한 건을 계산하고 결과 출력
    tokens = iter(sys.stdin.read().split())  # 공백과 줄바꿈을 같은 구분자로 처리
    n, m = int(next(tokens)), int(next(tokens))  # 정점 수와 간선 수
    edges = []  # 비용순으로 볼 간선 목록
    for _ in range(m):  # 무방향 간선 입력
        a, b, weight = int(next(tokens)), int(next(tokens)), int(next(tokens))  # 양끝과 비용
        edges.append((weight, a, b))  # 비용을 첫 정렬 키로 저장
    edges.sort()  # 작은 비용부터 검사
    parent = list(range(n))  # 초기 대표는 각 정점 자신
    sizes = [1] * n  # 초기 집합 크기
    def find_root(node):  # 현재 DSU 대표 찾기
        while parent[node] != node:  # 대표까지 부모를 따라 이동
            parent[node] = parent[parent[node]]  # 경로를 한 단계씩 줄이기
            node = parent[node]  # 짧아진 부모로 이동
        return node  # 현재 대표 반환
    selected = total = 0  # 선택 간선 수와 비용 합
    for weight, u, v in edges:  # 비용순 간선 확인
        a, b = find_root(u), find_root(v)  # 두 정점의 소속 조회
        if a == b:  # 이미 연결된 두 정점
            continue  # 사이클 간선 제외
        if sizes[a] < sizes[b]:  # 크기 기준 합치기 준비
            a, b = b, a  # 큰 집합을 앞에 두기
        parent[b] = a  # 작은 집합을 큰 대표에 연결
        sizes[a] += sizes[b]  # 새 집합 크기 갱신
        selected += 1  # 연결에 쓴 간선 수
        total += weight  # 해당 간선 비용 합산
    print(total if selected == n - 1 else "DISCONNECTED")  # 전체 연결 여부에 맞는 결과

if __name__ == "__main__":  # 직접 실행할 때만 예제 시작
    main()  # 표준 입력 한 건 처리
