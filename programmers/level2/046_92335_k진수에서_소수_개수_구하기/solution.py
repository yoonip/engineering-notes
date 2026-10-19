from math import isqrt

def solution(n, k):
    digits = ''
    while n:
        n, remainder = divmod(n, k)
        digits = str(remainder) + digits
    answer = 0
    # 0으로 분리한 숫자는 십진수로 읽는다.
    for piece in digits.split('0'):
        if not piece:
            continue
        value = int(piece)
        if value == 2:
            answer += 1
        # 2 이외의 짝수와 1을 제외하고 제곱근까지 약수를 확인한다.
        elif value > 2 and value % 2 and all(value % divisor for divisor in range(3, isqrt(value) + 1, 2)):
            answer += 1
    return answer
