"""해석적 기준·독립 계산·경계 조건으로 참조 모델을 검사한다."""

import math
import unittest

from .models import (adc_midrise, alias_frequency, amdahl, attention,
                     feedback_response, first_order_zoh, ideal_snr_db,
                     logistic_loss_gradient, roofline, sample_cosine,
                     sigmoid, train_logistic)


class SignalTests(unittest.TestCase):
    def test_alias_samples(self):
        # 900 Hz와 100 Hz는 1 kS/s에서 같은 코사인 표본을 만든다.
        high, low = sample_cosine(900, 1000, 100), sample_cosine(100, 1000, 100)
        self.assertLess(max(abs(a - b) for a, b in zip(high, low)), 1e-12)
        self.assertEqual(alias_frequency(2600, 1000), 400)
        self.assertEqual(alias_frequency(-900, 1000), 100)

    def test_nyquist_phase_counterexample(self):
        samples = sample_cosine(500, 1000, 16, math.pi / 2)
        self.assertLess(max(map(abs, samples)), 1e-13)

    def test_adc_codes_and_error(self):
        bits = 8
        for i in range(10001):
            x = i / 10000
            code, restored = adc_midrise(x, bits)
            self.assertTrue(0 <= code < 256)
            self.assertLessEqual(abs(restored - x), 1 / 512 + 1e-15)
        self.assertEqual(adc_midrise(-10, bits)[0], 0)
        self.assertEqual(adc_midrise(10, bits)[0], 255)

    def test_quantization_second_moment(self):
        # 각 구간의 균일 중점 표본으로 적분을 독립적으로 근사한다.
        bits, per_bin = 4, 200
        levels = 1 << bits
        error_squared = []
        for i in range(levels * per_bin):
            x = (i + 0.5) / (levels * per_bin)
            _, reconstructed = adc_midrise(x, bits)
            error_squared.append((reconstructed - x) ** 2)
        measured = math.fsum(error_squared) / len(error_squared)
        theoretical = (1 / levels) ** 2 / 12
        self.assertLess(abs(measured / theoretical - 1), 3e-5)
        self.assertAlmostEqual(ideal_snr_db(12), 74.008, places=3)

    def test_invalid(self):
        for fn, args in [(alias_frequency, (1, 0)), (sample_cosine, (1, 1, -1)),
                         (adc_midrise, (float('nan'), 8)), (adc_midrise, (0, 0))]:
            with self.assertRaises(ValueError):
                fn(*args)


class ControlTests(unittest.TestCase):
    def test_zoh_matches_constant_input_analytical(self):
        a, b = first_order_zoh(0.5, 0.01, 2.0)
        state = 0
        for n in range(1, 201):
            state = a * state + b * 3
            exact = 6 * (1 - math.exp(-n * 0.01 / 0.5))
            self.assertAlmostEqual(state, exact, places=12)

    def test_closed_loop_geometric_and_steady_state(self):
        a, b = first_order_zoh(1.0, 0.1)
        gain = 2.0
        pole = a - b * gain
        equilibrium = b * gain / (1 - pole)
        series = feedback_response(a, b, gain, 1, 100)
        for n, value in enumerate(series):
            self.assertAlmostEqual(value, equilibrium * (1 - pole ** n), places=12)
        self.assertAlmostEqual(equilibrium, 2 / 3)

    def test_excess_gain_and_saturation(self):
        a, b = first_order_zoh(1, 0.1)
        self.assertGreater(abs(a - 25 * b), 1)
        unstable = feedback_response(a, b, 25, 1, 20)
        limited = feedback_response(a, b, 25, 1, 20, limit=0.5)
        self.assertGreater(abs(unstable[-1]), 100)
        self.assertTrue(all(abs(y) <= 0.5 for y in limited))


