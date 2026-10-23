def solution(n):
    return [value for value in range(1, n + 1) if n % value == 0]

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의. 약수를 구할 정수 입력.
#     return [value for value in range(1, n + 1) if n % value == 0]  # range는 1부터 n까지 순회. %는 나머지, 리스트 내포의 if로 n을 나누어떨어지게 하는 수만 선택.

# 풀이 요약
# 1부터 n까지 검사해 나누어떨어지는 약수를 오름차순으로 모읍니다.
# 