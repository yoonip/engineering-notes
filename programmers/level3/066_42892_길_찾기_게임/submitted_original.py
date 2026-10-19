def solution(nodeinfo):
    n = len(nodeinfo)
    left, right = [-1] * n, [-1] * n
    order = sorted(range(n), key=lambda i: nodeinfo[i][0])
    stack = []
    for node in order:
        last = -1
        while stack and nodeinfo[stack[-1]][1] < nodeinfo[node][1]:
            last = stack.pop()
        if stack:
            right[stack[-1]] = node
        if last != -1:
            left[node] = last
        stack.append(node)
    root = stack[0]
    preorder, postorder = [], []
    stack = [(root, False)]
    while stack:
        node, finished = stack.pop()
        if finished:
            postorder.append(node + 1)
        else:
            preorder.append(node + 1)
            stack.append((node, True))
            if right[node] != -1:
                stack.append((right[node], False))
            if left[node] != -1:
                stack.append((left[node], False))
    return [preorder, postorder]

# 전체 코드 줄별 설명
# def solution(nodeinfo):  # def는 함수 정의. 0번 원소가 1번 노드인 좌표 목록을 받음.
#     n = len(nodeinfo)  # len은 노드 수.
#     left, right = [-1] * n, [-1] * n  # []는 리스트, *는 반복. 노드별 왼쪽·오른쪽 자식 인덱스. -1은 자식 없음.
#     order = sorted(range(n), key=lambda i: nodeinfo[i][0])  # sorted는 정렬, key는 비교 기준, lambda는 짧은 익명 함수. x좌표 순으로 노드 번호 정렬.
#     stack = []  # y가 큰 조상부터 작은 자손까지 담는 단조 스택. 마지막에 넣은 노드를 먼저 꺼냄.
#     for node in order:  # x가 작은 노드부터 트리에 추가.
#         last = -1  # 새 노드의 왼쪽 자식이 될 이전 부분 트리.
#         while stack and nodeinfo[stack[-1]][1] < nodeinfo[node][1]:  # and는 모두 참, [-1]은 마지막 원소. 새 노드보다 낮은 y의 노드는 조상이 될 수 없음.
#             last = stack.pop()  # pop은 마지막 원소를 꺼내 삭제. 제거한 부분 트리를 새 노드 아래로 옮길 준비.
#         if stack:  # 더 높은 조상이 남아 있으면 참.
#             right[stack[-1]] = node  # 새 노드를 남아 있는 조상의 오른쪽 자식으로 연결.
#         if last != -1:  # !=는 다름. 아래로 옮길 부분 트리가 있는지 확인.
#             left[node] = last  # x는 더 작으므로 새 노드의 왼쪽 자식으로 연결.
#         stack.append(node)  # append는 끝에 추가. 새 노드를 오른쪽 경로의 마지막 노드로 저장.
#     root = stack[0]  # 가장 높은 y를 가진 전체 트리의 루트.
#     preorder, postorder = [], []  # 전위·후위 방문 결과를 저장하는 리스트.
#     stack = [(root, False)]  # ()는 튜플. (노드,자식 처리 후인지) 상태로 재귀를 스택으로 대신함.
#     while stack:  # 처리할 방문 상태가 남아 있는 동안 반복.
#         node, finished = stack.pop()  # 상태를 꺼내 언패킹.
#         if finished:  # True이면 두 자식을 모두 처리한 뒤 다시 만난 상태.
#             postorder.append(node + 1)  # 후위 순회는 왼쪽→오른쪽→현재. 반환 노드 번호는 1부터이므로 +1.
#         else:  # 노드를 처음 방문한 상태.
#             preorder.append(node + 1)  # 전위 순회는 현재→왼쪽→오른쪽이므로 즉시 기록.
#             stack.append((node, True))  # 현재 노드의 후위 기록은 자식 처리 뒤로 미룸.
#             if right[node] != -1:  # 오른쪽 자식이 있을 때.
#                 stack.append((right[node], False))  # 스택은 나중에 넣은 것이 먼저 나오므로 오른쪽을 먼저 넣음.
#             if left[node] != -1:  # 왼쪽 자식이 있을 때.
#                 stack.append((left[node], False))  # 왼쪽을 마지막에 넣어 먼저 방문하게 함.
#     return [preorder, postorder]  # 두 순회 결과를 2차원 리스트로 반환.

# 풀이 요약
# x좌표는 이진 탐색 트리의 순서, y좌표는 부모가 더 높은 우선순위다. x순으로 읽으며 낮은 노드를 스택에서 꺼내 새 노드 아래에 붙인다.
# 전위는 나→왼쪽→오른쪽, 후위는 왼쪽→오른쪽→나. 방문 완료 표시를 스택에 다시 넣어 두 순회를 함께 만든다.
# 예제 루트는 7번이고 전위 첫 값·후위 마지막 값도 7이다. 정렬 포함 시간 O(N log N), 공간 O(N).
# 