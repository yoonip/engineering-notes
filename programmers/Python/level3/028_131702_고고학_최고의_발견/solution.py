# 각 자리에서 0~3을 중복 선택하는 모든 조합 생성.
from itertools import product

# clockHands는 각 시계의 0~3 방향이 담긴 정사각형 격자.
def solution(clockHands):
    # len은 격자의 한 변 길이.
    n = len(clockHands)
    # 각 시계는 4번 돌리면 원래대로이므로 최솟값은 최대 3N² 이내.
    answer = 3 * n * n + 1
    # repeat=n으로 첫 행의 회전 횟수 4^n가지를 모두 생성.
    for first in product(range(4), repeat=n):
        # 격자 위쪽의 없는 행을 0회 회전으로 처리.
        previous = [0] * n
        # 현재 행의 각 시계 회전 횟수.
        current = list(first)
        # 첫 행에 사용한 전체 회전 수.
        cost = sum(current)
        # 위에서 아래로 각 행을 12시 방향으로 맞춤.
        for r in range(n):
            # 이미 찾은 답을 개선할 수 없으면 중단.
            if cost >= answer:
                break
            # %4는 0~3의 회전 수.
            needed = [(-clockHands[r][c] - previous[c] - current[c] - (current[c - 1] if c else 0) - (current[c + 1] if c + 1 < n else 0)) % 4 for c in range(n)]
            # 마지막 행 아래에는 더 돌릴 시계가 없음.
            if r == n - 1:
                # 모든 추가 필요 횟수가 0인지 확인.
                if not any(needed):
                    # 모든 행이 맞춰졌으므로 더 작은 비용을 정답으로 갱신.
                    answer = cost
                break
            # 강제로 결정된 다음 행 회전 수를 비용에 추가.
            cost += sum(needed)
            # 두 변수 동시 대입으로 한 행 아래로 진행.
            previous, current = current, needed
    # return으로 모든 첫 행 후보 중 최소 회전 수 반환.
    return answer
