"""Consistency of archived aggregate metrics; not a new experiment."""
import json
import math
from pathlib import Path
import statistics
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ArchivedMetricsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / 'metrics/archived_metrics.json').read_text(encoding='utf-8'))

    def test_accuracy_counts_and_supported_masks(self):
        rows = self.data['cnn_test_evaluations']
        self.assertEqual(len(rows), 38)
        for row in rows:
            self.assertEqual(row['n'], 10000)
            self.assertAlmostEqual(row['accuracy'], 100 * row['correct'] / row['n'])
            if row['bits'] is not None:
                self.assertTrue(all(0 <= k < row['bits'] for k in row['stage_k'].values()))

    def test_seed_statistics(self):
        for row in self.data['cifar10_training_seed_statistics']:
            values = row['accuracies']
            self.assertEqual(row['n_seeds'], len(values))
            self.assertAlmostEqual(row['mean_accuracy'], statistics.mean(values))
            if len(values) > 1:
                self.assertAlmostEqual(row['std_accuracy'], statistics.stdev(values))
            else:
                self.assertIsNone(row['std_accuracy'])

    def test_circuit_totals_and_energy_units(self):
        sources = self.data['circuit_measurements']
        self.assertEqual(sum(len(group['runs']) for group in sources.values()), 36)
        self.assertEqual(sum(row['samples'] for group in sources.values()
                             for row in group['runs']), 768)
        for group in sources.values():
            self.assertEqual(group['status'], 'complete')
            for row in group['runs']:
                self.assertEqual(row['product_mismatches'], 0)
                self.assertEqual(row['accumulator_mismatches'], 0)
                self.assertTrue(math.isclose(row['energy_per_operation_fJ'],
                                row['average_supply_power_uW'] * row['period_ns'], rel_tol=1e-9))

    def test_scope_and_saved_replay(self):
        self.assertFalse(self.data['original_paper_accuracy_or_energy_claim_reproduced'])
        self.assertFalse(self.data['circuit_conditions']['whole_cnn_energy_measured'])
        for row in self.data['saved_replay']:
            self.assertTrue(row['labels_equal'] and row['predictions_equal'] and row['logits_equal'])
            self.assertEqual(row['maximum_absolute_logit_difference'], 0)


if __name__ == '__main__':
    unittest.main()
