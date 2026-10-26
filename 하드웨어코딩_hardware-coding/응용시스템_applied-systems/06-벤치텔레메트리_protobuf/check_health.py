"""Protobuf 코드를 생성하고 벤치 샘플의 존재·순서·시간 계약을 검사합니다."""  # 네트워크나 실제 탑재 장치를 사용하지 않는 실습
import argparse  # 의존성과 결과 경로 선택
from dataclasses import asdict  # 검증한 샘플을 읽기 쉬운 기록으로 변환
import hashlib  # 원본과 생성 코드의 바이트 해시
from importlib.metadata import version  # 실제 도구 판본
import json  # 실행 기록 저장
import math  # 오류 입력의 NaN·무한대
import os  # 코드 생성 자식 프로세스의 환경
from pathlib import Path  # 소스와 생성물 위치
import shutil  # 원본 스키마의 바이트 복사
import subprocess  # 실제 protoc 프로세스 실행
import sys  # 현재 Python과 import 경로
import tempfile  # 독립 코드 생성 위치
ROOT = Path(__file__).resolve().parent  # 예제 파일의 위치
def main():  # 실제 코드 생성과 데이터 계약 검사
    parser = argparse.ArgumentParser(description=__doc__)  # 실행 범위 안내
    parser.add_argument('--dependencies', type=Path)  # 임시 pip 설치 경로
    parser.add_argument('--report', type=Path, required=True)  # 이번 실행 결과
    args = parser.parse_args()  # 인자 읽기
    if sys.flags.optimize: parser.error('run without -O')  # assert가 빠진 성공 기록 금지
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONIOENCODING='utf-8')  # 소스 폴더 캐시와 출력 인코딩 관리
    if args.dependencies:  # 전역 설치를 바꾸지 않고 실행
        dependency = str(args.dependencies.resolve())  # 선택한 패키지 위치
        sys.path.insert(0, dependency)  # 현재 검사기의 외부 패키지 로드
        environment['PYTHONPATH'] = dependency + os.pathsep + environment.get('PYTHONPATH', '')  # 코드 생성기도 같은 판본 사용
    work = Path(tempfile.mkdtemp(prefix='bench-protobuf-'))  # 기존 생성 코드와 섞이지 않는 위치
    shutil.copyfile(ROOT / 'telemetry.proto', work / 'telemetry.proto')  # 컴파일 입력을 같은 바이트로 복사
    command = [sys.executable, '-B', '-m', 'grpc_tools.protoc', '-I.', '--python_out=.', 'telemetry.proto']  # 실제 protoc 생성 명령
    process = subprocess.run(command, cwd=work, env=environment, capture_output=True, timeout=60)  # 셸 문자열 없이 생성기 실행
    assert process.returncode == 0, process.stderr.decode('utf-8', 'replace')  # 생성 실패 상태에서 검사 진행 금지
    sys.path.insert(0, str(work))  # 이번에 생성한 클래스만 로드
    import telemetry_pb2 as wire  # 실제 생성된 Protobuf API
    from health import decode, Monitor  # 같은 생성 클래스를 사용하는 애플리케이션 검사
    checks, rejected = 0, 0  # assert와 명시적 오류의 집계
    def verify(condition):  # 실제 비교 수를 함께 세기
        nonlocal checks  # 바깥 집계 갱신
        assert condition  # 기대와 다른 결과는 실행 실패
        checks += 1  # 통과한 비교 집계
    def reject(function, expected):  # 특정 데이터 계약 오류를 요구
        nonlocal rejected  # 오류 거절 수 집계
        try: function()  # 잘못된 입력이나 시계 조건 실행
        except ValueError as error: verify(str(error) == expected)  # 관계없는 오류를 통과로 세지 않기
        else: raise AssertionError('invalid input accepted')  # 잘못된 입력이 정상 상태로 들어가면 실패
        rejected += 1  # 원하는 오류의 실제 거절 집계
    def packet(sequence=0, sampled_ms=0, bus_v=12, temperature_c=25):  # 독립 테스트 입력 직렬화
        message = wire.Sample(sequence=sequence, sampled_ms=sampled_ms)  # 순번과 시각 0도 명시적으로 존재
        message.readings.add(channel='bus_v', value=bus_v)  # 볼트 단위의 벤치 값
        message.readings.add(channel='temperature_c', value=temperature_c)  # 섭씨 단위의 벤치 값
        return message.SerializeToString(deterministic=True)  # 같은 스키마로 실제 wire 바이트 생성
    valid_cases = 0  # 범위 경계와 기본값의 정상 조합 수
    for sequence in [0, 1, 2**64 - 1]:  # 순번의 0·일반값·자료형 끝값
        for sampled_ms in [0, 10]:  # 시각 0의 명시적 존재도 검사
            for bus_v in [0, 12, 30]:  # 허용 범위 경계 포함
                for temperature_c in [-20, 25, 80]:  # 온도 범위 경계 포함
                    result = decode(packet(sequence, sampled_ms, bus_v, temperature_c))  # 실제 wire를 다시 해석
                    verify((result.sequence, result.sampled_ms, result.bus_v, result.temperature_c) == (sequence, sampled_ms, bus_v, temperature_c))  # 원래 값과 독립 비교
                    valid_cases += 1  # 정상 조합 집계
    reject(lambda: decode(b''), 'missing_sequence')  # 빈 메시지와 값 0 구분
    missing = wire.Sample(sampled_ms=0)  # 순번이 없는 메시지
    reject(lambda: decode(missing.SerializeToString()), 'missing_sequence')  # 기본값 0으로 누락을 대신하지 않기
    missing = wire.Sample(sequence=0)  # 측정 시각이 없는 메시지
    reject(lambda: decode(missing.SerializeToString()), 'missing_sampled_ms')  # 시각 누락 확인
    missing = wire.Sample(sequence=0, sampled_ms=0)  # 채널이 없는 메시지
    reject(lambda: decode(missing.SerializeToString()), 'missing_channel')  # 부분 샘플 거절
    incomplete = wire.Sample()  # 기존 정상 메시지를 수정할 작업 객체
    incomplete.ParseFromString(packet())  # 정상 원본의 테스트 복사본
    incomplete.readings[0].ClearField('value')  # 값이 0인 경우와 값이 없는 경우를 구분
    reject(lambda: decode(incomplete.SerializeToString()), 'value')  # optional 값의 누락 거절
    duplicate = wire.Sample()  # 중복 채널을 만들 테스트 객체
    duplicate.ParseFromString(packet())  # 정상 원본 읽기
    duplicate.readings.add(channel='bus_v', value=12)  # 같은 이름을 한 번 더 추가
    reject(lambda: decode(duplicate.SerializeToString()), 'channel')  # 나중 값으로 조용히 덮어쓰지 않기
    duplicate.readings[-1].channel = 'unknown'  # 모르는 채널 이름으로 변경
    reject(lambda: decode(duplicate.SerializeToString()), 'channel')  # 알려진 채널 계약 확인
    for bad in [math.nan, math.inf, -math.inf]: reject(lambda: decode(packet(bus_v=bad)), 'value')  # 비유한 값이 파서를 통과해도 앱에서는 거절
    reject(lambda: decode(packet(bus_v=31)), 'bench_range')  # 전원 범위 밖 값
    reject(lambda: decode(packet(temperature_c=-21)), 'bench_range')  # 온도 범위 밖 값
    reject(lambda: decode(b'\x08'), 'wire')  # 끊긴 varint의 실제 파서 실패
    reject(lambda: decode(b'x' * 257), 'payload_size_or_type')  # 파싱 전에 크기 거절
    reject(lambda: decode('not bytes'), 'payload_size_or_type')  # 잘못된 입력 자료형 거절
    verify(decode(packet() + b'\xa0\x06\x01') == decode(packet()))  # 모르는 field100이 있어도 기존 필드 의미 유지
    monitor = Monitor(100)  # 하나의 벤치에서만 쓰는 설명용 신선도 한도
    verify(monitor.status(0) == 'NO_DATA')  # 첫 데이터 이전 상태
    monitor.accept(packet(), 0)  # 값 0인 순번과 시각을 정상 수락
    trace = []  # 시간과 상태가 바뀌는 대표 흐름
    for now, expected in [(0, 'FRESH'), (100, 'FRESH'), (101, 'STALE')]:  # 경계는 포함하고 다음 ms부터 오래된 값
        actual = monitor.status(now)  # 수신 시각 대신 측정 시각의 나이 판정
        verify(actual == expected)  # 독립 시간표와 비교
        trace.append(dict(now_ms=now, status=actual))  # 읽기용 실행 흐름
    monitor.accept(packet(1, 100), 110)  # 측정 뒤 10ms 늦게 도착한 새 데이터
    verify(monitor.status(200) == 'FRESH')  # 측정 기준 경계 100ms
    verify(monitor.status(201) == 'STALE')  # 도착 기준으로 나이를 줄이지 않기
    before = monitor.sample  # 잘못된 메시지가 바꾸면 안 되는 상태
    reject(lambda: monitor.accept(packet(1, 201), 202), 'sequence')  # 중복 순번은 새 시각이어도 거절
    verify(monitor.sample == before)  # 거절 후 원래 상태 보존
    reject(lambda: monitor.accept(packet(2, 205), 204), 'sample_age')  # 미래 측정 시각 거절
    reject(lambda: monitor.accept(packet(2, 99), 204), 'sample_age')  # 이미 오래된 샘플 거절
    reject(lambda: monitor.status(203), 'clock_rewind')  # 수신기 단조 시계가 뒤로 가는 경우
    monitor.accept(packet(2, 204), 205)  # 올바른 새 순번과 시각은 이후에도 수락 가능
    reject(lambda: monitor.accept(packet(3, 203), 206), 'sample_rewind')  # 순번만 커진 역행 측정 시각 거절
    reject(lambda: Monitor(-1), 'max_age')  # 잘못된 생성 설정
    reject(lambda: Monitor().status(True), 'clock')  # bool을 정수 시각으로 오인하지 않기
    hashes = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in ('telemetry.proto', 'health.py', 'check_health.py')}  # 현재 소스의 바이트 해시
    report = dict(status='passed_actual_protoc_and_bench_checks', versions=dict(protobuf=version('protobuf'), grpcio_tools=version('grpcio-tools')), generation=dict(command=command, cwd=str(work), returncode=process.returncode, stdout=process.stdout.decode('utf-8', 'replace'), stderr=process.stderr.decode('utf-8', 'replace'), generated_sha256=hashlib.sha256((work / 'telemetry_pb2.py').read_bytes()).hexdigest()), source_sha256=hashes, valid_wire_cases=valid_cases, checks=checks, rejected_conditions=rejected, trace=trace, final_sample=asdict(monitor.sample), scope=dict(actual_schema_compilation=True, protobuf_runtime=True, shared_bench_clock=True, live_network=False, spacecraft_protocol=False, flight_software=False, actuation=False, authentication=False))  # 실행한 단계와 적용하지 않은 시스템 구분
    args.report.parent.mkdir(parents=True, exist_ok=True)  # 결과 파일의 부모 준비
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')  # 실제 기록 저장
    print(f'PASS protobuf valid={valid_cases} checks={checks} rejected={rejected}')  # 검사 집계 출력
if __name__ == '__main__': main()  # import만으로 코드 생성이나 파일 쓰기를 하지 않기
