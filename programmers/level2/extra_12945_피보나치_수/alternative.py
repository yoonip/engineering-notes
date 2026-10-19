def solution(n):
    modulus = 1234567
    def pair(k):
        if k == 0:
            return 0, 1
        a, b = pair(k // 2)
        even = a * (2 * b - a) % modulus
        odd = (a * a + b * b) % modulus
        return (odd, (even + odd) % modulus) if k % 2 else (even, odd)
    return pair(n)[0]
