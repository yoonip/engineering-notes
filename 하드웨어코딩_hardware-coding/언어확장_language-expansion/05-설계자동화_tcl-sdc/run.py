"""Yosys의 Tcl 실행과 SDC 생성 결과를 확인합니다. STA는 실행하지 않습니다."""  # 이 실행기의 확인 범위
import argparse  # 도구와 결과 위치 선택
import hashlib  # 실제 컴파일 입력의 바이트 해시
import json  # 생성된 일반 회로 구조 읽기
import os  # 하위 도구의 DLL 경로와 설정 전달
from pathlib import Path  # 소스와 임시 작업 경로
import shutil  # 도구 검색과 원본 바이트 복사
import subprocess  # 실제 Yosys 프로세스 실행
import sys  # assert를 제거하는 실행 옵션 확인
import tempfile  # 기존 결과와 겹치지 않는 작업 폴더
ROOT = Path(__file__).resolve().parent  # 현재 예제의 위치
RTL = ROOT.parents[1] / '예제_examples/01-전송대기_elastic-buffer/elastic_buffer.sv'  # 기존 직접 작성 회로를 읽기만 하기
def main():  # 정상 설정과 잘못된 주기 설정을 함께 실행
    parser = argparse.ArgumentParser(description=__doc__)  # CLI 설명과 도움말
    parser.add_argument('--yosys', default=shutil.which('yosys'), required=not shutil.which('yosys'))  # 실제 도구 경로
    parser.add_argument('--out', type=Path, required=True)  # 새 결과 JSON 위치
    parser.add_argument('--build-dir', type=Path)  # 작업 폴더의 선택 가능한 부모
    args = parser.parse_args()  # 실행 인자 읽기
    if sys.flags.optimize: parser.error('run without -O: assertions must remain enabled')  # 검사가 생략된 실행으로 성공 기록을 만들지 않기
    if args.build_dir: args.build_dir.mkdir(parents=True, exist_ok=True)  # 기존 폴더는 지우지 않기
    work = Path(tempfile.mkdtemp(prefix='tcl-sdc-', dir=args.build_dir)).resolve()  # 이번 실행만의 경로
    yosys = Path(args.yosys).resolve()  # 상대 실행 파일을 절대 경로로 고정
    suite = yosys.parent.parent  # OSS CAD Suite라면 bin과 lib의 공통 부모
    environment = os.environ.copy()  # 호출한 셸의 설정에서 시작
    environment['PATH'] = os.pathsep.join([str(yosys.parent), str(suite / 'lib'), environment.get('PATH', '')])  # Windows DLL 검색을 이 프로세스에만 적용
    environment['YOSYSHQ_ROOT'] = str(suite)  # 배포본의 내부 자료 위치
    commands = []  # 실제 실행 명령과 출력 보관
    def command(argv, cwd, env):  # 셸 문자열을 만들지 않는 실행
        result = subprocess.run([str(x) for x in argv], cwd=cwd, env=env, capture_output=True, timeout=60)  # 도구별 시간 상한
        item = dict(argv=[str(x) for x in argv], cwd=str(cwd), returncode=result.returncode, stdout=result.stdout.decode('utf-8', 'replace'), stderr=result.stderr.decode('utf-8', 'replace'))  # 성공과 실패 모두 기록
        commands.append(item)  # 재현할 수 있는 원래 출력 보존
        return item  # 호출한 검사에 결과 전달
    version = command([yosys, '-V'], work, environment)  # 실제 실행 파일의 판본 확인
    assert version['returncode'] == 0  # 도구 시작 실패를 성공으로 세지 않기
    records = []  # 주기별 구조 검사 결과
    for index, period in enumerate(['10.0', '5.0', '0', '-1', 'oops', '0.0001', 'NaN', 'Inf', '-Inf']):  # 정상 두 경우와 반올림·비유한값을 포함한 설정 오류 일곱 경우
        current = work / str(index)  # 매번 비어 있는 독립 작업 위치
        current.mkdir()  # 이전 netlist나 SDC를 재사용하지 않기
        shutil.copyfile(ROOT / 'flow.tcl', current / 'flow.tcl')  # 실행할 Tcl 소스 그대로 복사
        shutil.copyfile(ROOT / 'bootstrap.tcl', current / 'bootstrap.tcl')  # 입력 파일의 UTF-8 해석을 명시하는 작은 진입점
        shutil.copyfile(RTL, current / 'elastic_buffer.sv')  # 기존 RTL을 고치지 않고 복사
        child_env = dict(environment, PERIOD_NS=period)  # 주기 값만 설정별로 다르게 전달
        result = command([yosys, '-Q', '-c', 'bootstrap.tcl'], current, child_env)  # 실제 Tcl 내장 Yosys에서 UTF-8 스크립트 실행
        if index >= 2:  # 잘못된 입력은 합성 완료와 구분
            assert result['returncode'] != 0 and 'period_ns must be' in result['stderr'] + result['stdout']  # 지정한 설정 오류로 실패했는지 확인
            assert not (current / 'design.json').exists()  # 잘못된 설정에서 생성물을 내놓지 않기
            records.append(dict(period_ns=period, status='expected_configuration_rejection'))  # 입력 검사 결과 기록
            continue  # 다음 설정으로 진행
        assert result['returncode'] == 0 and 'PASS tcl_flow' in result['stdout']  # 도구 종료와 완료 표식을 함께 확인
        module = json.loads((current / 'design.json').read_text(encoding='utf-8'))['modules']['elastic_buffer']  # 실제 변환된 최상위 회로 읽기
        expected = dict(clk=('input', 1), rst=('input', 1), in_valid=('input', 1), in_data=('input', 8), in_ready=('output', 1), out_valid=('output', 1), out_data=('output', 8), out_ready=('input', 1))  # 독립 인터페이스 계약
        observed = {name: (port['direction'], len(port['bits'])) for name, port in module['ports'].items()}  # 도구가 만든 포트 폭과 방향
        assert observed == expected  # 빠지거나 잘못 연결된 외부 포트 검사
        registers = [cell for cell in module['cells'].values() if cell['type'] in ('$dff', '$dffe', '$sdff', '$sdffe', '$sdffce')]  # 일반 플립플롭 셀만 선택
        state_bits = sum(int(cell['parameters']['WIDTH'], 2) for cell in registers)  # 데이터와 점유 상태의 레지스터 폭 합계
        assert state_bits == 9  # 데이터 8비트와 점유 1비트의 독립 기대값
        sdc = (current / 'constraints.sdc').read_text(encoding='utf-8')  # 실제 생성한 제약 파일
        active = [line for line in sdc.splitlines() if line.strip() and not line.lstrip().startswith('#')]  # 명령 줄 개수 확인
        expected_lines = [  # 주기만 달라지고 나머지 경계 조건은 고정인 출력 계약
            f'create_clock -name core_clk -period {float(period):.3f} [get_ports clk]',  # 클록 이름·값·대상 포트
            'set_clock_uncertainty 0.1 [get_clocks core_clk]',  # 같은 클록의 불확실성
            'set_input_delay -clock core_clk -max 2.0 [get_ports {rst in_valid in_data* out_ready}]',  # 데이터 입력의 최대 도착 조건
            'set_input_delay -clock core_clk -min 0.2 [get_ports {rst in_valid in_data* out_ready}]',  # 같은 입력의 최소 도착 조건
            'set_output_delay -clock core_clk -max 2.0 [get_ports {in_ready out_valid out_data*}]',  # 외부 수신 조건의 최대값
            'set_output_delay -clock core_clk -min 0.2 [get_ports {in_ready out_valid out_data*}]',  # 외부 수신 조건의 최소값
        ]  # 여섯 활성 명령 전체를 대조할 기준
        assert [line.split(';', 1)[0].strip() for line in active] == expected_lines  # 주석을 뺀 명령·값·대상 목록이 모두 일치해야 통과
        assert not any(cell['type'].startswith('$dlatch') for cell in module['cells'].values())  # 의도하지 않은 래치 유무 확인
        records.append(dict(period_ns=period, status='passed_generic_structure_and_sdc_generation', port_count=len(observed), state_bits=state_bits, sdc_commands=len(active), sdc_text=sdc))  # STA 결과와 구분한 기록
    hashes = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in ('bootstrap.tcl', 'flow.tcl', 'run.py')}  # 실행한 자기 소스의 해시
    record = dict(status='passed', work_directory=str(work), source_sha256=hashes, dependency_sha256=hashlib.sha256(RTL.read_bytes()).hexdigest(), version=version, commands=commands, settings=records, scope=dict(generic_netlist=True, sdc_generation=True, sta=False, cell_library_mapping=False, physical_timing=False))  # 확인한 단계만 표시
    args.out.parent.mkdir(parents=True, exist_ok=True)  # 결과 JSON 부모 준비
    args.out.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')  # 전체 로그와 구조 기록 저장
    print('PASS tcl_sdc normal=2 configuration_rejections=7 ports=8 state_bits=9')  # 실제 통과 집계
if __name__ == '__main__': main()  # 직접 실행할 때만 도구 호출
