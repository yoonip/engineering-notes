def solution(arr):
    positions = [i for i, value in enumerate(arr) if value == 2]
    if not positions:
        return [-1]
    return arr[positions[0]:positions[-1] + 1]

# 전체 코드 줄별 설명
# def solution(arr):  # def는 함수 정의. 정수 리스트 입력.
#     positions = [i for i, value in enumerate(arr) if value == 2]  # [] 안의 for·if는 리스트 내포. enumerate로 위치를 받아 값이 2인 인덱스만 수집.
#     if not positions:  # not은 논리 부정. 빈 리스트인지 검사.
#         return [-1]  # 2가 없으면 -1 하나를 담은 리스트 반환.
#     return arr[positions[0]:positions[-1] + 1]  # 0은 첫 위치, -1은 마지막 위치. 처음 2부터 마지막 2까지 양 끝 포함 슬라이싱.

# 풀이 요약
# 모든 2를 포함하려면 첫 2에서 마지막 2까지의 구간이 필요합니다.
# 