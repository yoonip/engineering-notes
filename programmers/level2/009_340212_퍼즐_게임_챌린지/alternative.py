def solution(diffs, times, limit):
    for level in range(1, max(diffs)+1):
        total = 0
        for i, (difficulty, duration) in enumerate(zip(diffs, times)):
            previous = times[i-1] if i else 0
            total += duration + max(0,difficulty-level)*(duration+previous)
        if total <= limit:
            return level
