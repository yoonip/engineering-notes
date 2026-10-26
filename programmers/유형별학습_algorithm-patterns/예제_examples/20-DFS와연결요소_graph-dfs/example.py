import sys  # 표준 입력 전체를 토큰으로 읽기

def main():  # 입력 한 건을 계산하고 결과 출력
    tokens = iter(sys.stdin.read().split())  # 공백과 줄바꿈을 같은 구분자로 처리
    n, m = int(next(tokens)), int(next(tokens))  # 정점 수와 간선 수
    adj = [[0] * n for _ in range(n)]  # 독립적인 행들로 연결 표 생성
    for _ in range(m):  # 무방향 간선 입력
        a, b = int(next(tokens)), int(next(tokens))  # 간선의 양끝
        adj[a][b] = adj[b][a] = 1  # 양방향 연결
    label = [-1] * n  # 미방문 정점 표시
    count = 0  # 새 연결 요소 번호
    for start in range(n):  # 고립 정점도 출발 후보에 포함
        if label[start] != -1:  # 이전 요소에 들어간 정점
            continue  # 중복 탐색 생략
        stack = [start]  # 이번 요소의 DFS 스택
        label[start] = count  # 넣는 순간 현재 소속 기록
        while stack:  # 이 요소의 후보가 남은 동안 반복
            u = stack.pop()  # LIFO 순서로 정점 꺼내기
            for v in range(n):  # 연결된 이웃 후보 확인
                if adj[u][v] and label[v] == -1:  # 새 이웃만 등록
                    label[v] = count  # 스택 중복 삽입 방지
                    stack.append(v)  # 다음 DFS 후보 추가
        count += 1  # 한 요소를 끝내고 번호 증가
    print(count)  # 연결 요소 수
    print(*label)  # 정점별 소속

if __name__ == "__main__":  # 직접 실행할 때만 예제 시작
    main()  # 표준 입력 한 건 처리
