"""독립적인 해석해·전수 열거·보존식으로 계산 모델을 확인한다."""

import itertools
import math
import sqlite3
import unittest

from models import (IdempotencyStore, balanced_partitions, barycentric,
    bounded_tool, correlate_valid, cosine_learning_rate, decay_euler,
    dequantize, linear_loss_gradient, memory_sectors, occupancy_bound,
    page_after, pairwise_sum, pinhole, poisson_sine, quantize,
    quorum_overlap, retrieval_metrics, sales_totals, sample_token,
    tfidf_rank, token_probabilities, transfer, transform_point, tree_reduction_time)


class GPUAndTokens(unittest.TestCase):
    def test_memory_patterns(self):
        self.assertEqual(memory_sectors([4 * i for i in range(32)]), 4)
        self.assertEqual(memory_sectors([4 + 4 * i for i in range(32)]), 5)
        self.assertEqual(memory_sectors([32 * i for i in range(32)]), 32)
        self.assertEqual(memory_sectors([31], 4), 2)
        self.assertEqual(memory_sectors([0] * 32), 1)

    def test_occupancy_resource_bound(self):
        self.assertEqual(occupancy_bound(256, 32, 0), (8, 1.0))
        self.assertEqual(occupancy_bound(256, 64, 0), (4, 0.5))
        self.assertEqual(occupancy_bound(256, 32, 32768), (2, 0.25))
        self.assertEqual(occupancy_bound(4096, 1, 0), (0, 0.0))

    def test_softmax_analytic_and_shift(self):
        p = token_probabilities([0, math.log(3)])
        self.assertAlmostEqual(p[0], 0.25)
        self.assertAlmostEqual(p[1], 0.75)
        for x, y in zip(token_probabilities([1000, 1001]), token_probabilities([0, 1])):
            self.assertAlmostEqual(x, y)
        self.assertEqual(token_probabilities([2, 2, 1], top_k=1), [1, 0, 0])
        self.assertLess(token_probabilities([0, 1], 10)[1], token_probabilities([0, 1], 1)[1])

    def test_sampling_intervals(self):
        draws = [sample_token([0, 0.25, 0.75], (i + 0.5) / 100) for i in range(100)]
        self.assertEqual(draws.count(1), 25)
        self.assertEqual(draws.count(2), 75)
        with self.assertRaises(ValueError):
            token_probabilities([0], temperature=0)

    def test_top_k_conditional_distribution(self):
        probabilities = token_probabilities([0, math.log(2), math.log(3)], top_k=2)
        self.assertEqual(probabilities[0], 0)
        self.assertAlmostEqual(probabilities[1], 0.4)
        self.assertAlmostEqual(probabilities[2], 0.6)


