"""Independent arithmetic and boundary checks. Run: python -m unittest -v."""
import math
import unittest
from dataclasses import replace
from types import SimpleNamespace

from energy_analysis import (Transformer, FormulaEvaluator, parameter_count,
                             full_prefix_flops, decode_flops, decode_energy,
                             paper_sweep)


class EnergyTests(unittest.TestCase):
    def setUp(self):
        self.tiny = Transformer('tiny', 10, 3, 2, 1, 1, 2, 1, 3)

    def test_hand_calculated_tiny_model(self):
        # 20 embedding + 6 positional + 16 attention + 42 FFN.
        self.assertEqual(parameter_count(self.tiny), 84)
        self.assertEqual(full_prefix_flops(self.tiny), 360)
        self.assertEqual(decode_flops(self.tiny), 120)
        e = decode_energy(self.tiny)
        self.assertEqual(e['lm_head_flops'],40)
        self.assertAlmostEqual(e['modeled_total_j_per_batch_step'] / 1e-9, 7.032)

    def test_batch_reuses_weight_read(self):
        single = decode_energy(self.tiny)
        four = decode_energy(replace(self.tiny, batch=4))
        self.assertEqual(single['weight_j'], four['weight_j'])
        self.assertEqual(single['mac_j'] * 4, four['mac_j'])
        self.assertAlmostEqual(four['modeled_j_per_output_token'] / 1e-9, 2.496)

    def test_first_token_has_no_old_kv_read(self):
        e = decode_energy(replace(self.tiny, context=1))
        self.assertEqual(e['kv_read_j'], 0)
        self.assertGreater(e['kv_write_j'], 0)
        self.assertEqual(parameter_count(self.tiny),parameter_count(replace(self.tiny,context=1)))

    def test_invalid_source_dimensions_are_visible(self):
        with self.assertRaises(ValueError):
            decode_energy(replace(self.tiny, heads=2))
        with self.assertRaises(ValueError):
            decode_energy(replace(self.tiny, batch=0))
        with self.assertRaises(ValueError):
            decode_energy(self.tiny, precision_bits=0)

    def test_parameter_count_matches_gpt175_workbook(self):
        model=Transformer('GPT175',50257,2048,12288,96,96,128)
        self.assertEqual(parameter_count(model),174594797568)
        self.assertEqual(full_prefix_flops(model),732274744098816)

    def test_excel_subset_and_range(self):
        sheet={k:SimpleNamespace(value=v) for k,v in
               {'A1':2,'A2':3,'A3':'=SUM(A1:A2)','B1':'=A3^2/5'}.items()}
        self.assertEqual(FormulaEvaluator(sheet).cell('B1'),5)

    def test_rejects_executable_input_and_cycle(self):
        for values in ({'A1':'=__import__(1)'},{'A1':'=A2','A2':'=A1'}):
            sheet={k:SimpleNamespace(value=v) for k,v in values.items()}
            with self.assertRaises(ValueError):
                FormulaEvaluator(sheet).cell('A1')

    def test_published_table_rounding_and_scaling(self):
        rows=paper_sweep()
        self.assertEqual(len(rows),100)
        self.assertLessEqual(max(r['absolute_rounding_difference'] for r in rows),1e-4)
        for row in rows:
            self.assertTrue(math.isfinite(row['normalized_total']))
            self.assertGreaterEqual(row['reduction_percent'],-1e-12)
        selected=next(r for r in rows if r['model']=='ResNet18' and r['batch']==4
                      and r['scaled_component']=='mac' and r['scale']==1/16)
        self.assertAlmostEqual(selected['reduction_percent'],60.059,places=2)


if __name__=='__main__':
    unittest.main()
