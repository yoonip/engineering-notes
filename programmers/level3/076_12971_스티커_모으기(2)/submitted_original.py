def solution(sticker):
    n = len(sticker)
    if n == 1:
        return sticker[0]
    def linear(start, end):
        two_before, one_before = 0, 0
        for i in range(start, end):
            two_before, one_before = one_before, max(one_before, two_before + sticker[i])
        return one_before
    return max(linear(0, n - 1), linear(1, n))

# 전체 코드 줄별 설명
# def solution(sticker):  # def는 함수 정의. 원형으로 연결된 스티커 값 목록을 받음.
#     n = len(sticker)  # len은 스티커 수.
#     if n == 1:  # ==는 같음. 하나뿐인 경우 원형 분할 없이 그 스티커 선택.
#         return sticker[0]  # []로 첫 원소 반환.
#     def linear(start, end):  # [start,end) 범위를 일직선으로 보고 인접하지 않은 값들의 최대 합을 계산하는 내부 함수.
#         two_before, one_before = 0, 0  # 현재 칸보다 두 칸 전·한 칸 전까지의 최대 합을 저장하는 동적 계획법(DP) 상태.
#         for i in range(start, end):  # range는 end 제외. 왼쪽부터 한 칸씩 처리.
#             two_before, one_before = one_before, max(one_before, two_before + sticker[i])  # 언패킹 대입은 오른쪽을 먼저 계산. 현재 칸을 안 고르는 값과 두 칸 전 합+현재 값을 max로 비교.
#         return one_before  # 해당 일직선 범위의 최적 합 반환.
#     return max(linear(0, n - 1), linear(1, n))  # 첫 칸과 마지막 칸은 이웃이므로 마지막 제외·첫 칸 제외 두 경우 중 큰 값 선택.

# 풀이 요약
# 일직선에서는 dp[i]=max(dp[i-1],dp[i-2]+현재 값)이다. 원형에서는 첫 칸·마지막 칸 중 적어도 하나를 빼야 하므로 두 일직선 문제로 나눈다.
# 예제 1은 첫 칸을 제외하고 6+11+9+10=36을 고른다. 두 경우 모두 첫 칸·마지막 칸을 선택하지 않는 경우도 자연스럽게 포함된다.
# 각 DP에서 이전 값 두 개만 필요하다. 시간 O(N), 추가 공간 O(1).
# 