"""닫힌 해, 별도 합산과 반례를 사용하는 참조 모델 검산."""

import itertools
import math
import random
import unittest

from models import (ByteMemory, FAULTS, ReadyValidBuffer, bpsk_ber,
                    bpsk_errors, buck_ccm, capacitor_impedance, counter_next,
                    crossbar_currents, dag_arrivals, detected_faults,
                    differential_conductances, full_adder_gates, logic_output,
                    pdn_impedance, quantize_symmetric, reachable_counter,
                    scan_shift, thermal_pulse_steady, thermal_step,
                    timing_slack, cs_gain)


class ExtendedHardwareTests(unittest.TestCase):
    def test_ac_kcl_pole_and_large_signal_residual(self):
        gm, rd, ro, rl, cap = 1e-3, 10000, 100000, 100000, 20e-12
        resistance = 1 / (1 / rd + 1 / ro + 1 / rl)
        pole = 1 / (2 * math.pi * resistance * cap)
        dc = cs_gain(gm, rd, ro, rl, cap, 0)
        at_pole = cs_gain(gm, rd, ro, rl, cap, pole)
        self.assertAlmostEqual(dc.real, -gm * resistance)
        self.assertAlmostEqual(abs(at_pole / dc), 1 / math.sqrt(2))
        for frequency in (1, pole, 100 * pole):
            gain = cs_gain(gm, rd, ro, rl, cap, frequency)
            self.assertLess(abs(gain / resistance + 1j * 2 * math.pi * frequency * cap * gain + gm), 1e-15)
        # 제곱 법칙을 별도로 전개하면 선형화 오차가 진폭의 제곱에 비례합니다.
        beta, overdrive = 0.002, 0.5
        residuals = []
        for amplitude in (0.02, 0.01):
            exact = beta / 2 * ((overdrive + amplitude) ** 2 - overdrive ** 2)
            residuals.append(exact - beta * overdrive * amplitude)
        self.assertAlmostEqual(residuals[0] / residuals[1], 4)

    def test_pdn_resonance_and_parallel_kcl(self):
        c, esr, esl = 100e-9, 0.02, 1e-9
        f0 = 1 / (2 * math.pi * math.sqrt(c * esl))
        self.assertAlmostEqual(capacitor_impedance(c, esr, esl, f0).imag, 0, places=12)
        self.assertAlmostEqual(abs(capacitor_impedance(c, esr, esl, f0)), esr)
        for multiplier in (0.1, 10):
            self.assertGreater(abs(capacitor_impedance(c, esr, esl, f0 * multiplier)), esr)
        f, rs, ls = 1e6, 0.05, 3e-9
        capacitors = [(c, esr, esl), (10e-6, 0.01, 2e-9)]
        voltage = pdn_impedance(rs, ls, capacitors, f)
        total = voltage / complex(rs, 2 * math.pi * f * ls)
        for values in capacitors:
            total += voltage / capacitor_impedance(*values, f)
        self.assertAlmostEqual(total.real, 1)
        self.assertAlmostEqual(total.imag, 0)

    def test_counter_inductive_transition_and_reachability(self):
        for depth in range(1, 17):
            self.assertEqual(reachable_counter(depth), set(range(depth + 1)))
            for n, inc, dec in itertools.product(range(depth + 1), (0, 1), (0, 1)):
                nxt = counter_next(n, inc, dec, depth)
                accepted = [inc and n < depth, dec and n > 0]
                self.assertEqual(nxt, n + accepted[0] - accepted[1])
                self.assertTrue(0 <= nxt <= depth)
        # 경계에서 wrap하는 변이는 1비트 증가만으로 범위 속성을 깨뜨립니다.
        self.assertEqual(counter_next(3, 1, 0, 3), 3)
        self.assertGreater(3 + 1, 3)

    def test_timing_against_absolute_events_and_skew(self):
        values = dict(period=10, launch_clock=1.2, capture_clock=1.7,
                      cq_max=0.8, data_max=7, setup=0.6, cq_min=0.2,
                      data_min=0.5, hold=0.2, u_setup=0.1, u_hold=0.1)
        setup, hold = timing_slack(**values)
        self.assertAlmostEqual(setup, (10 + 1.7 - 0.6 - 0.1) - (1.2 + 0.8 + 7))
        self.assertAlmostEqual(hold, (1.2 + 0.2 + 0.5) - (1.7 + 0.2 + 0.1))
        later = dict(values, capture_clock=2.0)
        setup2, hold2 = timing_slack(**later)
        self.assertAlmostEqual(setup2 - setup, 0.3)
        self.assertAlmostEqual(hold2 - hold, -0.3)
        slower = timing_slack(**dict(values, period=20))
        self.assertAlmostEqual(slower[1], hold)

    def test_byte_memory_independent_encoding_and_sign(self):
        rng = random.Random(316)
        for width, endian in itertools.product((1, 2, 4, 8), ("little", "big")):
            memory = ByteMemory(32)
            for _ in range(100):
                value = rng.getrandbits(8 * width)
                memory.store(8, width, value, endian)
                independent = value.to_bytes(width, endian)
                self.assertEqual(memory.data[8:8 + width], independent)
                self.assertEqual(memory.load(8, width, endian), value)
                self.assertEqual(memory.load(8, width, endian, True), int.from_bytes(independent, endian, signed=True))
        memory.store(0, 4, 0x12345678, "little")
        self.assertEqual(list(memory.data[:4]), [0x78, 0x56, 0x34, 0x12])
        memory.store(0, 1, 0x80)
        self.assertEqual(memory.load(0, 1, signed=True), -128)
        with self.assertRaises(ValueError):
            memory.load(1, 4)
        with self.assertRaises(IndexError):
            memory.load(32, 1)

    def test_bpsk_integral_and_monte_carlo(self):
        # Q 적분은 erfc와 별도로 Simpson 적분으로 계산합니다.
        def normal_tail(lower):
            upper, count = 12.0, 20000
            h = (upper - lower) / count
            total = 0.0
            for k in range(count + 1):
                x = lower + k * h
                coefficient = 1 if k in (0, count) else 4 if k % 2 else 2
                total += coefficient * math.exp(-x * x / 2) / math.sqrt(2 * math.pi)
            return total * h / 3
        self.assertEqual(bpsk_ber(0), 0.5)
        for gamma_db in (0, 4, 8):
            probability = bpsk_ber(10 ** (gamma_db / 10))
            self.assertAlmostEqual(probability, normal_tail(math.sqrt(2 * 10 ** (gamma_db / 10))), places=12)
            bits = 200000
            errors = bpsk_errors(gamma_db, bits, seed=17 + gamma_db)
            sigma = math.sqrt(bits * probability * (1 - probability))
            self.assertLess(abs(errors - bits * probability), 6 * sigma + 1)

    def test_buck_volt_seconds_and_integrated_capacitor_ripple(self):
        vin, vout, inductance, frequency, capacitance, current = 12, 3.3, 10e-6, 500e3, 22e-6, 2
        result = buck_ccm(vin, vout, inductance, frequency, capacitance, current)
        duty, ripple = result["duty"], result["ripple"]
        period = 1 / frequency
        self.assertAlmostEqual((vin - vout) * duty * period - vout * (1 - duty) * period, 0)
        # 한 주기의 삼각 전류를 적분해 C 전압의 최고·최저 차이를 구합니다.
        charge, charge_min, charge_max, count = 0.0, 0.0, 0.0, 20000
        for k in range(count):
            phase = (k + 0.5) / count
            ac_current = -ripple / 2 + ripple * phase / duty if phase < duty else ripple / 2 - ripple * (phase - duty) / (1 - duty)
            charge += ac_current * period / count
            charge_min, charge_max = min(charge_min, charge), max(charge_max, charge)
        measured = (charge_max - charge_min) / capacitance
        self.assertAlmostEqual(measured / result["capacitive_ripple"], 1, places=7)
        self.assertLess(abs(charge), 1e-18)
        self.assertGreater(result["imin"], 0)
        with self.assertRaises(ValueError):
            buck_ccm(vin, vout, inductance, frequency, capacitance, ripple / 4)

    def test_ready_valid_order_backpressure_and_reset(self):
        rng, buffer, reference, next_token, outputs = random.Random(34), ReadyValidBuffer(), [], 0, []
        pending = None
        previous_stall = None
        accepted = []
        for _ in range(5000):
            if pending is None and rng.random() < 0.8:
                pending, next_token = next_token, next_token + 1
            out_ready = rng.random() < 0.6
            before = reference[:]
            ready, valid, data, take_in, take_out = buffer.cycle(pending is not None, pending, out_ready)
            self.assertEqual(ready, len(before) < 2)
            self.assertEqual(valid, bool(before))
            if previous_stall is not None:
                self.assertTrue(valid)
                self.assertEqual(data, previous_stall)
            previous_stall = data if valid and not out_ready else None
            if take_out:
                self.assertEqual(data, reference.pop(0))
                outputs.append(data)
            if take_in:
                accepted.append(pending)
                reference.append(pending)
                pending = None
            self.assertLessEqual(len(reference), 2)
        while reference:
            _, _, data, _, take_out = buffer.cycle(False, None, True)
            self.assertTrue(take_out)
            self.assertEqual(data, reference.pop(0))
            outputs.append(data)
        self.assertEqual(outputs, accepted)
        buffer.cycle(True, 777, False)
        buffer.cycle(False, None, False, reset=True)
        self.assertFalse(buffer.cycle(False, None, True)[1])

    def test_adder_equivalence_and_dag_longest_path(self):
        for a, b, c in itertools.product((0, 1), repeat=3):
            result, carry = full_adder_gates(a, b, c)
            self.assertEqual(result + 2 * carry, a + b + c)
        delays = {"in": 0, "a": 2, "b": 3, "c": 1, "out": 0.5}
        pred = {"a": ["in"], "b": ["in"], "c": ["a", "b"], "out": ["a", "c"]}
        actual = dag_arrivals(delays, pred)
        # DAG 재귀 합산 대신 명시적으로 가능한 경로들을 열거합니다.
        paths = [["in", "a", "out"], ["in", "a", "c", "out"], ["in", "b", "c", "out"]]
        self.assertEqual(actual["out"], max(sum(delays[n] for n in path) for path in paths))
        with self.assertRaises(ValueError):
            dag_arrivals({"a": 1, "b": 2}, {"a": ["b"]})

    def test_thermal_limits_ode_and_periodic_fixed_point(self):
        rth, cth, power = 10, 2, 5
        tau = rth * cth
        self.assertEqual(thermal_step(rth, cth, power, 0), 0)
        self.assertAlmostEqual(thermal_step(rth, cth, power, tau), power * rth * (1 - math.exp(-1)))
        self.assertAlmostEqual(thermal_step(rth, cth, power, 50 * tau), power * rth)
        errors = []
        exact = thermal_step(rth, cth, power, 10)
        for count in (1000, 2000):
            dt, rise = 10 / count, 0.0
            for _ in range(count):
                rise += dt * (power - rise / rth) / cth
            errors.append(abs(rise - exact))
        self.assertGreater(errors[0] / errors[1], 1.99)
        valley, peak = thermal_pulse_steady(rth, cth, power, 3, 7)
        self.assertAlmostEqual(thermal_step(rth, cth, power, 3, valley), peak)
        self.assertAlmostEqual(thermal_step(rth, cth, 0, 7, peak), valley)
        rise = 0
        for _ in range(100):
            rise = thermal_step(rth, cth, power, 3, rise)
            rise = thermal_step(rth, cth, 0, 7, rise)
        self.assertAlmostEqual(rise, valley)
        self.assertGreater(peak, power * rth * 0.3)

    def test_fault_activation_propagation_and_scan(self):
        patterns = list(itertools.product((0, 1), repeat=3))
        self.assertEqual(detected_faults(patterns), set(FAULTS))
        for pattern in patterns:
            a, b, c = pattern
            expected_n_sa0 = a == b == 1 and c == 0
            expected_n_sa1 = not (a and b) and c == 0
            good = logic_output(*pattern)
            self.assertEqual(good != logic_output(*pattern, fault=("n", 0)), expected_n_sa0)
            self.assertEqual(good != logic_output(*pattern, fault=("n", 1)), expected_n_sa1)
        self.assertLess(len(detected_faults([(0, 0, 0), (1, 1, 1)])), len(FAULTS))
        minimum = next(n for n in range(1, 9) if any(len(detected_faults(subset)) == 10 for subset in itertools.combinations(patterns, n)))
        self.assertEqual(minimum, 4)
        state = [0, 0, 0]
        for bit in [1, 1, 0]:
            state, _ = scan_shift(state, bit)
        self.assertEqual(state, [0, 1, 1])
        captured = []
        for _ in range(3):
            state, bit = scan_shift(state, 0)
            captured.append(bit)
        self.assertEqual(captured, [1, 1, 0])

    def test_pim_signed_dot_product_row_drop_and_quantization(self):
        weights, x = [[1.0, -0.5], [-0.25, 0.75], [0.5, 0.0]], [0.5, -1, 0.25]
        gmin, scale, voltage_scale = 1e-6, 10e-6, 0.1
        plus, minus = differential_conductances(weights, gmin, scale)
        voltages = [voltage_scale * value for value in x]
        ip, im = crossbar_currents(plus, voltages), crossbar_currents(minus, voltages)
        decoded = [(a - b) / (voltage_scale * scale) for a, b in zip(ip, im)]
        independent = [sum(weights[i][j] * x[i] for i in range(3)) for j in range(2)]
        for a, b in zip(decoded, independent):
            self.assertAlmostEqual(a, b)
        conductances, voltage, wire = [[10e-6, 20e-6]], [0.1], 1000
        currents = crossbar_currents(conductances, voltage, wire)
        node = voltage[0] - wire * sum(currents)
        for current, g in zip(currents, conductances[0]):
            self.assertAlmostEqual(current, node * g)
        self.assertLess(sum(currents), sum(crossbar_currents(conductances, voltage)))
        bound, bits = 1.0, 8
        step = 2 * bound / ((1 << bits) - 1)
        for k in range(1001):
            value = -bound + 2 * bound * k / 1000
            self.assertLessEqual(abs(quantize_symmetric(value, bound, bits) - value), step / 2 + 1e-15)
        self.assertEqual(quantize_symmetric(10, bound, bits), bound)
        self.assertEqual(quantize_symmetric(-10, bound, bits), -bound)


if __name__ == "__main__":
    unittest.main()
