# 원형으로 연결된 스티커 값 목록을 받음.
def solution(sticker):
    # len은 스티커 수.
    n = len(sticker)
    # 하나뿐인 경우 원형 분할 없이 그 스티커 선택.
    if n == 1:
        # []로 첫 원소 반환.
        return sticker[0]
    # [start,end) 범위를 일직선으로 보고 인접하지 않은 값들의 최대 합을 계산하는 내부 함수.
    def linear(start, end):
        # 현재 칸보다 두 칸 전·한 칸 전까지의 최대 합을 저장하는 동적 계획법(DP) 상태.
        two_before, one_before = 0, 0
        # 왼쪽부터 한 칸씩 처리.
        for i in range(start, end):
            # 현재 칸을 안 고르는 값과 두 칸 전 합+현재 값을 max로 비교.
            two_before, one_before = one_before, max(one_before, two_before + sticker[i])
        # 해당 일직선 범위의 최적 합 반환.
        return one_before
    # 첫 칸과 마지막 칸은 이웃이므로 마지막 제외·첫 칸 제외 두 경우 중 큰 값 선택.
    return max(linear(0, n - 1), linear(1, n))
