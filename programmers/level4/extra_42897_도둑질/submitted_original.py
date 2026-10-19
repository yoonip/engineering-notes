def solution(money):
    n = len(money)
    def best(start, end):
        previous, current = 0, 0
        for index in range(start, end):
            previous, current = current, max(current, previous + money[index])
        return current
    return max(best(0, n - 1), best(1, n))

# 전체 코드 줄별 설명
# def solution(money):  # def는 함수 정의. 원형으로 놓인 집들의 돈 액수를 입력받음.
#     n = len(money)  # len은 길이. 집 개수 계산.
#     def best(start, end):  # 지정한 일자 구간에서 인접한 집을 피하는 최댓값을 구하는 내부 함수.
#         previous, current = 0, 0  # 이전 두 단계의 DP 값 초기화. 아직 집을 선택하지 않았으므로 0.
#         for index in range(start, end):  # range는 start부터 end 직전까지 순회. 끝 인덱스는 포함하지 않음.
#             previous, current = current, max(current, previous + money[index])  # 동시 대입은 오른쪽을 먼저 계산. 현재 집을 건너뛰거나 두 집 전 최댓값에 현재 돈을 더함.
#         return current  # return으로 일자 구간의 최대 금액 반환.
#     return max(best(0, n - 1), best(1, n))  # max는 큰 값 반환. 마지막 집 제외·첫 집 제외 두 경우를 비교하여 원형 인접 충돌 방지.

# 풀이 요약
# 첫 집과 마지막 집을 동시에 털 수 없으므로 둘 중 하나를 제외한 두 일자 구간으로 나눕니다.
# 일자 구간에서는 현재 집을 털면 직전 집을 건너뛰고, 털지 않으면 직전까지 최댓값을 유지합니다. 예: [1,2,3,1]의 답은 1+3=4.
# 시간 O(n), 추가 공간 O(1). 백만 집도 DP 배열 전체를 저장하지 않습니다.
# 