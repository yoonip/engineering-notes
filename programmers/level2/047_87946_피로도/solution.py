# 문제: 피로도
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/87946
# 풀이: 방문한 던전 집합을 비트마스크 DP로 관리한다. 같은 집합의 총 소모량은 순서와 무관해 순열마다 다시 계산할 필요가 없다.
# 복잡도: 던전 N개: 시간 O(N·2^N), 추가 공간 O(2^N). 각 던전의 소모량은 최소 필요량 이하인 입력 조건을 사용한다.

def solution(k, dungeons):
    n = len(dungeons)
    remaining = [-1] * (1 << n)
    remaining[0] = k
    answer = 0
    for mask, fatigue in enumerate(remaining):
        if fatigue < 0:
            continue
        answer = max(answer, mask.bit_count())
        for index, (required, cost) in enumerate(dungeons):
            if mask & (1 << index) or fatigue < required:
                continue
            # 같은 방문 집합의 소모량은 순서와 무관하므로 상태를 합친다.
            next_mask = mask | (1 << index)
            remaining[next_mask] = max(remaining[next_mask], fatigue - cost)
    return answer
