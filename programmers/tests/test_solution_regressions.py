"""개선한 풀이를 작은 독립 기준 구현·경계값과 비교한다."""

from collections import deque
from itertools import permutations, product
from pathlib import Path
import random
import re
import runpy
import unittest


ROOT = Path(__file__).resolve().parents[1]
FUNCTIONS = {}
COMPARISONS = 0


def solve(identifier, *args):
    if identifier not in FUNCTIONS:
        paths = list(ROOT.joinpath('level2').glob(f'*_{identifier}_*/solution.py'))
        if len(paths) != 1:
            raise AssertionError(f'풀이 파일 수가 올바르지 않음: {identifier}')
        FUNCTIONS[identifier] = runpy.run_path(str(paths[0]))['solution']
    return FUNCTIONS[identifier](*args)


def delivery_reference(n, roads, limit):
    distance = [[float('inf')] * n for _ in range(n)]
    for i in range(n):
        distance[i][i] = 0
    for a, b, time in roads:
        distance[a - 1][b - 1] = min(distance[a - 1][b - 1], time)
        distance[b - 1][a - 1] = distance[a - 1][b - 1]
    for via in range(n):
        for start in range(n):
            for end in range(n):
                distance[start][end] = min(
                    distance[start][end], distance[start][via] + distance[via][end])
    return sum(value <= limit for value in distance[0])


def cache_reference(capacity, cities):
    cache = []
    elapsed = 0
    for city in cities:
        city = city.lower()
        if city in cache:
            elapsed += 1
            cache.remove(city)
        else:
            elapsed += 5
        if capacity:
            cache.append(city)
            if len(cache) > capacity:
                del cache[0]
    return elapsed


def expression_reference(expression):
    original = re.split(r'([+*-])', expression)
    operations = {'+': lambda a, b: a + b,
                  '-': lambda a, b: a - b,
                  '*': lambda a, b: a * b}
    answer = 0
    for order in permutations('+-*'):
        tokens = original[:]
        for operation in order:
            while operation in tokens:
                i = tokens.index(operation)
                value = operations[operation](int(tokens[i - 1]), int(tokens[i + 1]))
                tokens[i - 1:i + 2] = [str(value)]
        answer = max(answer, abs(int(tokens[0])))
    return answer


def fatigue_reference(k, dungeons):
    answer = 0
    for order in permutations(dungeons):
        fatigue = k
        count = 0
        for required, cost in order:
            if fatigue < required:
                break
            fatigue -= cost
            count += 1
        answer = max(answer, count)
    return answer


def cards_reference(cards):
    used = set()
    sizes = [0, 0]
    for start in range(len(cards)):
        size = 0
        while start not in used:
            used.add(start)
            size += 1
            start = cards[start] - 1
        sizes.append(size)
    sizes.sort(reverse=True)
    return sizes[0] * sizes[1]


def processes_reference(priorities, location):
    queue = deque(enumerate(priorities))
    executed = 0
    while queue:
        i, priority = queue.popleft()
        if any(other > priority for _, other in queue):
            queue.append((i, priority))
        else:
            executed += 1
            if i == location:
                return executed


def virus_reference(n, infection, edges, k):
    states = {frozenset((infection,))}
    best = 1
    for _ in range(k):
        following = set(states)
        for infected in states:
            for kind in (1, 2, 3):
                reached = set(infected)
                queue = list(infected)
                while queue:
                    node = queue.pop()
                    for a, b, pipe in edges:
                        if pipe != kind:
                            continue
                        neighbor = b if node == a else a if node == b else None
                        if neighbor is not None and neighbor not in reached:
                            reached.add(neighbor)
                            queue.append(neighbor)
                following.add(frozenset(reached))
        states = following
        best = max(best, max(map(len, states)))
    return best


def joystick_reference(name):
    required = sum(1 << i for i, character in enumerate(name) if character != 'A')
    vertical = sum(min(ord(character) - 65, 91 - ord(character)) for character in name)
    start = (0, required & 1)
    queue = deque([(start, 0)])
    visited = {start}
    while queue:
        (position, mask), moves = queue.popleft()
        if mask == required:
            return vertical + moves
        for next_position in ((position - 1) % len(name), (position + 1) % len(name)):
            state = (next_position, mask | (required & (1 << next_position)))
            if state not in visited:
                visited.add(state)
                queue.append((state, moves + 1))


