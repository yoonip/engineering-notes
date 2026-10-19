# 문제: 시소 짝꿍
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/152996
# 풀이: Counter로 무게별 인원을 센다. 가능한 무게 비만 확인하고 더 무거운 상대만 세어 쌍의 중복을 막는다.
# 복잡도: 사람 N명·고유 무게 U개: 평균 시간 O(N+U), 추가 공간 O(U).

from collections import Counter

def solution(weights):
    counts = Counter(weights)
    answer = 0
    for weight, count in counts.items():
        answer += count * (count - 1) // 2
        for numerator, denominator in ((2, 1), (3, 2), (4, 3)):
            if weight * numerator % denominator == 0:
                partner = weight * numerator // denominator
                answer += count * counts[partner]
    return answer
