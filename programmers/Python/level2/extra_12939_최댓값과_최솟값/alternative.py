def solution(s):
    numbers = sorted(map(int, s.split()))
    return f'{numbers[0]} {numbers[-1]}'
