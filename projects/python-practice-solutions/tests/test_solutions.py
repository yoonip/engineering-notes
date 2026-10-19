"""Small, deterministic local checks. Not a replacement for online grading."""
import ast
import contextlib
import copy
import io
import itertools
import json
import math
from pathlib import Path
import random
import runpy
import unittest


ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
SOLUTIONS = {row["number"]: runpy.run_path(str(ROOT / row["file"]))["solution"]
             for row in CATALOG}
CALL_COUNTS = {number: 0 for number in SOLUTIONS}


def call(number, *args):
    CALL_COUNTS[number] += 1
    captured = io.StringIO()
    with contextlib.redirect_stdout(captured):
        result = SOLUTIONS[number](*copy.deepcopy(args))
    if captured.getvalue():
        raise AssertionError("A solution unexpectedly wrote to stdout")
    return result


# Published examples and small synthetic inputs; no full problem statements.
CASES = {
    1: [((['SOO', 'OOO', 'OOO'], ['E 2', 'S 2', 'W 1']), [2, 1]),
        ((['SOO', 'OXX', 'OOO'], ['E 2', 'S 2', 'W 1']), [0, 1]),
        ((['SXX', 'OOO', 'OOO'], ['E 2', 'S 1', 'E 2']), [1, 2])],
    2: [(([[1, 0, 1, 1, 1], [1, 0, 1, 0, 1], [1, 0, 1, 1, 1],
            [1, 1, 1, 0, 1], [0, 0, 0, 0, 1]],), 11),
        (([[1, 0], [0, 1]],), -1), (([[1, 1], [1, 1]],), 3)],
    3: [((5, [[1, 2, 1], [2, 3, 3], [5, 2, 2], [1, 4, 2], [5, 3, 1], [5, 4, 2]], 3), 4),
        ((3, [[1, 2, 8], [1, 2, 1], [2, 3, 1]], 2), 3),
        ((3, [[1, 2, 1]], 1), 2)],
    4: [(([859, 900, 1000], [[909] * 7, [911] * 7, [1010] * 7], 1), 2),
        (([900], [[1200, 1200, 910, 910, 910, 910, 910]], 6), 1),
        (([900], [[911] * 7], 7), 0)],
    5: [(([[2, 1, 2], [5, 1, 1]],), 13),
        (([[2, 3, 2], [3, 1, 3], [2, 1, 1]],), 11),
        (([[3, 3, 3], [5, 4, 2], [2, 1, 2]],), 193),
        (([[1, 1, 4], [2, 1, 3], [3, 1, 2], [4, 1, 1]],), -1)],
    6: [(([1, 2, 3], [['-1'] * 3 for _ in range(2)]), 2),
        (([1, 2], [['X', 'X'], ['X', 'X']]), -1),
        (([1], [['-1']]), 1)],
    7: [((['u1', 'u2', 'u3'], ['u1 u2', 'u1 u2', 'u2 u1', 'u3 u1']), 2),
        ((['u1', 'u2'], ['u1 u2', 'u2 u1']), 0)],
    8: [(([[1, 20300104, 100, 80], [2, 20300804, 847, 37], [3, 20300401, 10, 8]],
          'date', 20300501, 'remain'), [[3, 20300401, 10, 8], [1, 20300104, 100, 80]]),
        (([[1, 20200101, 3, 2], [2, 20200102, 5, 4]], 'maximum', 5, 'code'),
         [[1, 20200101, 3, 2]])],
    9: [(([5, 1, 5], 30, [[2, 10], [9, 15], [10, 5], [11, 5]]), 5),
        (([3, 2, 7], 20, [[1, 15], [5, 16], [8, 6]]), -1),
        (([4, 2, 7], 20, [[1, 15], [5, 16], [8, 6]]), -1),
        (([1, 1, 1], 5, [[1, 2], [3, 2]]), 3)],
    10: [(([['red'] * 3 for _ in range(3)], 1, 1), 4),
         (([['red', 'red'], ['blue', 'red']], 0, 0), 1)],
    11: [(('aukks', 'wbqd', 5), 'happy'), (('z', 'a', 1), 'b'), (('b', 'a', 25), 'b')],
    12: [(([1, 10, 100], [[1, 2], [1, 3]],
           [[1, -1], [2, -1], [2, 7], [1, -1], [2, -1], [1, 0], [1, -1], [3, -1]]),
          [111, 10, 108, 1, 101, 100]),
         (([0], [], [[1, -1], [1, 5], [1, -1]]), [0, 5])],
    13: [((3, [10, 100, 20, 150, 1, 100, 200]), [10, 10, 10, 20, 20, 100, 100]),
         ((4, [0, 300, 40, 300, 20, 70, 150, 50, 500, 1000]), [0, 0, 0, 0, 20, 40, 70, 70, 150, 300])],
    14: [(([2, 1, 1, 2, 3, 1, 2, 3, 1],), 2),
         (([1, 3, 2, 1, 2, 1, 3, 1, 2],), 0), (([1, 2, 3, 1],), 1)],
    15: [(([-2, 3, 0, 2, -5],), 2), (([-3, -2, -1, 0, 1, 2, 3],), 5),
         (([-1, 1, -1, 1],), 0), (([0, 0, 0, 0],), 4)],
    16: [((['AN', 'CF', 'MJ', 'RT', 'NA'], [5, 3, 2, 7, 5]), 'TCMA'),
         ((['TR', 'RT', 'TR'], [7, 1, 3]), 'RCJA'), ((['RT'], [4]), 'RCJA')],
    17: [((['u1', 'u2', 'u3', 'u4'], ['u1 u2', 'u3 u2', 'u2 u4', 'u1 u4', 'u3 u1'], 2), [2, 1, 1, 0]),
         ((['u1', 'u2'], ['u1 u2'] * 4, 2), [0, 0])],
    18: [((10,), 3), ((12,), 11), ((3,), 2)],
    19: [(('one4seveneight',), 1478), (('23four5six7',), 234567),
         (('2three45sixseven',), 234567), (('123',), 123)],
    20: [((13, 17), 43), ((24, 27), 52), ((1, 1), -1)],
    21: [(([4, 7, 12], [True, False, True]), 9), (([1, 2, 3], [False, False, True]), 0)],
    22: [(('...!@BaT#*..y.abcdefghijklm',), 'bat.y.abcdefghi'), (('z-+.^.',), 'z--'),
         (('=.=',), 'aaa'), (('123_.def',), '123_.def'), (('abcdefghijklmn.p',), 'abcdefghijklmn')],
    23: [(([[0, 0, 0, 0, 0], [0, 0, 1, 0, 3], [0, 2, 5, 0, 1],
            [4, 2, 4, 4, 2], [3, 5, 1, 3, 1]], [1, 5, 3, 5, 1, 2, 1, 4]), 4),
         (([[0] * 5 for _ in range(5)], [1, 2, 3]), 0)],
    24: [(('1S2D*3T',), 37), (('1D2S#10S',), 9), (('1D2S0T',), 3),
         (('1S*2T*3S',), 23), (('1D#2S*3S',), 5), (('1T2D3D#',), -4), (('1D2S3T*',), 59)],
    25: [((5, [2, 1, 2, 6, 2, 4, 3, 3]), [3, 4, 2, 1, 5]),
         ((4, [4, 4, 4, 4, 4]), [4, 1, 2, 3]), ((3, [4, 4]), [1, 2, 3])],
    26: [((5, 24), 'TUE'), ((1, 1), 'FRI'), ((2, 29), 'MON'), ((12, 31), 'SAT')],
    27: [((['sun', 'bed', 'car'], 1), ['car', 'bed', 'sun']),
         ((['abce', 'abcd', 'cdx'], 2), ['abcd', 'abce', 'cdx'])],
    28: [(([1, 3, 2, 5, 4], 9), 3), (([2, 2, 3, 3], 10), 4), (([5], 4), 0)],
    29: [(([[1, 2], [2, 3]], [[3, 4], [5, 6]]), [[4, 6], [7, 9]]),
         (([[1], [2]], [[3], [4]]), [[4], [6]])],
    30: [(('00001234',), '****1234'), (('1234',), '1234')],
    31: [(([1, 2, 3, 4],), 2.5), (([5, 5],), 5.0), (([-3, 0, 3],), 0.0)],
    32: [((3,), 'Odd'), ((4,), 'Even'), ((0,), 'Even'), ((-3,), 'Odd')],
    33: [((121,), 144), ((3,), -1), ((1,), 4), ((50000000000000,), -1)],
    34: [((123,), 6), ((987,), 24), ((100000000,), 1)],
    35: [(('AB', 1), 'BC'), (('z', 1), 'a'), (('a B z', 4), 'e F d'), ((' Zz ', 1), ' Aa ')],
    36: [(('1234',), 1234), (('-1234',), -1234), (('+1234',), 1234), (('0',), 0)],
    37: [(('pPoooyY',), True), (('Pyy',), False), (('abc',), True), (('PYpy',), True)],
    38: [(([5, 9, 7, 10], 5), [5, 10]), (([2, 36, 1, 3], 1), [1, 2, 3, 36]),
         (([3, 2, 6], 10), [-1])],
    39: [(('abcde',), 'c'), (('qwer',), 'we'), (('a',), 'a'), (('ab',), 'ab')],
}


