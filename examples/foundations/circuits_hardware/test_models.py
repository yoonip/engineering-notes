import itertools
import math
import random
import unittest
from collections import deque

from models import (SyncFifo, amat, direct_mapped_hits, load_steps, nmos_current,
                    probe_transfer, rc_euler, rc_step, reflection,
                    resistance_uncertainty, rlc_free, rlc_rk4)


class CircuitTests(unittest.TestCase):
    def test_rc_initial_final_and_time_constant(self):
        self.assertEqual(rc_step(0, 1000, 1e-6, 5, 2), 2)
        self.assertAlmostEqual(rc_step(.001, 1000, 1e-6), 1 - math.exp(-1))
        self.assertAlmostEqual(rc_step(1, 1000, 1e-6, 5, 2), 5)

    def test_euler_convergence_and_stability_boundary(self):
        exact = rc_step(1, 1, 1)
        coarse = abs(rc_euler(20, .05, 1, 1) - exact)
        fine = abs(rc_euler(40, .025, 1, 1) - exact)
        self.assertGreater(coarse / fine, 1.9)
        self.assertLess(coarse / fine, 2.1)
        self.assertGreater(abs(rc_euler(10, 2.1, 1, 1) - 1), 1)

    def test_rlc_all_damping_regimes_against_rk4(self):
        for r in (0, .5, 2, 4, 20):
            with self.subTest(r=r):
                exact = rlc_free(2, r, 1, 1, .8, -.3)
                voltage, _ = rlc_rk4(4000, .0005, r, 1, 1, initial=.8, current=-.3)
                self.assertAlmostEqual(voltage, exact, delta=2e-10)

    def test_lossless_energy_and_dissipation(self):
        for r in (0, .5, 2, 4):
            v, i = rlc_rk4(4000, .001, r, 1, 1)
            energy = (v * v + i * i) / 2
            if r == 0:
                self.assertAlmostEqual(energy, .5, delta=1e-10)
            else:
                self.assertLess(energy, .5)

    def test_nmos_integration_and_boundary(self):
        beta, ov = .002, .8
        # 채널 전하의 수치 적분으로 폐형식과 별도로 비교한다.
        for vds in (.01, .2, .79):
            n = 1000
            integral = sum(ov - (k + .5) * vds / n for k in range(n)) * vds / n
            self.assertAlmostEqual(nmos_current(1.3, vds, .5, beta), beta * integral)
        self.assertAlmostEqual(nmos_current(1.3, ov, .5, beta), beta * ov * ov / 2)
        self.assertEqual(nmos_current(.4, 1, .5, beta), 0)
        self.assertEqual(nmos_current(1.3, 0, .5, beta), 0)

    def test_nmos_monotonic_and_geometry_scaling(self):
        currents = [nmos_current(1.3, k / 100, .5, .002) for k in range(201)]
        self.assertTrue(all(a <= b + 1e-15 for a, b in zip(currents, currents[1:])))
        self.assertAlmostEqual(nmos_current(1.3, .2, .5, .004), 2 * nmos_current(1.3, .2, .5, .002))


class DigitalTests(unittest.TestCase):
    def test_fifo_all_request_sequences(self):
        for depth in (1, 2, 3, 4):
            for requests in itertools.product(range(4), repeat=6):
                fifo, reference = SyncFifo(depth), deque()
                for value, request in enumerate(requests):
                    w, r = bool(request & 1), bool(request & 2)
                    old_count = len(reference)
                    aw, ar = w and old_count < depth, r and old_count > 0
                    expected = reference.popleft() if ar else None
                    if aw:
                        reference.append(value)
                    self.assertEqual(fifo.cycle(w, r, value), (aw, ar, expected))
                    self.assertEqual(fifo.count, len(reference))
                    self.assertTrue(0 <= fifo.count <= depth)

    def test_fifo_random_wrap_reset_and_order(self):
        rng = random.Random(773)
        for depth in (1, 3, 8, 17):
            fifo, reference = SyncFifo(depth), deque()
            for value in range(5000):
                if value % 773 == 0:
                    fifo.reset()
                    reference.clear()
                w, r = bool(rng.getrandbits(1)), bool(rng.getrandbits(1))
                old = len(reference)
                aw, ar = w and old < depth, r and old > 0
                expected = reference.popleft() if ar else None
                if aw:
                    reference.append(value)
                self.assertEqual(fifo.cycle(w, r, value), (aw, ar, expected))
                self.assertEqual(fifo.count, len(reference))

    def test_cache_known_trace_and_locality(self):
        self.assertEqual(list(direct_mapped_hits([0, 1, 7, 8, 0], 2, 4)),
                         [False, True, False, False, False])
        self.assertEqual(sum(direct_mapped_hits(range(64), 16, 4)), 60)
        self.assertEqual(sum(direct_mapped_hits([0, 64] * 30, 16, 4)), 0)

    def test_cache_reference_and_amat_counting(self):
        rng = random.Random(97)
        addresses = [rng.randrange(256) for _ in range(2000)]
        resident, expected = {}, []
        for address in addresses:
            block = address // 8
            index = block % 7
            expected.append(resident.get(index) == block)
            resident[index] = block
        actual = list(direct_mapped_hits(addresses, 8, 7))
        self.assertEqual(actual, expected)
        observed = sum(2 if hit else 102 for hit in actual) / len(actual)
        self.assertAlmostEqual(amat(2, 1 - sum(actual) / len(actual), 100), observed)