class SolutionRegressions(unittest.TestCase):
    def compare(self, actual, expected, label=None):
        global COMPARISONS
        COMPARISONS += 1
        self.assertEqual(actual, expected, label)

    def test_delivery_example_and_boundaries(self):
        self.compare(solve(12978, 5, [[1, 2, 1], [2, 3, 3], [5, 2, 2],
                     [1, 4, 2], [5, 3, 1], [5, 4, 2]], 3), 4)
        self.compare(solve(12978, 4, [[1, 2, 9], [1, 2, 2], [2, 3, 3]], 5), 3)
        self.compare(solve(12978, 1, [], 0), 1)
        self.compare(solve(12978, 5, [], 0), 1)

    def test_delivery_random_graphs(self):
        rng = random.Random(12978)
        for _ in range(400):
            n = rng.randint(1, 9)
            roads = []
            for a in range(1, n + 1):
                for b in range(a + 1, n + 1):
                    if rng.random() < 0.4:
                        roads.append([a, b, rng.randint(1, 10)])
                        if rng.random() < 0.2:
                            roads.append([a, b, rng.randint(1, 10)])
            limit = rng.randint(0, 25)
            self.compare(solve(12978, n, roads, limit), delivery_reference(n, roads, limit))

    def test_cache_examples_and_boundaries(self):
        cities = ['Jeju', 'Pangyo', 'Seoul', 'NewYork', 'LA'] * 2
        self.compare(solve(17680, 3, cities), 50)
        self.compare(solve(17680, 0, ['A', 'a']), 10)
        self.compare(solve(17680, 1, ['A', 'a', 'B', 'a']), 16)
        self.compare(solve(17680, 30, []), 0)

    def test_cache_random_requests(self):
        rng = random.Random(17680)
        for _ in range(600):
            capacity = rng.randint(0, 30)
            cities = [rng.choice(['Seoul', 'SEOUL', 'Jeju', 'jeju', 'Tokyo', 'A', 'B'])
                      for _ in range(rng.randint(0, 100))]
            self.compare(solve(17680, capacity, cities), cache_reference(capacity, cities))

    def test_expression_known_and_associativity(self):
        for expression, expected in [('100-200*300-500+20', 60420), ('50*6-3*2', 300),
                                     ('1-2-3', 4), ('0*9+0', 0), ('42', 42)]:
            self.compare(solve(67257, expression), expected)

    def test_expression_random_precedence(self):
        rng = random.Random(67257)
        for _ in range(700):
            count = rng.randint(1, 10)
            expression = str(rng.randint(0, 100))
            for _ in range(count - 1):
                expression += rng.choice('+-*') + str(rng.randint(0, 100))
            self.compare(solve(67257, expression), expression_reference(expression), expression)

    def test_fatigue_known_and_boundaries(self):
        self.compare(solve(87946, 80, [[80, 20], [50, 40], [30, 10]]), 3)
        self.compare(solve(87946, 1, [[2, 1]]), 0)
        self.compare(solve(87946, 8, [[1, 1]] * 8), 8)
        self.compare(solve(87946, 2, [[2, 2], [2, 2]]), 1)

    def test_fatigue_random_permutation_reference(self):
        rng = random.Random(87946)
        for _ in range(280):
            dungeons = []
            for _ in range(rng.randint(1, 7)):
                required = rng.randint(1, 20)
                dungeons.append([required, rng.randint(1, required)])
            k = rng.randint(1, 35)
            self.compare(solve(87946, k, dungeons), fatigue_reference(k, dungeons))

    def test_cards_examples_and_single_cycle(self):
        self.compare(solve(131130, [8, 6, 3, 7, 2, 5, 1, 4]), 12)
        self.compare(solve(131130, [2, 3, 4, 1]), 0)
        self.compare(solve(131130, [1, 2]), 1)

    def test_cards_random_permutations(self):
        rng = random.Random(131130)
        for _ in range(600):
            cards = list(range(1, rng.randint(2, 100) + 1))
            rng.shuffle(cards)
            self.compare(solve(131130, cards), cards_reference(cards))

    def test_process_examples_and_equal_priorities(self):
        self.compare(solve(42587, [2, 1, 3, 2], 2), 1)
        self.compare(solve(42587, [1, 1, 9, 1, 1, 1], 0), 5)
        self.compare(solve(42587, [5] * 100, 99), 100)
        self.compare(solve(42587, [1], 0), 1)

    def test_process_random_queue_reference(self):
        rng = random.Random(42587)
        for _ in range(800):
            priorities = [rng.randint(1, 9) for _ in range(rng.randint(1, 100))]
            location = rng.randrange(len(priorities))
            self.compare(solve(42587, priorities, location),
                         processes_reference(priorities, location))

    def test_virus_disconnected_and_repeated_states(self):
        self.compare(solve(468373, 4, 1, [], 10), 1)
        self.compare(solve(468373, 4, 1, [[1, 2, 1], [2, 3, 2], [3, 4, 3]], 0), 1)
        self.compare(solve(468373, 4, 1, [[1, 2, 1], [2, 3, 2], [3, 4, 3]], 3), 4)
        edges = [[1, 2, 1], [1, 2, 2], [2, 3, 3], [3, 4, 1], [3, 4, 2]]
        self.compare(solve(468373, 4, 1, edges, 100), 4)

    def test_virus_random_full_state_reference(self):
        rng = random.Random(468373)
        for _ in range(320):
            n = rng.randint(1, 8)
            edges = []
            for a in range(1, n + 1):
                for b in range(a + 1, n + 1):
                    if rng.random() < 0.3:
                        edges.append([a, b, rng.randint(1, 3)])
            infection = rng.randint(1, n)
            k = rng.randint(0, 6)
            self.compare(solve(468373, n, infection, edges, k),
                         virus_reference(n, infection, edges, k))

    def test_joystick_examples_and_all_a(self):
        for name, expected in [('JEROEN', 56), ('JAN', 23), ('A', 0), ('AAAAAA', 0),
                               ('BAAAAA', 1), ('AAAAAB', 2)]:
            self.compare(solve(42860, name), expected)

    def test_joystick_exhaustive_required_positions(self):
        for n in range(1, 9):
            for characters in product('AB', repeat=n):
                name = ''.join(characters)
                self.compare(solve(42860, name), joystick_reference(name), name)

    def test_joystick_random_names(self):
        rng = random.Random(42860)
        for _ in range(300):
            name = ''.join(rng.choice('AAABCDXYZ') for _ in range(rng.randint(1, 9)))
            self.compare(solve(42860, name), joystick_reference(name), name)

    def test_tuple_digit_regex_examples(self):
        self.compare(solve(64065, '{{2},{2,1},{2,1,3},{2,1,3,4}}'), [2, 1, 3, 4])
        self.compare(solve(64065, '{{20,111},{111}}'), [111, 20])
        self.compare(solve(64065, '{{123}}'), [123])

    def test_tuple_random_nested_sets(self):
        rng = random.Random(64065)
        for _ in range(250):
            expected = rng.sample(range(1, 100001), rng.randint(1, 20))
            groups = []
            for length in range(1, len(expected) + 1):
                values = expected[:length]
                rng.shuffle(values)
                groups.append('{' + ','.join(map(str, values)) + '}')
            rng.shuffle(groups)
            self.compare(solve(64065, '{' + ','.join(groups) + '}'), expected)

    def test_filename_regex_examples_and_stability(self):
        self.compare(solve(17686, ['img12.png', 'img10.png', 'img02.png', 'img1.png',
                                  'IMG01.GIF', 'img2.JPG']),
                     ['img1.png', 'IMG01.GIF', 'img02.png', 'img2.JPG', 'img10.png', 'img12.png'])
        self.compare(solve(17686, ['A001z', 'a1x', 'A00001y']), ['A001z', 'a1x', 'A00001y'])
        self.compare(solve(17686, ['F-15', 'F-5', 'F-14']), ['F-5', 'F-14', 'F-15'])

    def test_filename_random_manual_scanner(self):
        rng = random.Random(17686)

        def scanner(filename):
            first = next(i for i, character in enumerate(filename) if character.isdigit())
            end = first
            while end < len(filename) and filename[end].isdigit() and end - first < 5:
                end += 1
            return filename[:first].lower(), int(filename[first:end])

        for _ in range(300):
            files = [rng.choice(['img', 'IMG', 'F-', 'a b']) +
                     str(rng.randint(0, 99999)).zfill(rng.randint(1, 5)) +
                     rng.choice(['.png', 'tail42', '.GIF', ''])
                     for _ in range(rng.randint(1, 50))]
            self.compare(solve(17686, files), sorted(files, key=scanner))

    def test_long_expression_without_middle_deletions(self):
        self.compare(solve(67257, '+'.join(['1'] * 3000)), 3000)

    def test_long_a_run(self):
        self.compare(solve(42860, 'B' + 'A' * 100000 + 'B'), 3)

    def test_large_uniform_process_queue(self):
        self.compare(solve(42587, [9] * 20000, 19999), 20000)


if __name__ == '__main__':
    unittest.main()
