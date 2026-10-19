from math import isqrt

def solution(n, k):
    digits = ''
    while n:
        n, remainder = divmod(n, k)
        digits = str(remainder) + digits
    answer = 0
    for piece in digits.split('0'):
        if not piece:
            continue
        value = int(piece)
        if value == 2:
            answer += 1
        elif value > 2 and value % 2 and all(value % divisor for divisor in range(3, isqrt(value) + 1, 2)):
            answer += 1
    return answer

# 전체 코드 줄별 설명
# from math import isqrt  # math의 isqrt를 import. 정수 제곱근을 내림해 반환하는 함수.
# 
# def solution(n, k):  # def는 함수 정의. n은 원래 수, k는 변환할 진법.
#     digits = ''  # ''는 빈 문자열. 진수 변환 결과 초기화.
#     while n:  # while은 조건 반복. 몫이 0이 될 때까지 실행.
#         n, remainder = divmod(n, k)  # divmod는 몫·나머지 반환. 다음 몫과 현재 자릿수로 언패킹.
#         digits = str(remainder) + digits  # str은 문자열 변환, +는 연결. 낮은 자리부터 얻으므로 앞에 붙임.
#     answer = 0  # =는 대입. 조건에 맞는 소수 개수 초기화.
#     for piece in digits.split('0'):  # split('0')으로 0을 경계로 나눈 문자열들을 for로 순회.
#         if not piece:  # not은 참·거짓 반전. 빈 문자열 조각은 거짓이라 건너뜀.
#             continue  # continue는 다음 조각으로 이동.
#         value = int(piece)  # int는 문자열을 10진수 정수로 해석. k진수 값으로 재해석하지 않음.
#         if value == 2:  # ==는 같음. 유일한 짝수 소수 2 검사.
#             answer += 1  # +=는 더해 저장. 소수 개수 증가.
#         elif value > 2 and value % 2 and all(value % divisor for divisor in range(3, isqrt(value) + 1, 2)):  # elif는 추가 분기, and는 모두 참, %는 나머지. all은 홀수 약수가 하나도 없는지 검사.
#             answer += 1  # 2보다 큰 홀수 소수도 개수에 추가.
#     return answer  # return으로 조건을 만족하는 소수 개수 반환.

# 풀이 요약
# k진수로 변환한 문자열을 0으로 나누면 필요한 경계 조건을 만족하는 후보만 남습니다. 각 후보를 10진수로 읽어 소수 판정합니다.
# 예: 437674의 3진수에서 211·2·11이 남아 3개. 후보 값 p에 대해 소수 검사는 O(√p), 변환 문자열 공간 O(log_k n).
