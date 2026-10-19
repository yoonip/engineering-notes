"""동일한 FPGA 조건에서 MAX-EX와 일반 E8M7 트리의 실제 결과를 비교한다.

새 합성 결과를 만들어 내는 도구가 아니라, 완료한 각 원시 JSON·DCP·소스의
해시를 확인한 뒤 비교표를 만든다. 두 알고리즘은 반올림 위치가 다르다.
LUT 차이를 전체 Transformer·실물 DRAM-PIM의 전력/속도 향상으로 해석하지 않는다.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from model.e8m7_maxex import exact_dot_e8m7, maxex_dot, rounded_product_tree_dot


def sha(path: Path) -> str:
    value=hashlib.sha256()
    with path.open('rb') as source:
        for chunk in iter(lambda:source.read(1024*1024),b''): value.update(chunk)
    return value.hexdigest()


def load(relative: str) -> dict:
    return json.loads((ROOT/relative).read_text(encoding='utf-8-sig'))


def main() -> int:
    output=ROOT/'build/reports/e8m7_implementation_comparison.json'
    report={'passed':False,'mode':'independent_e8m7_arithmetic_implementation_comparison',
            'physical_board_measured':False,'physical_dram_pim_measured':False,
            'connected_to_q88_transformer':False,
            'conditions_ko':['동일한 E8M7 입력 16개 쌍, 16비트 결과와 valid/reset 인터페이스',
                'Nexys part xc7a100tcsg324-1, 입력·출력 등록, edge N→N+1 결과',
                'Vivado 2024.1 OOC 합성·배치·배선, 200ns clock, 입출력 delay 각각 2ns',
                'MAX-EX는 마지막 RNE, 일반 트리는 각 곱과 각 덧셈에서 RNE',
                'LUT·FF·DSP·BRAM·STA 비교이며 전력·실물 throughput·전체 GPT accuracy 측정 아님']}
    reports={}
    try:
        configurations=[('pairwise','build/e8m7_pairwise/vivado',
                          'build/e8m7_pairwise/netlist'),
                        ('maxex_guard16','build/e8m7_maxex/vivado_guard16',
                          'build/e8m7_maxex/netlist_guard16'),
                        ('maxex_guard32','build/e8m7_maxex/vivado_guard32',
                          'build/e8m7_maxex/netlist_guard32')]
        rows={}
        for name,implementation_folder,netlist_folder in configurations:
            implementation=load(implementation_folder+'/result.json')
            netlist=load(netlist_folder+'/result.json')
            assert implementation['passed'] and netlist['passed'],name+' 실제 구현/배선 회로 시험 실패'
            assert implementation['device']=='xc7a100tcsg324-1'
            assert implementation['lanes']==16 and implementation['clock_period_ns']==200.0
            assert sha(ROOT/implementation_folder/'routed.dcp')==implementation['routed_checkpoint_sha256']==netlist['routed_checkpoint_sha256']
            for item in implementation['source_snapshot']:
                assert sha(ROOT/item['file'])==sha(ROOT/implementation_folder/'source_snapshot'/item['file'])==item['sha256']
            assert implementation['no_clock_endpoints']==implementation['unconstrained_internal_endpoints']==0
            assert min(implementation['timing'][key] for key in ('WNS_ns','WHS_ns','WPWS_ns'))>=0
            for file,wanted in netlist['source_sha256'].items(): assert sha(ROOT/file)==wanted
            assert not implementation['physical_board_measured'] and not netlist['sdf_annotated']
            rows[name]={'resources_routed':implementation['resources_routed'],
                        'timing':implementation['timing'],
                        'implementation_wall_seconds':implementation['wall_seconds'],
                        'functional_netlist_exact_word_comparisons':netlist['exact_word_comparisons'],
                        'routed_checkpoint_sha256':implementation['routed_checkpoint_sha256']}
            for folder in (implementation_folder,netlist_folder): reports[folder+'/result.json']=sha(ROOT/folder/'result.json')
        baseline_luts=rows['pairwise']['resources_routed']['LUT']['used']
        for name in ('maxex_guard16','maxex_guard32'):
            rows[name]['lut_reduction_vs_pairwise_percent']=round(
                100*(baseline_luts-rows[name]['resources_routed']['LUT']['used'])/baseline_luts,4)
        experiment=load('build/reports/e8m7_maxex_experiment.json')
        assert experiment['passed'] and experiment['summary']['samples']==670
        for file,wanted in experiment['source_sha256'].items(): assert sha(ROOT/file)==wanted
        reports['build/reports/e8m7_maxex_experiment.json']=sha(ROOT/'build/reports/e8m7_maxex_experiment.json')
        # 가까운 큰 수 두 개 사이의 작은 항이 중간 반올림에서 사라지는 예다.
        a=[0x3f80,0x3b80,0xbf80]+[0]*13
        b=[0x3f80,0x3f80,0x3f80]+[0]*13
        words={'exact_final_rne':exact_dot_e8m7(a,b),
               'pairwise_each_operation_rne':rounded_product_tree_dot(a,b),
               'maxex_guard16':maxex_dot(a,b,16),'maxex_guard32':maxex_dot(a,b,32)}
        assert words=={'exact_final_rne':0x3b80,'pairwise_each_operation_rne':0,
                      'maxex_guard16':0x3b80,'maxex_guard32':0x3b80}
        # 반대로 매우 큰 상쇄 사이의 1은 좁은 MAX-EX 정렬에서도 사라진다.
        # 중간 Inf를 만들지 않는 것과 작은 항까지 보존하는 것은 별개의 문제다.
        extreme_a=[0x7f7f,0xff7f,0x3f80]+[0]*13
        extreme_b=[0x7f7f,0x7f7f,0x3f80]+[0]*13
        extreme_words={'exact_final_rne':exact_dot_e8m7(extreme_a,extreme_b),
                       'pairwise_each_operation_rne':rounded_product_tree_dot(extreme_a,extreme_b),
                       'maxex_guard16':maxex_dot(extreme_a,extreme_b,16),
                       'maxex_guard32':maxex_dot(extreme_a,extreme_b,32),
                       'maxex_guard512':maxex_dot(extreme_a,extreme_b,512)}
        assert extreme_words=={'exact_final_rne':0x3f80,'pairwise_each_operation_rne':0x7fc0,
                              'maxex_guard16':0,'maxex_guard32':0,'maxex_guard512':0x3f80}
        report.update({'passed':True,'implementations':rows,
                       'existing_numerical_experiment_summary':experiment['summary'],
                       'illustrative_rounding_case':{'formula':'1 + 2^-8 - 1',
                           'a_words':a,'b_words':b,'output_words':words,
                           'scope_ko':'Python의 명시한 수치 규칙 예시. 실제 RTL 전체 검증과 구별한다.'},
                       'illustrative_extreme_cancellation_case':{'formula':'max_finite^2 - max_finite^2 + 1',
                           'a_words':extreme_a,'b_words':extreme_b,'output_words':extreme_words,
                           'scope_ko':'G16/G32의 범위 제한을 보여 주는 Python 예시. G512는 수치 실험이며 이번 FPGA 비교에 넣지 않는다.'},
                       'source_reports_sha256':reports,
                       'source_sha256':{'analysis/compare_e8m7_implementations.py':sha(Path(__file__)),
                                        'model/e8m7_maxex.py':sha(ROOT/'model/e8m7_maxex.py')},
                       'interpretation_ko':'동일 인터페이스/제약 아래 서로 다른 반올림 구조의 비교다. guard16/32는 일반 유한 입력 전체에 대해 정확한 Fraction 내적과 같다는 보장이 없다. 각 결과를 실제 LM 내적 195개와 임의 경계/난수 실험의 범위별로 해석한다.'})
    except Exception as error:
        report['failure_ko']=str(error)
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'passed':report['passed'],'report':str(output),
                      'failure_ko':report.get('failure_ko')},ensure_ascii=False))
    return 0 if report['passed'] else 1


if __name__=='__main__':
    if hasattr(sys.stdout,'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
    raise SystemExit(main())
