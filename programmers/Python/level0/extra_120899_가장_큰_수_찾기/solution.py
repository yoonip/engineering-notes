def solution(array):
    largest = max(array)
    return [largest, array.index(largest)]

# 전체 코드 줄별 설명
# def solution(array):  # def는 함수 정의. 중복 없는 정수 리스트 입력.
#     largest = max(array)  # max는 최댓값. 가장 큰 원소 저장.
#     return [largest, array.index(largest)]  # []는 리스트 생성, index는 값의 위치 조회. 최대값과 인덱스 반환.

# 풀이 요약
# 최댓값을 구한 다음 그 값이 있는 위치를 찾습니다.
# 