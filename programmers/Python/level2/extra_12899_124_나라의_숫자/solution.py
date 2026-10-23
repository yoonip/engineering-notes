def solution(n):
    digits = []
    while n > 0:
        # 1을 빼서 1·2·4를 0·1·2 인덱스로 대응시키는 0 없는 3진법 처리.
        n, remainder = divmod(n - 1, 3)
        digits.append('124'[remainder])
    return ''.join(reversed(digits))
