def solution(land, P, Q):
    heights = sorted(height for row in land for height in row)
    count = len(heights)
    index = count * Q // (P + Q)
    target = heights[index]
    answer = 0
    for height in heights:
        if height < target:
            answer += (target - height) * P
        else:
            answer += (height - target) * Q
    return answer

# 전체 코드 줄별 설명
# def solution(land, P, Q):  # def는 함수 정의. 격자 높이와 블록 추가 비용 P·제거 비용 Q를 입력받음.
#     heights = sorted(height for row in land for height in row)  # 중첩 제너레이터로 2차원 높이를 펼치고 sorted로 새 오름차순 리스트 생성.
#     count = len(heights)  # len은 길이. 전체 칸 수 계산.
#     index = count * Q // (P + Q)  # //는 정수 나눗셈. 높이를 올릴 때 추가 비용과 제거 비용이 균형을 이루는 순위 선택.
#     target = heights[index]  # []는 인덱스 접근. 가중 중앙값에 해당하는 목표 높이 선택.
#     answer = 0  # 전체 지형 편집 비용 초기화.
#     for height in heights:  # for로 각 칸의 현재 높이를 순회.
#         if height < target:  # if는 조건문. 목표보다 낮은 칸인지 검사.
#             answer += (target - height) * P  # +=는 더한 값 저장. 부족한 블록 수×추가 단가 합산.
#         else:  # else는 목표 이상인 칸에 실행.
#             answer += (height - target) * Q  # 초과 블록 수×제거 단가 합산. 같은 높이면 비용 0.
#     return answer  # return으로 모든 칸을 같은 높이로 만드는 최소 비용 반환.

# 풀이 요약
# 목표 높이를 1 올리면 낮은 칸 수×P만큼 비용이 늘고 높은 칸 수×Q만큼 줄어듭니다. 정렬 순위가 전체 칸 수×Q/(P+Q)를 넘는 지점에서 감소가 증가로 바뀝니다.
# 따라서 해당 순위의 높이 하나만 계산하면 됩니다. 예: [[1,2],[2,3]], P=3,Q=2의 목표는 2이고 비용은 5.
# 칸 수 V에 대해 시간 O(V*log V), 공간 O(V).
# 