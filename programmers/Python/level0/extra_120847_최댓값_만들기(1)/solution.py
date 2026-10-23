def solution(numbers):
    values = sorted(numbers)
    return values[-1] * values[-2]

# 전체 코드 줄별 설명
# def solution(numbers):  # def는 함수 정의. 음이 아닌 정수 리스트 입력.
#     values = sorted(numbers)  # sorted는 오름차순 정렬한 새 리스트 반환.
#     return values[-1] * values[-2]  # -1은 마지막, -2는 끝에서 두 번째. 가장 큰 두 수를 곱함.

# 풀이 요약
# 모든 수가 0 이상이므로 가장 큰 두 원소의 곱이 최대입니다.
# 