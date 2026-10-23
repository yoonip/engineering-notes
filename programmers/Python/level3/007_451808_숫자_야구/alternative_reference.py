from itertools import permutations

def solution(n, submit):
    candidates = [''.join(map(str, p)) for p in permutations(range(1, 10), 4)]
    for _ in range(n):
        if len(candidates) == 1:
            return int(candidates[0])
        guess = candidates[0]
        clue = submit(int(guess))
        strikes, balls = int(clue[0]), int(clue[3])
        next_candidates = []
        for secret in candidates:
            same_position = sum(a == b for a, b in zip(guess, secret))
            common_digits = len(set(guess) & set(secret))
            if (same_position, common_digits - same_position) == (strikes, balls):
                next_candidates.append(secret)
        candidates = next_candidates
    if len(candidates) != 1:
        raise ValueError('이 비교 전략의 질문 예산이 부족합니다.')
    return int(candidates[0])
