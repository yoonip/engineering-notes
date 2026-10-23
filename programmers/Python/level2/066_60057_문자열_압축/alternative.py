from itertools import groupby

def solution(s):
    answer = len(s)
    for width in range(1, len(s) // 2 + 1):
        chunks = [s[i:i + width] for i in range(0, len(s), width)]
        encoded = []
        for chunk, group in groupby(chunks):
            count = sum(1 for _ in group)
            encoded.append((str(count) if count > 1 else '') + chunk)
        answer = min(answer, len(''.join(encoded)))
    return answer