class ExampleTests(unittest.TestCase):
    pass


def make_examples(number):
    def test(self):
        for index, (args, expected) in enumerate(CASES[number]):
            with self.subTest(number=number, case=index):
                result = call(number, *args)
                self.assertEqual(result, expected)
                self.assertIs(type(result), type(expected))
    return test


for _number in sorted(CASES):
    setattr(ExampleTests, f"test_examples_{_number:02}", make_examples(_number))


def gravity_oracle(values, edges, queries):
    values = list(values)
    n = len(values)
    graph = [[] for _ in values]
    for a, b in edges:
        graph[a - 1].append(b - 1)
        graph[b - 1].append(a - 1)
    parent = [-1] * n
    children = [[] for _ in values]
    order = [0]
    for node in order:
        for nxt in graph[node]:
            if nxt != parent[node]:
                parent[nxt] = node
                children[node].append(nxt)
                order.append(nxt)
    result = []
    for node, value in queries:
        node -= 1
        if value == -1:
            pending, total = [node], 0
            while pending:
                current = pending.pop()
                total += values[current]
                pending.extend(children[current])
            result.append(total)
        else:
            while parent[node] != -1:
                values[node] = values[parent[node]]
                node = parent[node]
            values[0] = value
    return result


class ComparisonTests(unittest.TestCase):
    def test_annotated_code_matches_active_code(self):
        for row in CATALOG:
            text = (ROOT / row['file']).read_text(encoding='utf-8')
            marker = '# 같은 코드의 문법 설명: 아래 부분은 전체 주석입니다.\n'
            clean, annotated = text.split(marker, 1)
            decoded = '\n'.join(line[2:] if line.startswith('# ') else line[1:] if line.startswith('#') else ''
                                for line in annotated.splitlines())
            with self.subTest(file=row['file']):
                self.assertEqual(ast.dump(ast.parse(clean)), ast.dump(ast.parse(decoded)))

    def test_bfs_against_repeated_edge_relaxation(self):
        rng = random.Random(20261019)
        for _ in range(60):
            rows, cols = rng.randint(2, 5), rng.randint(2, 5)
            board = [[rng.randrange(2) for _ in range(cols)] for _ in range(rows)]
            board[0][0] = board[-1][-1] = 1
            dist = [[math.inf] * cols for _ in range(rows)]
            dist[0][0] = 1
            for _ in range(rows * cols):
                for r in range(rows):
                    for c in range(cols):
                        if not board[r][c]:
                            continue
                        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc]:
                                dist[nr][nc] = min(dist[nr][nc], dist[r][c] + 1)
            expected = -1 if math.isinf(dist[-1][-1]) else dist[-1][-1]
            self.assertEqual(call(2, board), expected)

    def test_delivery_against_floyd_warshall(self):
        rng = random.Random(3)
        for _ in range(60):
            n = rng.randint(2, 7)
            road = [[a, b, rng.randint(1, 9)] for a in range(1, n + 1)
                    for b in range(a + 1, n + 1) if rng.random() < 0.5]
            if not road:
                road = [[1, 2, 1]]
            road.append([road[0][0], road[0][1], rng.randint(1, 9)])
            dist = [[math.inf] * n for _ in range(n)]
            for i in range(n):
                dist[i][i] = 0
            for a, b, cost in road:
                dist[a - 1][b - 1] = dist[b - 1][a - 1] = min(dist[a - 1][b - 1], cost)
            for k in range(n):
                for i in range(n):
                    for j in range(n):
                        dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
            limit = rng.randint(1, 15)
            self.assertEqual(call(3, n, road, limit), sum(d <= limit for d in dist[0]))

    def test_gravity_against_direct_parent_copy(self):
        rng = random.Random(77887)
        for _ in range(120):
            n = rng.randint(1, 14)
            values = [rng.randint(0, 1000) for _ in range(n)]
            edges = [[rng.randint(1, node - 1), node] for node in range(2, n + 1)]
            rng.shuffle(edges)
            queries = [[rng.randint(1, n), -1 if rng.random() < 0.5 else rng.randint(0, 1000)]
                       for _ in range(35)]
            queries.extend([[node, -1] for node in range(1, n + 1)])
            self.assertEqual(call(12, values, edges, queries), gravity_oracle(values, edges, queries))

    def test_heap_against_sorted_prefixes(self):
        rng = random.Random(13)
        for _ in range(60):
            scores = [rng.randrange(20) for _ in range(rng.randint(7, 25))]
            k = rng.randint(3, 10)
            expected = [sorted(scores[:i], reverse=True)[:k][-1] for i in range(1, len(scores) + 1)]
            self.assertEqual(call(13, k, scores), expected)

    def test_hamburger_against_direct_removal(self):
        rng = random.Random(14)
        for _ in range(100):
            items = [rng.randint(1, 3) for _ in range(rng.randint(1, 60))]
            remaining = list(items)
            expected = 0
            while True:
                start = next((i for i in range(len(remaining) - 3)
                              if remaining[i:i + 4] == [1, 2, 3, 1]), None)
                if start is None:
                    break
                del remaining[start:start + 4]
                expected += 1
            self.assertEqual(call(14, items), expected)

    def test_three_friends_against_combinations(self):
        rng = random.Random(15)
        for _ in range(60):
            numbers = [rng.randint(-4, 4) for _ in range(rng.randint(3, 10))]
            expected = sum(sum(triple) == 0 for triple in itertools.combinations(numbers, 3))
            self.assertEqual(call(15, numbers), expected)

    def test_budget_against_all_subsets(self):
        rng = random.Random(28)
        for _ in range(60):
            costs = [rng.randint(1, 10) for _ in range(rng.randint(1, 8))]
            budget = rng.randint(1, 25)
            expected = max((len(combination) for count in range(len(costs) + 1)
                            for combination in itertools.combinations(costs, count)
                            if sum(combination) <= budget), default=0)
            self.assertEqual(call(28, costs, budget), expected)

    def test_all_2016_dates_against_datetime(self):
        import datetime
        date = datetime.date(2016, 1, 1)
        weekdays = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
        while date.year == 2016:
            self.assertEqual(call(26, date.month, date.day), weekdays[date.weekday()])
            date += datetime.timedelta(days=1)

    def test_square_checks_for_small_integers(self):
        for number in range(1, 301):
            root = next((x for x in range(1, number + 1) if x * x == number), None)
            expected = -1 if root is None else (root + 1) ** 2
            self.assertEqual(call(33, number), expected)

    def test_caesar_roundtrip(self):
        text = 'Az By Cz XYZ abc  '
        for shift in range(1, 26):
            encoded = call(35, text, shift)
            self.assertEqual(call(35, encoded, 26 - shift), text)


if __name__ == '__main__':
    unittest.main()
