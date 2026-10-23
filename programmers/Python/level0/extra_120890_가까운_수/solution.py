def solution(array, n):
    return min(array, key=lambda x: (abs(x - n), x))

# 전체 코드 줄별 설명
# def solution(array, n):  # def는 함수 정의. 후보 정수 리스트와 기준 정수 입력.
#     return min(array, key=lambda x: (abs(x - n), x))  # min은 기준이 가장 작은 원소 선택, lambda는 익명 함수, abs는 절댓값. 튜플로 거리 우선·값 작은 순 기준 지정.

# 풀이 요약
# 거리 차이를 먼저 비교하고 거리가 같으면 더 작은 원소를 고릅니다.
# 