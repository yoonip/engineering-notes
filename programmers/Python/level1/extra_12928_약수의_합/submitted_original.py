
def solution(n):
    answer = 0

    for i in range(1, n + 1):
        if n % i == 0:
            answer += i

    return answer


# ========== 공부용 코드 (전체 주석 처리) ==========

# def solution(n):                    # def는 함수를 정의하는 명령어, n은 입력받는 정수
#     answer = 0                      # 약수의 합을 저장할 변수, 처음에는 0으로 초기화
#
#     for i in range(1, n + 1):      # for는 반복문, i는 1부터 n까지 차례대로 증가
#         if n % i == 0:             # if는 조건문, %는 나머지 연산, 나머지가 0이면 i는 n의 약수
#             answer += i            # answer = answer + i 와 같음, 약수 i를 합계에 더함
#
#     return answer                  # return은 함수의 결과를 반환하고 함수를 종료
