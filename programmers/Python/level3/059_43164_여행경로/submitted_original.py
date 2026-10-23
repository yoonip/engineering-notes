def solution(tickets):
    graph = {}
    for start, end in tickets:
        graph.setdefault(start, []).append(end)
    for destinations in graph.values():
        destinations.sort(reverse=True)
    stack = ['ICN']
    route = []
    while stack:
        airport = stack[-1]
        if graph.get(airport):
            stack.append(graph[airport].pop())
        else:
            route.append(stack.pop())
    return route[::-1]

# 전체 코드 줄별 설명
# def solution(tickets):  # def는 함수 정의. 출발·도착 공항으로 이루어진 항공권 목록을 받음.
#     graph = {}  # {}는 딕셔너리. 출발 공항별 도착 공항 목록을 저장.
#     for start, end in tickets:  # for로 각 항공권의 두 공항을 언패킹.
#         graph.setdefault(start, []).append(end)  # setdefault는 키가 없으면 빈 리스트 생성, append는 도착 공항 추가. 같은 항공권도 별개로 보관.
#     for destinations in graph.values():  # values는 딕셔너리의 값인 도착 공항 목록들을 순회.
#         destinations.sort(reverse=True)  # sort는 제자리 정렬, reverse=True는 내림차순. 뒤에서 꺼내면 알파벳이 가장 작은 공항.
#     stack = ['ICN']  # []는 리스트. 현재 여행 경로를 후입선출 스택으로 관리.
#     route = []  # 더 갈 곳 없는 공항부터 확정되는 역순 경로.
#     while stack:  # while은 스택이 비어 있지 않은 동안 반복.
#         airport = stack[-1]  # [-1]은 마지막 원소 조회. 현재 공항.
#         if graph.get(airport):  # get은 키 조회, 없으면 None. 남은 항공권 리스트가 비어 있지 않으면 참.
#             stack.append(graph[airport].pop())  # pop은 마지막 도착 공항을 꺼내 항공권 한 장 소비. append로 다음 공항 이동.
#         else:  # 현재 공항에서 쓸 항공권이 없는 경우.
#             route.append(stack.pop())  # 막힌 지점을 경로 뒤쪽에 확정하고 이전 공항으로 돌아감. 오일러 경로를 만드는 방법.
#     return route[::-1]  # [::-1]은 역순 슬라이스. 뒤에서부터 확정한 공항 목록을 실제 여행 순서로 뒤집음.

# 풀이 요약
# 모든 항공권을 간선으로 한 오일러 경로를 만든다. 작은 공항부터 탐색하되 막힌 공항은 뒤에서 확정하므로 중간에 표가 남는 단순 탐욕의 실패를 피한다.
# 예: ICN→AAA가 막다른 길이고 ICN→BBB→ICN도 있으면 최종 경로는 ICN→BBB→ICN→AAA다.
# 항공권 T장일 때 시간 O(T log T), 공간 O(T). 스택을 사용해 재귀 깊이 제한도 피한다.
# 