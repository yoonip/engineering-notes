def solution(arr, queries):
    for i, j in queries:
        arr[i], arr[j] = arr[j], arr[i]
    return arr

# 전체 코드 줄별 설명
# def solution(arr, queries):  # def는 함수 정의. 정수 리스트와 교환할 위치 쌍 리스트 입력.
#     for i, j in queries:  # for로 각 쿼리를 순회하고 두 인덱스를 나누어 받음.
#         arr[i], arr[j] = arr[j], arr[i]  # 다중 대입은 오른쪽 값을 먼저 읽어 두 위치의 원소를 안전하게 교환.
#     return arr  # 모든 교환을 마친 리스트 반환.

# 풀이 요약
# 각 인덱스 쌍의 값을 주어진 순서대로 맞바꿉니다.
# 