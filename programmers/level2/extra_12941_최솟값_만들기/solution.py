def solution(A, B):
    # A의 작은 값부터 사용.
    small_first = sorted(A)
    large_first = sorted(B, reverse=True)
    return sum(a * b for a, b in zip(small_first, large_first))
