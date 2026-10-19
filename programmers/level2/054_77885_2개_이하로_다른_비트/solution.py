def solution(numbers):
    answer = []
    for number in numbers:
        # 가장 오른쪽 0비트만 켜진 값을 만든다.
        zero = (~number) & (number + 1)
        # 그 0을 1로, 바로 아래 1을 0으로 바꿔 증가량을 최소화한다.
        answer.append(number + zero - (zero >> 1))
    return answer
