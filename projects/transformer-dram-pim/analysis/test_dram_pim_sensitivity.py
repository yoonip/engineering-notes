"""추가 캐시·반복 분석의 독립 산술과 기존 CSV 교차 검증 시험."""
from __future__ import annotations

import copy
import json
import unittest
from fractions import Fraction

from analysis.dram_pim_model import Config
from analysis.dram_pim_sensitivity import (ROOT,BASELINE,PIM,HOST_EVERY,HOST_WEIGHT,
    PIM_RESIDENT,HOST_IDEAL,build_analysis,parse_trace_text,repeated_case,reduction,require_safe_outputs)


class DramPimSensitivityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.trace=(ROOT/'fixtures/dram_pim_command_trace.csv').read_text(encoding='utf-8-sig')
        cls.original=json.loads((ROOT/'fixtures/dram_pim_model.json').read_text(encoding='utf-8-sig'))
        cls.analysis=build_analysis(cls.trace,cls.original)
        cls.components=cls.analysis['boundary_bytes_components']

    def test_actual_trace_components(self):
        expected=dict(weight_initial_host_read_bytes=32768,weight_initial_pim_write_bytes=32768,
            input_boundary_bytes_per_prompt=1024,output_boundary_bytes_per_prompt=1024,
            compulsory_io_bytes_per_prompt=2048,host_unfused_total_bytes_per_prompt=114688,
            host_unfused_nonweight_bytes_per_prompt=81920,original_baseline_input_read_bytes=4096,
            original_baseline_final_output_write_bytes=1024,weight_tensor_count=12,
            logical_weight_storage_bytes=32768)
        for key,value in expected.items():
            with self.subTest(field=key): self.assertEqual(self.components[key],value)

    def test_actual_read_write_counts_and_bytes(self):
        summaries=self.analysis['trace_counts']
        for scenario,read,write in ((BASELINE,1216,576),(PIM,16,528)):
            with self.subTest(scenario=scenario):
                self.assertEqual(summaries[scenario]['command_counts']['READ'],read)
                self.assertEqual(summaries[scenario]['command_counts']['WRITE'],write)
                self.assertEqual(summaries[scenario]['total_boundary_bytes'],(read+write)*64)

    def test_original_cold_reduction_is_preserved(self):
        cold=self.analysis['original_cold_trace']
        self.assertEqual(cold['host_bytes'],114688)
        self.assertEqual(cold['pim_bytes'],34816)
        self.assertEqual(round(cold['pim_reduction_percent'],2),69.64)
        self.assertEqual(cold['original_report_rounded_reduction_percent'],69.64)

    def test_cold_start_totals_for_all_requested_repetitions(self):
        expected={1:(114688,114688,34816),2:(229376,196608,36864),
                  4:(458752,360448,40960),16:(1835008,1343488,65536)}
        for case in self.analysis['cold_start_repeated_cases']:
            scenario=case['scenarios']
            with self.subTest(R=case['repetitions']):
                self.assertEqual(tuple(scenario[name]['total_boundary_bytes']
                    for name in (HOST_EVERY,HOST_WEIGHT,PIM_RESIDENT)),expected[case['repetitions']])
                self.assertEqual(scenario[HOST_IDEAL]['total_boundary_bytes'],
                                 scenario[PIM_RESIDENT]['total_boundary_bytes'])

    def test_first_prompt_has_no_warm_weight_saving(self):
        case=repeated_case(self.components,1)
        self.assertEqual(case['scenarios'][HOST_WEIGHT]['total_boundary_bytes'],
                         case['scenarios'][HOST_EVERY]['total_boundary_bytes'])

    def test_already_warm_interval_excludes_prior_setup_only_for_resident_scenarios(self):
        for repetitions in (1,2,4,16):
            warm=repeated_case(self.components,repetitions,already_warm=True)
            self.assertEqual(warm['scenarios'][HOST_EVERY]['total_boundary_bytes'],114688*repetitions)
            self.assertEqual(warm['scenarios'][HOST_WEIGHT]['total_boundary_bytes'],81920*repetitions)
            self.assertEqual(warm['scenarios'][PIM_RESIDENT]['total_boundary_bytes'],2048*repetitions)
            self.assertEqual(warm['scenarios'][HOST_IDEAL]['total_boundary_bytes'],2048*repetitions)

    def test_exact_average_retains_fraction(self):
        case=repeated_case(self.components,3)
        value=case['scenarios'][PIM_RESIDENT]['average_bytes_per_prompt']
        self.assertEqual(Fraction(value['numerator'],value['denominator']),Fraction(38912,3))

    def test_infinite_limit_is_average_not_infinite_total(self):
        limit=self.analysis['infinite_repetition_limit']
        self.assertEqual(limit['average_bytes_per_prompt'],
            {HOST_EVERY:114688,HOST_WEIGHT:81920,PIM_RESIDENT:2048,HOST_IDEAL:2048})
        self.assertEqual(limit['pim_reduction_against'][HOST_EVERY]['fraction']['numerator'],55)
        self.assertEqual(limit['pim_reduction_against'][HOST_EVERY]['fraction']['denominator'],56)
        self.assertEqual(limit['pim_reduction_against'][HOST_WEIGHT]['percent'],97.5)
        self.assertEqual(limit['pim_reduction_against'][HOST_IDEAL]['percent'],0)

    def test_ideal_host_equality_is_conditioned_on_common_external_io(self):
        self.assertIn('2048B',json.dumps(self.analysis['assumptions_ko'],ensure_ascii=False))
        for case in self.analysis['cold_start_repeated_cases']:
            self.assertEqual(case['pim_reduction_against'][HOST_IDEAL]['bytes_saved'],0)
        changed=copy.deepcopy(self.components)
        changed['compulsory_io_bytes_per_prompt']=4096
        self.assertEqual(repeated_case(changed,2)['scenarios'][PIM_RESIDENT]['total_boundary_bytes'],40960)

    def test_invalid_repetitions_are_rejected(self):
        for value in (0,-1,True,1.5,'2'):
            with self.subTest(value=value),self.assertRaises(ValueError):
                repeated_case(self.components,value)

    def test_duplicate_read_is_not_silently_deduplicated(self):
        row=next(line for line in self.trace.splitlines() if ',unfused_baseline,READ,' in line)
        changed=self.trace+'\n'+row+'\n'
        with self.assertRaises(ValueError): build_analysis(changed,self.original)
        matching=next(row for row in self.analysis['tensor_command_counts']
                      if row['scenario']==BASELINE and row['tensor']=='input_hidden' and row['command']=='READ')
        self.assertEqual(matching['burst_commands'],64)
        self.assertEqual(matching['unique_burst_offsets'],16)

    def test_model_report_mismatch_rejected(self):
        changed=copy.deepcopy(self.original)
        changed[BASELINE]['read_commands']+=1
        with self.assertRaises(ValueError): build_analysis(self.trace,changed)

    def test_missing_or_changed_csv_data_command_rejected(self):
        lines=self.trace.splitlines()
        index=next(i for i,line in enumerate(lines) if ',pim_data_resident,WRITE,' in line)
        del lines[index]
        with self.assertRaises(ValueError): build_analysis('\n'.join(lines),self.original)

    def test_unknown_command_or_bad_offset_rejected(self):
        for before,after in ((',ACT,',',BOGUS,'),('L0_wq,0','L0_wq,1')):
            with self.subTest(change=after),self.assertRaises(ValueError):
                parse_trace_text(self.trace.replace(before,after,1),Config())

    def test_act_pre_do_not_add_payload_bytes(self):
        for scenario in (BASELINE,PIM):
            data=self.analysis['trace_counts'][scenario]
            self.assertGreater(data['command_counts']['ACT'],0)
            self.assertGreater(data['command_counts']['PRE'],0)
            self.assertEqual(data['total_boundary_bytes'],data['read_bytes']+data['write_bytes'])

    def test_no_time_power_or_physical_claim(self):
        for field in ('new_dram_trace_generated','original_trace_modified','new_vivado_execution_performed',
                      'training_performed','ddr_time_measured','power_measured','physical_board_measured'):
            self.assertIs(self.analysis[field],False)
        self.assertNotIn('estimated_memory_service_cycles',self.analysis)

    def test_reduction_invalid_bytes_rejected(self):
        for host,pim in ((0,0),(-1,0),(1,-1),(True,0)):
            with self.subTest(host=host,pim=pim),self.assertRaises(ValueError): reduction(host,pim)

    def test_output_cannot_overwrite_existing_input_or_leave_reports(self):
        protected=ROOT/'fixtures/dram_pim_command_trace.csv'
        good=ROOT/'build/reports/independent_sensitivity_fixture.json'
        require_safe_outputs([protected],[good])
        for paths in ([protected],[good,good],[ROOT/'analysis/dram_pim_model.py']):
            with self.subTest(paths=paths),self.assertRaises(ValueError):
                require_safe_outputs([protected],paths)


if __name__=='__main__':
    unittest.main(verbosity=2)
