import sys # 전체 정수 입력을 읽을 표준 모듈
data = list(map(int, sys.stdin.buffer.read().split())) # 공백 토큰을 정수로 변환
n, q = data[:2] # 원소 수와 질의 수 해체
values = data[2:2 + n] # 원래 값 배열 분리
queries = [tuple(data[2 + n + 2 * i:4 + n + 2 * i]) for i in range(q)] # 질의의 반열린 경계 묶기
direct = [] # 직접 합산 결과 목록
for left, right in queries: # 각 질의를 입력 순서대로 확인
    total = 0 # 이번 구간 합 초기화
    for index in range(left, right): # 대상 구간 인덱스 순회
        total += values[index] # 원소 하나씩 합산
    direct.append(total) # 직접 구한 합 저장
prefix = [0] # 빈 접두 구간의 합
for value in values: # 원소를 한 번씩만 읽기
    prefix.append(prefix[-1] + value) # 다음 접두 합 생성
fast = [prefix[right] - prefix[left] for left, right in queries] # 같은 질의를 두 접두 합 차이로 계산
print(*direct) # 직접 합산 결과를 첫 줄에 출력
print(*fast) # 누적합 결과를 둘째 줄에 출력
