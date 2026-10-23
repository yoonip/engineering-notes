def solution(arr, idx):
    for i in range(idx, len(arr)):
        if arr[i] == 1:
            return i
    return -1

# 전체 코드 줄별 설명
# def solution(arr, idx):  # def는 함수 정의. 0·1 리스트와 탐색 시작 위치 입력.
#     for i in range(idx, len(arr)):  # len은 길이, range는 idx부터 마지막 인덱스까지 순회.
#         if arr[i] == 1:  # if는 조건, []는 인덱스 접근, ==는 값 같음 비교.
#             return i  # 처음 찾은 1의 위치를 반환하며 함수 종료.
#     return -1  # 조건에 맞는 위치가 없으면 -1 반환.

# 풀이 요약
# 시작 인덱스부터 오른쪽으로 탐색해 처음 만나는 1의 위치를 반환합니다.
# 