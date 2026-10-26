# Tcl 설계 자동화와 SDC 클록·입출력 조건

[언어 확장 목차](../README.md) · [기존 전송 버퍼](../../예제_examples/01-전송대기_elastic-buffer/README.md)

## Tcl과 SDC를 따로 익힐 이유

Tcl은 설계 도구에 작업 순서·설정·파일을 전달하는 언어입니다. SDC는 Tcl 문법을 바탕으로 클록과 입출력 지연 같은 타이밍 조건을 기술하는 명령 집합입니다. 회로 소스를 작성하는 것과 합성 작업을 재현하는 것, 어떤 속도로 동작해야 하는지를 요구하는 것은 서로 다른 역할입니다.

이 예제는 기존 전송 버퍼를 변경하지 않고 임시 폴더에 복사한 뒤 Yosys의 실제 Tcl 인터프리터로 읽습니다. proc·opt·check를 실행하고 포트·레지스터·래치 유무를 검사하며, 다음 타이밍 분석에 사용할 SDC 파일을 생성합니다. Tcl을 읽는 단계에서는 SDC 안의 get_ports 같은 명령을 실행하지 않습니다.

## 입력에서 결과까지

| 단계 | 입력·실행 | 확인한 결과 |
| --- | --- | --- |
| 1 | PERIOD_NS=10.0과 사전의 top·source | 설정의 자료형·범위와 파일 존재 확인 |
| 2 | bootstrap.tcl에서 UTF-8 source | 한국어 주석을 포함한 flow.tcl 읽기 |
| 3 | format과 puts | 클록·불확실성·최대/최소 입출력 조건 6줄 생성 |
| 4 | yosys read_verilog와 hierarchy | elastic_buffer 모듈과 계층 확인 |
| 5 | yosys proc·opt·check -assert | 일반 회로 구조 변환과 구조 오류 확인 |
| 6 | design.json | 포트 8개, 저장 상태 9비트, 래치 없음 확인 |

주기 5.0에서도 같은 구조 검사를 통과했습니다. 두 주기 값은 생성 SDC에 들어가는 요구 조건이며, 이 흐름의 Yosys 최적화가 SDC를 읽고 타이밍을 맞춘 결과는 아닙니다. 일반 셀 구조를 FPGA의 LUT 개수나 실제 동작 주파수로 해석하지 않습니다.

## 줄별 문법과 의도

| 문법 | 이 예제에서 쓰는 이유 |
| --- | --- |
| dict create / dict get | 한 작업의 설정을 이름으로 묶어 관리 |
| 중괄호로 감싼 문자열 | SDC의 대괄호 명령을 생성 단계에서 실행하지 않기 |
| format | 입력 주기를 소수 셋째 자리까지 기록 |
| source -encoding utf-8 | 이 배포본의 기본 파일 해석과 무관하게 UTF-8 주석 보존 |
| yosys 접두사 | Tcl 자체의 proc와 Yosys의 proc 명령 충돌 구분 |
| check -assert | 구조 오류가 있으면 성공 기록을 내기 전에 중단 |

주기는 이 예제에서 0.001~1,000,000ns 범위로 제한합니다. 더 작은 양수를 소수 셋째 자리로 출력하면 0.000이 될 수 있으므로 범위 검사에서 거절합니다. 시간 숫자는 ns로 정한 예시 계약이며 실제 STA 환경에서는 Liberty와 도구의 시간 단위에 맞춥니다. 데이터 입력 목록에는 clk를 넣지 않으며, 동기 입력으로 다루는 rst도 명시합니다. 비동기 리셋이나 다른 클록 도메인의 예외 조건을 자동으로 가정하지 않습니다.

## 실제 실행과 확인 범위

Yosys0.69+187의 내장 Tcl에서 정상 주기 두 경우가 통과했습니다. 0·음수·숫자가 아닌 값·0으로 반올림될 0.0001·NaN·양/음의 무한대는 각각 설정 오류로 거절됐고 netlist를 만들지 않았습니다. 실행기는 Python -O를 거절하여 assert가 제거된 상태로 성공 기록을 만들지 않습니다.

SDC는 생성한 명령과 주기를 텍스트로 대조한 범위입니다. OpenSTA나 상용 STA 엔진에서 read_sdc를 실행하거나 Liberty·배선 기생값·핀 부하로 setup/hold를 계산한 결과가 아닙니다. 실패 경로를 숨기는 false_path나 multicycle 예외도 추가하지 않습니다.

```bash
python -B run.py --yosys /path/to/yosys --out /path/to/new-tcl-results.json
```

각 실행은 새 작업 폴더에서 수행합니다. Windows OSS CAD Suite에서는 실행기에서만 bin·lib 검색 경로를 지정하며 전역 PATH를 바꾸지 않습니다. 실제 명령·출력·생성한 SDC·소스 해시는 [example.json](example.json)에 있습니다. constraints.sdc는 정상 10ns 실행에서 생성한 예시 파일입니다.

## 실무에 연결할 때

같은 소스를 같은 설정으로 읽었는지, 잘못된 설정을 초기에 거절하는지, 생성물이 이전 실행의 잔재가 아닌지를 자동화합니다. 이후 셀 라이브러리에 매핑한 netlist와 실제 시간 제약을 STA 도구에 전달합니다. 설계가 바뀌면 대상 포트가 실제로 선택되는지도 해당 도구에서 확인합니다. 제약 파일이 만들어졌다는 사실만으로 타이밍 충족을 판단하지 않습니다.

