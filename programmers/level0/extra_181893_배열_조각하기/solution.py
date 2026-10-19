def solution(arr, query):
    for i, cut in enumerate(query):
        arr = arr[:cut + 1] if i % 2 == 0 else arr[cut:]
    return arr

# 전체 코드 줄별 설명
# def solution(arr, query):  # def는 함수 정의. 원본 리스트와 자를 위치 쿼리 입력.
#     for i, cut in enumerate(query):  # enumerate는 쿼리 순서와 자를 위치를 함께 제공.
#         arr = arr[:cut + 1] if i % 2 == 0 else arr[cut:]  # %는 나머지. 짝수 순서는 뒤를 버리고, 홀수 순서는 앞을 버림. 기준 원소는 보존.
#     return arr  # 순서대로 잘라 남은 리스트 반환.

# 풀이 요약
# 각 쿼리는 이전 작업 후 남은 리스트의 인덱스를 기준으로 적용합니다.
# 