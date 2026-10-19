"""경계값, 독립 기준해와 상태 순서를 이용한 검증."""

from fractions import Fraction
from itertools import permutations, product
import json
import math
from pathlib import Path
import random
import tempfile
import unittest
from unittest.mock import patch

import extended_models as m


class ExtendedSystemsTests(unittest.TestCase):
    def test_mode_owner_does_not_fall_through(self):
        self.assertFalse(m.unix_mode_allows(0o047, True, True, 4))
        self.assertTrue(m.unix_mode_allows(0o047, False, True, 4))
        self.assertTrue(m.unix_mode_allows(0o640, True, False, 6))
        self.assertFalse(m.unix_mode_allows(0o640, False, False, 4))

    def test_mode_all_bit_combinations(self):
        for mode in range(0o1000):
            for shift, owner, group in ((6, True, False), (3, False, True), (0, False, False)):
                bits = format(mode, "09b")[6-shift:9-shift]
                for requested in range(8):
                    needed = format(requested, "03b")
                    expected = all(want == "0" or have == "1" for have, want in zip(bits, needed))
                    self.assertEqual(m.unix_mode_allows(mode, owner, group, requested), expected)

    def test_pipeline_failures(self):
        self.assertEqual(m.pipeline_status([2, 0, 0]), 0)
        self.assertEqual(m.pipeline_status([2, 3, 0], True), 3)
        self.assertEqual(m.pipeline_status([0, 0], True), 0)
        with self.assertRaises(ValueError):
            m.pipeline_status([])

    def test_dependency_diamond(self):
        graph = {"merge": ["left", "right"], "left": ["base"], "right": ["base"], "base": []}
        order = m.dependency_order(graph)
        self.assertEqual(set(order), set(graph))
        for node, parents in graph.items():
            for parent in parents:
                self.assertLess(order.index(parent), order.index(node))

    def test_dependency_errors(self):
        for graph in ({"a": ["b"]}, {"a": ["b"], "b": ["a"]}, {"a": ["a"]}):
            with self.assertRaises(ValueError):
                m.dependency_order(graph)

    def test_digest_order_and_boundaries(self):
        self.assertEqual(m.snapshot_digest({"a": b"1", "b": b"2"}), m.snapshot_digest({"b": b"2", "a": b"1"}))
        self.assertNotEqual(m.snapshot_digest({"a": b"bc"}), m.snapshot_digest({"ab": b"c"}))
        self.assertNotEqual(m.snapshot_digest({"a": b"1"}), m.snapshot_digest({"a": b"2"}))

    def test_notebook_order(self):
        self.assertEqual(m.run_cells([("set", "x", 1), ("add", "x", 2)]), {"x": 3})
        self.assertEqual(m.run_cells([("set", "x", 1), ("add", "x", 2), ("add", "x", 2)]), {"x": 5})
        with self.assertRaises(KeyError):
            m.run_cells([("add", "x", 2), ("set", "x", 1)])

    def test_solver_against_exact_rational_reference(self):
        rng = random.Random(20261019)
        checked = 0
        for _ in range(300):
            a, b, c, d, u, v = (rng.randint(-10, 10) for _ in range(6))
            determinant = a*d-b*c
            if determinant == 0:
                continue
            expected = (Fraction(u*d-b*v, determinant), Fraction(a*v-u*c, determinant))
            actual = m.solve2([[a, b], [c, d]], [u, v])
            for observed, exact in zip(actual, expected):
                self.assertAlmostEqual(observed, float(exact), places=10)
            self.assertLess(m.backward_error([[a, b], [c, d]], [u, v], actual), 1e-14)
            checked += 1
        self.assertGreater(checked, 250)

    def test_solver_pivot_and_invalid_inputs(self):
        self.assertEqual(m.solve2([[0, 1], [2, 1]], [3, 7]), (2, 3))
        for matrix in ([[1, 2], [2, 4]], [[0, 0], [0, 1]], [[math.nan, 1], [0, 1]]):
            with self.assertRaises(ValueError):
                m.solve2(matrix, [1, 2])

    def test_small_residual_can_hide_large_forward_error(self):
        a = [[1, 0], [0, 1e-8]]
        self.assertAlmostEqual(m.condition_inf2(a), 1e8)
        self.assertLess(m.backward_error(a, [1, 1e-8], [1, 2]), 1e-8)
        self.assertEqual(m.condition_inf2([[1, 2], [2, 4]]), math.inf)

    def test_dijkstra_against_bellman_ford(self):
        rng = random.Random(19)
        for n in range(1, 9):
            for _ in range(30):
                graph = {i: [(j, rng.randrange(10)) for j in range(n) if rng.random() < 0.3] for i in range(n)}
                expected = [math.inf]*n
                expected[0] = 0
                for _ in range(n-1):
                    previous = expected[:]
                    for i, edges in graph.items():
                        for j, weight in edges:
                            expected[j] = min(expected[j], previous[i]+weight)
                self.assertEqual(m.dijkstra(graph, 0), dict(enumerate(expected)))

    def test_dijkstra_stale_zero_unreachable(self):
        graph = {"s": [("a", 10), ("b", 1)], "b": [("a", 1)], "a": [("z", 0)], "u": []}
        self.assertEqual(m.dijkstra(graph, "s"), {"s": 0, "b": 1, "a": 2, "z": 2, "u": math.inf})
        with self.assertRaises(ValueError):
            m.dijkstra({"s": [], "unreachable": [("s", -1)]}, "s")

    def test_probe_matching_is_not_success(self):
        self.assertEqual(m.probe_model(["vendor,part"], {"vendor,part"}, {"clock"}, set()), "deferred")
        self.assertEqual(m.probe_model(["vendor,part"], {"vendor,part"}, {"clock"}, {"clock"}), "bound")
        self.assertEqual(m.probe_model(["vendor,other"], {"vendor,part"}, set(), set()), "no-match")

    def test_debug_state_contract(self):
        target = m.DebugTarget(pc=0x100)
        with self.assertRaises(RuntimeError):
            target.read_pc()
        target.halt()
        target.step_model(2)
        self.assertEqual(target.read_pc(), 0x102)
        target.resume()
        with self.assertRaises(ValueError):
            target.step_model(2)

    def test_wheel_inverse_round_trip(self):
        for v, omega in product((-1, 0, 1), repeat=2):
            left, right = m.wheel_rates(v, omega, 0.1, 0.5)
            self.assertAlmostEqual(0.1*(left+right)/2, v)
            self.assertAlmostEqual(0.1*(right-left)/0.5, omega)

    def test_odometry_straight_spin_and_arc(self):
        self.assertEqual(m.odometry_step((0, 0, 0), 1, 1, 0.5), (1, 0, 0))
        x, y, angle = m.odometry_step((2, 3, 0), -0.25, 0.25, 0.5)
        self.assertEqual((x, y, angle), (2, 3, 1))
        x, y, angle = m.odometry_step((0, 0, 0), 0, math.pi/2, 1)
        self.assertAlmostEqual(x, 0.5)
        self.assertAlmostEqual(y, 0.5)
        self.assertAlmostEqual(angle, math.pi/2)

    def test_odometry_subdivision_and_inverse(self):
        whole = m.odometry_step((1, 2, 0.7), 0.3, 0.5, 0.4)
        subdivided = (1, 2, 0.7)
        for _ in range(100):
            subdivided = m.odometry_step(subdivided, 0.003, 0.005, 0.4)
        for a, b in zip(whole, subdivided):
            self.assertAlmostEqual(a, b, places=12)
        back = m.odometry_step(whole, -0.3, -0.5, 0.4)
        for observed, expected in zip(back, (1, 2, 0.7)):
            self.assertAlmostEqual(observed, expected, places=12)

    def test_publish_idempotent_and_canonical(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)/"result.json"
            self.assertTrue(m.publish_json(target, {"b": 2, "a": 1}))
            original = target.read_bytes()
            self.assertFalse(m.publish_json(target, {"a": 1, "b": 2}))
            self.assertEqual(target.read_bytes(), original)
            self.assertEqual(json.loads(original), {"a": 1, "b": 2})

    def test_publish_failure_preserves_previous(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)/"result.json"
            m.publish_json(target, {"ok": 1})
            original = target.read_bytes()
            with self.assertRaises(ValueError):
                m.publish_json(target, {"ok": 2}, lambda value: False)
            with patch.object(m.os, "replace", side_effect=OSError("교체 실패")):
                with self.assertRaises(OSError):
                    m.publish_json(target, {"ok": 2})
            self.assertEqual(target.read_bytes(), original)
            self.assertEqual([p.name for p in Path(directory).iterdir()], ["result.json"])

    def test_publish_nonfinite_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                m.publish_json(Path(directory)/"result.json", {"value": math.nan})

    def test_records_known_encoding_and_round_trip(self):
        self.assertEqual(m.encode_records([b"A", b""]), b"\x00\x01A\x00\x00")
        rng = random.Random(1)
        for _ in range(100):
            records = [rng.randbytes(rng.randrange(40)) for _ in range(rng.randrange(10))]
            self.assertEqual(m.decode_records(m.encode_records(records)), records)

    def test_record_limits_and_truncation(self):
        for data in (b"\x00", b"\x00\x02A", b"\x10\x00"):
            with self.assertRaises(ValueError):
                m.decode_records(data)
        with self.assertRaises(ValueError):
            m.encode_records([b"a"*1025])
        with self.assertRaises(ValueError):
            m.decode_records(b"a"*8193)
        with self.assertRaises(ValueError):
            m.encode_records([b"aa"], max_total=3)

    def test_metamorphic_distance_scaling(self):
        graph = {0: [(1, 2), (2, 9)], 1: [(2, 3)], 2: []}
        scaled = {u: [(v, weight*7) for v, weight in edges] for u, edges in graph.items()}
        base = m.dijkstra(graph, 0)
        self.assertEqual(m.dijkstra(scaled, 0), {u: distance*7 for u, distance in base.items()})

    def test_latest_result_all_completion_orders(self):
        for order in permutations(range(3)):
            state = m.LatestResults()
            tickets = [state.begin(query) for query in ("a", "ab", "abc")]
            accepted = []
            for i in order:
                if state.finish(tickets[i], [i]):
                    accepted.append(i)
            self.assertEqual(accepted, [2])
            self.assertEqual((state.query, state.phase, state.result), ("abc", "ready", (2,)))

    def test_latest_close_and_duplicate_completion(self):
        state = m.LatestResults()
        ticket = state.begin("query")
        self.assertTrue(state.finish(ticket, [1]))
        self.assertFalse(state.finish(ticket, [2]))
        ticket = state.begin("new")
        state.close()
        self.assertFalse(state.finish(ticket, [3]))
        with self.assertRaises(RuntimeError):
            state.begin("closed")


if __name__ == "__main__":
    unittest.main()
