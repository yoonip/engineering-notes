import sys  # 정수 토큰 읽기
tokens = iter(map(int, sys.stdin.read().split()))  # 표준 입력 순회
n, target = next(tokens), next(tokens)  # 물건 수와 목표
bits = 1  # 합 0만 가능한 초기 비트
limit = (1 << (target + 1)) - 1  # 목표 이하 마스크
for _ in range(n):  # 물건 한 개씩 처리
    weight = next(tokens)  # 현재 무게
    if weight <= target:  # 양수이므로 목표 초과 물건 제외
        bits = (bits | (bits << weight)) & limit  # 이전 상태에서 한 번만 이동
print("YES" if (bits >> target) & 1 else "NO")  # 목표 합의 비트 출력
