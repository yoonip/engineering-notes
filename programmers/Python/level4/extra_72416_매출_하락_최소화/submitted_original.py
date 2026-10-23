def solution(sales, links):
    n = len(sales)
    children = [[] for _ in range(n)]
    for leader, member in links:
        children[leader - 1].append(member - 1)
    order = [0]
    for node in order:
        order.extend(children[node])
    attend = sales[:]
    absent = [0] * n
    for node in reversed(order):
        if not children[node]:
            continue
        total = 0
        extra = 10**18
        for child in children[node]:
            best = min(attend[child], absent[child])
            total += best
            extra = min(extra, attend[child] - best)
        attend[node] += total
        absent[node] = total + extra
    return min(attend[0], absent[0])

# 전체 코드 줄별 설명
# def solution(sales, links):  # def는 함수 정의. 직원별 매출과 팀장·팀원 관계를 입력받음.
#     n = len(sales)  # len은 길이. 직원 수를 구함.
#     children = [[] for _ in range(n)]  # 리스트 내포로 직원별 독립적인 직속 팀원 목록 생성.
#     for leader, member in links:  # for로 팀장 번호와 팀원 번호를 순회.
#         children[leader - 1].append(member - 1)  # 1부터 시작하는 번호를 인덱스로 변환. append는 목록 끝에 추가.
#     order = [0]  # 루트인 CEO부터 순회할 노드 목록 초기화.
#     for node in order:  # 리스트 순회 중 뒤에 추가된 노드도 차례대로 처리.
#         order.extend(children[node])  # extend는 여러 원소 추가. 부모보다 뒤에 자식을 배치.
#     attend = sales[:]  # [:]는 리스트 복사. attend[i]는 i가 참석할 때 그 하위 조직의 최소 손실.
#     absent = [0] * n  # absent[i]는 i가 불참할 때의 최소 손실. 말단 직원의 불참 비용은 0.
#     for node in reversed(order):  # reversed는 역순 순회. 자식 DP를 먼저 계산한 뒤 부모 계산.
#         if not children[node]:  # not은 부정. 자식이 없는 말단 직원이면 실행.
#             continue  # continue는 이번 반복을 건너뜀. 말단은 팀장이 아니므로 추가 참석 조건 없음.
#         total = 0  # 자식 하위 조직의 최소 비용 합계 초기화.
#         extra = 10**18  # **는 거듭제곱. 직속 팀원 한 명을 참석시키는 최소 추가 비용 초기화.
#         for child in children[node]:  # 직속 팀원을 하나씩 검사.
#             best = min(attend[child], absent[child])  # min은 작은 값 반환. 자식의 참석·불참 중 저렴한 선택.
#             total += best  # +=는 더한 값 저장. 각 자식 하위 조직의 최소 손실 합산.
#             extra = min(extra, attend[child] - best)  # 불참하던 자식을 참석으로 바꿀 최소 추가 비용. 이미 참석 선택 가능하면 0.
#         attend[node] += total  # 현재 직원이 참석하면 자기 팀 조건은 충족되므로 자식은 자유롭게 최소 선택.
#         absent[node] = total + extra  # 현재 팀장이 불참하면 직속 팀원 중 최소 한 명은 참석해야 함.
#     return min(attend[0], absent[0])  # CEO의 참석·불참 중 전체 손실이 작은 값 반환.

# 풀이 요약
# 각 직원의 참석·불참 두 상태를 트리 DP로 계산합니다. 팀장이 불참할 때만 직속 팀원 한 명의 참석을 강제합니다.
# 예: 팀장 손실 5, 말단 팀원 손실 3이면 팀원만 참석해 손실 3으로 조건을 충족합니다.
# 반복문으로 자식부터 계산하므로 깊이 30만 트리도 재귀 제한 없이 처리합니다. 시간·공간 O(직원 수).
# 