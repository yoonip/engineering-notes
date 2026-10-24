def solution(heights):
    ordered = sorted(heights)
    n = len(ordered)
    half = n // 2
    smallest = second = float("inf")
    for left in range(n - half):
        gap = ordered[left + half] - ordered[left]
        if gap < smallest:
            second = smallest
            smallest = gap
        elif gap < second:
            second = gap
    return smallest if n % 2 == 0 else second

# 전체 코드 줄별 설명
# def solution(heights):  # 지점 순서를 바꿔 이웃 높이 차이의 최솟값을 최대화
#     ordered = sorted(heights)  # 높이를 오름차순으로 정렬한 새 리스트
#     n = len(ordered)  # 기둥 수
#     half = n // 2  # 정렬한 목록에서 절반 간격
#     smallest = second = float("inf")  # 가장 작은 간격과 두 번째 간격을 무한대로 초기화
#     for left in range(n - half):  # 절반 간격으로 마주 보는 모든 높이 쌍 확인
#         gap = ordered[left + half] - ordered[left]  # 두 높이의 차이
#         if gap < smallest:  # 지금까지의 최솟값보다 더 작은 차이
#             second = smallest  # 기존 최솟값이 두 번째 값으로 이동
#             smallest = gap  # 새 최솟값 저장
#         elif gap < second:  # 최솟값이 아니어도 두 번째 값이 될 수 있음
#             second = gap  # 같은 값도 별개 쌍이면 두 번째 후보로 포함
#     return smallest if n % 2 == 0 else second  # 짝수는 최소 간격, 홀수는 두 번째 간격이 한계

# 풀이 요약
# 정렬한 높이에서 절반 간격으로 떨어진 값들의 차이를 비교.
# 기둥이 2m개면 이 차이들의 최솟값이 가능한 최적값. 2m+1개면 절반을 가르는 경계가 한 번 더 겹쳐 두 번째로 작은 차이가 한계.
# 홀수일 때 차이가 같은 두 쌍도 따로 세야 함. 서로 다른 값만 남겨 두 번째를 찾으면 오답.
# 정렬 시간 O(N log N), 정렬 결과를 저장할 공간 O(N).
