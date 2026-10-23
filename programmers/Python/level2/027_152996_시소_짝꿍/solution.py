from collections import Counter

def solution(weights):
    counts = Counter(weights)
    answer = 0
    for weight, count in counts.items():
        # 같은 무게끼리는 순서 없는 두 사람을 고른다.
        answer += count * (count - 1) // 2
        # 약분한 거리비 중 큰 무게 방향만 확인해 중복을 막는다.
        for numerator, denominator in ((2, 1), (3, 2), (4, 3)):
            if weight * numerator % denominator == 0:
                partner = weight * numerator // denominator
                answer += count * counts[partner]
    return answer
