"""기존 DRAM/PIM CSV를 읽어 캐시·반복 실행의 byte 민감도를 계산한다.

기존 명령 trace와 모델은 바꾸지 않는다. 실제 생성된 READ/WRITE 행을 burst
크기로 계수하고, 고정 가중치를 여러 prompt에서 유지한다는 별도 가정을
산술에 적용한다. 새 DDR timing schedule·전력·실물 결과를 생성하지 않는다.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import sys
import time
from collections import Counter, defaultdict
from dataclasses import asdict
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from analysis.dram_pim_model import Config, TensorAddresses, build_workload

BASELINE = 'unfused_baseline'
PIM = 'pim_data_resident'
SCENARIOS = (BASELINE, PIM)
HOST_EVERY = 'host_weights_read_each_prompt'
HOST_WEIGHT = 'host_weights_resident_intermediates_unfused'
PIM_RESIDENT = 'pim_weights_resident_intermediates_resident'
HOST_IDEAL = 'host_ideal_weights_and_intermediates_resident_fused_lower_bound'
REPETITIONS = (1, 2, 4, 16)
NAMES_KO = {
    HOST_EVERY: '가중치를 매번 읽는 host',
    HOST_WEIGHT: '가중치만 상주하는 host',
    PIM_RESIDENT: '가중치와 중간값이 상주하는 PIM',
    HOST_IDEAL: '가중치·중간값 전체가 상주하는 이상적 host',
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open('rb') as source:
        for chunk in iter(lambda: source.read(1024*1024), b''):
            value.update(chunk)
    return value.hexdigest()


def relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def require_safe_outputs(inputs: list[Path], outputs: list[Path]) -> None:
    """출처 파일을 output 인수로 넣어도 덮어쓰기 전에 거부한다."""
    protected={path.resolve() for path in inputs}
    resolved=[path.resolve() for path in outputs]
    if len(resolved)!=len(set(resolved)) or any(path in protected for path in resolved):
        raise ValueError('분석 출력은 서로 달라야 하며 기존 입력·소스를 덮어쓸 수 없습니다.')
    for path in resolved:
        path.relative_to((ROOT/'build/reports').resolve())


def fraction_record(value: Fraction) -> dict:
    """정확한 분수와 읽기 쉬운 실수 표시를 모두 남긴다."""
    return dict(numerator=value.numerator, denominator=value.denominator,
                decimal=float(value))


def reduction(host_bytes: int, pim_bytes: int) -> dict:
    if type(host_bytes) is not int or type(pim_bytes) is not int or host_bytes <= 0 or pim_bytes < 0:
        raise ValueError('비교 byte는 양의 host와 0 이상의 PIM 정수여야 합니다.')
    value = Fraction(host_bytes-pim_bytes, host_bytes)
    return dict(bytes_saved=host_bytes-pim_bytes, fraction=fraction_record(value),
                percent=float(value*100))


def parse_trace_text(text: str, config: Config) -> list[dict]:
    """각 CSV data 행을 한 burst로 센다. 같은 offset의 반복 READ도 다시 센다."""
    reader = csv.DictReader(io.StringIO(text))
    if reader.fieldnames != ['cycle', 'scenario', 'command', 'bank', 'row', 'tensor', 'byte_offset']:
        raise ValueError('기존 DRAM command CSV의 정확한 일곱 열이 필요합니다.')
    records = []
    last_cycles = defaultdict(lambda: -1)
    for line, row in enumerate(reader, 2):
        if row['scenario'] not in SCENARIOS or row['command'] not in ('ACT', 'PRE', 'READ', 'WRITE'):
            raise ValueError(f'알려지지 않은 scenario/command: CSV {line}행')
        item = dict(row)
        for key in ('cycle', 'bank', 'row', 'byte_offset'):
            item[key] = int(row[key])
        if (item['cycle'] < 0 or not 0 <= item['bank'] < config.banks
                or item['row'] < 0 or item['byte_offset'] < 0
                or item['byte_offset'] % config.burst_bytes or not item['tensor']):
            raise ValueError(f'잘못된 bank/cycle/offset: CSV {line}행')
        if item['cycle'] < last_cycles[item['scenario']]:
            raise ValueError(f'scenario 안의 cycle 순서가 역전됐습니다: CSV {line}행')
        last_cycles[item['scenario']] = item['cycle']
        records.append(item)
    if not records or {row['scenario'] for row in records} != set(SCENARIOS):
        raise ValueError('기존 두 scenario의 trace가 모두 필요합니다.')
    return records


def count_trace(records: list[dict], config: Config) -> tuple[dict, list[dict], dict]:
    """READ/WRITE만 byte에 반영하고 ACT/PRE는 원 trace의 명령수만 보존한다."""
    addresses = TensorAddresses(config)
    expected_baseline, expected_pim, _ = build_workload(config, addresses)
    weights = {f'L{layer}_{name}' for layer in range(config.layers)
               for name in ('wq', 'wk', 'wv', 'wo', 'w1', 'w2')}
    output_name = f'L{config.layers-1}_output'
    commands = {scenario: Counter() for scenario in SCENARIOS}
    counter = Counter()
    offsets = defaultdict(set)
    actual_requests = {scenario: [] for scenario in SCENARIOS}
    for row in records:
        commands[row['scenario']][row['command']] += 1
        if row['command'] in ('READ', 'WRITE'):
            name = row['tensor']
            if name not in addresses.addresses:
                raise ValueError('실제 모델에 없는 tensor입니다: '+name)
            _, logical_bytes = addresses.addresses[name]
            if row['byte_offset'] >= logical_bytes:
                raise ValueError('tensor 범위를 넘는 burst offset입니다: '+name)
            key = row['scenario'], name, row['command']
            counter[key] += 1
            offsets[key].add(row['byte_offset'])
            actual_requests[row['scenario']].append((row['command'], name, row['byte_offset']))
    # 기존 소스의 request 생성과 CSV의 data 명령 순서가 일치해야 새 분해를 신뢰한다.
    # ACT/PRE schedule를 새로 실행하지 않고 READ/WRITE 목록만 비교한다.
    for scenario, requests in ((BASELINE, expected_baseline), (PIM, expected_pim)):
        expected = [(request.operation, request.tensor, request.offset) for request in requests]
        if actual_requests[scenario] != expected:
            raise ValueError('기존 CSV의 data 명령이 현재 모델 request와 다릅니다: '+scenario)
    tensor_rows = []
    for (scenario, name, command), count in sorted(counter.items()):
        tensor_rows.append(dict(scenario=scenario, tensor=name, command=command,
            kind='weight' if name in weights else 'activation',
            logical_tensor_bytes=addresses.addresses[name][1], burst_commands=count,
            boundary_bytes=count*config.burst_bytes,
            unique_burst_offsets=len(offsets[(scenario, name, command)])))
    summary = {}
    for scenario in SCENARIOS:
        data = commands[scenario]
        summary[scenario] = dict(command_counts=dict(data),
            read_bytes=data['READ']*config.burst_bytes,
            write_bytes=data['WRITE']*config.burst_bytes,
            total_boundary_bytes=(data['READ']+data['WRITE'])*config.burst_bytes,
            weight_read_bytes=sum(count*config.burst_bytes for (s,n,c),count in counter.items()
                                  if s==scenario and n in weights and c=='READ'),
            weight_write_bytes=sum(count*config.burst_bytes for (s,n,c),count in counter.items()
                                   if s==scenario and n in weights and c=='WRITE'))
    def counted(scenario, tensor, command):
        return counter[(scenario, tensor, command)]*config.burst_bytes
    weight_read = summary[BASELINE]['weight_read_bytes']
    weight_write = summary[PIM]['weight_write_bytes']
    input_bytes = counted(PIM, 'input_hidden', 'WRITE')
    output_bytes = counted(PIM, output_name, 'READ')
    if weight_read != weight_write or summary[BASELINE]['weight_write_bytes'] or summary[PIM]['weight_read_bytes']:
        raise ValueError('기존 모델의 weight READ/초기 WRITE 대응이 다릅니다.')
    if summary[PIM]['total_boundary_bytes'] != weight_write+input_bytes+output_bytes:
        raise ValueError('PIM 외부 data 명령에 weight/input/output 이외의 이동이 있습니다.')
    input_logical = config.tokens*config.d_model*config.bytes_per_element
    rounded_io = ((input_logical+config.burst_bytes-1)//config.burst_bytes)*config.burst_bytes
    if input_bytes != rounded_io or output_bytes != rounded_io:
        raise ValueError('입출력 hidden matrix의 burst 크기와 trace가 다릅니다.')
    components = dict(weight_initial_host_read_bytes=weight_read,
        weight_initial_pim_write_bytes=weight_write,
        input_boundary_bytes_per_prompt=input_bytes,
        output_boundary_bytes_per_prompt=output_bytes,
        compulsory_io_bytes_per_prompt=input_bytes+output_bytes,
        host_unfused_total_bytes_per_prompt=summary[BASELINE]['total_boundary_bytes'],
        host_unfused_nonweight_bytes_per_prompt=summary[BASELINE]['total_boundary_bytes']-weight_read,
        original_baseline_input_read_bytes=counted(BASELINE, 'input_hidden', 'READ'),
        original_baseline_final_output_write_bytes=counted(BASELINE, output_name, 'WRITE'),
        weight_tensor_count=len(weights),
        logical_weight_storage_bytes=sum(addresses.addresses[name][1] for name in weights),
        all_allocated_logical_activation_tensor_bytes=sum(size for name,(_,size) in addresses.addresses.items()
                                                        if name not in weights))
    # 전체 tensor 논리 크기의 단순 합은 동시 live set/cache capacity가 아니다.
    checks = dict(csv_data_commands_match_model_requests=True,
                  no_dram_schedule_reexecution=True,
                  logical_activation_sum_is_not_proven_cache_capacity=True,
                  weight_initial_read_write_bytes_match=True)
    return summary, tensor_rows, dict(components=components, checks=checks)


def repeated_case(components: dict, repetitions: int, *, already_warm: bool = False) -> dict:
    """R번의 독립 고정-shape prompt를 byte 식으로 계산한다. 새 command trace가 아니다."""
    if type(repetitions) is not int or repetitions <= 0:
        raise ValueError('반복횟수 R은 양의 정수여야 합니다.')
    weight = components['weight_initial_host_read_bytes']
    weight_pim = components['weight_initial_pim_write_bytes']
    host_per = components['host_unfused_total_bytes_per_prompt']
    host_nonweight = components['host_unfused_nonweight_bytes_per_prompt']
    io_bytes = components['compulsory_io_bytes_per_prompt']
    totals = {
        HOST_EVERY: host_per*repetitions,
        HOST_WEIGHT: (0 if already_warm else weight)+host_nonweight*repetitions,
        PIM_RESIDENT: (0 if already_warm else weight_pim)+io_bytes*repetitions,
        HOST_IDEAL: (0 if already_warm else weight)+io_bytes*repetitions,
    }
    return dict(repetitions=repetitions, already_resident_before_counted_interval=already_warm,
        scope_ko='초기 적재가 관측 구간보다 먼저 끝난 warm 실행만 센다.' if already_warm else
                 '가중치 초기 이동 한 번을 포함하여 R개 독립 prompt의 총 byte를 센다.',
        scenarios={name:dict(name_ko=NAMES_KO[name], total_boundary_bytes=value,
                           average_bytes_per_prompt=fraction_record(Fraction(value,repetitions)))
                   for name,value in totals.items()},
        pim_reduction_against={host:reduction(totals[host],totals[PIM_RESIDENT])
                               for host in (HOST_EVERY,HOST_WEIGHT,HOST_IDEAL)})


def build_analysis(trace_text: str, original_report: dict) -> dict:
    config = Config(**original_report['configuration'])
    config.validate()
    records = parse_trace_text(trace_text, config)
    summary, tensor_rows, detail = count_trace(records, config)
    for scenario in SCENARIOS:
        recorded = original_report[scenario]
        for field, observed in (('bytes_crossing_host_memory_boundary',summary[scenario]['total_boundary_bytes']),
                                ('read_commands',summary[scenario]['command_counts']['READ']),
                                ('write_commands',summary[scenario]['command_counts']['WRITE']),
                                ('activate_commands',summary[scenario]['command_counts']['ACT']),
                                ('precharge_commands',summary[scenario]['command_counts']['PRE'])):
            if recorded[field] != observed:
                raise ValueError('기존 JSON과 CSV 계수가 다릅니다: '+scenario+'/'+field)
    components = detail['components']
    cold = repeated_case(components, 1)
    percentage = cold['pim_reduction_against'][HOST_EVERY]['percent']
    if round(percentage,2) != original_report['comparison']['offchip_byte_reduction_percent']:
        raise ValueError('기존 69.64% 기록과 cold trace 산술이 다릅니다.')
    limits = {
        HOST_EVERY:components['host_unfused_total_bytes_per_prompt'],
        HOST_WEIGHT:components['host_unfused_nonweight_bytes_per_prompt'],
        PIM_RESIDENT:components['compulsory_io_bytes_per_prompt'],
        HOST_IDEAL:components['compulsory_io_bytes_per_prompt'],
    }
    return dict(passed=True, model_name='existing_dram_trace_cache_and_repetition_byte_sensitivity',
        scope_ko='기존 실제 생성 CSV의 READ/WRITE를 계수한 뒤 별도 캐시·반복 가정으로 byte만 계산했다. '
                 '새 DDR/PIM controller 실행·필터된 trace timing·전력·실물 측정 결과가 아니다.',
        configuration=asdict(config), existing_csv_rows=len(records),
        trace_counts=summary, tensor_command_counts=tensor_rows, boundary_bytes_components=components,
        validation=detail['checks'],
        original_cold_trace=dict(host_bytes=summary[BASELINE]['total_boundary_bytes'],
            pim_bytes=summary[PIM]['total_boundary_bytes'],
            pim_reduction_percent=percentage,
            original_report_rounded_reduction_percent=original_report['comparison']['offchip_byte_reduction_percent'],
            original_report_unchanged=True),
        cold_start_repeated_cases=[repeated_case(components,r) for r in REPETITIONS],
        already_resident_warm_cases=[repeated_case(components,r,already_warm=True) for r in REPETITIONS],
        infinite_repetition_limit=dict(average_bytes_per_prompt=limits,
            pim_reduction_against={host:reduction(limits[host],limits[PIM_RESIDENT])
                                   for host in (HOST_EVERY,HOST_WEIGHT,HOST_IDEAL)},
            total_bytes_are_not_finite_for_infinite_prompts=True),
        assumptions_ko=[
            'R은 같은 가중치와 T16/D32/H4/F64/L2 형상을 사용하는 독립 hidden-matrix prompt 계산 횟수다. '
            '한 prompt 안의 토큰 생성 횟수나 실제 사용자의 ChatGPT 요청시간이 아니다.',
            '입력은 prompt마다 새로 전달하고 최종 출력도 prompt마다 외부에 전달한다. '
            '기존 모델의 PIM input WRITE와 output READ 크기를 공통 입출력 경계로 남겨 둔다.',
            'weight-only host는 첫 READ 뒤 weight cache eviction 없이 유지하며, 중간 activation 이동은 기존 미융합 trace와 같다.',
            'PIM은 최초 weight WRITE 한 번 뒤 가중치와 중간 activation이 계속 bank 가까이에 머문다고 가정한다.',
            '이상적 host는 weight cache가 충분하고 모든 중간 activation이 경계 밖으로 나가지 않는 fused/resident 하한 가정이다. '
            '현재 CPU/GPU cache 용량·커널 최적화·실측으로 구현 가능성을 증명하지 않았다.',
            '이상적 host와 PIM의 같은 byte 및 0% 차이는 공통 외부 입출력을 매 prompt 남겨 두는 이 경계 정의 안에서만 성립한다. '
            '입출력도 처음부터 온칩에 있으면 경계가 달라져 2048B 하한도 달라진다.',
            'READ를 산술에서 빼도 ACT/PRE와 service cycle이 같은 비율로 줄지는 않는다. 새 schedule/time/power는 계산하지 않는다.',
            'DRAM 분석의 D32/T16은 실제 Nexys GPT의 D16/T8 또는 D16/T32와 다른 workload다.',
        ],
        new_dram_trace_generated=False, original_trace_modified=False,
        new_vivado_execution_performed=False, training_performed=False,
        ddr_time_measured=False, power_measured=False, physical_board_measured=False)


def write_tensor_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w',encoding='utf-8-sig',newline='') as target:
        writer=csv.DictWriter(target,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def make_plot(result: dict, output: Path, library_directory: Path) -> dict:
    """표준 matplotlib의 정적 그림. 실제 byte 산술표와 같은 점만 그린다."""
    if library_directory.is_dir():
        sys.path.insert(0,str(library_directory))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties, fontManager
    fonts=[Path('C:/Windows/Fonts/malgun.ttf'),Path('C:/Windows/Fonts/NanumGothic.ttf')]
    font=next((path for path in fonts if path.is_file()),None)
    if font is None:
        raise RuntimeError('한글 그래프에 맑은 고딕 또는 나눔고딕 TTF가 필요합니다.')
    fontManager.addfont(str(font))
    font_name=FontProperties(fname=str(font)).get_name()
    plt.rcParams.update({'font.family':font_name,'axes.unicode_minus':False,'font.size':10})
    labels=['1','2','4','16','무한 반복 한계']
    cases=result['cold_start_repeated_cases']
    limits=result['infinite_repetition_limit']
    data={name:[case['scenarios'][name]['average_bytes_per_prompt']['decimal']/1024 for case in cases]
               +[limits['average_bytes_per_prompt'][name]/1024]
          for name in (HOST_EVERY,HOST_WEIGHT,PIM_RESIDENT,HOST_IDEAL)}
    percentages={host:[case['pim_reduction_against'][host]['percent'] for case in cases]
                       +[limits['pim_reduction_against'][host]['percent']]
                 for host in (HOST_EVERY,HOST_WEIGHT,HOST_IDEAL)}
    fig,axes=plt.subplots(1,2,figsize=(14,6),dpi=160)
    colors={HOST_EVERY:'#354E70',HOST_WEIGHT:'#E58B23',PIM_RESIDENT:'#168D80',HOST_IDEAL:'#7858A6'}
    for name,label in ((HOST_EVERY,NAMES_KO[HOST_EVERY]),(HOST_WEIGHT,NAMES_KO[HOST_WEIGHT]),
                       (PIM_RESIDENT,'PIM · 이상적 host (이 가정에서는 값 일치)')):
        axes[0].plot(range(5),data[name],marker='o',linewidth=2,color=colors[name],label=label)
    axes[0].set_title('초기 가중치 이동 1회 포함: prompt당 평균 전송량')
    axes[0].set_ylabel('외부 경계를 넘는 byte / 1024 (KiB)')
    axes[0].set_ylim(0,120)
    for host,label in ((HOST_EVERY,'매번 weight READ host와 비교'),
                       (HOST_WEIGHT,'weight 상주 host와 비교'),
                       (HOST_IDEAL,'이상적 전체 상주 host와 비교')):
        axes[1].plot(range(5),percentages[host],marker='o',linewidth=2,color=colors[host],label=label)
    axes[1].set_title('PIM의 byte 감소율: 비교 기준이 바뀌면 값도 바뀜')
    axes[1].set_ylabel('(host byte - PIM byte) / host byte × 100')
    axes[1].set_ylim(-5,105)
    axes[1].annotate('원 cold trace 69.64%',(0,percentages[HOST_EVERY][0]),
                     xytext=(.12,55),arrowprops=dict(arrowstyle='->',color='#354E70'))
    axes[1].annotate('이상적 host 대비 0%',(3,0),xytext=(1.6,12),
                     arrowprops=dict(arrowstyle='->',color='#7858A6'))
    for axis in axes:
        axis.set_xticks(range(5),labels)
        axis.set_xlabel('R: 같은 가중치로 계산한 독립 prompt 수 (범주 간격)')
        axis.grid(alpha=.2)
        axis.legend(loc='center right',fontsize=9)
    fig.suptitle('DRAM-PIM 캐시·반복 실행 민감도 | T16 · D32 · H4 · F64 · L2',fontsize=15)
    fig.text(.5,.02,'기존 CSV 계수에 추가 가정을 적용한 byte 산술이며 DDR 시간·전력·실물 측정값이 아닙니다. '
             '공통 외부 입출력 1,024 + 1,024B를 유지합니다.',ha='center',fontsize=9)
    fig.tight_layout(rect=(0,.06,1,.94))
    output.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(output)
    plt.close(fig)
    from PIL import Image
    with Image.open(output) as image:
        width,height=image.size
    return dict(file=relative(output),sha256=digest(output),width=width,height=height,
        source_data_kiB=data,source_reduction_percent=percentages,
        font_file=font.name,font_sha256=digest(font),matplotlib_version=matplotlib.__version__,
        visual_review_completed=False,new_measurement=False)


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--trace',default='fixtures/dram_pim_command_trace.csv')
    parser.add_argument('--model-report',default='fixtures/dram_pim_model.json')
    parser.add_argument('--output',default='build/reports/dram_pim_sensitivity.json')
    parser.add_argument('--tensor-csv',default='build/reports/dram_pim_sensitivity_tensor_counts.csv')
    parser.add_argument('--plot',action='store_true')
    parser.add_argument('--plot-output',default='build/reports/dram_pim_sensitivity.png')
    parser.add_argument('--plot-libraries',default='build/vendor_ff_probe/plot_libs')
    args=parser.parse_args()
    started=time.perf_counter()
    trace=(ROOT/args.trace).resolve()
    model_report=(ROOT/args.model_report).resolve()
    inputs=[trace,model_report,ROOT/'analysis/dram_pim_model.py',Path(__file__),
            ROOT/'analysis/test_dram_pim_sensitivity.py']
    output=(ROOT/args.output).resolve()
    tensor_csv=(ROOT/args.tensor_csv).resolve()
    plot=(ROOT/args.plot_output).resolve()
    require_safe_outputs(inputs,[output,tensor_csv]+([plot] if args.plot else []))
    source_before={relative(path):digest(path) for path in inputs}
    result=build_analysis(trace.read_text(encoding='utf-8-sig'),
                          json.loads(model_report.read_text(encoding='utf-8-sig')))
    write_tensor_csv(tensor_csv,result['tensor_command_counts'])
    result['tensor_count_csv']=dict(file=relative(tensor_csv),sha256=digest(tensor_csv))
    if args.plot:
        result['plot']=make_plot(result,plot,(ROOT/args.plot_libraries).resolve())
    result['source_sha256']=source_before
    result['source_sha256_after']={relative(path):digest(path) for path in inputs}
    if result['source_sha256_after'] != source_before:
        raise RuntimeError('분석 중 기존 입력 또는 분석 소스가 바뀌었습니다.')
    result['existing_inputs_unchanged']=True
    result['wall_seconds']=round(time.perf_counter()-started,6)
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(passed=result['passed'],output=relative(output),
        source_sha256=result['source_sha256'],components=result['boundary_bytes_components'],
        cold_start_totals=[dict(R=case['repetitions'],
            totals={key:value['total_boundary_bytes'] for key,value in case['scenarios'].items()})
                          for case in result['cold_start_repeated_cases']],
        infinite_limit=result['infinite_repetition_limit']),ensure_ascii=False,indent=2))
    return 0


if __name__ == '__main__':
    for stream in (sys.stdout,sys.stderr):
        if hasattr(stream,'reconfigure'):
            stream.reconfigure(encoding='utf-8')
    raise SystemExit(main())
