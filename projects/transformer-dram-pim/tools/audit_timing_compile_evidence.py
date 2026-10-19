"""완료된 SDF 실행의 실제 simulator 생성 옵션을 전달 폴더에 보존한다.

이 명령은 회로를 다시 실행하지 않는다. 실행 JSON에 쓴 희망 설정과 실제
xelab 명령, 생성된 Compile_Options.txt, 준비 manifest의 SHA를 대조한다.
실행 중인 stage에는 쓰지 않으며 실제 옵션 원문은 해당 결과 폴더에 복사한다.
UART PASS 여부는 원 실행 결과 그대로 별도 필드에 남긴다.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import shlex
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from fpga.nexys4_ddr.verify_timing_netlist import compile_policy, verify_prepared_identity
from fpga.nexys4_ddr.verify_netlist import testbench
from tools.verify_delivery import timing_history_path


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open('rb') as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b''):
            value.update(chunk)
    return value.hexdigest()


def bound_identity(report: dict, manifest: dict, folder: Path, wanted: dict) -> dict:
    """보고서와 실제 TB에서 정체성을 새로 만든다. manifest의 자기 비교를 막는다.

    identity의 TB SHA는 생성 문자열 UTF-8/LF이고 files의 SHA는 Windows가 쓴
    실제 CRLF byte일 수 있다. 둘을 구분하여 검사하므로 줄바꿈 차이를 회로
    변화로 오해하지 않으면서 TB 내용/baud가 다른 준비 자료는 거부한다.
    """
    context = report['core_context']
    assert context in (8, 32), '감사 대상은 현재 8/32-token 보드 실행입니다.'
    board_folder = ROOT / 'build/nexys4_ddr' / (
        'board' if context == 8 else 'board_context32_distributed')
    board = json.loads((board_folder / 'result.json').read_text(encoding='utf-8-sig'))
    assert digest(board_folder / 'result.json') == report['board_implementation_report_sha256']
    assert board['routed_checkpoint']['sha256'] == report['routed_checkpoint_sha256']
    assert digest(board_folder / 'routed.dcp') == report['routed_checkpoint_sha256']
    assert board['checkpoint_sha256'] == report['model_checkpoint_sha256']
    assert digest(ROOT / 'output/tiny_gpt_full_ops_qat/tiny_gpt_qat_q88.json') == report['model_checkpoint_sha256']
    assert board['max_context'] == context
    assert board['clock_hz'] == report['board_clock_hz']
    assert board.get('host_baud', 115200) == report['host_baud']
    assert report['timing_corner'] in ('slow', 'fast')
    assert report['delay_mode'] == {'slow': 'max', 'fast': 'min'}[report['timing_corner']]
    raw_tb = folder / 'tb_nexys_netlist.sv'
    assert digest(raw_tb) == manifest['files']['tb_nexys_netlist.sv']
    generated = testbench(report['host_baud']).replace(
        'post-route functional netlist', 'post-route timing netlist')
    assert raw_tb.read_text(encoding='utf-8') == generated, '현재 baud의 공통 TB와 보존 TB 내용이 다릅니다.'
    wanted_identity = {
        'dcp_sha256': report['routed_checkpoint_sha256'],
        'model_sha256': report['model_checkpoint_sha256'],
        'corner': report['timing_corner'], 'delay_mode': report['delay_mode'],
        'host_baud': report['host_baud'], 'safe_instance_names': report['safe_instance_names'],
        'name_invariance_mode': report['name_invariance_mode'],
        'testbench_sha256': hashlib.sha256(generated.encode('utf-8')).hexdigest(),
        **wanted,
    }
    if report.get('lexical_safe_instance_names'):
        wanted_identity['lexical_safe_instance_names'] = True
    for key in wanted_identity.keys() - wanted.keys():
        assert manifest['identity'].get(key) == wanted_identity[key], '보고서/TB와 manifest 조건 불일치: ' + key
    return wanted_identity


def annotation_flags(tokens: list[str], delay_mode: str) -> None:
    """희망 설정이 아닌 실제 명령/생성 옵션 양쪽의 annotation 조건을 검사한다."""
    assert tokens.count('--' + delay_mode + 'delay') == 1
    assert sum(tokens.count('--' + value + 'delay') for value in ('min', 'typ', 'max')) == 1
    assert tokens.count('--transport_int_delays') == 1
    assert not any(flag in tokens for flag in ('--notimingchecks', '--nospecify'))
    libraries = [tokens[index + 1] for index, token in enumerate(tokens[:-1]) if token == '-L']
    assert libraries == ['simprims_ver', 'secureip']
    assert tokens.count('xil_defaultlib.tb_nexys_netlist') == 1
    assert tokens.count('xil_defaultlib.glbl') == 1
    assert tokens.count('-s') == 1 and tokens[tokens.index('-s') + 1] == 'nexys_timing'


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', required=True, help='현재 프로젝트 아래 완료된 result.json 또는 그 폴더')
    parser.add_argument('--policy', required=True, choices=('Transport0', 'Inertial100'))
    args = parser.parse_args()
    path = (ROOT / args.run).resolve()
    if path.is_dir():
        path /= 'result.json'
    path.relative_to((ROOT / 'build/nexys4_ddr').resolve())
    assert path.name == 'result.json' and path.is_file(), '완료 결과 JSON이 필요합니다.'
    report = json.loads(path.read_text(encoding='utf-8-sig'))
    assert report.get('prepared') is True, 'xelab 준비가 완료되지 않은 실행입니다.'
    folder = path.parent
    manifest_path = folder / 'prepared_manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8-sig'))
    value = 0 if args.policy == 'Transport0' else 100
    wanted = dict(pulse_r_percent=value, pulse_int_r_percent=value,
                  pulse_e_percent=value, pulse_int_e_percent=value, optimization_level=2)
    # 옛 manifest가 r/O 필드를 기록하지 않은 경우도 실제 옵션/명령에 한해
    # 0/0/O2를 입증한다. 누락을 arbitrary policy로 해석하지 않는다.
    requested = bound_identity(report, manifest, folder, wanted)
    source = Path(report['ascii_stage']) / 'xsim.dir/nexys_timing/Compile_Options.txt'
    preserved = folder / 'actual_Compile_Options.txt'
    previous_path = folder / 'compile_policy_evidence.json'
    previous = None
    if previous_path.is_file():
        previous = json.loads(previous_path.read_text(encoding='utf-8'))
    if not source.is_file():
        assert previous is not None and preserved.is_file(), '실제 옵션 원문 또는 이전 보존 증거가 없습니다.'
        assert previous['run_report_sha256'] == digest(path), '이전 보존 뒤 실행 결과가 변경됐습니다.'
        assert previous['prepared_manifest_sha256'] == digest(manifest_path)
        assert digest(preserved) == previous['actual_compile_options_sha256']
        source = preserved
    original_bytes = source.read_bytes()
    options_tokens = shlex.split(original_bytes.decode('utf-8-sig'))
    actual = compile_policy(options_tokens)
    annotation_flags(options_tokens, report['delay_mode'])
    assert actual == wanted, '실제 Compile_Options의 pulse/최적화 정책이 요청과 다릅니다.'
    identity_evidence = verify_prepared_identity(manifest['identity'], requested, source)
    compile_report = report
    if report.get('preparation_reused'):
        reference = timing_history_path(report['preparation_source_result_path'])
        assert digest(reference) == report['preparation_source_result_sha256']
        compile_report = json.loads(reference.read_text(encoding='utf-8-sig'))
        assert compile_report['prepared'] is True
        for key in ('routed_checkpoint_sha256', 'model_checkpoint_sha256', 'timing_corner',
                    'delay_mode', 'host_baud', 'board_clock_hz', 'core_context', 'ascii_stage',
                    'safe_instance_names', 'name_invariance_mode', 'lexical_safe_instance_names',
                    'timing_netlist_sha256', 'board_implementation_report_sha256'):
            assert compile_report.get(key) == report.get(key), '준비 출처와 완료 실행 조건 불일치: ' + key
        assert compile_report['sdf']['sha256'] == report['sdf']['sha256']
        assert digest(manifest_path) == report['preparation_manifest_sha256']
    steps = [step for step in compile_report['steps'] if step['stage'] == 'xelab']
    assert len(steps) == 1 and steps[0]['returncode'] == 0
    assert not steps[0].get('timed_out', False)
    command_policy = compile_policy(steps[0]['command'])
    assert command_policy == actual, '실제 xelab 명령과 생성 옵션이 다릅니다.'
    annotation_flags(steps[0]['command'], report['delay_mode'])
    for key, expected in wanted.items():
        # 이전 driver의 명시되지 않은 reject/O2는 위 원문 두 증거로 보완한다.
        if key in report:
            assert report[key] == expected, key
        else:
            assert args.policy == 'Transport0' and key in (
                'pulse_r_percent', 'pulse_int_r_percent', 'optimization_level')
    manifest_option_sha = manifest['files'].get('xsim.dir/nexys_timing/Compile_Options.txt')
    if manifest_option_sha is not None:
        assert hashlib.sha256(original_bytes).hexdigest() == manifest_option_sha
    if source != preserved:
        preserved.write_bytes(original_bytes)
    assert digest(preserved) == hashlib.sha256(original_bytes).hexdigest()
    kernel = Path(report['ascii_stage']) / 'xsim.dir/nexys_timing/xsimk.exe'
    recorded_kernel_sha = manifest['files']['xsim.dir/nexys_timing/xsimk.exe']
    if kernel.is_file():
        assert digest(kernel) == recorded_kernel_sha, '실제 kernel의 준비 SHA가 다릅니다.'
        kernel_verified = True
    else:
        assert previous is not None and previous['kernel_sha_verified_at_original_audit']
        assert previous['run_report_sha256'] == digest(path)
        assert previous['prepared_manifest_sha256'] == digest(manifest_path)
        assert previous['kernel_sha256'] == recorded_kernel_sha
        kernel_verified = True
    result = dict(
        passed=True, mode='completed_timing_run_compile_options_preservation',
        new_simulations_performed=False, physical_board_measured=False,
        simulation_passed=report['passed'], requested_profile=args.policy,
        actual_policy=actual, command_policy=command_policy,
        identity_evidence=identity_evidence,
        run_report=path.relative_to(ROOT).as_posix(), run_report_sha256=digest(path),
        prepared_manifest_sha256=digest(manifest_path),
        actual_compile_options_file=preserved.relative_to(ROOT).as_posix(),
        actual_compile_options_sha256=digest(preserved),
        compile_options_recorded_in_original_manifest=manifest_option_sha is not None,
        kernel_sha256=recorded_kernel_sha,
        kernel_sha_verified_at_original_audit=kernel_verified,
        kernel_binary_in_delivery_package=False,
        source_sha256={p.relative_to(ROOT).as_posix(): digest(p) for p in (
            Path(__file__), ROOT / 'fpga/nexys4_ddr/verify_timing_netlist.py')},
        scope_ko='완료 실행의 실제 compile 설정 보존 검사. 이 감사의 PASS는 UART/SDF 시뮬레이션 PASS를 새로 만들지 않는다.')
    previous_path.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(passed=True, simulation_passed=result['simulation_passed'],
                         report=previous_path.relative_to(ROOT).as_posix()), ensure_ascii=False))


if __name__ == '__main__':
    main()
