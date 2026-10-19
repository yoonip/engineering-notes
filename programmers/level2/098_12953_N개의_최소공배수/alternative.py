def solution(arr):
    maximum = {}
    for value in arr:
        factor = 2
        while factor * factor <= value:
            exponent = 0
            while value % factor == 0:
                value //= factor
                exponent += 1
            maximum[factor] = max(maximum.get(factor, 0), exponent)
            factor += 1
        if value > 1:
            maximum[value] = max(maximum.get(value, 0), 1)
    result = 1
    for prime, exponent in maximum.items():
        result *= prime ** exponent
    return result
