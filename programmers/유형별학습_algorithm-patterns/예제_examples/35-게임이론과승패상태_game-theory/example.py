import sys  # 게임 조건의 정수 입력
tokens = iter(map(int, sys.stdin.read().split()))  # 공백 토큰 순회
k, n = next(tokens), next(tokens)  # 이동 종류와 무더기 수
moves = [next(tokens) for _ in range(k)]  # 양의 허용 이동
piles = [next(tokens) for _ in range(n)]  # 각 독립 게임의 돌 수
maximum = max(piles, default=0)  # 계산할 마지막 상태
grundy = [0] * (maximum + 1)  # 종료 상태 G[0]=0
for stones in range(1, maximum + 1):  # 의존 상태가 먼저 정해지는 순서
    seen = {grundy[stones - step] for step in moves if step <= stones}  # 다음 상태의 그런디 값
    mex = 0  # 없는 최소값 탐색 시작
    while mex in seen:  # 도달 가능한 값은 제외
        mex += 1  # 다음 후보
    grundy[stones] = mex  # 현재 게임의 값
combined = 0  # 독립 합
values = [grundy[stones] for stones in piles]  # 출력할 무더기별 값
for value in values:  # 독립 게임 결합
    combined ^= value  # XOR 누적
print("GRUNDY", *values)  # 빈 목록도 후행 공백 없이 출력
print("XOR", combined)  # 합성한 그런디 값
print("WIN" if combined else "LOSE")  # 현재 차례의 승패
