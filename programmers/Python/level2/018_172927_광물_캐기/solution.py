from functools import lru_cache

def solution(picks, minerals):
    fatigue = {'diamond': (1, 5, 25), 'iron': (1, 1, 5), 'stone': (1, 1, 1)}
    blocks = []
    # 곡괭이 하나가 처리하는 최대 다섯 광물을 묶는다.
    for start in range(0, len(minerals), 5):
        chunk = minerals[start:start + 5]
        blocks.append(tuple(sum(fatigue[name][pick] for name in chunk) for pick in range(3)))
    # 같은 위치와 남은 곡괭이 상태의 결과를 재사용한다.
    @lru_cache(None)
    def dfs(index, remaining):
        if index == len(blocks) or sum(remaining) == 0:
            return 0
        best = float('inf')
        for pick, count in enumerate(remaining):
            if count > 0:
                next_remaining = list(remaining)
                next_remaining[pick] -= 1
                # 현재 묶음 비용과 이후 최솟값을 합한다.
                cost = blocks[index][pick] + dfs(index + 1, tuple(next_remaining))
                best = min(best, cost)
        return best
    return dfs(0, tuple(picks))
