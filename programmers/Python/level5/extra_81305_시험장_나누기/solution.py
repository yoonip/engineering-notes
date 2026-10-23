def solution(k, num, links):
    n = len(num)
    has_parent = [False] * n
    for left, right in links:
        if left != -1:
            has_parent[left] = True
        if right != -1:
            has_parent[right] = True
    root = has_parent.index(False)
    stack = [root]
    order = []
    while stack:
        node = stack.pop()
        order.append(node)
        for child in links[node]:
            if child != -1:
                stack.append(child)
    order.reverse()
    total = sum(num)
    low = max(max(num), (total + k - 1) // k)
    high = total
    while low < high:
        limit = (low + high) // 2
        remaining = [0] * n
        groups = 1
        for node in order:
            left, right = links[node]
            a = remaining[left] if left != -1 else 0
            b = remaining[right] if right != -1 else 0
            people = num[node]
            if people + a + b <= limit:
                remaining[node] = people + a + b
            elif people + min(a, b) <= limit:
                remaining[node] = people + min(a, b)
                groups += 1
            else:
                remaining[node] = people
                groups += 2
            if groups > k:
                break
        if groups <= k:
            high = limit
        else:
            low = limit + 1
    return low

# 전체 코드 줄별 설명
# def solution(k, num, links):  # def는 함수 정의. k는 그룹 수, num은 인원 리스트, links는 왼쪽·오른쪽 자식 번호 리스트.
#     n = len(num)  # len은 길이. 시험장 개수 저장.
#     has_parent = [False] * n  # []는 리스트. False를 n개 만들어 부모가 있는지 기록.
#     for left, right in links:  # for는 반복. 각 행의 두 자식 번호를 left, right로 나누어 받음.
#         if left != -1:  # if는 조건문, !=는 다름 비교. 왼쪽 자식이 있을 때만 처리.
#             has_parent[left] = True  # []는 인덱스 접근. 해당 자식에게 부모가 있음을 기록.
#         if right != -1:  # 오른쪽 자식이 있는지 검사. -1은 자식 없음을 의미.
#             has_parent[right] = True  # 오른쪽 자식의 부모 존재 표시.
#     root = has_parent.index(False)  # index(값)는 처음 나오는 위치 반환. 부모가 없는 유일한 노드가 루트.
#     stack = [root]  # 스택은 나중에 넣은 값을 먼저 꺼내는 자료구조. 방문할 노드를 리스트에 저장.
#     order = []  # 부모를 자식보다 먼저 기록할 방문 순서 리스트.
#     while stack:  # while은 조건이 참인 동안 반복. 리스트에 노드가 남아 있으면 계속.
#         node = stack.pop()  # pop()은 리스트 마지막 원소를 제거해 반환. 재귀 없이 DFS로 방문.
#         order.append(node)  # append는 리스트 끝에 추가. 현재 노드 기록.
#         for child in links[node]:  # 현재 노드의 두 자식 번호 순회.
#             if child != -1:  # 실제로 존재하는 자식만 방문 대상으로 선택.
#                 stack.append(child)  # 스택 끝에 자식을 넣어 나중에 방문.
#     order.reverse()  # reverse는 리스트 순서를 제자리에서 반전. 자식부터 부모로 계산하는 후위 순서 생성.
#     total = sum(num)  # sum은 원소 합계. 전체 응시자 수 계산.
#     low = max(max(num), (total + k - 1) // k)  # max는 최댓값, //는 정수 나눗셈. 가장 큰 시험장과 전체 평균 올림이 답의 하한.
#     high = total  # 모든 시험장을 한 그룹으로 두는 인원 합이 답의 상한.
#     while low < high:  # 가능한 답 구간이 한 값으로 좁혀질 때까지 이진 탐색.
#         limit = (low + high) // 2  # 양 끝의 중간 정수를 이번 그룹 인원 제한으로 선택.
#         remaining = [0] * n  # 각 서브트리에서 부모에게 이어 붙일 열린 그룹의 인원을 저장.
#         groups = 1  # 최초 하나의 그룹에서 시작. 간선을 하나 끊을 때마다 그룹 수 증가.
#         for node in order:  # 자식 결과가 먼저 준비되는 후위 순서로 계산.
#             left, right = links[node]  # 현재 시험장의 두 자식 번호 조회.
#             a = remaining[left] if left != -1 else 0  # 조건 표현식. 왼쪽 자식이 없으면 인원 0으로 처리.
#             b = remaining[right] if right != -1 else 0  # 오른쪽 자식의 열린 그룹 인원, 없으면 0.
#             people = num[node]  # 현재 시험장 자체의 응시자 수.
#             if people + a + b <= limit:  # <=는 이하 비교. 두 자식을 모두 이어도 제한 이내인지 검사.
#                 remaining[node] = people + a + b  # 간선을 끊지 않고 두 자식을 모두 현재 그룹에 포함.
#             elif people + min(a, b) <= limit:  # elif는 다음 조건. min은 작은 값. 더 작은 자식 그룹 하나를 붙일 수 있는지 검사.
#                 remaining[node] = people + min(a, b)  # 부모에 전달할 그룹을 작게 유지하도록 작은 자식만 포함하는 그리디 선택.
#                 groups += 1  # +=는 더해 저장. 큰 자식 쪽 간선을 끊어 독립 그룹 하나 추가.
#             else:  # 어느 자식도 붙일 수 없는 경우.
#                 remaining[node] = people  # 현재 시험장만 부모에게 전달할 그룹에 남김.
#                 groups += 2  # 두 자식 간선을 모두 끊어 독립 그룹 두 개 추가.
#             if groups > k:  # 이미 필요한 그룹 수를 초과했다면 이 제한은 불가능.
#                 break  # break는 가장 가까운 반복문 종료. 불필요한 나머지 노드 계산 생략.
#         if groups <= k:  # 제한 이내에서 k개 이하 그룹으로 분할 가능. 더 잘게 잘라 정확히 k개로 만들 수도 있음.
#             high = limit  # 가능한 인원 제한을 더 낮춰 최솟값 탐색.
#         else:  # 그룹 수 초과로 현재 인원 제한이 너무 작은 경우.
#             low = limit + 1  # 불가능한 중간값 이하를 버리고 더 큰 제한 탐색.
#     return low  # return은 결과 반환. 가능한 최소의 최대 그룹 인원.

# 풀이 요약
# 최대 그룹 인원을 이진 탐색하고, 각 후보가 가능한지 자식부터 부모로 계산합니다.
# 둘 다 붙이기 → 작은 쪽만 붙이기 → 둘 다 끊기 순서로 판단하면 필요한 그룹 수가 최소가 됩니다.
# 명시적 스택으로 깊은 트리의 재귀 한도를 피합니다. 예제 답은 40, 27, 14, 9이며 시간 O(N log(전체 인원)), 공간 O(N)입니다.
# 