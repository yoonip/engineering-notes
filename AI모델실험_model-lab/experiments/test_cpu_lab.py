import math
import unittest

from cpu_lab import (
    distillation_experiment,
    kv_bytes,
    memory_experiment,
    quantization_experiment,
    recursive_state_experiment,
    softmax,
    uniform_quantize,
)


class NumericalChecks(unittest.TestCase):
    def test_kv_dimensions_and_linear_scaling(self):
        self.assertEqual(kv_bytes(1, 1, 1, 1), 4)
        self.assertEqual(kv_bytes(28, 2, 128, 4096), 117440512)
        self.assertEqual(kv_bytes(28, 2, 128, 8192), 2 * kv_bytes(28, 2, 128, 4096))
        self.assertEqual(kv_bytes(28, 2, 128, 4096, batch=2), 2 * kv_bytes(28, 2, 128, 4096))
        with self.assertRaises(ValueError):
            kv_bytes(0, 2, 128, 4096)

    def test_different_head_counts_matter_more_than_model_size_for_this_cache(self):
        rows = memory_experiment()["rows"]
        deepseek, qwen = rows[0], rows[3]
        self.assertEqual(qwen["kv_bf16_GiB"], 4 * deepseek["kv_bf16_GiB"])

    def test_iteration_has_a_stable_case_and_an_unstable_counterexample(self):
        rows = recursive_state_experiment()["rows"]
        stable = [row for row in rows if row["latent_gain"] == 0.5]
        unstable = [row for row in rows if row["latent_gain"] == 1.2]
        self.assertTrue(all(0 <= row["y"] < 1 / 3 for row in stable))
        self.assertLess(abs(stable[-1]["y"] - 1 / 3), abs(stable[0]["y"] - 1 / 3))
        self.assertGreater(unstable[-1]["y"], 100 * stable[-1]["y"])
        self.assertEqual({row["shared_scalar_coefficients"] for row in rows}, {4})

    def test_softmax_numerical_stability_and_shift_invariance(self):
        left = softmax([1000, 1001, 1002])
        right = softmax([0, 1, 2])
        self.assertAlmostEqual(sum(left), 1.0)
        for a, b in zip(left, right):
            self.assertAlmostEqual(a, b)

    def test_student_learning_recovers_teacher_distribution_in_this_setup(self):
        hard, soft = distillation_experiment()["rows"]
        self.assertLess(soft["mean_KL_teacher_to_student"], 1e-4)
        self.assertGreater(hard["mean_KL_teacher_to_student"], soft["mean_KL_teacher_to_student"])
        self.assertGreaterEqual(soft["argmax_agreement"], 0.95)

    def test_quantization_endpoints_and_error_bound(self):
        values = [-1, -0.33, 0.2, 1]
        reconstructed = uniform_quantize(values, 4)
        self.assertEqual(reconstructed[0], -1)
        self.assertEqual(reconstructed[-1], 1)
        self.assertLessEqual(max(abs(a-b) for a,b in zip(values, reconstructed)), 1 / 15 + 1e-12)
        self.assertEqual(uniform_quantize([2.0, 2.0], 4), [2.0, 2.0])
        self.assertTrue(all(math.isfinite(row["dot_absolute_error"]) for row in quantization_experiment()["rows"]))


if __name__ == "__main__":
    unittest.main()
