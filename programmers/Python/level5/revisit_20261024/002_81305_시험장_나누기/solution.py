def solution(k, num, links):
    n = len(num)
    has_parent = bytearray(n)
    for children in links:
        for child in children:
            if child != -1:
                has_parent[child] = 1
    root = has_parent.index(0)
    order = [root]
    for node in order:
        for child in links[node]:
            if child != -1:
                order.append(child)
    order.reverse()
    low = max(max(num), (sum(num) + k - 1) // k)
    high = sum(num)
    remaining = [0] * n
    while low < high:
        limit = (low + high) // 2
        groups = 1
        for node in order:
            left, right = links[node]
            a = remaining[left] if left != -1 else 0
            b = remaining[right] if right != -1 else 0
            if a > b:
                a, b = b, a
            people = num[node]
            if people + a + b <= limit:
                remaining[node] = people + a + b
            elif people + a <= limit:
                remaining[node] = people + a
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
# def solution(k, num, links):  # 트리를 k개 그룹으로 나눴을 때 최대 인원의 최솟값 반환
#     n = len(num)  # 정점 수
#     has_parent = bytearray(n)  # 부모가 있는 정점을 바이트 하나씩 표시
#     for children in links:  # 각 정점의 자식 목록 확인
#         for child in children:  # 왼쪽과 오른쪽 자식 순회
#             if child != -1:  # 실제 자식이 있는 경우
#                 has_parent[child] = 1  # 이 정점은 루트가 아님
#     root = has_parent.index(0)  # 부모가 없는 유일한 정점이 루트
#     order = [root]  # 부모가 자식보다 먼저 오는 순서 준비
#     for node in order:  # 뒤에 자식을 붙이면서 전체 트리 순회
#         for child in links[node]:  # 두 자식을 순서 배열에 추가
#             if child != -1:  # 없는 자식은 제외
#                 order.append(child)  # 자식은 부모 뒤에 위치
#     order.reverse()  # 뒤집어서 자식부터 계산할 순서로 변경
#     low = max(max(num), (sum(num) + k - 1) // k)  # 한 정점 인원과 평균 그룹 인원보다 작은 상한은 불가능
#     high = sum(num)  # 모두 한 그룹으로 묶는 인원을 탐색 상한으로 설정
#     remaining = [0] * n  # 각 정점에서 부모와 이어질 열린 그룹 인원
#     while low < high:  # 가능한 최대 인원의 경계를 이분 탐색
#         limit = (low + high) // 2  # 이번에 시험할 그룹 인원 상한
#         groups = 1  # 간선을 자를 때마다 늘어날 그룹 수
#         for node in order:  # 자식의 열린 그룹을 먼저 계산한 순서로 처리
#             left, right = links[node]  # 현재 정점의 두 자식 번호
#             a = remaining[left] if left != -1 else 0  # 왼쪽 자식이 없으면 합칠 인원도 0
#             b = remaining[right] if right != -1 else 0  # 오른쪽 자식의 열린 그룹 인원
#             if a > b:  # 하나만 합칠 때 작은 쪽을 남기기 위한 순서
#                 a, b = b, a  # 두 인원을 작은 값부터 정렬
#             people = num[node]  # 현재 정점의 인원
#             if people + a + b <= limit:  # 두 자식 그룹을 모두 이어도 상한 이내
#                 remaining[node] = people + a + b  # 세 부분을 하나의 열린 그룹으로 합치기
#             elif people + a <= limit:  # 작은 자식 그룹 하나만 합칠 수 있는 경우
#                 remaining[node] = people + a  # 부모 쪽에 남길 인원을 작게 유지
#                 groups += 1  # 큰 자식과의 간선을 잘라 그룹 하나 확정
#             else:  # 두 자식 어느 쪽도 현재 정점과 합칠 수 없음
#                 remaining[node] = people  # 현재 정점만 부모 쪽에 남기기
#                 groups += 2  # 두 자식의 그룹을 각각 분리
#             if groups > k:  # 이미 필요한 그룹 수를 넘었으면 이후 계산은 불필요
#                 break  # 이번 상한 검사를 중단
#         if groups <= k:  # k개 이하로 만들 수 있으면 더 나눠 정확히 k개로도 만들 수 있음
#             high = limit  # 더 작은 상한이 가능한지 탐색
#         else:  # 상한이 작아 너무 많은 그룹이 필요
#             low = limit + 1  # 불가능한 상한 이하를 제외
#     return low  # 가능한 최대 그룹 인원의 최솟값

# 풀이 요약
# 인원 상한을 먼저 정하면 트리를 아래에서 위로 보며 필요한 그룹 수를 셀 수 있음.
# 둘 다 합칠 수 있으면 함께 남기고, 하나만 가능하면 작은 쪽을 남기기. 부모에 넘길 인원이 작을수록 위에서 합칠 여지가 많아짐.
# 이 상한으로 k개 이하가 나오면 충분히 더 잘라 k개로 맞출 수 있음. 가능한 상한의 경계를 이분 탐색.
# 트리 순회는 배열을 뒤집어 처리하므로 일자 트리에서도 재귀 깊이 문제 없음. 시간 O(N log(sum(num))), 공간 O(N).
