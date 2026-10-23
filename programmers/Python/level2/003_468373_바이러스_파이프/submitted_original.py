def solution(n, infection, edges, k):
    graph = [[[] for _ in range(n)] for _ in range(3)]
    for x, y, kind in edges:
        graph[kind - 1][x - 1].append(y - 1)
        graph[kind - 1][y - 1].append(x - 1)

    groups = [[] for _ in range(3)]
    for kind in range(3):
        visited = [False] * n
        for start in range(n):
            if visited[start]:
                continue
            visited[start] = True
            stack = [start]
            component = 0
            while stack:
                node = stack.pop()
                component |= 1 << node
                for neighbor in graph[kind][node]:
                    if not visited[neighbor]:
                        visited[neighbor] = True
                        stack.append(neighbor)
            groups[kind].append(component)

    answer = 1

    def dfs(mask, remaining):
        nonlocal answer
        answer = max(answer, bin(mask).count('1'))
        if remaining == 0 or answer == n:
            return
        for components in groups:
            next_mask = mask
            for component in components:
                if mask & component:
                    next_mask |= component
            if next_mask != mask:
                dfs(next_mask, remaining - 1)

    dfs(1 << (infection - 1), k)
    return answer

# 전체 코드 줄별 설명 (아래는 모두 실행되지 않는 주석입니다.)
# def solution(n, infection, edges, k):  # def는 함수 정의. n·infection·edges·k는 입력 매개변수.
#     graph = [[[] for _ in range(n)] for _ in range(3)]  # 중첩 리스트 컴프리헨션으로 종류별 인접 목록 생성. range는 정수 순회, _는 안 쓸 변수.
#     for x, y, kind in edges:  # for로 간선 순회. x,y,kind는 한 간선의 세 값을 풀어 받는 언패킹.
#         graph[kind - 1][x - 1].append(y - 1)  # [][]는 종류·정점의 목록 접근. append는 끝에 원소 추가, -1은 번호를 인덱스로 변환.
#         graph[kind - 1][y - 1].append(x - 1)  # 무방향 간선이므로 반대 방향도 목록에 추가.
#
#     groups = [[] for _ in range(3)]  # 각 종류의 연결 요소를 담을 서로 다른 빈 리스트 3개 생성.
#     for kind in range(3):  # range(3)은 0,1,2를 차례로 제공. 세 종류를 순회.
#         visited = [False] * n  # False는 거짓. [False]*n으로 미방문 목록 초기화.
#         for start in range(n):  # 정점 인덱스 0부터 n-1까지 순회.
#             if visited[start]:  # if는 조건문. visited[start]가 참이면 이미 방문한 정점.
#                 continue  # continue는 이번 정점을 건너뛰고 다음 반복으로 진행.
#             visited[start] = True  # True는 참. 시작 정점을 방문 처리.
#             stack = [start]  # [start]는 시작 정점 하나를 담은 리스트. 스택으로 사용.
#             component = 0  # 연결 요소의 정점 집합을 표현할 정수 비트마스크 초기화.
#             while stack:  # while은 조건이 참인 동안 반복. 빈 스택은 거짓으로 평가.
#                 node = stack.pop()  # pop()은 리스트 끝 원소를 제거하고 반환. 스택은 마지막에 넣은 값을 먼저 꺼냄.
#                 component |= 1 << node  # 1<<node는 해당 정점 비트. |=는 비트 OR 결과를 다시 저장.
#                 for neighbor in graph[kind][node]:  # 현재 종류의 간선으로 이어진 이웃들을 순회.
#                     if not visited[neighbor]:  # not은 참·거짓 부정. 이웃이 미방문이면 실행.
#                         visited[neighbor] = True  # 이웃을 방문 처리해 중복으로 스택에 넣지 않음.
#                         stack.append(neighbor)  # append로 이웃을 스택 끝에 추가.
#             groups[kind].append(component)  # 완성한 연결 요소 비트마스크를 해당 종류 목록에 추가.
#
#     answer = 1  # 처음 감염된 정점은 1개이므로 정답 초기값 1.
#
#     def dfs(mask, remaining):  # 현재 감염 집합과 남은 횟수를 받는 중첩 재귀 함수 정의.
#         nonlocal answer  # nonlocal로 바깥 answer를 갱신하도록 지정.
#         answer = max(answer, bin(mask).count('1'))  # bin은 이진 문자열 변환, count('1')은 1의 개수, max는 큰 값 선택.
#         if remaining == 0 or answer == n:  # ==는 같음, or는 둘 중 하나가 참이면 참. 횟수 소진 또는 전원 감염 확인.
#             return  # return으로 현재 재귀 호출 종료.
#         for components in groups:  # 종류별 연결 요소 목록을 하나씩 선택.
#             next_mask = mask  # 이번 선택의 감염 집합을 현재 mask로 시작.
#             for component in components:  # 선택한 종류의 연결 요소를 차례로 순회.
#                 if mask & component:  # &는 두 비트마스크의 교집합. 0이 아니면 감염 정점과 연결됨.
#                     next_mask |= component  # |=로 연결 요소 전체를 다음 감염 집합에 합침.
#             if next_mask != mask:  # !=는 다름 비교. 감염 집합이 늘어난 경우만 탐색.
#                 dfs(next_mask, remaining - 1)  # ()로 dfs 호출. 남은 횟수를 1 줄임.
#
#     dfs(1 << (infection - 1), k)  # 감염 시작 번호의 비트만 켜고 k번 탐색 시작.
#     return answer  # 최대 감염 수를 반환.

# 풀이 요약
# 파이프 종류별 연결 요소를 미리 구하고, 그 집합을 비트마스크로 저장합니다.
# 한 종류를 선택하면 감염 정점과 닿은 연결 요소 전체가 감염됩니다. 최대 k번의 선택을 DFS로 비교합니다.
# 예: 감염 집합 {1}, 선택한 종류의 연결 요소 {1,2,3}이면 다음 감염 집합은 {1,2,3}입니다.
