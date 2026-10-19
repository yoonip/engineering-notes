def solution(n, t, m, p):
    alphabet = '0123456789ABCDEF'
    output, position, number = [], 0, 0
    while len(output) < t:
        value, digits = number, []
        if value == 0:
            digits.append('0')
        while value:
            value, remainder = divmod(value, n)
            digits.append(alphabet[remainder])
        for digit in reversed(digits):
            if position % m == p - 1 and len(output) < t:
                output.append(digit)
            position += 1
        number += 1
    return ''.join(output)
