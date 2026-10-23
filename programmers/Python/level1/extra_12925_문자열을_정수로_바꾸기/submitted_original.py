#def solution(s):
 #   return int(s)  # 문자열을 정수로 변환

def solution(s):
    number = int(s)  # 문자열 s를 정수로 바꿔 number에 저장
    return number   # 저장한 정수를 반환



# def solution(n):                  # n을 입력받는 solution 함수를 정의합니다.
#     debug = True                  # True면 확인용 출력 실행, False면 출력 생략.
#     answer = 0                    # 자릿수의 합을 저장할 변수를 만듭니다.
#
#     if debug:                     # debug가 True일 때 아래 내용을 실행합니다.
#         print("입력받은 값:", n)    # 함수가 실제로 받은 입력값을 보여줍니다.
#
#     for digit in str(n):          # 숫자를 문자열로 바꾸고 한 글자씩 꺼냅니다.
#         answer += int(digit)      # 꺼낸 글자를 정수로 바꿔 합계에 더합니다.
#
#         if debug:                 # 확인용 출력을 켰을 때만 실행합니다.
#             print("현재 자릿수:", digit, "/ 현재까지의 합:", answer)
#                                   # 지금 처리한 자릿수와 누적 합계를 보여줍니다.
#
#     if debug:                     # 확인용 출력을 켰을 때만 실행합니다.
#         print("최종 반환값:", answer)  # 반환 직전의 최종 결과를 보여줍니다.
#
#     return answer                 # 계산 결과를 프로그래머스 채점기에 전달합니다.