class SignalMeasurementTests(unittest.TestCase):
    def test_reflection_boundaries_and_energy(self):
        self.assertEqual(reflection(50, 50), 0)
        self.assertEqual(reflection(0, 50), -1)
        self.assertEqual(reflection(math.inf, 50), 1)
        for load in (1, 25, 100, 1000):
            gamma = reflection(load, 50)
            transmitted = (1 + gamma) ** 2 * 50 / load
            self.assertAlmostEqual(gamma * gamma + transmitted, 1)

    def test_bounce_timing_dc_and_source_termination(self):
        for source, load in ((10, 100), (50, 50), (80, 20), (50, math.inf)):
            steps = list(load_steps(3.3, source, load, 50, 1e-9, 100))
            expected = 3.3 if load == math.inf else 3.3 * load / (source + load)
            self.assertAlmostEqual(steps[-1][1], expected)
            self.assertAlmostEqual(steps[0][0], 1e-9)
            self.assertAlmostEqual(steps[1][0], 3e-9)
        levels = [v for _, v in load_steps(3.3, 50, math.inf, 50, 1e-9)]
        self.assertEqual(levels, [3.3] * len(levels))

    def test_probe_dc_high_frequency_and_pole(self):
        self.assertAlmostEqual(probe_transfer(0, 1000, 1e6, 10e-12).real, 1e6 / 1001000)
        parallel = 1000 * 1e6 / 1001000
        pole = 1 / (2 * math.pi * parallel * 10e-12)
        dc = abs(probe_transfer(0, 1000, 1e6, 10e-12))
        self.assertAlmostEqual(abs(probe_transfer(pole, 1000, 1e6, 10e-12)), dc / math.sqrt(2))
        self.assertLess(abs(probe_transfer(1e12, 1000, 1e6, 10e-12)), 1e-4)

    def test_resistance_uncertainty_and_correlation(self):
        u = resistance_uncertainty(1, .001, .001, 1e-6)
        self.assertAlmostEqual(u, math.sqrt(2))
        self.assertAlmostEqual(resistance_uncertainty(1, .001, .001, 1e-6, 1e-9), 0, delta=1e-7)
        # 독립적인 작은 사각 분포의 몬테카를로 표준편차와 선형 전파를 비교한다.
        rng = random.Random(1297)
        samples = [(1 + rng.uniform(-1, 1) * math.sqrt(3) * .001)
                   / (.001 + rng.uniform(-1, 1) * math.sqrt(3) * 1e-6) for _ in range(30000)]
        mean = sum(samples) / len(samples)
        spread = math.sqrt(sum((x - mean) ** 2 for x in samples) / (len(samples) - 1))
        self.assertAlmostEqual(spread, u, delta=.03 * u)

    def test_invalid_dimensions(self):
        for call in (lambda: rc_step(1, 0, 1), lambda: SyncFifo(0),
                     lambda: nmos_current(1, -1, .5, .001),
                     lambda: reflection(-1, 50),
                     lambda: resistance_uncertainty(1, 0, .1, .1)):
            with self.assertRaises(ValueError):
                call()


if __name__ == "__main__":
    unittest.main()
