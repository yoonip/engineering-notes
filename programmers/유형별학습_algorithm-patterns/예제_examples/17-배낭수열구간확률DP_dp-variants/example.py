import sys  # 두 입력 묶음의 정수 읽기
tokens = iter(map(int, sys.stdin.read().split()))  # 공백 토큰 순회
n, capacity = next(tokens), next(tokens)  # 배낭 조건
dp = [0] * (capacity + 1)  # 용량 이하의 최대 가치
for _ in range(n):  # 각 물건을 한 번씩 반영
    weight, value = next(tokens), next(tokens)  # 현재 물건 정보
    for w in range(capacity, weight - 1, -1):  # 내림차순으로 이전 물건 상태만 읽기
        dp[w] = max(dp[w], dp[w - weight] + value)  # 선택과 미선택 비교
m = next(tokens)  # 증가 부분 수열 입력 길이
sequence = [next(tokens) for _ in range(m)]  # 수열 원소 저장
length = [1] * m  # 각 위치에서 끝나는 LIS의 최소 길이
for i in range(m):  # 현재 끝 위치 확정
    for j in range(i):  # 그 앞에 붙일 끝 위치 확인
        if sequence[j] < sequence[i]:  # 같은 값은 엄격 증가에 포함하지 않기
            length[i] = max(length[i], length[j] + 1)  # 현재 원소를 이어 붙인 길이
print("KNAPSACK", dp[capacity])  # 배낭 결과
print("LIS", max(length, default=0))  # 빈 수열도 길이 0으로 처리
