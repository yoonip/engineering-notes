def solution(n):
    required = n.bit_count()
    candidate = n + 1
    while candidate.bit_count() != required:
        candidate += 1
    return candidate