class LearningTests(unittest.TestCase):
    def test_gradient_central_difference(self):
        xs, ys, w, b = [-2, -0.5, 0.2, 2], [0, 0, 1, 1], 0.7, -0.2
        _, analytic = logistic_loss_gradient(xs, ys, w, b)
        h = 1e-5
        numeric_w = (logistic_loss_gradient(xs, ys, w+h, b)[0] -
                     logistic_loss_gradient(xs, ys, w-h, b)[0]) / (2*h)
        numeric_b = (logistic_loss_gradient(xs, ys, w, b+h)[0] -
                     logistic_loss_gradient(xs, ys, w, b-h)[0]) / (2*h)
        for expected, measured in zip(analytic, (numeric_w, numeric_b)):
            self.assertLess(abs(expected - measured), 1e-9)

    def test_extreme_logits(self):
        self.assertEqual(sigmoid(1000), 1)
        self.assertEqual(sigmoid(-1000), 0)
        loss, gradient = logistic_loss_gradient([-1000, 1000], [1, 0], 1, 0)
        self.assertEqual(loss, 1000)
        self.assertEqual(gradient, (1000, 0))

    def test_training_reduces_loss(self):
        xs, ys = [-2, -1, 1, 2], [0, 0, 1, 1]
        baseline, _ = logistic_loss_gradient(xs, ys, 0, 0)
        w, b, final = train_logistic(xs, ys, iterations=200)
        self.assertLess(final, baseline / 10)
        self.assertGreater(w, 0)
        self.assertAlmostEqual(b, 0)

    def test_attention_uniform_and_one_key(self):
        actual = attention([[0, 0], [0, 0]], [[1, 2], [2, 3]], [[1, 4], [5, 8]])
        self.assertEqual(actual, [[3, 6], [3, 6]])
        self.assertEqual(attention([[2]], [[3]], [[7, -1]]), [[7, -1]])

    def test_attention_manual_and_causal_mask(self):
        expected = (2 + 8 * math.exp(1)) / (1 + math.exp(1))
        actual = attention([[1]], [[0], [1]], [[2], [8]])[0][0]
        self.assertAlmostEqual(actual, expected)
        mask = [[True, False], [True, True]]
        before = attention([[1], [1]], [[1], [1]], [[2], [4]], mask)
        after = attention([[1], [1]], [[1], [1]], [[2], [400]], mask)
        self.assertEqual(before[0], after[0])
        self.assertEqual(before[0], [2])
        self.assertNotEqual(before[1], after[1])

    def test_attention_permutation_and_convex_range(self):
        q, k, v = [[1, 2]], [[2, 1], [-1, 0], [0, 1]], [[2, -3], [7, 5], [-1, 2]]
        before = attention(q, k, v)[0]
        after = attention(q, list(reversed(k)), list(reversed(v)))[0]
        for a, b in zip(before, after):
            self.assertAlmostEqual(a, b)
        self.assertTrue(-1 <= before[0] <= 7)
        self.assertTrue(-3 <= before[1] <= 5)

    def test_attention_numeric_and_shape_guards(self):
        self.assertEqual(attention([[1000]], [[1000], [999]], [[4], [8]])[0][0], 4)
        for args in [([[1]], [[1]], [[2]], [[False]]), ([[1, 2]], [[1]], [[2]]),
                     ([[1]], [[1], [2]], [[2]])]:
            with self.assertRaises(ValueError):
                attention(*args)


class PerformanceTests(unittest.TestCase):
    def test_memory_and_compute_ceilings(self):
        memory = roofline(1e6, 4e6, 1e12, 1e11)
        self.assertEqual(memory['limiting_resource'], 'memory')
        self.assertAlmostEqual(memory['time_lower_bound_s'], 4e-5)
        compute = roofline(1e9, 1e6, 1e12, 1e11)
        self.assertEqual(compute['limiting_resource'], 'compute')
        self.assertAlmostEqual(compute['ceiling_flop_s'], 1e12)

    def test_ceiling_time_consistency_and_reuse(self):
        for work, traffic in [(16, 64), (1e8, 1e6), (100, 100)]:
            report = roofline(work, traffic, 1000, 10)
            self.assertAlmostEqual(work / report['time_lower_bound_s'], report['ceiling_flop_s'])
        first, reused = roofline(100, 100, 1000, 10), roofline(100, 20, 1000, 10)
        self.assertGreater(reused['ceiling_flop_s'], first['ceiling_flop_s'])

    def test_amdahl_limits(self):
        self.assertEqual(amdahl(0, 100), 1)
        self.assertEqual(amdahl(1, 16), 16)
        self.assertAlmostEqual(amdahl(0.9, 10), 1 / 0.19)
        self.assertLess(amdahl(0.9, 1000), 10)
        with self.assertRaises(ValueError):
            amdahl(1.1, 4)


if __name__ == '__main__':
    unittest.main()
