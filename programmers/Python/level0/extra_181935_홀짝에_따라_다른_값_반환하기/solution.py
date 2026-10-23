def solution(n):
    if n % 2:
        return sum(range(1, n + 1, 2))
    return sum(x ** 2 for x in range(2, n + 1, 2))

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의. 상한 정수 n 입력.
#     if n % 2:  # if는 조건, %는 나머지. 나머지 1은 참이므로 홀수일 때 실행.
#         return sum(range(1, n + 1, 2))  # range(시작,끝,간격)는 끝 제외 수열 생성. sum은 홀수들의 합.
#     return sum(x ** 2 for x in range(2, n + 1, 2))  # **는 거듭제곱. 생성기 표현식으로 짝수 제곱을 만들고 sum으로 합산.

# 풀이 요약
# 홀수이면 홀수 합, 짝수이면 짝수 제곱 합을 구합니다.
# 