class DataAndParallel(unittest.TestCase):
    def test_sql_aggregate_python_reference(self):
        rows = [("A", 120), ("B", 30), ("A", -20), ("B", 70)]
        self.assertEqual(sales_totals(rows), {"A": 100, "B": 100})
        self.assertEqual(sales_totals([]), {})

    def test_transaction_rollback_and_conservation(self):
        with sqlite3.connect(":memory:") as connection:
            connection.execute("CREATE TABLE accounts(id INTEGER PRIMARY KEY, balance INTEGER CHECK(balance>=0))")
            connection.executemany("INSERT INTO accounts VALUES (?,?)", [(1, 100), (2, 40)])
            connection.commit()
            with self.assertRaises(ValueError):
                transfer(connection, 1, 3, 20)
            self.assertEqual(list(connection.execute("SELECT balance FROM accounts ORDER BY id")), [(100,), (40,)])
            transfer(connection, 1, 2, 30)
            self.assertEqual(list(connection.execute("SELECT balance FROM accounts ORDER BY id")), [(70,), (70,)])
            with self.assertRaises(ValueError):
                transfer(connection, 1, 2, 100)

    def test_transfer_autocommit_connections_are_atomic(self):
        for options in ({"isolation_level": None}, {"autocommit": True}):
            with self.subTest(options=options):
                connection = sqlite3.connect(":memory:", **options)
                try:
                    connection.execute("CREATE TABLE accounts(id INTEGER PRIMARY KEY, balance INTEGER CHECK(balance>=0))")
                    connection.executemany("INSERT INTO accounts VALUES (?,?)", [(1, 100), (2, 40)])
                    self.assertFalse(connection.in_transaction)
                    with self.assertRaises(ValueError):
                        transfer(connection, 1, 3, 20)
                    self.assertFalse(connection.in_transaction)
                    self.assertEqual(list(connection.execute("SELECT balance FROM accounts ORDER BY id")), [(100,), (40,)])
                    transfer(connection, 1, 2, 30)
                    self.assertFalse(connection.in_transaction)
                    self.assertEqual(list(connection.execute("SELECT balance FROM accounts ORDER BY id")), [(70,), (70,)])
                    with self.assertRaises(ValueError):
                        transfer(connection, 1, 2, 100)
                    self.assertFalse(connection.in_transaction)
                    self.assertEqual(connection.execute("SELECT SUM(balance) FROM accounts").fetchone()[0], 140)
                finally:
                    connection.close()

    def test_transfer_rejects_existing_transaction_without_changing_it(self):
        connection = sqlite3.connect(":memory:", isolation_level=None)
        try:
            connection.execute("CREATE TABLE accounts(id INTEGER PRIMARY KEY, balance INTEGER)")
            connection.executemany("INSERT INTO accounts VALUES (?,?)", [(1, 100), (2, 40)])
            connection.execute("BEGIN")
            connection.execute("UPDATE accounts SET balance=90 WHERE id=1")
            with self.assertRaises(ValueError):
                transfer(connection, 1, 2, 20)
            self.assertTrue(connection.in_transaction)
            self.assertEqual(list(connection.execute("SELECT balance FROM accounts ORDER BY id")), [(90,), (40,)])
            connection.execute("ROLLBACK")
            self.assertEqual(list(connection.execute("SELECT balance FROM accounts ORDER BY id")), [(100,), (40,)])
        finally:
            connection.close()

    def test_quorum_against_all_subsets(self):
        for n in range(1, 7):
            universe = range(n)
            for r in range(1, n + 1):
                for w in range(1, n + 1):
                    actual = min(len(set(a) & set(b))
                                 for a in itertools.combinations(universe, r)
                                 for b in itertools.combinations(universe, w))
                    self.assertEqual(quorum_overlap(n, r, w), actual)

    def test_partition_exhaustive_coverage(self):
        for size in range(40):
            for workers in range(1, 12):
                ranges = balanced_partitions(size, workers)
                covered = [i for start, stop in ranges for i in range(start, stop)]
                self.assertEqual(covered, list(range(size)))
                sizes = [stop - start for start, stop in ranges]
                self.assertLessEqual(max(sizes) - min(sizes), 1)

    def test_reduction_exact_integer_reference(self):
        for n in range(100):
            values = [i * i - 4 for i in range(n)]
            self.assertEqual(pairwise_sum(values), sum(values))
        self.assertAlmostEqual(tree_reduction_time(8, 1000, 1e-6, 1e-9), 6e-6)
        self.assertEqual(tree_reduction_time(1, 1000, 1e-6, 1e-9), 0)


class VisionTrainingRetrieval(unittest.TestCase):
    def test_projection_similar_triangles(self):
        self.assertEqual(pinhole((1, 2, 4), 800, 800, 320, 240), (520, 640))
        self.assertEqual(pinhole((2, 4, 8), 800, 800, 320, 240), (520, 640))
        with self.assertRaises(ValueError):
            pinhole((1, 1, 0), 800, 800)

    def test_filter_constant_and_asymmetric_kernel(self):
        self.assertEqual(correlate_valid([[5] * 4 for _ in range(4)], [[0.25] * 2 for _ in range(2)]), [[5] * 3 for _ in range(3)])
        self.assertEqual(correlate_valid([[1, 2, 3]], [[1, -1]]), [[-1, -1]])
        self.assertEqual(correlate_valid([[1, 2], [3, 4]], [[1]]), [[1, 2], [3, 4]])

    def test_gradient_independent_finite_difference(self):
        xs, ys, weight, epsilon = [1, 2, -1], [2, 4, -2], 0.7, 1e-6
        loss, gradient = linear_loss_gradient(xs, ys, weight)
        difference = (linear_loss_gradient(xs, ys, weight + epsilon)[0]
                      - linear_loss_gradient(xs, ys, weight - epsilon)[0]) / (2 * epsilon)
        self.assertAlmostEqual(gradient, difference, places=8)
        self.assertLess(linear_loss_gradient(xs, ys, weight - 0.1 * gradient)[0], loss)
        for _ in range(100):
            weight -= 0.1 * linear_loss_gradient(xs, ys, weight)[1]
        self.assertAlmostEqual(weight, 2, places=8)

    def test_schedule_and_unequal_batch_weighting(self):
        rates = [cosine_learning_rate(t, 10, 0.1, 0.01) for t in range(11)]
        self.assertAlmostEqual(rates[0], 0.1)
        self.assertAlmostEqual(rates[-1], 0.01)
        self.assertTrue(all(a >= b for a, b in zip(rates, rates[1:])))
        xs, ys = [1, 2, 3], [2, 4, 6]
        full = linear_loss_gradient(xs, ys, 0)[1]
        batch_a = linear_loss_gradient(xs[:2], ys[:2], 0)[1]
        batch_b = linear_loss_gradient(xs[2:], ys[2:], 0)[1]
        self.assertAlmostEqual(full, (2 * batch_a + batch_b) / 3)

    def test_retrieval_metrics_and_known_ranking(self):
        ranking = tfidf_rank(["silicon wafer", "robot motor", "silicon silicon"], "wafer")
        self.assertEqual(ranking[0][0], 0)
        self.assertEqual([score for _, score in tfidf_rank(["a", "b"], "z")], [0, 0])
        self.assertEqual(retrieval_metrics([3, 2, 1], {1, 2}, 2), {"recall": 0.5, "reciprocal_rank": 0.5})
        self.assertEqual(retrieval_metrics([1, 2, 3], {1, 2}, 2), {"recall": 1, "reciprocal_rank": 1})

    def test_tool_rejects_unregistered_and_invalid_inputs(self):
        self.assertEqual(bounded_tool("sum_numbers", {"values": [1, 2, 3]}), 6)
        for name, args in [("shell", {"values": []}), ("sum_numbers", {"values": [True]}),
                           ("sum_numbers", {"values": [float("nan")]}),
                           ("sum_numbers", {"values": [1], "command": "x"})]:
            with self.assertRaises(ValueError):
                bounded_tool(name, args)


