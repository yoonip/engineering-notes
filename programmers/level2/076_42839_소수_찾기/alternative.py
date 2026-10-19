from itertools import permutations
from math import isqrt

def solution(numbers):
    values = {int(''.join(p)) for length in range(1, len(numbers) + 1)
              for p in permutations(numbers, length)}
    maximum = max(values)
    prime = bytearray(b'\x01') * (maximum + 1)
    prime[:min(2, len(prime))] = b'\x00' * min(2, len(prime))
    for p in range(2, isqrt(maximum) + 1):
        if prime[p]:
            prime[p * p:maximum + 1:p] = b'\x00' * ((maximum - p * p) // p + 1)
    return sum(prime[value] for value in values)
