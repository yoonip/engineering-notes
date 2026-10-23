def solution(n):
    length, block = 1, 3
    while n > block:
        n -= block
        length += 1
        block *= 3
    rank, result = n - 1, ['1'] * length
    for i in range(length - 1, -1, -1):
        rank, digit = divmod(rank, 3)
        result[i] = '124'[digit]
    return ''.join(result)
