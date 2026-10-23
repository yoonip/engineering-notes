
def solution(x):
    digit_sum = sum(map(int, str(x)))

    answer = (x % digit_sum == 0)

    return answer


# ========== 공부용 코드 (전체 주석 처리) ==========

# def solution(x):                          # 자연수 x를 입력받는 함수
#     digit_sum = sum(map(int, str(x)))     # x를 문자열로 바꾸고, 각 문자를 정수로 변환한 뒤 모두 더함
#
#     answer = (x % digit_sum == 0)         # x를 자릿수의 합으로 나눈 나머지가 0이면 True, 아니면 False
#
#     return answer                         # 하샤드 수인지 판단한 결과 반환
