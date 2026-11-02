def solution(numbers):
    values = sorted(numbers)
    return max(values[0] * values[1], values[-1] * values[-2])

# 전체 코드 줄별 설명
# def solution(numbers):  # def는 함수 정의. 음수도 가능한 정수 리스트 입력.
#     values = sorted(numbers)  # sorted는 오름차순 정렬한 새 리스트 반환.
#     return max(values[0] * values[1], values[-1] * values[-2])  # 0·1은 가장 작은 두 수, -1·-2는 가장 큰 두 수. max로 두 곱 중 큰 값 선택.

# 풀이 요약
# 정렬한 배열의 가장 작은 두 수의 곱과 가장 큰 두 수의 곱을 비교합니다. 0이나 서로 다른 부호의 두 원소도 처리합니다.
# 