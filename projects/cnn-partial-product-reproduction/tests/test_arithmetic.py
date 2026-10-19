"""Fast, offline checks of signed arithmetic; no ML runtime or SPICE needed."""
from pathlib import Path
import importlib.util
import unittest

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "public_column_arithmetic", ROOT / "circuit" / "arithmetic.py"
)
ARITHMETIC = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ARITHMETIC)


def direct_signed_columns(a, b, width, dropped):
    """Independent signed-weight matrix, without Baugh-Wooley complements."""
    total = 0
    for i in range(width):
        wi = -(1 << i) if i == width - 1 else 1 << i
        for j in range(width):
            if i + j < dropped:
                continue
            wj = -(1 << j) if j == width - 1 else 1 << j
            total += ((a >> i) & 1) * ((b >> j) & 1) * wi * wj
    return total


class SignedColumnTests(unittest.TestCase):
    def test_exact_mode_all_input_pairs(self):
        for width in (6, 8):
            values = np.arange(-(1 << (width - 1)), 1 << (width - 1))
            with self.subTest(width=width):
                np.testing.assert_array_equal(
                    ARITHMETIC.column_mask_mul(values[:, None], values[None, :], width, 0),
                    values[:, None] * values[None, :],
                )

    def test_independent_signed_matrix_and_baugh_wooley(self):
        rng = np.random.default_rng(19)
        for width in (6, 8):
            low, high = -(1 << (width - 1)), (1 << (width - 1)) - 1
            boundaries = (low, low + 1, -1, 0, 1, high - 1, high)
            pairs = [(a, b) for a in boundaries for b in boundaries]
            pairs += [tuple(map(int, p)) for p in rng.integers(low, high + 1, (80, 2))]
            for dropped in range(width):
                for a, b in pairs:
                    expected = direct_signed_columns(a, b, width, dropped)
                    with self.subTest(width=width, k=dropped, a=a, b=b):
                        self.assertEqual(int(ARITHMETIC.column_mask_mul(a, b, width, dropped)), expected)
                        self.assertEqual(ARITHMETIC.baugh_wooley_mul(a, b, width, dropped), expected)

    def test_columns_are_not_product_or_accumulator_masking(self):
        self.assertEqual(int(ARITHMETIC.column_mask_mul(3, 3, 6, 2)), 4)
        self.assertEqual((3 * 3 >> 2) << 2, 8)
        # Even k=1 differs when masking once after a sum of two products.
        self.assertEqual(((1 * 1 + 1 * 1) >> 1) << 1, 2)
        self.assertEqual(sum(int(ARITHMETIC.column_mask_mul(1, 1, 6, 1)) for _ in range(2)), 0)

    def test_signed_negative_product_can_cross_zero(self):
        self.assertEqual(int(ARITHMETIC.column_mask_mul(-1, -1, 6, 5)), -128)
        self.assertEqual(int(ARITHMETIC.column_mask_mul(-32, -32, 6, 5)), 1024)

    def test_error_is_nonpositive_and_uses_supported_low_columns(self):
        for width in (6, 8):
            values = np.arange(-(1 << (width - 1)), 1 << (width - 1))
            exact = values[:, None] * values[None, :]
            for dropped in range(width):
                result = ARITHMETIC.column_mask_mul(values[:, None], values[None, :], width, dropped)
                loss = exact - result
                worst = sum((column + 1) * (1 << column) for column in range(dropped))
                with self.subTest(width=width, k=dropped):
                    self.assertTrue(np.all(loss >= 0))
                    self.assertEqual(int(loss.max()), worst)
                    np.testing.assert_array_equal(result, result.T)

    def test_lut_indexing_and_broadcasting(self):
        for width in (6, 8):
            low = -(1 << (width - 1))
            lut = ARITHMETIC.make_lut(width, 2)
            self.assertEqual(lut.shape, (1 << width, 1 << width))
            for a, b in ((low, low), (-1, 1), (3, 3)):
                self.assertEqual(int(lut[a - low, b - low]), direct_signed_columns(a, b, width, 2))

    def test_invalid_masks_and_out_of_range_operands(self):
        for width in (6, 8):
            for dropped in (-1, width, width + 1):
                with self.assertRaises(ValueError):
                    ARITHMETIC.column_mask_mul(0, 0, width, dropped)
                with self.assertRaises(ValueError):
                    ARITHMETIC.baugh_wooley_mul(0, 0, width, dropped)
            for value in (-(1 << (width - 1)) - 1, 1 << (width - 1)):
                with self.assertRaises(ValueError):
                    ARITHMETIC.column_mask_mul(value, 0, width, 0)
                with self.assertRaises(ValueError):
                    ARITHMETIC.column_mask_mul(0, value, width, 0)

    def test_accumulator_width_includes_most_negative_squared(self):
        for width, terms, expected in ((6, 784, 21), (8, 784, 25),
                                       (6, 4608, 24), (8, 4608, 28)):
            actual = ARITHMETIC.accumulator_width(width, terms)
            worst_positive = terms * (1 << (2 * width - 2))
            with self.subTest(width=width, terms=terms):
                self.assertEqual(actual, expected)
                self.assertLessEqual(worst_positive, (1 << (actual - 1)) - 1)
                self.assertGreater(worst_positive, (1 << (actual - 2)) - 1)
        with self.assertRaises(ValueError):
            ARITHMETIC.accumulator_width(6, 0)

    def test_twos_complement_decode(self):
        for width in (6, 8, 16, 32):
            self.assertEqual(ARITHMETIC.signed_value((1 << width) - 1, width), -1)
            self.assertEqual(ARITHMETIC.signed_value(1 << (width - 1), width), -(1 << (width - 1)))
            self.assertEqual(ARITHMETIC.signed_value((1 << width) + 3, width), 3)


if __name__ == "__main__":
    unittest.main()
