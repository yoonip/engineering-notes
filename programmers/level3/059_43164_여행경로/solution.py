# 출발·도착 공항으로 이루어진 항공권 목록을 받음.
def solution(tickets):
    # 출발 공항별 도착 공항 목록을 저장.
    graph = {}
    # for로 각 항공권의 두 공항을 언패킹.
    for start, end in tickets:
        # 같은 항공권도 별개로 보관.
        graph.setdefault(start, []).append(end)
    # values는 딕셔너리의 값인 도착 공항 목록들을 순회.
    for destinations in graph.values():
        # 뒤에서 꺼내면 알파벳이 가장 작은 공항.
        destinations.sort(reverse=True)
    # 현재 여행 경로를 후입선출 스택으로 관리.
    stack = ['ICN']
    # 더 갈 곳 없는 공항부터 확정되는 역순 경로.
    route = []
    # while은 스택이 비어 있지 않은 동안 반복.
    while stack:
        airport = stack[-1]
        # 남은 항공권 리스트가 비어 있지 않으면 참.
        if graph.get(airport):
            # append로 다음 공항 이동.
            stack.append(graph[airport].pop())
        else:
            # 오일러 경로를 만드는 방법.
            route.append(stack.pop())
    # 뒤에서부터 확정한 공항 목록을 실제 여행 순서로 뒤집음.
    return route[::-1]
