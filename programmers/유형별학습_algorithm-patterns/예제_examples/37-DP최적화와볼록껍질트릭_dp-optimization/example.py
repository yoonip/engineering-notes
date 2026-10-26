import sys  # 상태와 좌표 입력 읽기
tokens = iter(map(int, sys.stdin.read().split()))  # 공백 토큰 순회
n, cost = next(tokens), next(tokens)  # 전이 수와 상수 비용
x = [0] + [next(tokens) for _ in range(n)]  # 증가 좌표와 초기 x0
dp = [0] * (n + 1)  # 상태별 최적 비용
slope, intercept = [0] * (n + 1), [0] * (n + 1)  # 직선 계수
queue = [0] * (n + 1)  # 후보 덱의 배열 저장
head, tail = 0, 1  # 초기 직선0만 포함
def evaluate(line, coordinate):  # 한 직선의 현재 값
    return slope[line] * coordinate + intercept[line]  # 선형식 계산
def redundant(first, middle, last):  # 가운데 후보의 불필요성
    return (intercept[middle] - intercept[first]) * (slope[middle] - slope[last]) >= (intercept[last] - intercept[middle]) * (slope[first] - slope[middle])  # 감소 기울기의 교점 순서 비교
for i in range(1, n + 1):  # 증가하는 질의 좌표
    while tail - head >= 2 and evaluate(queue[head], x[i]) >= evaluate(queue[head + 1], x[i]):  # 뒤 직선이 더 낮은 경우
        head += 1  # 앞으로 불리한 앞 후보 제거
    dp[i] = x[i] * x[i] + cost + evaluate(queue[head], x[i])  # 직선 질의로 DP 전이
    slope[i] = -2 * x[i]  # 감소하는 새 기울기
    intercept[i] = dp[i] + x[i] * x[i]  # 새 상태의 절편
    while tail - head >= 2 and redundant(queue[tail - 2], queue[tail - 1], i):  # 아래 껍질에 필요 없는 후보
        tail -= 1  # 덱 뒤쪽에서 제거
    queue[tail] = i  # 새 직선 저장
    tail += 1  # 후보 범위 확장
print(dp[n])  # 마지막 상태의 최적값
