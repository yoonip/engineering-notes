def solution(money):
    n = len(money)
    def best(start, end):  # 지정한 일자 구간에서 인접한 집을 피하는 최댓값을 구하는 내부 함수.
        previous, current = 0, 0  # 이전 두 단계의 DP 값 초기화. 아직 집을 선택하지 않았으므로 0.
        for index in range(start, end):
            previous, current = current, max(current, previous + money[index])  # 동시 대입은 오른쪽을 먼저 계산. 현재 집을 건너뛰거나 두 집 전 최댓값에 현재 돈을 더함.
        return current  # return으로 일자 구간의 최대 금액 반환.
    return max(best(0, n - 1), best(1, n))  # max는 큰 값 반환. 마지막 집 제외·첫 집 제외 두 경우를 비교하여 원형 인접 충돌 방지.
