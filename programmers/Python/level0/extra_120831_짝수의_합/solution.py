def solution(n):
    return sum(range(2, n + 1, 2))

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의. 더할 짝수의 상한 입력.
#     return sum(range(2, n + 1, 2))  # range는 2부터 n까지 2칸 간격 정수 생성. sum은 수열의 합계.

# 풀이 요약
# 2,4,6 순서로 짝수만 만들어 더합니다.
# 