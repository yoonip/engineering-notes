from heapq import heappush, heappop

def solution(land, height):
    n = len(land)
    visited = [bytearray(n) for _ in range(n)]
    heap = [(0, 0, 0)]
    answer = 0
    while heap:
        cost, r, c = heappop(heap)
        if visited[r][c]:
            continue
        visited[r][c] = 1
        answer += cost
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc]:
                gap = abs(land[r][c] - land[nr][nc])
                fee = 0 if gap <= height else gap
                heappush(heap, (fee, nr, nc))
    return answer

# 전체 코드 줄별 설명
# from heapq import heappush, heappop  # from A import B는 모듈에서 함수 가져오기. heapq는 최솟값 우선순위 큐인 최소 힙 제공.
# 
# def solution(land, height):  # def는 함수 정의. 지형 높이와 무료 이동 가능한 최대 높이 차 입력.
#     n = len(land)  # len은 길이. 정사각 격자의 한 변 길이.
#     visited = [bytearray(n) for _ in range(n)]  # 리스트 내포와 bytearray로 칸별 방문 여부 0·1 저장.
#     heap = [(0, 0, 0)]  # (연결 비용, 행, 열) 튜플을 저장하는 최소 힙. 시작 칸 연결 비용은 0.
#     answer = 0  # 선택한 사다리의 총비용 초기화.
#     while heap:  # while은 힙에 후보가 남아 있는 동안 반복.
#         cost, r, c = heappop(heap)  # heappop은 가장 작은 연결 비용의 후보를 제거·반환.
#         if visited[r][c]:  # if는 조건문. 이미 연결한 칸인지 확인.
#             continue  # continue는 이번 후보를 건너뜀. 같은 칸의 다른 연결 후보는 사용하지 않음.
#         visited[r][c] = 1  # 현재 칸을 연결 완료로 표시.
#         answer += cost  # +=는 더한 값 저장. 새 칸을 연결하는 비용만 합산.
#         for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):  # ()는 튜플. 상하좌우 방향 순회.
#             nr, nc = r + dr, c + dc  # 이웃 칸 좌표 계산.
#             if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc]:  # 연속 비교·and·not으로 격자 안의 미방문 칸만 검사.
#                 gap = abs(land[r][c] - land[nr][nc])  # abs는 절댓값. 두 칸 높이 차 계산.
#                 fee = 0 if gap <= height else gap  # 조건 표현식. 무료 이동 가능하면 0, 아니면 사다리 비용은 높이 차 전체.
#                 heappush(heap, (fee, nr, nc))  # heappush는 최소 힙 구조를 유지하며 연결 후보 추가.
#     return answer  # return으로 모든 칸을 연결한 최소 사다리 비용 반환.

# 풀이 요약
# 무료 이동은 비용 0, 사다리는 높이 차를 간선 비용으로 보고 모든 칸을 잇는 최소 신장 트리를 구합니다.
# 프림 알고리즘은 이미 연결한 영역에서 나가는 가장 저렴한 간선을 하나씩 선택합니다. 높이 차에서 height를 빼는 것이 아닙니다.
# 예제 1은 비용 5와 10의 사다리를 골라 합계 15. 시간 O(N^2*log N), 공간 O(N^2).
# 