## 출처

[Yosys Tcl 명령 문서](https://yosyshq.readthedocs.io/projects/yosys/en/0.45/cmd/tcl.html)의 yosys 접두사·명령 충돌 설명과 설치 도구의 help tcl을 대조했습니다. [Tcl source 원문](https://github.com/tcltk/tcl/blob/core-8-6-branch/doc/source.n)은 입력 인코딩 옵션의 근거입니다. [OpenSTA 공식 저장소](https://github.com/parallaxsw/OpenSTA)는 SDC·Liberty·netlist의 역할을 구분할 때 참고했습니다. 웹 문서의 판본과 실제 실행한 Yosys 판본은 구분합니다. 스크립트와 설명은 직접 작성했으며 외부 도구 코드를 포함하지 않습니다.

## bootstrap.tcl의 전체 코드

```tcl
source -encoding utf-8 flow.tcl ; # Load the script with an explicit input encoding
```

## flow.tcl의 전체 코드

```tcl
set config [dict create top elastic_buffer source elastic_buffer.sv period_ns 10.0] ; # 이번 합성 작업의 이름·소스·클록 조건
if {[info exists ::env(PERIOD_NS)]} { dict set config period_ns $::env(PERIOD_NS) } ; # 실행 환경이 넘긴 클록 주기를 선택
set period [dict get $config period_ns] ; # 사전에서 사용할 주기를 한 번 꺼내기
if {![string is double -strict $period]} { error "period_ns must be a positive finite number" } ; # 숫자가 아닌 설정을 합성 전에 거절
if {$period < 0.001 || $period > 1000000 || $period != $period} { error "period_ns must be a number in 0.001..1000000" } ; # 1ps 이상 범위와 자기 비교가 다른 NaN을 함께 검사
set source [dict get $config source] ; # 공백을 쪼개지 않는 Tcl 단어로 소스 이름 전달
if {![file isfile $source]} { error "source RTL is missing" } ; # 입력 파일 부재를 먼저 알리기
set sdc [open constraints.sdc w] ; # 새 작업 폴더 안에만 제약 파일 작성
fconfigure $sdc -encoding utf-8 -translation lf ; # 한글 메모와 줄바꿈을 파일에 그대로 유지
puts $sdc [format {create_clock -name core_clk -period %.3f [get_ports clk] ; # 클록 주기의 입력 계약} $period] ; # 중괄호로 감싼 명령은 이 단계에서 실행하지 않기
puts $sdc {set_clock_uncertainty 0.1 [get_clocks core_clk] ; # 클록 불확실성으로 따로 남긴 여유} ; # STA 도구가 나중에 해석할 SDC 줄
puts $sdc {set_input_delay -clock core_clk -max 2.0 [get_ports {rst in_valid in_data* out_ready}] ; # 가장 늦은 외부 입력 도착} ; # 클록 포트는 데이터 입력 목록에서 제외
puts $sdc {set_input_delay -clock core_clk -min 0.2 [get_ports {rst in_valid in_data* out_ready}] ; # 가장 빠른 외부 입력 도착} ; # hold 검토에 필요한 최소 조건도 함께 기록
puts $sdc {set_output_delay -clock core_clk -max 2.0 [get_ports {in_ready out_valid out_data*}] ; # 외부 수신 회로의 최대 지연 조건} ; # 출력 사용처와 연결할 계약
puts $sdc {set_output_delay -clock core_clk -min 0.2 [get_ports {in_ready out_valid out_data*}] ; # 외부 수신 회로의 최소 지연 조건} ; # 최대 조건 하나로 모든 검사를 대신하지 않기
close $sdc ; # 파일 내용을 실제로 저장
set top [dict get $config top] ; # 합성 최상위 회로 이름
yosys read_verilog -sv $source ; # Yosys의 HDL 읽기 명령을 Tcl에서 호출
yosys hierarchy -check -top $top ; # 모듈 연결과 최상위 이름 확인
yosys proc ; # 순차·조합 절차를 내부 회로 셀로 변환
yosys opt ; # 상수와 불필요한 연결을 정리한 일반 회로 구조
yosys check -assert ; # 구조 검사 오류가 있으면 작업을 실패로 종료
yosys write_json design.json ; # 외부 검사기가 읽을 일반 셀·포트 정보
yosys stat ; # 도구가 실제 만든 구조의 통계 출력
puts "PASS tcl_flow top=$top period_ns=$period sdc_commands=6" ; # 성공한 Tcl 실행과 생성한 제약 명령 수 기록
```

## constraints.sdc의 전체 코드

```tcl
create_clock -name core_clk -period 10.000 [get_ports clk] ; # 클록 주기의 입력 계약
set_clock_uncertainty 0.1 [get_clocks core_clk] ; # 클록 불확실성으로 따로 남긴 여유
set_input_delay -clock core_clk -max 2.0 [get_ports {rst in_valid in_data* out_ready}] ; # 가장 늦은 외부 입력 도착
set_input_delay -clock core_clk -min 0.2 [get_ports {rst in_valid in_data* out_ready}] ; # 가장 빠른 외부 입력 도착
set_output_delay -clock core_clk -max 2.0 [get_ports {in_ready out_valid out_data*}] ; # 외부 수신 회로의 최대 지연 조건
set_output_delay -clock core_clk -min 0.2 [get_ports {in_ready out_valid out_data*}] ; # 외부 수신 회로의 최소 지연 조건
```

## run.py의 전체 코드

```python
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
```
