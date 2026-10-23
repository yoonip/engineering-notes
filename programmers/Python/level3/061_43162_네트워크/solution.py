# 컴퓨터 수와 연결 여부를 나타낸 2차원 배열을 받음.
def solution(n, computers):
    # False는 아직 방문하지 않았음을 뜻하는 불리언 값.
    visited = [False] * n
    # 독립적인 네트워크 수.
    answer = 0
    # 모든 컴퓨터를 출발 후보로 확인.
    for start in range(n):
        # 이미 탐색한 네트워크라면 참.
        if visited[start]:
            # 이번 반복을 건너뜀.
            continue
        # 미방문 컴퓨터에서 새 네트워크 탐색 시작.
        answer += 1
        # 큐·스택에 넣는 순간 방문 표시.
        visited[start] = True
        # 마지막 원소부터 꺼내는 스택을 리스트로 구현.
        stack = [start]
        # 스택에 원소가 있는 동안 깊이 우선 탐색(DFS).
        while stack:
            # pop은 마지막 원소를 꺼내 삭제.
            node = stack.pop()
            # 연결 표의 현재 행에서 모든 이웃 후보 확인.
            for neighbor in range(n):
                # 연결되어 있고 아직 방문하지 않은 경우.
                if computers[node][neighbor] and not visited[neighbor]:
                    # 방문 표시해 중복 추가 방지.
                    visited[neighbor] = True
                    # 이 컴퓨터도 같은 네트워크로 탐색.
                    stack.append(neighbor)
    # 연결된 덩어리 수 반환.
    return answer
