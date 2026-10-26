import sys # 정수 토큰 입력
data = list(map(int, sys.stdin.buffer.read().split())) # 입력을 정수로 변환
n, limit = data[:2] # 작업 수와 허용 그룹 수
values = data[2:] # 순서를 유지할 작업량 배열
def feasible(capacity): # 정해진 용량의 가능 여부 판정
    groups, current = 1, 0 # 첫 그룹과 현재 그룹 합
    for value in values: # 작업을 원래 순서대로 배치
        if value > capacity: # 단일 작업도 담기지 않는 경우
            return False # 이 용량은 불가능
        if current + value > capacity: # 현재 그룹에 추가하면 용량 초과
            groups += 1 # 새 연속 그룹 열기
            current = value # 새 그룹에 이번 작업 배치
        else: # 현재 그룹에 여유가 있는 경우
            current += value # 이번 작업량 누적
    return groups <= limit # 허용 그룹 수 이내인지 반환
low, high = max(values), sum(values) # 가장 큰 작업과 전체 합을 탐색 경계로 설정
while low < high: # 최소 가능한 용량이 하나 남을 때까지 반복
    middle = low + (high - low) // 2 # 정수 중간 용량
    if feasible(middle): # 해당 용량으로 작업을 나눌 수 있는 경우
        high = middle # 더 작은 정답 가능성 유지
    else: # 그룹 수 제한을 넘는 경우
        low = middle + 1 # 불가능한 용량을 제외
print(low) # 최소 가능한 용량 출력
