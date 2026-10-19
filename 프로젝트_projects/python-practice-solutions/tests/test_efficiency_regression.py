"""Deterministic local comparisons for seven algorithm changes."""
import copy
import random
import re
import runpy
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1] / 'solutions'
FILES = {
    6: '06_park_mats.py',
    9: '09_bandage.py',
    11: '11_secret_code.py',
    18: '18_remainder_one.py',
    20: '20_divisor_count_sum.py',
    22: '22_new_id.py',
    23: '23_crane_game.py',
}
SOLUTIONS = {number: runpy.run_path(str(ROOT / name))['solution']
             for number, name in FILES.items()}
CALL_COUNTS = {number: 0 for number in FILES}


def call(number, *args):
    CALL_COUNTS[number] += 1
    snapshots = copy.deepcopy(args)
    result = SOLUTIONS[number](*args)
    if args != snapshots:
        raise AssertionError(f'Solution {number} mutated its input')
    return result


def mats_oracle(mats, park):
    possible = []
    for side in mats:
        for row in range(len(park) - side + 1):
            for col in range(len(park[0]) - side + 1):
                if all(park[r][c] == '-1'
                       for r in range(row, row + side)
                       for c in range(col, col + side)):
                    possible.append(side)
    return max(possible, default=-1)


def bandage_oracle(bandage, health, attacks):
    duration, heal, bonus = bandage
    by_time = dict(attacks)
    current, streak = health, 0
    for time in range(1, attacks[-1][0] + 1):
        if time in by_time:
            current -= by_time[time]
            streak = 0
            if current <= 0:
                return -1
        else:
            current += heal
            streak += 1
            if streak == duration:
                current += bonus
                streak = 0
            current = min(current, health)
    return current


def cipher_oracle(text, skip, offset):
    result = []
    for char in text:
        for _ in range(offset):
            char = chr((ord(char) - ord('a') + 1) % 26 + ord('a'))
            while char in skip:
                char = chr((ord(char) - ord('a') + 1) % 26 + ord('a'))
        result.append(char)
    return ''.join(result)


def divisor_sum_oracle(left, right):
    answer = 0
    for number in range(left, right + 1):
        count = sum(number % divisor == 0 for divisor in range(1, number + 1))
        answer += number if count % 2 == 0 else -number
    return answer


def new_id_oracle(value):
    value = ''.join(char for char in value.lower() if char.isalnum() or char in '-_.')
    value = re.sub(r'\.+', '.', value).strip('.') or 'a'
    value = value[:15].rstrip('.')
    return value + value[-1] * max(0, 3 - len(value))


def crane_oracle(board, moves):
    board = copy.deepcopy(board)
    basket = []
    removed = 0
    for move in moves:
        for row in range(len(board)):
            doll = board[row][move - 1]
            if doll:
                board[row][move - 1] = 0
                if basket and basket[-1] == doll:
                    basket.pop()
                    removed += 2
                else:
                    basket.append(doll)
                break
    return removed


