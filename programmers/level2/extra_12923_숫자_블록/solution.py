from math import isqrt

def solution(begin, end):
    answer = []
    # range는 끝 제외이므로 end+1로 마지막 위치까지 포함.
    for value in range(begin, end + 1):
        if value == 1:
            # 초기값 0 유지.
            answer.append(0)
            continue
        block = 1
        for divisor in range(2, isqrt(value) + 1):
            # 나누어떨어지면 약수 쌍 발견.
            if value % divisor == 0:
                partner = value // divisor
                # 실제 존재하는 블록 번호의 최대값 천만 이하인지 검사.
                if partner <= 10000000:
                    block = partner
                    break
                # 이 후보를 놓치면 소수의 큰 배수에서 틀림.
                block = divisor
        answer.append(block)
    return answer
