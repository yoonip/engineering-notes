def solution(n, z, roads, queries):
    infinity = 10**9
    limit = (z - 1) ** 2
    by_gain = [[] for _ in range(z)]
    for start, end, gain in roads:
        by_gain[gain].append((start, end))
    groups = [(gain, edges) for gain, edges in enumerate(by_gain) if edges]
    rows = [[infinity] * n for _ in range(z)]
    rows[0][0] = 0
    loss = [infinity] * z
    small = [-1] * (limit + 1)
    for money in range(limit + 1):
        remainder = money % z
        row = rows[remainder]
        best = min(row)
        if best != infinity:
            deficit = z * best - money
            if deficit < loss[remainder]:
                loss[remainder] = deficit
            teleport = best + 1
            for gain, edges in groups:
                following = money + gain
                if following > limit:
                    continue
                target = rows[following % z]
                for start, end in edges:
                    before = row[start]
                    if before > teleport:
                        before = teleport
                    candidate = before + 1
                    if candidate < target[end]:
                        target[end] = candidate
        if loss[remainder] != infinity:
            small[money] = (money + loss[remainder]) // z
        rows[remainder] = [infinity] * n
    answer = []
    for money in queries:
        if money <= limit:
            answer.append(small[money])
        else:
            deficit = loss[money % z]
            answer.append(-1 if deficit == infinity else (money + deficit) // z)
    return answer

# 전체 코드 줄별 설명
# def solution(n, z, roads, queries):  # 도시 수·한 턴 최대 획득액·도로·목표 금액들을 받는 함수
#     infinity = 10**9  # 도달하지 못한 도시·금액 상태를 표시할 큰 턴 수
#     limit = (z - 1) ** 2  # 나머지별 최적 기본 경로의 획득액 상한
#     by_gain = [[] for _ in range(z)]  # 획득액별로 독립적인 도로 목록 생성
#     for start, end, gain in roads:  # 도로의 출발·도착·획득액을 나눠 받기
#         by_gain[gain].append((start, end))  # 같은 미래 금액 행을 갱신할 도로끼리 모으기
#     groups = [(gain, edges) for gain, edges in enumerate(by_gain) if edges]  # 실제 존재하는 획득액만 남겨 빈 반복 생략
#     rows = [[infinity] * n for _ in range(z)]  # 금액 나머지별로 도시 최소 턴을 저장할 z개의 순환 행
#     rows[0][0] = 0  # 0번 도시·0원에서 0턴으로 출발
#     loss = [infinity] * z  # 나머지마다 찾은 최소 손실 z×턴수−획득액
#     small = [-1] * (limit + 1)  # 기본 경로 상한 이하의 정확한 답; 불가능은 -1
#     for money in range(limit + 1):  # 기본 획득액을 0부터 상한까지 차례로 처리
#         remainder = money % z  # 현재 금액의 순환 행 번호
#         row = rows[remainder]  # 이 금액에서 각 도시에 도착한 최소 턴
#         best = min(row)  # 순간이동을 시작할 수 있는 가장 빠른 현재 상태
#         if best != infinity:  # 도로·순간이동만으로 이 기본 금액을 만들 수 있는 경우
#             deficit = z * best - money  # 같은 턴을 전부 z원 획득에 썼을 때와의 차이
#             if deficit < loss[remainder]:  # 같은 나머지의 더 효율적인 기본 경로를 찾은 경우
#                 loss[remainder] = deficit  # 이후 같은 나머지 쿼리에 쓸 최소 손실 갱신
#             teleport = best + 1  # 어느 도로 출발점으로든 순간이동 한 번이면 도착 가능
#             for gain, edges in groups:  # 획득액이 같은 도로끼리 미래 금액 행 재사용
#                 following = money + gain  # 도로 이동 뒤의 기본 획득액
#                 if following > limit:  # 필요한 기본 경로 상한을 넘어가는 경우
#                     continue  # 이 획득액의 도로는 이번 금액에서 처리하지 않음
#                 target = rows[following % z]  # 이번 도로들이 갱신할 미래 금액의 도시 행
#                 for start, end in edges:  # 같은 획득액의 일방통행 도로를 하나씩 확인
#                     before = row[start]  # 이미 도로 출발 도시에 와 있는 최소 턴
#                     if before > teleport:  # 다른 도시에서 순간이동하는 편이 더 빠른 경우
#                         before = teleport  # 현재 금액의 전역 최솟값+1을 출발 턴으로 사용
#                     candidate = before + 1  # 도로를 타는 한 턴을 추가
#                     if candidate < target[end]:  # 도착 도시의 더 빠른 경로를 찾은 경우
#                         target[end] = candidate  # 미래 금액·도시 상태의 최소 턴 갱신
#         if loss[remainder] != infinity:  # 현재 금액 이하의 같은 나머지 기본 경로가 있는 경우
#             small[money] = (money + loss[remainder]) // z  # 기본 경로 뒤에 필요한 z원 획득 턴을 붙인 정확한 답
#         rows[remainder] = [infinity] * n  # 처리한 행을 비워 z원 뒤의 금액이 재사용하도록 준비
#     answer = []  # 입력 쿼리 순서의 결과를 담을 리스트
#     for money in queries:  # 각 목표 금액에 전처리 결과로 응답
#         if money <= limit:  # 최적 기본 경로 금액이 목표보다 클 수 있는 작은 쿼리
#             answer.append(small[money])  # 해당 목표 이하 경로만 반영한 작은 답 사용
#         else:  # 모든 최적 기본 경로의 금액 이상인 큰 쿼리
#             deficit = loss[money % z]  # 목표 금액의 나머지에 맞는 최종 최소 손실
#             answer.append(-1 if deficit == infinity else (money + deficit) // z)  # 나머지가 불가능하면 -1, 아니면 기본 경로와 머무르기 턴 합
#     return answer  # 최소 턴 또는 -1을 담은 결과 반환

# 풀이 요약
# 손실을 z×턴수−획득액으로 두면 같은 목표 금액에서는 손실이 작을수록 빠름. 가만히 z원 얻기는 위치가 안 바뀌어 마지막에 몰아도 됨.
# 각 나머지의 최소 손실 경로 중 기본 획득액도 최소인 경로를 선택. 도로를 지난 직후의 나머지가 반복되면 그 사이를 순간이동 한 번으로 바꿀 수 있어 모순.
# 따라서 최적 기본 경로의 도로는 최대 z−1번, 획득액은 (z−1)^2 이하. 이 범위만 도시·금액 DP로 조사하면 큰 쿼리도 처리 가능.
# 현재 금액의 전역 최소 턴+1이 임의 도로 출발점까지의 순간이동 비용. 획득액별로 도로를 묶어 미래 금액 행을 재사용.
# 도로 획득액이 1..z−1이라 금액 행은 z개만 순환 저장. 같은 나머지의 최소 손실을 누적해 작은 쿼리에도 목표 이하의 경로만 반영.
# 큰 금액은 (목표+나머지별 최소 손실)//z. 작은 금액은 별도 답을 써서 최적 기본 경로보다 목표가 작은 경우를 처리.
# z50·도로49원인 경우 나머지1의 최적 기본 금액은2401원. 1원 같은 작은 쿼리는 불가능하므로 최종 손실만 무조건 적용하면 안 됨.
# 시간 O(z²(N+M)+Q), 공간 O(Nz+z²+M+Q). Python 정수로10^18원까지 계산.
