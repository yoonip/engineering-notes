# 각 유형에 적어도 한 명씩 배정하는 모든 분배를 탐색합니다. 대기시간은 작은 배열의 최솟값으로 계산합니다. 기본 DP보다
# 느리지만 분배 누락을 확인하기 쉽습니다.
# 작은 입력의 비교·검증용입니다. 원래 최대 입력 제출에는 기본 풀이를 사용합니다.
def solution(k, n, reqs):
    groups = [[] for _ in range(k)]
    for start, duration, kind in reqs:
        groups[kind-1].append((start, duration))
    def wait(kind, staff):
        free = [0]*staff
        total = 0
        for start, duration in groups[kind]:
            person = min(range(staff), key=free.__getitem__)
            begin = max(start, free[person])
            total += begin-start
            free[person] = begin+duration
        return total
    def allocate(kind, remaining):
        if kind == k-1:
            return wait(kind, remaining)
        return min(wait(kind, staff)+allocate(kind+1, remaining-staff)
                   for staff in range(1, remaining-(k-kind-1)+1))
    return allocate(0,n)
