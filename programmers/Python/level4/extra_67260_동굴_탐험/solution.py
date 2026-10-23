from collections import deque  # from A import B는 모듈에서 가져오기. deque는 먼저 넣은 원소를 먼저 처리하는 큐로 사용.

def solution(n, path, order):
    graph = [[] for _ in range(n)]  # 리스트 내포로 방마다 독립적인 이웃 목록 생성.
    for a, b in path:  # 각 통로의 두 방 번호를 나눠 받음.
        graph[a].append(b)  # append는 끝에 추가. a에서 b로 갈 수 있음을 기록.
        graph[b].append(a)  # 양방향 통로이므로 반대 방향도 기록.
    before = [-1] * n  # before[b]는 b보다 먼저 방문할 방. -1은 선행 조건 없음.
    for a, b in order:  # 주어진 선행·후행 방 쌍을 순회.
        before[b] = a  # b에 들어가기 전에 방문해야 할 방 a 저장.
    if before[0] != -1:  # !=는 다름 비교. 유일한 입구 0번에 선행 방이 있으면 시작 불가능.
        return False  # False는 거짓 논릿값. 모든 방 방문이 불가능함을 반환.
    waiting = [-1] * n  # waiting[a]는 a를 기다리며 방문이 보류된 방. 문제에서 각 선행 방의 후행 방은 최대 하나.
    visited = bytearray(n)  # bytearray는 작은 정수 배열. 방문 여부를 0·1로 저장.
    queue = deque([0])  # 입구 방을 큐에 넣어 탐색 시작.
    count = 0  # 실제로 방문한 방 개수 초기화.
    while queue:  # while은 큐가 비어 있지 않은 동안 반복.
        node = queue.popleft()  # popleft는 맨 앞 원소 제거·반환. 다음 방문 후보 방 선택.
        if visited[node]:
            continue  # continue는 이번 반복을 건너뜀.
        if before[node] != -1 and not visited[before[node]]:  # and는 모두 참, not은 부정. 선행 방을 아직 방문하지 않았다면 보류.
            waiting[before[node]] = node  # 선행 방 방문 시 다시 꺼낼 수 있도록 대기 방 저장.
            continue  # 이 방을 통과하지 않고 다음 후보 처리.
        visited[node] = 1  # 선행 조건을 만족한 방을 방문 처리.
        count += 1
        if waiting[node] != -1:  # 지금 방을 기다리던 방이 있으면 실행.
            queue.append(waiting[node])  # 기다리던 방은 이미 접근 가능했던 방이므로 다시 방문 후보에 추가.
        for neighbor in graph[node]:  # 현재 방과 연결된 이웃을 순회.
            if not visited[neighbor]:  # 아직 방문하지 않은 이웃인지 확인.
                queue.append(neighbor)  # 이웃을 방문 후보 큐에 추가.
    return count == n  # ==는 같음 비교. 모든 방을 방문했는지 논릿값 반환.
