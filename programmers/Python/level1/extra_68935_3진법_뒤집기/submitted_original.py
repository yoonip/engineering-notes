
def solution(n):
    ternary = ""

    while n > 0:
        ternary += str(n % 3)
        n //= 3

    answer = int(ternary, 3)

    return answer


# ========== 공부용 코드 (전체 주석 처리) ==========

# def solution(n):                         # 자연수 n을 입력받는 함수
#     ternary = ""                         # 뒤집힌 3진법 숫자를 저장할 빈 문자열
#
#     while n > 0:                         # n이 0보다 큰 동안 반복
#         ternary += str(n % 3)            # n을 3으로 나눈 나머지를 문자열로 변환하여 뒤에 추가
#         n //= 3                          # n을 3으로 나눈 몫으로 갱신
#
#     answer = int(ternary, 3)             # ternary를 3진법 숫자로 해석하여 10진수 정수로 변환
#
#     return answer                        # 최종 10진수 결과 반환
