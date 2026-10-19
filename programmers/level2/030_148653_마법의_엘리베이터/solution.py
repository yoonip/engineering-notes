def solution(storey):
    answer = 0
    while storey:
        storey, digit = divmod(storey, 10)
        # 5에서 동률이면 다음 자리의 올림 이득까지 확인한다.
        if digit > 5 or (digit == 5 and storey % 10 >= 5):
            answer += 10 - digit
            storey += 1
        else:
            answer += digit
    return answer
