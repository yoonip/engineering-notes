from bisect import bisect_right

def solution(n, bans):
    def rank(word):
        value = 0
        for ch in word:
            value = value * 26 + ord(ch) - 96
        return value
    removed = sorted(map(rank, bans))
    left, right = n, n + len(removed)
    while left < right:
        middle = (left + right) // 2
        if middle - bisect_right(removed, middle) >= n:
            right = middle
        else:
            left = middle + 1
    result = []
    while left:
        left, digit = divmod(left - 1, 26)
        result.append(chr(97 + digit))
    return ''.join(reversed(result))
