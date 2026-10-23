def solution(n, computers):
    visited = [False] * n
    answer = 0
    for start in range(n):
        if visited[start]:
            continue
        answer += 1
        visited[start] = True
        stack = [start]
        while stack:
            node = stack.pop()
            for neighbor in range(n):
                if computers[node][neighbor] and not visited[neighbor]:
                    visited[neighbor] = True
                    stack.append(neighbor)
    return answer

# 전체 코드 줄별 설명
# def solution(n, computers):  # def는 함수 정의. 컴퓨터 수와 연결 여부를 나타낸 2차원 배열을 받음.
#     visited = [False] * n  # []는 리스트, *는 반복. False는 아직 방문하지 않았음을 뜻하는 불리언 값.
#     answer = 0  # 독립적인 네트워크 수.
#     for start in range(n):  # range(n)은 0~n-1. 모든 컴퓨터를 출발 후보로 확인.
#         if visited[start]:  # []로 방문 여부 조회. 이미 탐색한 네트워크라면 참.
#             continue  # 이번 반복을 건너뜀.
#         answer += 1  # +=는 더해 저장. 미방문 컴퓨터에서 새 네트워크 탐색 시작.
#         visited[start] = True  # 큐·스택에 넣는 순간 방문 표시.
#         stack = [start]  # 마지막 원소부터 꺼내는 스택을 리스트로 구현.
#         while stack:  # 스택에 원소가 있는 동안 깊이 우선 탐색(DFS).
#             node = stack.pop()  # pop은 마지막 원소를 꺼내 삭제.
#             for neighbor in range(n):  # 연결 표의 현재 행에서 모든 이웃 후보 확인.
#                 if computers[node][neighbor] and not visited[neighbor]:  # and는 모두 참, not은 부정. 연결되어 있고 아직 방문하지 않은 경우.
#                     visited[neighbor] = True  # 방문 표시해 중복 추가 방지.
#                     stack.append(neighbor)  # append는 끝에 추가. 이 컴퓨터도 같은 네트워크로 탐색.
#     return answer  # 연결된 덩어리 수 반환.

# 풀이 요약
# 미방문 컴퓨터를 발견할 때마다 네트워크 수를 하나 늘리고, 연결된 모든 컴퓨터를 DFS로 방문한다.
# 예: 0번과 1번이 연결되고 2번이 혼자이면 DFS를 두 번 시작하므로 답은 2.
# 연결 행렬의 모든 행·열을 검사하므로 시간 O(N²), 추가 공간 O(N).
# 