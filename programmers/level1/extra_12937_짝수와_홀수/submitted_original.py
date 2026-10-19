def solution(num):
    if num % 2 == 0:
        return "Even"
    else:
        return "Odd"


# 같은 정답 코드 + 줄별 문법 설명
# 아래는 전체가 주석이므로 실행되지 않습니다.

# def solution(num):  # def로 함수를 정의합니다. num은 입력 정수를 받는 매개변수입니다.
#     if num % 2 == 0:  # %는 나머지 연산, ==는 같은지 비교입니다. 나머지가 0이면 짝수입니다.
#         return "Even"  # 문자열 "Even"을 반환하고 함수를 종료합니다.
#     else:  # if 조건이 거짓, 즉 홀수일 때 실행합니다.
#         return "Odd"  # 문자열 "Odd"를 반환하고 함수를 종료합니다.