def solution(arr, queries):
    for start, end in queries:
        for i in range(start, end + 1):
            arr[i] += 1
    return arr

# 전체 코드 줄별 설명
# def solution(arr, queries):  # def는 함수 정의. 정수 리스트와 구간 쿼리 입력.
#     for start, end in queries:  # 각 쿼리의 시작과 끝 위치를 나누어 받음.
#         for i in range(start, end + 1):  # range는 끝 제외. end까지 포함하도록 1을 더해 순회.
#             arr[i] += 1  # []로 원소 접근, +=는 더해 저장. 구간의 각 원소 증가.
#     return arr  # 모든 쿼리를 적용한 리스트 반환.

# 풀이 요약
# 각 닫힌 구간에 속한 원소를 모두 1씩 증가시킵니다.
# 