# Protobuf 벤치 샘플의 존재·순서·측정 시각 검사

[하드웨어 코딩 목차](../../README.md)

동일 벤치의 전원 전압·온도를 바이트 메시지로 만들고, 실제 protoc 생성 코드와 Protobuf 런타임으로 읽는 선별 실습입니다. 스키마가 정하는 자료형과 애플리케이션의 값·순서·시간 계약을 분리합니다. 실제 네트워크·장치 제어·우주 통신 규격을 구현한 예제는 아닙니다.

## 스키마와 생성 코드

telemetry.proto는 Sample과 Reading의 필드 번호·자료형·존재 여부를 정합니다. check_health.py는 임시 폴더에서 실제 grpc_tools.protoc를 실행해 telemetry_pb2.py를 생성하고, 그 클래스로 wire 바이트를 직렬화·파싱합니다. 수동으로 흉내 낸 파서가 아닙니다. [공식 Python 생성 코드 안내](https://protobuf.dev/reference/python/python-generated/)와 [grpcio-tools의 protoc 설명](https://grpc.io/docs/languages/python/quickstart/)이 이 단계의 근거입니다.

| 필드 | 뜻 | 이 예제의 계약 |
| --- | --- | --- |
| sequence | uint64 순번 | 명시적으로 존재하고 이전 수락값보다 커야 합니다. |
| sampled_ms | uint64 측정 시각 | 같은 벤치 단조 시계의 ms입니다. |
| readings.channel | 채널 이름 | bus_v·temperature_c 두 이름만 사용합니다. |
| readings.value | optional double 값 | 0을 포함한 유한값이 명시적으로 있어야 합니다. |

sequence·sampled_ms·value는 optional로 존재를 추적합니다. 0을 읽었다는 사실과 필드가 없다는 사실을 HasField로 구분합니다. 기본값만 확인하면 누락된 순번을 sequence=0으로 오인할 수 있습니다. [공식 field-presence 설명](https://protobuf.dev/programming-guides/field_presence/)은 proto3의 explicit presence를 설명합니다.

bus_v는 0~30V, temperature_c는 −20~80°C의 설명용 벤치 범위입니다. 스키마의 double·uint64만으로 이 범위·채널 중복·신선도가 자동 확인되는 것은 아닙니다. health.py가 별도 계약을 검사합니다.

## wire와 애플리케이션의 검사 순서

decode는 bytes 자료형과 전체 크기 256바이트 이하를 먼저 확인한 뒤 실제 ParseFromString을 호출합니다. 이어 optional 필드의 존재, 정확히 두 종류의 채널, 채널 중복·모르는 이름, value 누락·NaN·양/음의 무한대, 벤치 값 범위를 검사합니다. 결과는 생성된 wire 객체와 분리한 frozen dataclass입니다.

모르는 Protobuf 필드 번호와 모르는 애플리케이션 채널은 다릅니다. 시험에서는 field100을 추가한 호환 메시지의 기존 값이 유지됐지만 unknown 채널 이름은 거절했습니다. [proto3의 unknown-field 설명](https://protobuf.dev/programming-guides/proto3/)과 이 벤치의 두 채널 계약을 구분합니다. 모든 wire 인코딩이나 다른 언어 구현과의 상호 운용을 전수 검사한 것은 아닙니다.

## 공유 단조 시계와 신선도

송신·수신·조회가 같은 원점의 단조 ms 시계를 사용한다고 가정합니다. 서로 다른 장치 시계를 동기화하는 구현은 없습니다. received_ms는 수신 시각이고 sampled_ms는 실제 측정 시각입니다. 수신 때는 미래 또는 나이 100ms 초과인 샘플을 거절하며, 조회 때도 now_ms−sampled_ms로 FRESH·STALE을 정합니다. 도착이 늦었다고 측정 나이를 0으로 바꾸지 않습니다.

| 단계 | 입력·조회 | 확인한 결과 |
| --- | --- | --- |
| 수신 전 | status(0) | NO_DATA입니다. |
| 첫 수락 | sequence=0,sampled=0,received=0 | 0값이 있는 정상 샘플입니다. |
| 경계 조회 | now=100ms | 나이 100ms로 FRESH입니다. |
| 다음 조회 | now=101ms | 나이 101ms로 STALE입니다. |
| 지연 수락 | sequence=1,sampled=100,received=110 | 측정 뒤 10ms에 받은 새 샘플입니다. |
| 측정 기준 경계 | now=200·201ms | 각각 FRESH·STALE입니다. |
| 중복 순번 | sequence=1,sampled=201,received=202 | 새 측정 시각이어도 sequence 오류입니다. |
| 미래·오래된 값 | sampled=205 또는 99,received=204 | sample_age 오류입니다. |
| 수신 시계 역행 | status(203),직전 now=204 | clock_rewind 오류입니다. |
| 새 정상 샘플 | sequence=2,sampled=204,received=205 | 모든 검사를 통과해 교체합니다. |
| 측정 시각 역행 | sequence=3,sampled=203,received=206 | 순번이 커도 sample_rewind 오류입니다. |

Monitor.observe는 거절된 패킷의 수신에서도 단조 시계의 관측값을 전진시킵니다. 실제 수신 시간이 흘렀다는 사실과 샘플을 수락했다는 사실이 다르기 때문입니다. 검증된 sample은 모든 검사가 끝난 뒤에만 교체합니다. 거절을 받았다고 이전 샘플을 새 데이터처럼 신선하게 만들지 않습니다.

순번은 연속일 필요는 없지만 엄격히 증가해야 합니다. 이 실습은 단일 생산자·하나의 벤치 세션이며 생산자 재시작·uint64 순번 rollover를 처리하지 않습니다. 그런 경우에는 세션 식별과 재초기화 정책이 추가로 필요합니다.

## 실제 생성·검사 결과

2026-10-26에 Python 3.12.14, protobuf 7.36.2, grpcio-tools 1.85.0으로 실제 생성기와 런타임을 실행했습니다. protoc와 검사기의 종료 코드는 0이며 stdout·stderr를 [example.json](example.json)에 기록합니다. protoc는 메시지 클래스를 만드는 데만 사용했고 gRPC 서버·클라이언트·연결을 실행하지 않았습니다.

정상 wire는 순번 0·1·uint64 최댓값, 측정 시각 0·10ms, 전압 0·12·30V, 온도 −20·25·80°C의 3×2×3×3=54조합입니다. 각 바이트 메시지를 다시 읽은 값과 원래 네 입력을 대조합니다. 같은 생성 API를 통한 round-trip 검사이며 별도 언어 인코더와의 비교는 아닙니다.

누락 필드·채널·비유한값·벤치 범위·끊긴 varint·257바이트·잘못된 자료형·중복 순번·측정 나이·시계 역행·설정 오류를 포함해 22개 거절을 확인했습니다. 정상 54개 비교, 거절 이유 22개 비교, unknown field·상태 흐름·거절 후 보존 8개 비교로 총 84개입니다. malformed wire의 모든 가능성을 검사했다는 뜻은 아닙니다.

```text
PASS protobuf valid=54 checks=84 rejected=22
```

생성 코드의 SHA도 실제 결과에 보관했습니다. 도구 판본과 생성 경로가 바뀐 환경에서 같은 산출물 바이트가 만들어진다고 보장하는 값은 아닙니다. 원본 스키마·애플리케이션·검사기 소스 SHA는 별도로 기록하며, 저장된 결과와 현재 파일의 정적 대조를 도구 재실행과 구분합니다.

## 재현 명령

임시 --target 경로에 사용 판본을 준비합니다. 생성 코드는 새 임시 폴더에서만 만들고 기존 Python 풀이를 수정하지 않습니다. 저장소 루트의 PowerShell에서 아래와 같이 실행합니다. -O는 assert를 제거하므로 검사기가 거절합니다.

```powershell
$py = 'C:/path/to/python.exe'
$deps = Join-Path (Get-Location) 'tmp/protobuf-example-deps'
& $py -B -m pip install --target $deps 'protobuf==7.36.2' 'grpcio-tools==1.85.0'
& $py -B '하드웨어코딩_hardware-coding/응용시스템_applied-systems/06-벤치텔레메트리_protobuf/check_health.py' --dependencies $deps --report 'tmp/bench-protobuf-validation.json'
```

## 모델·인증·실제 통신의 한계

Protobuf의 파싱 성공은 CRC 검사나 송신자 인증이 아닙니다. 이 코드에는 CRC·서명·암호화·네트워크 프레이밍·재전송·전송률 제한·시계 동기화가 없습니다. 값이 범위 안에 있는 잘못된 패킷은 존재 검사만으로 식별할 수 없습니다. deterministic 직렬화 옵션도 인증이나 표준 canonical 인코딩을 뜻하지 않습니다.

FRESH·STALE은 이 벤치의 시간 라벨이며 장치를 자동 정지시키는 제어 명령이 아닙니다. 실제 장치에 적용하려면 단위·범위·시계·세션·통신 보호·오류 대응을 시스템 요구와 함께 정해야 합니다. NASA 통신 규격·탑재 소프트웨어·우주기 제어·실제 네트워크를 구현하거나 인증한 기록은 아닙니다.

## 전체 소스와 줄별 메모

### telemetry.proto

```protobuf
syntax = "proto3"; // 코드 생성기가 사용할 문법 판본
package bench; // 벤치 실습 메시지의 이름 공간
message Reading { // 단위가 정해진 한 채널의 값
  string channel = 1; // bus_v 또는 temperature_c 중 하나
  optional double value = 2; // 값 0과 값 누락을 구분
} // 채널 정의 끝
message Sample { // 공유 단조 시계를 쓰는 한 벤치의 샘플
  optional uint64 sequence = 1; // 순번 0도 명시적으로 담기
  optional uint64 sampled_ms = 2; // 측정 시점이며 수신 시점과 구분
  repeated Reading readings = 3; // 이 예제에서는 서로 다른 두 채널을 요구
} // 메시지 정의 끝
```

### health.py

```python
from dataclasses import dataclass  # 검증한 읽기 전용 샘플 표현
import math  # 비유한 센서값 거절
from google.protobuf.message import DecodeError  # 실제 wire 파서의 실패 구분
import telemetry_pb2  # telemetry.proto에서 실제 생성한 메시지 클래스
@dataclass(frozen=True)  # 검사 뒤 샘플 내용을 바꾸지 않기
class Sample:  # 애플리케이션에 전달할 값
    sequence: int  # 성공적으로 읽은 순번
    sampled_ms: int  # 벤치의 공통 단조 시각
    bus_v: float  # 볼트 단위 전원 관측값
    temperature_c: float  # 섭씨 단위 온도 관측값
def decode(payload):  # wire 해석과 이 벤치의 데이터 계약 확인
    if not isinstance(payload, bytes) or len(payload) > 256: raise ValueError('payload_size_or_type')  # 파서 앞에서 입력 크기 제한
    message = telemetry_pb2.Sample()  # 생성된 클래스의 빈 메시지
    try: message.ParseFromString(payload)  # 실제 Protobuf 런타임으로 역직렬화
    except DecodeError as error: raise ValueError('wire') from error  # 구문 실패를 값 검증과 구분
    for name in ('sequence', 'sampled_ms'):  # 기본값 0이 누락을 숨기지 않게 확인
        if not message.HasField(name): raise ValueError('missing_' + name)  # optional의 명시적 존재 검사
    values = {}  # 같은 채널을 두 번 받아 덮어쓰지 않기
    for reading in message.readings:  # 파서가 읽은 각 채널 검사
        if reading.channel in values or reading.channel not in ('bus_v', 'temperature_c'): raise ValueError('channel')  # 중복과 모르는 이름 거절
        if not reading.HasField('value') or not math.isfinite(reading.value): raise ValueError('value')  # 누락과 NaN·무한대 거절
        values[reading.channel] = reading.value  # 검사한 채널만 보관
    if set(values) != {'bus_v', 'temperature_c'}: raise ValueError('missing_channel')  # 일부 채널만으로 새 상태를 만들지 않기
    if not 0 <= values['bus_v'] <= 30 or not -20 <= values['temperature_c'] <= 80: raise ValueError('bench_range')  # 설명용 벤치 입력 범위
    return Sample(message.sequence, message.sampled_ms, values['bus_v'], values['temperature_c'])  # wire 객체와 분리된 검증 결과
class Monitor:  # 공유 단조 시계와 단일 생산자를 가정한 수신 상태
    def __init__(self, max_age_ms=100):  # 예제의 데이터 신선도 계약
        if type(max_age_ms) is not int or max_age_ms < 0: raise ValueError('max_age')  # 음수나 부동소수 임계값 거절
        self.max_age_ms, self.sample, self.last_now = max_age_ms, None, None  # 값 없음과 0인 값을 분리
    def observe(self, now_ms):  # 수신기에서 관측한 단조 시각 검사
        if type(now_ms) is not int or now_ms < 0: raise ValueError('clock')  # bool·음수·소수는 벤치 시각으로 쓰지 않기
        if self.last_now is not None and now_ms < self.last_now: raise ValueError('clock_rewind')  # 시계가 뒤로 가면 별도 재초기화 필요
        self.last_now = now_ms  # 잘못된 패킷을 받았어도 수신기 시간 관측은 보존
    def accept(self, payload, received_ms):  # 검증한 새 샘플만 상태로 반영
        self.observe(received_ms)  # 외부 메시지의 시각과 수신기 시각을 구분
        candidate = decode(payload)  # 잘못된 wire나 값은 현재 샘플을 바꾸지 않기
        if candidate.sampled_ms > received_ms or received_ms - candidate.sampled_ms > self.max_age_ms: raise ValueError('sample_age')  # 미래 또는 이미 오래된 샘플 거절
        if self.sample is not None and candidate.sequence <= self.sample.sequence: raise ValueError('sequence')  # 중복·역순이 신선도를 갱신하지 않게 처리
        if self.sample is not None and candidate.sampled_ms < self.sample.sampled_ms: raise ValueError('sample_rewind')  # 순번이 커도 측정 시각이 뒤로 가면 거절
        self.sample = candidate  # 모든 검사를 통과한 뒤에만 교체
    def status(self, now_ms):  # 관측값의 신선도만 표시하며 장치를 제어하지 않기
        self.observe(now_ms)  # 화면 조회도 같은 단조 시각 계약 사용
        if self.sample is None: return 'NO_DATA'  # 수신 전 상태
        return 'FRESH' if now_ms - self.sample.sampled_ms <= self.max_age_ms else 'STALE'  # 도착이 아니라 측정 시각에서 나이 계산
```

### check_health.py

```python
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
```

## 공식 근거와 직접 작성한 범위

- [Protobuf field presence](https://protobuf.dev/programming-guides/field_presence/)·[Python 생성 코드](https://protobuf.dev/reference/python/python-generated/)는 optional 존재와 HasField·직렬화·파싱의 근거입니다.
- [proto3 언어 안내](https://protobuf.dev/programming-guides/proto3/)·[직렬화의 비정규성 설명](https://protobuf.dev/programming-guides/serialization-not-canonical/)은 필드 번호·호환 확장과 deterministic 옵션의 범위를 구분할 때 참고합니다.
- [gRPC Python의 도구 설명](https://grpc.io/docs/languages/python/quickstart/)은 grpcio-tools가 protoc를 제공하는 근거입니다. 이 예제는 RPC를 사용하지 않습니다.
- 스키마·애플리케이션·검사 입력은 직접 작성했습니다. 외부 라이브러리와 생성기는 임시 의존성이며, 그 소스·바이너리나 공식 예제 코드를 이 폴더에 복제하지 않습니다.

[Protobuf 라이선스](https://raw.githubusercontent.com/protocolbuffers/protobuf/main/LICENSE)는 BSD 계열 고지를, [gRPC 라이선스](https://raw.githubusercontent.com/grpc/grpc/master/LICENSE)는 Apache-2.0을 제시합니다. 자체 스키마·검사 코드와 외부 도구의 이용 조건을 구분합니다.

자료 열람과 실제 실행 기준일은 2026-10-26입니다.