class QuantizationGraphicsNumericsHTTP(unittest.TestCase):
    def test_quantization_exact_grid_rounding_clipping(self):
        for q in range(-128, 128):
            self.assertEqual(quantize(dequantize(q, 0.125, -3), 0.125, -3), q)
        self.assertEqual(quantize(0.25, 0.5, 0), 0)
        self.assertEqual(quantize(0.75, 0.5, 0), 2)
        self.assertEqual(quantize(100, 0.5, 0), 127)
        self.assertEqual(quantize(-100, 0.5, 0), -128)

    def test_quantization_error_bound(self):
        scale, zero = 0.125, -3
        for i in range(1001):
            x = -15 + 30 * i / 1000
            recovered = dequantize(quantize(x, scale, zero), scale, zero)
            self.assertLessEqual(abs(x - recovered), scale / 2 + 1e-14)

    def test_transform_inverse_and_barycentric_reconstruction(self):
        transform = [[0, -1, 0, 2], [1, 0, 0, 3], [0, 0, 1, 4], [0, 0, 0, 1]]
        inverse = [[0, 1, 0, -3], [-1, 0, 0, 2], [0, 0, 1, -4], [0, 0, 0, 1]]
        point = (1, 2, 3)
        self.assertEqual(transform_point(inverse, transform_point(transform, point)), point)
        a, b, c, p = (0, 0), (2, 0), (0, 2), (0.5, 0.5)
        weights = barycentric(p, a, b, c)
        self.assertEqual(weights, (0.5, 0.25, 0.25))
        self.assertEqual(tuple(sum(w * vertex[j] for w, vertex in zip(weights, (a, b, c))) for j in range(2)), p)
        self.assertLess(min(barycentric((3, 3), a, b, c)), 0)

    def test_poisson_convergence_and_independent_eigenmode(self):
        errors = []
        for intervals in (16, 32, 64):
            u = poisson_sine(intervals)
            h = 1 / intervals
            eigenvalue = 4 * math.sin(math.pi * h / 2) ** 2 / h ** 2
            analytic_discrete = [math.pi ** 2 / eigenvalue * math.sin(math.pi * i * h)
                                 for i in range(intervals + 1)]
            self.assertLess(max(abs(a - b) for a, b in zip(u, analytic_discrete)), 2e-13)
            errors.append(max(abs(value - math.sin(math.pi * i * h)) for i, value in enumerate(u)))
        self.assertTrue(all(3.9 < a / b < 4.1 for a, b in zip(errors, errors[1:])))

    def test_poisson_flux_balance(self):
        intervals = 40
        u, h = poisson_sine(intervals), 1 / intervals
        flux = [-(b - a) / h for a, b in zip(u, u[1:])]
        source_integral = h * sum(math.pi ** 2 * math.sin(math.pi * i * h)
                                  for i in range(1, intervals))
        self.assertAlmostEqual(flux[-1] - flux[0], source_integral, places=11)

    def test_time_convergence(self):
        errors = [abs(decay_euler(n) - math.exp(-1)) for n in (40, 80, 160)]
        self.assertTrue(all(1.95 < a / b < 2.05 for a, b in zip(errors, errors[1:])))

    def test_idempotency_retries_conflicts_and_copy(self):
        store = IdempotencyStore()
        first = store.create("key", {"name": "note"})
        first["name"] = "modified"
        self.assertEqual(store.create("key", {"name": "note"}), {"id": 1, "name": "note"})
        self.assertEqual(store.created, 1)
        with self.assertRaises(ValueError):
            store.create("key", {"name": "different"})
        with self.assertRaises(ValueError):
            store.create("next", {"name": "", "extra": 1})

    def test_pagination_complete_without_duplicates(self):
        ids, cursor, collected = [2, 4, 6, 8, 10, 12, 14], None, []
        while True:
            page, cursor = page_after(ids, cursor, 3)
            collected.extend(page)
            if cursor is None:
                break
        self.assertEqual(collected, ids)
        self.assertEqual(page_after([], None, 3), ([], None))
        self.assertEqual(page_after(ids, 100, 3), ([], None))


if __name__ == "__main__":
    unittest.main()
