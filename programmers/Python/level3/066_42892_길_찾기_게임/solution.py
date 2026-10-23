# 0번 원소가 1번 노드인 좌표 목록을 받음.
def solution(nodeinfo):
    # len은 노드 수.
    n = len(nodeinfo)
    # -1은 자식 없음.
    left, right = [-1] * n, [-1] * n
    # x좌표 순으로 노드 번호 정렬.
    order = sorted(range(n), key=lambda i: nodeinfo[i][0])
    # 마지막에 넣은 노드를 먼저 꺼냄.
    stack = []
    # x가 작은 노드부터 트리에 추가.
    for node in order:
        # 새 노드의 왼쪽 자식이 될 이전 부분 트리.
        last = -1
        # 새 노드보다 낮은 y의 노드는 조상이 될 수 없음.
        while stack and nodeinfo[stack[-1]][1] < nodeinfo[node][1]:
            # 제거한 부분 트리를 새 노드 아래로 옮길 준비.
            last = stack.pop()
        # 더 높은 조상이 남아 있으면 참.
        if stack:
            # 새 노드를 남아 있는 조상의 오른쪽 자식으로 연결.
            right[stack[-1]] = node
        # 아래로 옮길 부분 트리가 있는지 확인.
        if last != -1:
            # x는 더 작으므로 새 노드의 왼쪽 자식으로 연결.
            left[node] = last
        # 새 노드를 오른쪽 경로의 마지막 노드로 저장.
        stack.append(node)
    # 가장 높은 y를 가진 전체 트리의 루트.
    root = stack[0]
    # 전위·후위 방문 결과를 저장하는 리스트.
    preorder, postorder = [], []
    # (노드,자식 처리 후인지) 상태로 재귀를 스택으로 대신함.
    stack = [(root, False)]
    # 처리할 방문 상태가 남아 있는 동안 반복.
    while stack:
        # 상태를 꺼내 언패킹.
        node, finished = stack.pop()
        # True이면 두 자식을 모두 처리한 뒤 다시 만난 상태.
        if finished:
            # 반환 노드 번호는 1부터이므로 +1.
            postorder.append(node + 1)
        else:
            # 전위 순회는 현재→왼쪽→오른쪽이므로 즉시 기록.
            preorder.append(node + 1)
            # 현재 노드의 후위 기록은 자식 처리 뒤로 미룸.
            stack.append((node, True))
            # 오른쪽 자식이 있을 때.
            if right[node] != -1:
                # 스택은 나중에 넣은 것이 먼저 나오므로 오른쪽을 먼저 넣음.
                stack.append((right[node], False))
            # 왼쪽 자식이 있을 때.
            if left[node] != -1:
                # 왼쪽을 마지막에 넣어 먼저 방문하게 함.
                stack.append((left[node], False))
    # 두 순회 결과를 2차원 리스트로 반환.
    return [preorder, postorder]
