def solution(n):
    for x in range(2, n):
        if n % x == 1:
            return x


# 같은 정답 코드 + 줄별 문법 설명
# 아래는 전체가 주석이므로 실행되지 않습니다.

# def solution(n):  # def로 함수를 정의합니다. n은 입력 정수를 받는 매개변수입니다.
#     for x in range(2, n):  # range(시작, 끝)은 끝을 제외합니다. x에 2부터 n-1까지 차례로 넣습니다.
#         if n % x == 1:  # %는 나머지 연산, ==는 같은지 비교하는 연산입니다.
#             return x  # x를 반환하고 함수 전체를 종료합니다. 처음 찾은 값이 가장 작은 값입니다.