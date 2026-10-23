def solution(n):
    return sum(any(value % divisor == 0 for divisor in range(2, value)) for value in range(2, n + 1))

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의. 합성수를 셀 상한 입력.
#     return sum(any(value % divisor == 0 for divisor in range(2, value)) for value in range(2, n + 1))  # range는 정수 순회, %는 나머지. 1과 자기 자신 외의 약수가 하나라도 있으면 any가 참. sum으로 합성수 개수 집계.

# 풀이 요약
# 2부터 n까지의 각 수에서 1과 자기 자신 외의 약수가 존재하는지 검사합니다.
# 