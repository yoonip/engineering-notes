import math
from pathlib import Path
import random
import statistics
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from models import (
    decay_euler, heat_ftcs, least_squares_qr, mean_variance,
    normal_mean_interval, oscillator_verlet, resistance_uncertainty,
)


class MeasurementTests(unittest.TestCase):
    def test_resistance_independent_reference(self):
        r, u = resistance_uncertainty(2.0, 0.01, 0.002, 0.00001)
        self.assertEqual(r, 200.0)
        self.assertAlmostEqual(u, math.sqrt(0.08), places=12)

    def test_common_scale_cancels_to_first_order(self):
        self.assertLess(resistance_uncertainty(2, 0.01, 0.002, 0.00001, 1)[1], 1e-8)

    def test_negative_correlation_increases_ratio_uncertainty(self):
        self.assertAlmostEqual(resistance_uncertainty(2, 0.01, 0.002, 0.00001, -1)[1], .4)

    def test_reject_invalid_measurements(self):
        for args in ((1, 0, 0, 0), (1, 1, -1, 0), (1, 1, 1, 1, 1.1), (math.nan, 1, 0, 0)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                resistance_uncertainty(*args)


class LeastSquaresTests(unittest.TestCase):
    def test_calibration_line(self):
        self.assertSequenceClose(least_squares_qr([[1, 0], [1, 1], [1, 2]], [1, 2, 2]), [7/6, .5])

    def assertSequenceClose(self, a, b):
        for x, y in zip(a, b, strict=True):
            self.assertAlmostEqual(x, y, places=10)

    def test_exact_polynomial(self):
        points = [-2, -1, 0, 1, 2, 3]
        self.assertSequenceClose(least_squares_qr([[1, t, t*t] for t in points], [2-3*t+.5*t*t for t in points]), [2, -3, .5])

    def test_residual_orthogonality(self):
        rng = random.Random(48)
        a = [[1, rng.uniform(-2, 2), rng.uniform(-2, 2)] for _ in range(30)]
        b = [rng.uniform(-4, 4) for _ in a]
        x = least_squares_qr(a, b)
        residual = [sum(v*z for v, z in zip(row, x))-target for row, target in zip(a, b)]
        for j in range(3):
            self.assertLess(abs(sum(row[j]*r for row, r in zip(a, residual))), 1e-12)

    def test_common_scale_preserves_solution(self):
        for scale in (1e-9, 1, 1e9):
            self.assertSequenceClose(least_squares_qr([[scale, 0], [scale, scale], [scale, 2*scale]], [scale, 2*scale, 2*scale]), [7/6, .5])

    def test_rank_deficiency_and_invalid_shape(self):
        for a, b in (([[1, 2], [2, 4]], [1, 2]), ([[1, 1], [1, 1+1e-14]], [1, 2]), ([[1, 2]], [1]), ([[1], [1, 2]], [1, 2]), ([], [])):
            with self.subTest(a=a), self.assertRaises(ValueError):
                least_squares_qr(a, b)


class EstimationTests(unittest.TestCase):
    def test_statistics_independent_reference(self):
        data = [1e6+v/10 for v in range(23)]
        n, mean, variance = mean_variance(iter(data))
        self.assertEqual(n, len(data))
        self.assertAlmostEqual(mean, statistics.mean(data), places=8)
        self.assertAlmostEqual(variance, statistics.variance(data), places=8)

    def test_known_sigma_quantile(self):
        lo, hi = normal_mean_interval(10, 2, 100)
        self.assertAlmostEqual(hi-10, .3919927969080108, places=12)
        self.assertAlmostEqual(10-lo, hi-10, places=12)

    def test_more_samples_reduce_width(self):
        a = normal_mean_interval(0, 1, 25)
        b = normal_mean_interval(0, 1, 100)
        self.assertAlmostEqual(a[1], 2*b[1])

    def test_seeded_normal_interval_coverage(self):
        rng = random.Random(20261019)
        hits = 0
        for _ in range(2000):
            mean = sum(rng.gauss(3, 2) for _ in range(25)) / 25
            lo, hi = normal_mean_interval(mean, 2, 25)
            hits += lo <= 3 <= hi
        self.assertLess(abs(hits/2000-.95), .025)

    def test_variance_and_interval_boundaries(self):
        self.assertEqual(mean_variance([4, 4, 4]), (3, 4, 0))
        self.assertEqual(normal_mean_interval(4, 0, 2), (4, 4))
        for values in ([], [1], [1, math.inf]):
            with self.assertRaises(ValueError):
                mean_variance(values)
        for args in ((0, -1, 2), (0, 1, 0), (0, 1, 4, 1)):
            with self.assertRaises(ValueError):
                normal_mean_interval(*args)


class TimeIntegrationTests(unittest.TestCase):
    def test_euler_first_order_convergence(self):
        errors = [abs(decay_euler(1, 1, 1, n)-math.exp(-1)) for n in (20, 40, 80)]
        self.assertTrue(1.9 < errors[0]/errors[1] < 2.1)
        self.assertTrue(1.9 < errors[1]/errors[2] < 2.1)

    def test_euler_monotonic_and_zero_time(self):
        self.assertEqual(decay_euler(3, 1, 0, 3), 3)
        self.assertEqual(decay_euler(0, 1, 2, 4), 0)
        self.assertTrue(0 < decay_euler(1, 1, 1, 10) < 1)

    def test_euler_stability_guard(self):
        for args in ((1, 1, 2, 1), (1, 0, 1, 2), (1, 1, 1, 0)):
            with self.assertRaises(ValueError):
                decay_euler(*args)

    def test_verlet_exact_solution_and_second_order(self):
        t = 2.3
        exact_x = .3*math.cos(2*t) + .1*math.sin(2*t)
        errors = []
        for steps in (100, 200):
            last = None
            for last in oscillator_verlet(1, 4, .3, .2, t, steps):
                pass
            errors.append(abs(last[1]-exact_x))
        self.assertTrue(3.8 < errors[0]/errors[1] < 4.2)

    def test_verlet_long_time_energy(self):
        energies = [.5*v*v+2*x*x for _, x, v in oscillator_verlet(1, 4, .3, 0, 100, 10000)]
        self.assertLess(max(abs(e-.18) for e in energies)/.18, .00011)

    def test_verlet_equilibrium_and_invalid_step(self):
        self.assertTrue(all(x == v == 0 for _, x, v in oscillator_verlet(1, 1, 0, 0, 1, 10)))
        with self.assertRaises(ValueError):
            list(oscillator_verlet(1, 4, 1, 0, 1, 1))


class HeatTests(unittest.TestCase):
    def test_constant_and_linear_steady_states(self):
        for initial in ([7]*11, list(range(11))):
            result = heat_ftcs(initial, 1, 1, .1, 100)
            for x, y in zip(result, initial):
                self.assertAlmostEqual(x, y, places=12)

    def test_sine_mode_and_grid_convergence(self):
        errors = []
        for cells in (20, 40):
            initial = [math.sin(math.pi*i/cells) for i in range(cells+1)]
            result = heat_ftcs(initial, 1, 1, .05, cells*cells//2)
            exact = [v*math.exp(-math.pi**2*.05) for v in initial]
            errors.append(max(abs(a-b) for a, b in zip(result, exact)))
            self.assertEqual(result[0], initial[0])
            self.assertEqual(result[-1], initial[-1])
        self.assertTrue(3.9 < errors[0]/errors[1] < 4.1)

    def test_discrete_maximum_principle(self):
        initial = [0, 1, 8, 3, 2, 1, 0]
        result = heat_ftcs(initial, 1, 1, .5, 40)
        self.assertTrue(all(0 <= v <= 8 for v in result))

    def test_stability_guard_and_zero_time(self):
        self.assertEqual(heat_ftcs([0, 1, 0], 1, 1, 0, 10), [0, 1, 0])
        for args in (([0, 1, 0], 1, 1, 1, 1), ([0, 0], 1, 1, 1, 100), ([0, math.nan, 0], 1, 1, 0, 1)):
            with self.assertRaises(ValueError):
                heat_ftcs(*args)


if __name__ == "__main__":
    unittest.main()
