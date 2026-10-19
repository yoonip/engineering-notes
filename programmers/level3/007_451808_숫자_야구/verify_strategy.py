from itertools import permutations
import json

def verify():
    patterns = list(permutations(range(1, 10), 4))
    masks = [sum(1 << digit for digit in value) for value in patterns]
    cache = {}

    def response_row(index):
        if index not in cache:
            a, b, c, d = patterns[index]
            mask = masks[index]
            # 공통 숫자 수와 제자리 숫자 수를 손실 없이 하나의 값으로 묶는다.
            cache[index] = bytes(
                (mask & masks[i]).bit_count() * 5
                + (a == w) + (b == x) + (c == y) + (d == z)
                for i, (w, x, y, z) in enumerate(patterns)
            )
        return cache[index]

    def choose(candidates):
        best, selected = len(candidates) + 1, candidates[0]
        for guess in candidates:
            row = response_row(guess)
            counts, worst = [0] * 25, 0
            for hidden in candidates:
                clue = row[hidden]
                counts[clue] += 1
                worst = max(worst, counts[clue])
                if worst >= best:
                    break
            if worst < best:
                best, selected = worst, guess
                if best == 1:
                    break
        return selected

    leaf_depths = {}
    def visit(candidates, depth):
        if len(candidates) == 1:
            leaf_depths[depth] = leaf_depths.get(depth, 0) + 1
            return
        # 주 풀이와 같이 첫 질문은 1234, 동률은 먼저 나온 후보를 선택한다.
        guess = 0 if depth == 0 else choose(candidates)
        row, groups = response_row(guess), {}
        for candidate in candidates:
            groups.setdefault(row[candidate], []).append(candidate)
        for group in groups.values():
            visit(group, depth + 1)

    visit(list(range(len(patterns))), 0)
    assert sum(leaf_depths.values()) == 3024
    assert max(leaf_depths) <= 6
    return {'secrets': 3024, 'maximum_queries': max(leaf_depths),
            'leaf_depth_counts': leaf_depths}

if __name__ == '__main__':
    print(json.dumps(verify(), ensure_ascii=False))
