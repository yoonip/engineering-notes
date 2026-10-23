from functools import cmp_to_key

def solution(numbers):
    parts = list(map(str, numbers))
    def compare(a, b):
        return (a + b < b + a) - (a + b > b + a)
    parts.sort(key=cmp_to_key(compare))
    return '0' if parts[0] == '0' else ''.join(parts)