class EfficiencyRegressionTests(unittest.TestCase):
    def test_mats_against_exhaustive_rectangles(self):
        rng = random.Random(2026101906)
        for case in range(300):
            rows, cols = rng.randint(1, 7), rng.randint(1, 8)
            park = [['-1' if rng.random() < 0.7 else 'A' for _ in range(cols)]
                    for _ in range(rows)]
            mats = [rng.randint(1, 10) for _ in range(rng.randint(1, 8))]
            with self.subTest(case=case):
                self.assertEqual(call(6, mats, park), mats_oracle(mats, park))

    def test_mats_large_grid_and_boundaries(self):
        park = [['-1'] * 320 for _ in range(240)]
        park[120][160] = 'A'
        self.assertEqual(call(6, [240, 161, 160], park), 160)
        self.assertEqual(call(6, [1, 2], [['A']]), -1)
        self.assertEqual(call(6, [1, 2, 1], [['-1']]), 1)
        self.assertEqual(call(6, [], [['-1']]), -1)

    def test_bandage_against_second_by_second_recovery(self):
        rng = random.Random(2026101909)
        for case in range(500):
            bandage = [rng.randint(1, 8), rng.randint(1, 6), rng.randint(1, 12)]
            health = rng.randint(5, 100)
            times = sorted(rng.sample(range(1, 70), rng.randint(1, 12)))
            attacks = [[time, rng.randint(1, health)] for time in times]
            with self.subTest(case=case):
                self.assertEqual(call(9, bandage, health, attacks),
                                 bandage_oracle(bandage, health, attacks))

    def test_bandage_large_gap_and_attack_boundaries(self):
        self.assertEqual(call(9, [3, 2, 8], 100,
                              [[1, 40], [10**12, 70], [10**12 + 1, 29]]), 1)
        self.assertEqual(call(9, [1, 2, 3], 10, [[1, 10]]), -1)
        self.assertEqual(call(9, [3, 1, 5], 20, [[1, 10], [5, 1]]), 17)

    def test_cipher_against_single_letter_stepping(self):
        rng = random.Random(2026101911)
        letters = 'abcdefghijklmnopqrstuvwxyz'
        for case in range(400):
            skip = ''.join(rng.sample(letters, rng.randint(0, 20)))
            allowed = [char for char in letters if char not in skip]
            text = ''.join(rng.choice(allowed) for _ in range(rng.randint(0, 60)))
            offset = rng.randint(1, 50)
            with self.subTest(case=case):
                self.assertEqual(call(11, text, skip, offset), cipher_oracle(text, skip, offset))

    def test_cipher_wraparound_and_single_remaining_letter(self):
        self.assertEqual(call(11, 'zaz', '', 26), 'zaz')
        self.assertEqual(call(11, 'zzz', 'abcdefghijklmnopqrstuvwxy', 10**12), 'zzz')
        self.assertEqual(call(11, '', 'ab', 3), '')

    def test_remainder_against_direct_modulo_search(self):
        for number in range(3, 501):
            with self.subTest(number=number):
                expected = next(x for x in range(2, number) if number % x == 1)
                self.assertEqual(call(18, number), expected)

    def test_remainder_prime_and_square_boundaries(self):
        self.assertEqual(call(18, 1_000_000_008), 1_000_000_007)
        self.assertEqual(call(18, 101 * 101 + 1), 101)
        self.assertEqual(call(18, 10**12 + 1), 2)

    def test_divisor_sum_against_full_divisor_counts(self):
        rng = random.Random(2026101920)
        for case in range(300):
            left = rng.randint(1, 180)
            right = left + rng.randint(0, 30)
            with self.subTest(case=case):
                self.assertEqual(call(20, left, right), divisor_sum_oracle(left, right))

    def test_divisor_sum_exact_square_boundaries(self):
        square = 10**24
        self.assertEqual(call(20, square - 1, square + 1), square)
        self.assertEqual(call(20, square, square), -square)
        self.assertEqual(call(20, 1, 1), -1)

    def test_divisor_sum_large_intervals_and_partition_additivity(self):
        # Only the first value is a square: the next square is over 2*10**50 away.
        left = 10**100
        right = left + 10**30
        expected = (left + right) * (right - left + 1) // 2 - 2 * left
        self.assertEqual(call(20, left, right), expected)
        for left, right in [(1, 10**18), (10**24 + 17, 10**30 + 5),
                            (10**60, 10**60 + 10**30)]:
            middle = (left + right) // 2
            with self.subTest(left=left, right=right):
                self.assertEqual(call(20, left, right),
                                 call(20, left, middle) + call(20, middle + 1, right))

    def test_new_id_against_separate_normalization_steps(self):
        rng = random.Random(2026101922)
        characters = 'abcXYZ0123456789-_.!@#$%^&*()아이디'
        for case in range(400):
            value = ''.join(rng.choice(characters) for _ in range(rng.randint(0, 250)))
            with self.subTest(case=case):
                self.assertEqual(call(22, value), new_id_oracle(value))

    def test_new_id_long_runs_and_padding_boundaries(self):
        self.assertEqual(call(22, 'A' * 50_000 + '.' * 50_000), 'a' * 15)
        self.assertEqual(call(22, '.' * 100_000), 'aaa')
        self.assertEqual(call(22, 'ab.'), 'abb')
        self.assertEqual(call(22, 'ABCDEFGHIJKLMN.P'), 'abcdefghijklmn')

    def test_crane_against_top_down_board_scanning(self):
        rng = random.Random(2026101923)
        for case in range(400):
            size = rng.randint(1, 8)
            board = [[rng.randrange(5) for _ in range(size)] for _ in range(size)]
            moves = [rng.randint(1, size) for _ in range(rng.randint(0, 60))]
            with self.subTest(case=case):
                self.assertEqual(call(23, board, moves), crane_oracle(board, moves))

    def test_crane_empty_repeated_moves_and_last_row(self):
        self.assertEqual(call(23, [[0, 0], [1, 1]], [1, 1, 2, 2]), 2)
        self.assertEqual(call(23, [[0] * 100 for _ in range(100)], [1] * 100_000), 0)
        self.assertEqual(call(23, [[1]], []), 0)


if __name__ == '__main__':
    unittest.main()
