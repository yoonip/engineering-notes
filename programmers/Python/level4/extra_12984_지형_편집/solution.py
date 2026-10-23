def solution(land, P, Q):
    heights = sorted(height for row in land for height in row)  # 중첩 제너레이터로 2차원 높이를 펼치고 sorted로 새 오름차순 리스트 생성.
    count = len(heights)
    index = count * Q // (P + Q)  # //는 정수 나눗셈. 높이를 올릴 때 추가 비용과 제거 비용이 균형을 이루는 순위 선택.
    target = heights[index]  # []는 인덱스 접근. 가중 중앙값에 해당하는 목표 높이 선택.
    answer = 0  # 전체 지형 편집 비용 초기화.
    for height in heights:
        if height < target:
            answer += (target - height) * P
        else:  # else는 목표 이상인 칸에 실행.
            answer += (height - target) * Q  # 초과 블록 수×제거 단가 합산. 같은 높이면 비용 0.
    return answer  # return으로 모든 칸을 같은 높이로 만드는 최소 비용 반환.
