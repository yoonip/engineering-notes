import sys  # 작은 그래프 입력 읽기
tokens = iter(map(int, sys.stdin.read().split()))  # 정수 토큰 순회
n, m = next(tokens), next(tokens)  # 정점과 간선 수
edges = [(next(tokens), next(tokens)) for _ in range(m)]  # 무방향 간선
partitions = 1 << n  # 각 정점의 두 배치를 조합
total, best = 0, 0  # 평균의 분자와 전수 최적값
for mask in range(partitions):  # 모든 이진 분할
    score = 0  # 현재 점수
    for first, second in edges:  # 간선의 양끝 집합 비교
        if (mask >> first) & 1 != (mask >> second) & 1:  # 양끝의 비트가 다른 경우
            score += 1  # 절단 간선 증가
    total += score  # 균등 평균용 합계
    best = max(best, score)  # 실제 최적값
expectation = total / partitions  # 모든 분할의 확률 평균
print(f"EXPECTED {expectation:.6f}")  # 소수점6자리 고정
print("BEST", best)  # 기대값과 구별한 최적값
