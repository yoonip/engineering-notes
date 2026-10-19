# 문제: 광물 캐기
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/172927
# 풀이: 광물을 다섯 개씩 묶고 곡괭이별 피로도를 미리 계산한다. 같은 묶음 위치와 남은 곡괭이 상태는 캐시로 재사용한다.
# 복잡도: 광물 M개·묶음 B개·곡괭이 D/I/S개: 시간 O(M+B(D+1)(I+1)(S+1)), 추가 공간 O(B(D+1)(I+1)(S+1)).

from functools import lru_cache

def solution(picks, minerals):
    fatigue = {'diamond': (1, 5, 25), 'iron': (1, 1, 5), 'stone': (1, 1, 1)}
    blocks = []
    for start in range(0, len(minerals), 5):
        chunk = minerals[start:start + 5]
        blocks.append(tuple(sum(fatigue[name][pick] for name in chunk) for pick in range(3)))
    @lru_cache(None)
    def dfs(index, remaining):
        if index == len(blocks) or sum(remaining) == 0:
            return 0
        best = float('inf')
        for pick, count in enumerate(remaining):
            if count > 0:
                next_remaining = list(remaining)
                next_remaining[pick] -= 1
                cost = blocks[index][pick] + dfs(index + 1, tuple(next_remaining))
                best = min(best, cost)
        return best
    return dfs(0, tuple(picks))
