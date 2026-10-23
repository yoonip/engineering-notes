def solution(edges, target):
    n = len(target)
    children = [[] for _ in range(n)]  # 리스트 내포로 각 노드의 독립적인 자식 목록 생성.
    for parent, child in edges:  # for는 순회. 간선의 부모·자식 번호를 두 변수로 나눠 받음.
        children[parent - 1].append(child - 1)  # 번호를 0부터 시작하도록 변환. append는 자식 목록 끝에 추가.
    for branch in children:  # 모든 자식 목록을 순회.
        branch.sort()  # sort()는 리스트 자체를 오름차순 정렬. 번호가 작은 자식부터 길을 설정.
    pointers = [0] * n  # 각 노드에서 다음 공이 지나갈 자식의 인덱스를 0으로 초기화.
    counts = [0] * n  # 각 리프에 도착한 공 개수를 저장할 리스트.
    unmet = sum(value > 0 for value in target)  # 제너레이터 표현식과 sum으로 아직 목표를 만들 수 없는 리프 수 계산.
    order = []  # []는 빈 리스트. 공이 도착한 리프 순서 저장.
    while unmet:  # while은 조건이 참인 동안 반복. 모든 목표가 가능한 첫 시점까지 공을 보냄.
        node = 0  # 각 공은 0번 인덱스인 루트에서 출발.
        while children[node]:  # 자식 목록이 비어 있지 않은 동안 아래로 이동.
            index = pointers[node]  # 현재 길이 가리키는 자식의 위치를 저장.
            pointers[node] = (index + 1) % len(children[node])  # %는 나머지. 다음 자식으로 바꾸고 마지막 다음에는 처음으로 순환.
            node = children[node][index]  # 기존 길을 따라 자식 노드로 이동.
        counts[node] += 1
        order.append(node)  # 공의 값과 무관하게 정해지는 도착 순서를 기록.
        if counts[node] > target[node]:
            return [-1]
        if 3 * (counts[node] - 1) < target[node] <= 3 * counts[node]:  # 연속 비교. 이번 공으로 처음 최대 가능 합이 목표에 도달했는지 검사.
            unmet -= 1  # -=는 뺀 값 저장. 목표를 만들 수 있게 된 리프 수를 반영.
    remaining = target[:]  # [:]는 리스트 전체의 얕은 복사. 원본을 바꾸지 않고 남은 목표 합 관리.
    answer = []  # 실제로 떨어트릴 숫자 목록 초기화.
    for node in order:  # 저장한 리프 도착 순서를 그대로 순회.
        counts[node] -= 1  # 이번 공을 제외한 남은 공 개수로 갱신.
        value = max(1, remaining[node] - 3 * counts[node])  # max는 큰 값 반환. 뒤의 공을 모두 3으로 채울 수 있는 범위에서 지금 값을 최소화.
        answer.append(value)  # 선택한 1·2·3을 정답 목록에 추가.
        remaining[node] -= value  # 해당 리프의 남은 목표 합에서 선택한 값을 뺌.
    return answer  # 가장 짧고 그중 사전순으로 가장 작은 숫자 목록 반환.
