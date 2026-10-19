"""공개 데이터·학습 가중치 없이 causal 구조의 불변조건을 확인한다."""
import math
import unittest

import numpy as np
import torch

from st_awfd_model import CausalMultiHorizonGPT, causal_invariance_audit, gaussian_nll, multi_horizon_loss, score_signals


class CausalModelTests(unittest.TestCase):
    def setUp(self):
        torch.set_num_threads(1)
        torch.manual_seed(17)
        self.model = CausalMultiHorizonGPT(feature_count=3, sequence_length=32).eval()
        self.signals = np.random.default_rng(17).normal(size=(3, 3, 32)).astype(np.float32)

    def test_future_perturbation_does_not_change_present_forecast(self):
        audit = causal_invariance_audit(self.model, self.signals[0], torch.device("cpu"))
        self.assertTrue(audit["passes_strict_causal_invariance"])
        self.assertLess(audit["max_forecast_mean_delta_at_cutoff"], 1e-6)
        self.assertLess(audit["max_log_sigma_delta_at_cutoff"], 1e-6)

    def test_standard_normal_nll_has_normalization_constant(self):
        zero = torch.zeros(2)
        result = gaussian_nll(zero, zero, zero)
        self.assertTrue(torch.allclose(result, torch.full((2,), 0.5 * math.log(2 * math.pi))))

    def test_shapes_and_finite_multi_horizon_loss(self):
        mean, log_sigma = self.model(torch.from_numpy(self.signals[:, :, :-1]))
        self.assertEqual(tuple(mean.shape), (3, 31, 4, 3))
        self.assertEqual(tuple(log_sigma.shape), tuple(mean.shape))
        self.assertTrue(torch.isfinite(multi_horizon_loss(self.model, torch.from_numpy(self.signals))))

    def test_inference_batch_partition_preserves_scores(self):
        together = score_signals(self.model, self.signals, torch.device("cpu"), batch_size=3)
        separate = score_signals(self.model, self.signals, torch.device("cpu"), batch_size=1)
        for actual, expected in zip(together, separate):
            np.testing.assert_allclose(actual, expected, rtol=1e-5, atol=1e-6)


if __name__ == "__main__":
    unittest.main()
