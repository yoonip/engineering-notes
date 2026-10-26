[현업 언어 목차](../README.md) · [하드웨어 코딩 목차](../../README.md)

# SystemRDL로 명세한 32비트 CSR과 생성 C 헤더 대조

이 예제는 직접 구성한 작은 실험 장치의 레지스터 세 개를 SystemRDL로 명세합니다. SystemRDL Compiler로 명세를 컴파일·전개한 뒤, 주소와 접근 속성을 고정 기대표와 비교합니다. PeakRDL-CHeader가 실제로 생성한 헤더는 별도의 C 정적 단언 21개로 대조하고 호스트에서 실행합니다.

SystemRDL은 레지스터의 주소, 비트 범위, 소프트웨어·하드웨어 접근 의미를 표현하는 명세 언어입니다. Accellera는 같은 명세에서 RTL이나 문서 같은 여러 산출물을 생성하는 사용 방식을 설명합니다. 이 `.rdl` 파일 자체를 범용 순차·조합 회로를 작성하는 합성 HDL로 취급하지 않습니다. 이 예제에서 생성하는 산출물은 C 헤더이며 RTL은 생성하지 않습니다. [Accellera 공식 표준 안내](https://www.accellera.org/downloads/standards/systemrdl)

## 입력 명세와 주소 단위

입력은 표준입력이 아니라 [example.rdl](example.rdl) 파일입니다. 실제 제품의 주소표가 아닌 직접 구성한 주소 공간입니다. 레지스터 주소는 바이트 단위이며, 필드의 `[high:low]`는 레지스터 안의 비트 번호입니다.

| 레지스터 | 바이트 오프셋 | 필드 | 소프트웨어 접근 | 하드웨어 접근 | 필드 초기값 |
| --- | ---: | --- | --- | --- | ---: |
| `version` | `0x00` | `revision[31:0]` | 읽기 | 읽기 | `0x00010002` |
| `control` | `0x04` | `run_en[0]` | 읽기·쓰기 | 읽기 | `0` |
| `control` | `0x04` | `mode_sel[3:1]` | 읽기·쓰기 | 읽기 | `2` |
| `events` | `0x08` | `flags[3:0]` | 읽기·1쓰기 소거 | 쓰기 | `0` |

`regwidth=32`는 레지스터 폭이며 `accesswidth=32`는 최소 소프트웨어 접근 폭입니다. 세 레지스터의 시작 주소는 4바이트 간격이고 전체 주소 공간의 크기는 12바이트입니다. 버전값 `0x00010002`를 이 예제에서는 1.2라는 임의의 식별값으로 사용합니다. 공개된 실제 장치의 버전 번호가 아닙니다. [SystemRDL 속성 참조](https://systemrdl-compiler.readthedocs.io/en/stable/property_reference.html)

`mode_sel`의 필드 초기값은 2입니다. 필드가 비트 1에서 시작하므로 `control`에서 명세된 필드의 초기 비트 패턴은 `2 << 1 = 4`입니다. 헤더의 `_reset` 매크로를 이미 이동된 레지스터 값으로 해석하지 않습니다. 초기값 속성을 검사한 것이며 실제 리셋 신호의 극성이나 회로 타이밍을 시험한 것은 아닙니다.

## RO·RW·W1C의 명세 의미

RO는 소프트웨어 읽기 전용이고 RW는 읽기·쓰기 가능을 뜻합니다. `flags`의 `onwrite=woclr`는 쓴 데이터가 1인 비트를 소거하는 W1C 조건입니다. `hw=w`는 하드웨어가 해당 필드를 갱신할 수 있다는 속성이며, 자동으로 특정 인터럽트 수집 회로나 sticky 비트를 구현한다는 뜻은 아닙니다. 이 예제는 하드웨어·소프트웨어 갱신이 충돌할 때의 우선순위를 `precedence=hw`로 명시합니다. [SystemRDL 2.0 공식 명세](https://www.accellera.org/images/downloads/standards/systemrdl/SystemRDL_2.0_Jan2018.pdf)

다음 표는 하드웨어 갱신이 없다고 가정한 비트 의미의 직접 계산입니다. 버스 시뮬레이션의 측정 결과가 아닙니다.

| 단계 | 대상 | 입력 또는 계산 | 해석 |
| --- | --- | --- | --- |
| 1 | `control` 초기 필드 | `run_en=0`, `mode_sel=2` | 정의한 필드의 레지스터 비트 패턴은 `0x4`입니다. |
| 2 | 모드와 실행 허용 설정 | `(5 << 1) \| 1` | 두 필드를 합친 비트 패턴은 `0xb`입니다. |
| 3 | `flags`의 기존 값 | `1011₂` | 네 상태 비트 중 3·1·0번이 1입니다. |
| 4 | 소거 데이터 | `0010₂` | W1C에서 1번 비트만 소거하여 `1001₂`가 됩니다. |
| 5 | 소거 데이터 | `0000₂` | 소거할 비트가 없으므로 `1001₂`를 유지합니다. |

이 예제의 C 헤더는 필드를 일반 `uint32_t` 멤버와 마스크로 나타냅니다. RO 필드를 쓰지 못하도록 C 형식이 강제하지 않으며, C 대입문이 W1C 회로를 구현하지도 않습니다. 실제 버스 구현, 주소 매핑, 접근 폭·정렬, 메모리 순서와 `volatile` 접근 정책은 별도의 장치 계약이 필요합니다. 여기서는 물리 주소에 포인터를 만들거나 MMIO를 수행하지 않습니다.

## 입력에서 검사 결과까지의 흐름

| 순서 | 실제 처리 | 확인 대상 |
| --- | --- | --- |
| 1 | 정상 RDL 파일을 새 결과 폴더에 복사합니다. | 기존 파일을 덮어쓰지 않습니다. |
| 2 | `compile_file()`과 `elaborate()`를 호출합니다. | 문법뿐 아니라 전개된 주소와 의미 제약을 확인합니다. |
| 3 | 레지스터·필드 노드에서 50개 값을 읽습니다. | 별도로 적은 주소·비트·접근·초기값·우선순위 기대표와 비교합니다. |
| 4 | 같은 모델에서 `registers.h`를 두 번 생성합니다. | 서로 다른 디렉터리의 생성 결과가 바이트 단위로 같습니다. |
| 5 | 별도 C 파일이 생성 헤더를 포함합니다. | 마스크·시작 비트·폭·초기값·멤버 오프셋·크기를 컴파일 타임에 대조합니다. |
| 6 | 호스트 검사 실행 파일을 실행합니다. | 종료값 0과 정확한 정상 출력 한 줄을 확인합니다. |
| 7 | 잘못된 명세 네 개를 각각 새 컴파일러로 처리합니다. | 실패 예외와 해당 규칙의 진단 단어를 모두 확인합니다. |
| 8 | 헤더의 모드 마스크만 `0xe`에서 `0x6`으로 바꿉니다. | C의 `mode mask` 정적 단언이 실제로 실패하는지 확인합니다. |

`elaborate()`는 표현식과 주소·필드 배치를 결정하고 검증 조건을 적용하는 단계입니다. 실패한 컴파일러 인스턴스를 다음 입력에 재사용하지 않습니다. Python 스크립트는 명세 컴파일 오류만 예상 거절로 인정하며, 다른 Python 예외나 실행 도구 장애를 오류 입력 검출로 집계하지 않습니다. [SystemRDL Compiler API](https://systemrdl-compiler.readthedocs.io/en/stable/api/compiler.html)

생성 API는 `CStandard.gnu11`과 `generate_bitfields=False`를 지정합니다. 이 선택은 C 비트필드의 구현별 배치에 의존하지 않고 마스크와 정수 멤버를 확인하기 위한 것입니다. 생성 구조체의 `packed` 속성은 GNU 확장이므로 여기서 통과한 호스트 컴파일 결과를 모든 C 컴파일러나 임의의 장치 ABI로 일반화하지 않습니다. [PeakRDL-CHeader API](https://peakrdl-cheader.readthedocs.io/en/latest/api.html)

## SystemRDL 전체 명세

각 `field { ... }`는 필드 형식과 속성을 선언하며 뒤의 이름·범위가 인스턴스를 만듭니다. `@` 뒤의 값은 해당 레지스터의 바이트 오프셋입니다. `default`는 같은 주소 공간 안의 기본 폭을 지정합니다.

```systemrdl
addrmap bench_csr { // 작은 실험 장치의 레지스터 주소 공간
    default regwidth = 32; // 각 레지스터의 논리 폭32비트
    default accesswidth = 32; // 소프트웨어 접근 단위32비트
    reg { // 읽기 전용 버전 레지스터
        field { sw = r; hw = r; reset = 32'h00010002; } revision[31:0]; // 버전값1.2를32비트 상수로 명세
    } version @ 0x00; // 기준 주소에서0바이트 오프셋
    reg { // 소프트웨어가 설정하고 하드웨어가 읽는 제어값
        field { sw = rw; hw = r; reset = 0; } run_en[0:0]; // 실행 허용 한 비트의 초기값0
        field { sw = rw; hw = r; reset = 2; } mode_sel[3:1]; // 세 비트 모드의 초기값2
    } control @ 0x04; // 다음32비트 접근 위치
    reg { // 하드웨어 상태와 소프트웨어의1쓰기 소거
        field { // 네 비트 상태 필드의 속성
            sw = rw; // 소프트웨어가 읽고 소거용 쓰기 가능
            hw = w; // 하드웨어가 상태값을 갱신할 수 있음
            onwrite = woclr; // 쓴 데이터가1인 비트만 소거하도록 명세
            precedence = hw; // 동시 갱신 충돌에서는 하드웨어 우선
            reset = 0; // 상태 필드의 초기값0
        } flags[3:0]; // 낮은 네 비트만 상태로 사용
    } events @ 0x08; // 세 번째 정렬된 레지스터
}; // 전체 CSR 명세 끝
```

## 독립 검사 스크립트 전체 코드

`EXPECTED`는 정상 입력에서 다시 파싱하여 만든 값이 아니라 별도로 적은 기대표입니다. 필드마다 하위·상위 비트, 폭, 소프트웨어 접근, 하드웨어 접근, 초기값, 쓰기 부작용, 갱신 우선순위를 비교합니다. 헤더 생성 결과를 두 번 비교하는 검사는 결정성 확인이며, 같은 생성기의 의미 오류를 독립적으로 검출하는 검사를 대신하지 않습니다. 독립 값 검사는 AST 기대표와 C 정적 단언이 담당합니다.

```python
import argparse  # 실행할 도구와 새 출력 폴더 인자
import contextlib  # 잘못된 명세의 진단 출력을 따로 수집
import hashlib  # 원본과 생성물의 SHA-256 계산
import importlib.metadata  # 실제 설치한 패키지 버전 기록
import io  # 컴파일러 진단을 담을 문자열 버퍼
import json  # 재현 결과를 기계 판독 형태로 저장
import os  # 컴파일러 임시 파일 위치를 출력 폴더로 제한
from pathlib import Path  # 소스와 결과의 경로 처리
import re  # 진단의 터미널 색상 코드 제거
import shutil  # 원본 입력을 결과 폴더에 바이트 그대로 복사
import subprocess  # 실제 C 컴파일러와 검사 실행 파일 호출
import sys  # 개인 설치 경로를 모듈 검색 앞에 추가

EXPECTED = {  # 컴파일 결과에서 추출하지 않은 독립 기대값
    "version": (0, {"revision": (0, 31, 32, "r", "r", 65538, None, "sw")}),  # 버전의 주소와 필드 속성
    "control": (4, {"run_en": (0, 0, 1, "rw", "r", 0, None, "sw"), "mode_sel": (1, 3, 3, "rw", "r", 2, None, "sw")}),  # 제어 필드 두 개
    "events": (8, {"flags": (0, 3, 4, "rw", "w", 0, "woclr", "hw")}),  # 상태의 소거 방식과 충돌 우선순위
}  # 세 레지스터의 고정 기대표 끝
MUTATIONS = [  # 한 조건만 어기는 잘못된 입력 네 개
    ("address_overlap", "} control @ 0x04;", "} control @ 0x00;", "overlap"),  # 레지스터 주소 중복
    ("field_overlap", "mode_sel[3:1]", "mode_sel[2:0]", "overlap"),  # 필드 비트 범위 중복
    ("readonly_w1c", "            sw = rw;", "            sw = r;", "onwrite"),  # 쓰기 불가능한 필드에 쓰기 부작용 지정
    ("reset_overflow", "reset = 2; } mode_sel", "reset = 8; } mode_sel", "reset"),  # 세 비트에 들어가지 않는 초기값
]  # 각 입력에 필요한 진단 단어도 함께 보관

def sha256(path):  # 파일 이름과 무관한 바이트 해시
    return hashlib.sha256(path.read_bytes()).hexdigest()  # 변경을 비교할 64자리 문자열

def enum_name(value):  # 열거 속성을 JSON에 기록할 이름으로 정규화
    return None if value is None else value.name  # 기본 부작용 없음은 null로 유지

def main():  # 새 출력 디렉터리에서만 생성과 검사 진행
    parser = argparse.ArgumentParser(description="Compile, export and check the original CSR specification")  # 실행 방법 정의
    parser.add_argument("--deps", type=Path)  # 선택한 개인 pip 설치 디렉터리
    parser.add_argument("--zig", required=True, type=Path)  # 실제 C 컴파일에 사용할 Zig 실행 파일
    parser.add_argument("--out", required=True, type=Path)  # 덮어쓰지 않을 새 결과 디렉터리
    args = parser.parse_args()  # 명령줄 인자를 경로 객체로 수집
    if args.deps is not None:  # 전역 환경 대신 개인 패키지를 쓸 경우
        sys.path.insert(0, str(args.deps.resolve()))  # 실제 import 전에 해당 디렉터리 우선 검색
    from systemrdl import RDLCompiler, RDLCompileError  # 실제 SystemRDL 컴파일러와 명세 오류 형식
    from peakrdl_cheader.exporter import CHeaderExporter  # 실제 C 헤더 생성기
    from peakrdl_cheader.c_standards import CStandard  # 생성물이 사용할 GNU C 표준 선택
    source_dir = Path(__file__).resolve().parent  # 실행 위치와 무관하게 원본 소스 찾기
    out = args.out.resolve()  # 결과 경로를 절대 경로로 고정
    out.mkdir(parents=True, exist_ok=False)  # 기존 검사 기록의 덮어쓰기 거절
    zig = args.zig.resolve()  # cwd를 바꾼 뒤에도 같은 컴파일러 사용
    for name in ("example.rdl", "check_header.c"):  # 도구가 읽을 두 입력만 새 폴더로 복사
        shutil.copyfile(source_dir / name, out / name)  # 텍스트 재인코딩 없이 바이트 보존
    checks = 0  # 독립 AST 기대값과의 비교 횟수
    commands = []  # 실제 subprocess 명령과 종료 상태

    def require(actual, expected, label):  # 모든 AST 비교에 같은 실패 처리 적용
        nonlocal checks  # 바깥 비교 횟수 갱신
        if actual != expected:  # 잘못된 생성 결과는 즉시 중단
            raise AssertionError(f"{label}: {actual!r} != {expected!r}")  # 실패한 속성과 두 값 출력
        checks += 1  # 일치한 독립 비교만 집계

    def run(command):  # 실제 C 도구 실행과 원출력 보존
        environment = os.environ.copy()  # 호출자의 검색 경로 등은 그대로 사용
        environment.update({"TEMP": ".", "TMP": ".", "TMPDIR": "."})  # 임시 파일도 결과 cwd 아래에 생성
        result = subprocess.run(command, cwd=out, env=environment, capture_output=True, text=True, encoding="utf-8", errors="replace")  # 반환값을 숨기지 않고 수집
        item = {"command": command, "cwd": str(out), "returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr}  # 재현에 필요한 실행 기록
        commands.append(item)  # 성공과 의도한 실패 모두 기록
        return result  # 호출한 검사가 정상/오류 여부 판정

    compiler = RDLCompiler()  # 정상 명세를 위한 새 컴파일러
    compiler.compile_file(str(out / "example.rdl"))  # RDL 문법과 선언을 실제 파싱
    root = compiler.elaborate()  # 주소·속성을 결정하고 명세 제약 검사
    top = root.top  # 전개된 최상위 주소 공간
    require(top.inst_name, "bench_csr", "top name")  # 의도한 주소 공간이 선택됐는지 확인
    require(top.size, 12, "address space size")  # 마지막 32비트 레지스터까지12바이트
    registers = list(top.registers())  # 실제 레지스터 인스턴스 순서
    require([reg.inst_name for reg in registers], list(EXPECTED), "register names")  # 누락과 추가 레지스터 검출
    observed = {}  # 읽어 낸 AST 속성을 결과 JSON에 보존
    for reg in registers:  # 세 레지스터를 고정 기대표와 대조
        offset, expected_fields = EXPECTED[reg.inst_name]  # 해당 레지스터의 독립 주소와 필드표
        require(reg.address_offset, offset, f"{reg.inst_name} offset")  # 바이트 주소 확인
        require(reg.size, 4, f"{reg.inst_name} size")  # 레지스터당 네 바이트
        require(reg.get_property("regwidth"), 32, f"{reg.inst_name} regwidth")  # 논리 폭 확인
        require(reg.get_property("accesswidth"), 32, f"{reg.inst_name} accesswidth")  # 최소 소프트웨어 접근 폭 확인
        fields = list(reg.fields())  # 선언된 필드 인스턴스 수집
        require([field.inst_name for field in fields], list(expected_fields), f"{reg.inst_name} fields")  # 필드 누락·추가 검출
        observed[reg.inst_name] = {"offset": reg.address_offset, "size": reg.size, "fields": {}}  # 실제 레지스터 배치 기록
        for field in fields:  # 비트 위치와 읽기·쓰기 의미를 함께 확인
            values = (field.low, field.high, field.width, enum_name(field.get_property("sw")), enum_name(field.get_property("hw")), field.get_property("reset"), enum_name(field.get_property("onwrite")), enum_name(field.get_property("precedence")))  # 전개된 여덟 속성
            labels = ("low", "high", "width", "sw", "hw", "reset", "onwrite", "precedence")  # 각 비교의 진단 이름
            for label, actual, expected in zip(labels, values, expected_fields[field.inst_name]):  # 기대값과 순서대로 짝짓기
                require(actual, expected, f"{reg.inst_name}.{field.inst_name} {label}")  # 속성별 독립 비교
            observed[reg.inst_name]["fields"][field.inst_name] = dict(zip(labels, values))  # 확인한 속성 원값 보존

    for directory in ("generated_a", "generated_b"):  # 서로 다른 디렉터리에 같은 이름으로 두 번 생성
        (out / directory).mkdir()  # 헤더별 생성 위치 분리
        CHeaderExporter().export(root, str(out / directory / "registers.h"), std=CStandard.gnu11, generate_bitfields=False)  # C 비트필드 대신 마스크와 구조체 생성
    header_a = out / "generated_a/registers.h"  # 정상 검사에 사용할 실제 생성 헤더
    header_b = out / "generated_b/registers.h"  # 동일 입력 재생성 결과
    if header_a.read_bytes() != header_b.read_bytes():  # 결정적 생성 여부를 바이트로 대조
        raise AssertionError("non-deterministic header export")  # 서로 다른 출력은 정상 완료 금지
    version = run([str(zig), "cc", "--version"])  # 실행한 호스트 C 컴파일러 정보 보존
    if version.returncode != 0:  # 실행 도구 자체 오류 구분
        raise RuntimeError(version.stderr)  # 컴파일 실패를 검사 통과로 오해하지 않기
    compile_command = [str(zig), "cc", "-std=gnu11", "-Wall", "-Wextra", "-Werror", "-Igenerated_a", "check_header.c", "-o", "header_check.exe"]  # 생성 헤더를 독립 C 단언으로 컴파일
    compiled = run(compile_command)  # 호스트 구조체 배치와 마스크를 컴파일 타임에 확인
    if compiled.returncode != 0:  # 정적 단언이나 C 문법 오류는 정상 실패
        raise RuntimeError(compiled.stderr)  # 실제 컴파일 진단 전달
    executed = run([str(out / "header_check.exe")])  # MMIO 접근 없이 호스트 결과만 실행
    expected_stdout = "PASS header assertions=21 size=12 offsets=0,4,8 control_reset=4\n"  # 출력도 고정 기대값과 비교
    if executed.returncode != 0 or executed.stdout != expected_stdout or executed.stderr:  # 종료값·표준출력·오류출력 모두 확인
        raise AssertionError("header executable output mismatch")  # 출력만 비슷한 실패 실행 제외

    (out / "generated_bad").mkdir()  # 정상 생성물을 바꾸지 않을 결함 대조 폴더
    header_text = header_a.read_text(encoding="utf-8")  # 마스크 한 개만 바꿀 원문
    needle = "#define BENCH_CSR__CONTROL__MODE_SEL_bm 0xe"  # 정확히 하나여야 하는 정상 매크로
    if header_text.count(needle) != 1:  # 생성기 형식 변경을 무시하지 않기
        raise AssertionError("header mutation anchor missing")  # 의미 없는 음성 대조 방지
    (out / "generated_bad/registers.h").write_text(header_text.replace(needle, needle[:-3] + "0x6"), encoding="utf-8", newline="\n")  # 모드의 최상위 비트가 빠진 결함 주입
    bad_command = [str(zig), "cc", "-std=gnu11", "-Igenerated_bad", "check_header.c", "-o", "bad_header.exe"]  # 같은 독립 단언을 결함 헤더에 적용
    negative_header = run(bad_command)  # 잘못된 헤더가 실제 C 검사에 걸리는지 확인
    if negative_header.returncode == 0 or "mode mask" not in negative_header.stderr:  # 의도한 단언 실패까지 요구
        raise AssertionError("corrupted header was not rejected by mode mask assertion")  # 도구 장애를 결함 검출로 집계하지 않기

    errors = []  # 잘못된 명세별 실제 컴파일 진단
    text = (out / "example.rdl").read_text(encoding="utf-8")  # 정상 명세에서 한 조건만 바꿀 기준
    for name, old, new, diagnostic in MUTATIONS:  # 겹침·접근·폭 오류 네 종류
        if text.count(old) != 1:  # 오직 한 군데만 바뀌는 변형 요구
            raise AssertionError(f"ambiguous mutation: {name}")  # 원본 변경 시 잘못된 검사 생성을 중단
        candidate = out / f"{name}.rdl"  # 잘못된 입력도 결과 폴더에만 저장
        candidate.write_text(text.replace(old, new), encoding="utf-8", newline="\n")  # 정상 파일은 그대로 보존
        log = io.StringIO()  # 해당 입력의 원진단 전용 버퍼
        rejected = False  # 실제 컴파일 오류가 발생했을 때만 갱신
        with contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):  # 예상 오류를 정상 검사 출력과 분리
            try:  # 다른 파이썬 예외를 명세 오류로 숨기지 않기
                invalid_compiler = RDLCompiler()  # 실패 후 컴파일러는 재사용하지 않기
                invalid_compiler.compile_file(str(candidate))  # 잘못된 입력을 실제 파싱
                invalid_compiler.elaborate()  # 전개 단계의 의미 제약까지 검사
            except RDLCompileError:  # 실제 명세 컴파일 오류만 거절로 인정
                rejected = True  # 도구가 해당 입력을 거절했다는 상태
        message = re.sub(r"\x1b\[[0-9;]*m", "", log.getvalue())  # 파일에 색상 제어 문자 없이 기록
        if not rejected or diagnostic not in message.lower():  # 실패 이유도 의도한 규칙인지 확인
            raise AssertionError(f"wrong rejection for {name}: {message}")  # 무관한 오류로 인한 가짜 통과 제외
        errors.append({"name": name, "rejected": True, "required_diagnostic": diagnostic, "diagnostic": message, "input_sha256": sha256(candidate)})  # 실제 오류 근거 저장

    marker = f"PASS systemrdl ast_checks={checks} header_assertions=21 rejected=4 header_negative_controls=1 deterministic_exports=2"  # 정상 완료의 정확한 한 줄
    report = {"scope": "SystemRDL compile/elaborate, AST properties and host C header layout; no RTL or bus simulation", "source_sha256": {name: sha256(source_dir / name) for name in ("example.rdl", "check_spec.py", "check_header.c")}, "tools": {"python": sys.version.split()[0], "systemrdl-compiler": importlib.metadata.version("systemrdl-compiler"), "peakrdl-cheader": importlib.metadata.version("peakrdl-cheader")}, "ast_checks": checks, "observed": observed, "header_sha256": sha256(header_a), "identical_export_sha256": sha256(header_b), "header_assertions": 21, "invalid_inputs": errors, "commands": commands, "returncode": 0, "stdout": marker + "\n", "stderr": ""}  # 성공 조건과 실제 검사 범위를 한 기록으로 저장
    (out / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")  # 기존 자료에 손대지 않고 결과 파일 생성
    print(marker)  # 실제 실행과 독립 비교가 모두 끝났을 때만 출력

if __name__ == "__main__":  # 다른 코드에서 import할 때는 검사하지 않기
    main()  # 明示的なコマンド実行で検査開始
```

## 생성 헤더용 독립 C 검사 전체 코드

이 파일은 생성 헤더의 매크로를 다른 매크로만으로 재계산하여 비교하지 않고, 별도로 적은 수치와 대조합니다. `offsetof`는 컴파일한 구조체의 실제 바이트 배치를 확인합니다. `_Static_assert`가 하나라도 실패하면 실행 파일을 정상 결과로 인정하지 않습니다.

```c
#include <stddef.h> // offsetof로 실제 구조체 멤버 위치 확인
#include <stdio.h> // 검사 결과 한 줄 출력
#include "registers.h" // 실제 PeakRDL 생성물의 선언과 매크로

_Static_assert(BENCH_CSR__VERSION__REVISION_bm == 0xffffffffu, "revision mask"); // 버전 필드의 32비트 마스크
_Static_assert(BENCH_CSR__VERSION__REVISION_bp == 0, "revision position"); // 버전값 시작 비트0
_Static_assert(BENCH_CSR__VERSION__REVISION_bw == 32, "revision width"); // 버전값 폭32
_Static_assert(BENCH_CSR__VERSION__REVISION_reset == 0x10002, "revision reset"); // 명세와 별도로 적은 버전 초기값
_Static_assert(BENCH_CSR__CONTROL__RUN_EN_bm == 0x1, "run mask"); // 실행 허용 비트만 선택
_Static_assert(BENCH_CSR__CONTROL__RUN_EN_bp == 0, "run position"); // 실행 허용 위치0
_Static_assert(BENCH_CSR__CONTROL__RUN_EN_bw == 1, "run width"); // 단일 비트 필드
_Static_assert(BENCH_CSR__CONTROL__RUN_EN_reset == 0, "run reset"); // 기본 실행 금지
_Static_assert(BENCH_CSR__CONTROL__MODE_SEL_bm == 0xe, "mode mask"); // 비트3부터1까지의 마스크1110
_Static_assert(BENCH_CSR__CONTROL__MODE_SEL_bp == 1, "mode position"); // 모드값을 한 비트 왼쪽에 배치
_Static_assert(BENCH_CSR__CONTROL__MODE_SEL_bw == 3, "mode width"); // 모드 범위0부터7
_Static_assert(BENCH_CSR__CONTROL__MODE_SEL_reset == 2, "mode reset"); // 필드 자체의 초기값2
_Static_assert(BENCH_CSR__EVENTS__FLAGS_bm == 0xf, "flags mask"); // 상태 비트3부터0까지만 선택
_Static_assert(BENCH_CSR__EVENTS__FLAGS_bp == 0, "flags position"); // 상태 필드 시작 비트0
_Static_assert(BENCH_CSR__EVENTS__FLAGS_bw == 4, "flags width"); // 네 상태 비트
_Static_assert(BENCH_CSR__EVENTS__FLAGS_reset == 0, "flags reset"); // 초기 상태값0
_Static_assert(offsetof(bench_csr_t, version) == 0, "version offset"); // 첫 레지스터의 바이트 위치
_Static_assert(offsetof(bench_csr_t, control) == 4, "control offset"); // 두 번째 레지스터의 바이트 위치
_Static_assert(offsetof(bench_csr_t, events) == 8, "events offset"); // 세 번째 레지스터의 바이트 위치
_Static_assert(sizeof(bench_csr_t) == 12, "block size"); // 패딩까지 포함한 전체 주소 공간
_Static_assert((BENCH_CSR__CONTROL__MODE_SEL_reset << BENCH_CSR__CONTROL__MODE_SEL_bp) == 4, "control reset word"); // 필드 초기값2를 비트1에 놓으면 레지스터값4

int main(void) { // 메모리 장치 없이 호스트에서 검사 결과 출력
    printf("PASS header assertions=21 size=%zu offsets=%zu,%zu,%zu control_reset=4\n", sizeof(bench_csr_t), offsetof(bench_csr_t, version), offsetof(bench_csr_t, control), offsetof(bench_csr_t, events)); // 컴파일이 통과한 실제 배치 출력
    return 0; // 정적 단언을 모두 만족한 정상 종료
} // 호스트 검사 끝
```

## 실제 실행과 결과

2026-10-26의 로컬 실행에서 Python 3.12.14, SystemRDL Compiler 1.33.0, PeakRDL-CHeader 1.1.0을 사용했습니다. 생성 헤더의 호스트 C 검사는 Zig의 Clang 21.1.0, `x86_64-unknown-windows-gnu`, GNU C11 모드로 컴파일했습니다. 버전·실제 명령·종료값·표준출력·오류 진단·소스 SHA-256은 [실행 메타데이터](example.json)에 기록합니다.

```text
PASS header assertions=21 size=12 offsets=0,4,8 control_reset=4
PASS systemrdl ast_checks=50 header_assertions=21 rejected=4 header_negative_controls=1 deterministic_exports=2
```

첫 줄은 Python이 내부에서 실행하고 수집한 C 프로그램의 출력입니다. 최상위 Python 명령의 표준출력에는 두 번째 줄만 나타납니다. 생성 헤더의 자체 크기 단언은 독립 검사 수 21개에 추가로 들어 있지만 이 숫자에는 중복 집계하지 않습니다.

| 검사 묶음 | 실제 수 | 판정 기준 |
| --- | ---: | --- |
| 주소 공간 이름·크기·레지스터 목록 | 3 | 독립 기대값과 일치합니다. |
| 세 레지스터의 오프셋·크기·레지스터 폭·접근 폭 | 12 | 각 네 항목이 일치합니다. |
| 세 레지스터의 필드 목록 | 3 | 필드 누락·추가가 없습니다. |
| 네 필드의 여덟 속성 | 32 | RO·RW·W1C 속성까지 포함합니다. |
| C 정적 단언 | 21 | 필드 매크로 16개, 오프셋 3개, 크기 1개, 초기 비트 패턴 1개가 일치합니다. |
| 잘못된 RDL 입력 | 4 | `RDLCompileError`와 해당 규칙의 진단을 확인합니다. |
| 결함 헤더 대조 | 1 | `mode mask` 단언으로 컴파일이 실패합니다. |
| 같은 헤더 재생성 | 2회 생성·1회 비교 | 바이트가 동일합니다. |

잘못된 RDL 입력 네 개의 변경과 실제 진단은 다음과 같습니다. 정상 명세와 생성 원본은 바꾸지 않으며, 변형 입력은 새 결과 디렉터리에만 만듭니다.

| 이름 | 한 가지 변경 | 실제 진단의 핵심 |
| --- | --- | --- |
| `address_overlap` | `control` 주소를 `0x00`으로 변경합니다. | `control`과 `version`의 주소가 겹친다고 거절합니다. |
| `field_overlap` | `mode_sel[3:1]`을 `[2:0]`으로 변경합니다. | `run_en[0:0]`과 필드가 겹친다고 거절합니다. |
| `readonly_w1c` | `flags`의 `sw=rw`만 `sw=r`로 변경합니다. | 쓰기 접근 없이 `onwrite`를 지정했다고 거절합니다. |
| `reset_overflow` | 세 비트 모드의 초기값을 8로 변경합니다. | 필드 폭에 초기값이 들어가지 않는다고 거절합니다. |

결함 헤더 검사는 `MODE_SEL_bm=0x6`을 넣었을 때 별도 C 파일의 기대값 `0xe`가 일치하지 않는 경우입니다. 실제 C 컴파일러는 `6 == 14` 조건과 `mode mask` 단언 실패를 출력했고 종료값은 1입니다. 정상 실행의 종료값 0과 구분하여 기록합니다.

생성된 정상 `registers.h`의 SHA-256은 `7cc65aa4b32d7be482d2c59d006ad1009ab809e8bcb064d323ea02528d96b05c`입니다. 헤더와 실행 파일은 빌드 디렉터리에 생성하며 이 폴더의 직접 작성한 소스 목록에는 포함하지 않습니다.

## 재현 명령

다음은 이 예제 폴더를 현재 디렉터리로 둔 PowerShell 명령입니다. `$work`는 원하는 별도 작업 디렉터리로 지정합니다. Python 명령과 Zig 경로는 설치 환경에 맞게 지정합니다. `run-new`는 아직 없는 폴더여야 하며, 이 스크립트는 기존 출력 디렉터리의 덮어쓰기를 거절합니다.

```powershell
$work = 'C:/temp/systemrdl-check'
$pythonExe = 'python'
$zigExe = 'C:/tools/zig/zig.exe'
& $pythonExe -m pip install --target "$work/deps" 'systemrdl-compiler==1.33.0' 'peakrdl-cheader==1.1.0'
& $pythonExe ./check_spec.py --deps "$work/deps" --zig $zigExe --out "$work/run-new"
```

개인 설치 경로 없이 가상 환경에 패키지를 설치한 경우에는 `--deps`를 생략합니다. 실제 수행한 명령은 `example.json`의 경로와 구분해서 볼 수 있습니다. 스크립트는 `report.json`, 두 정상 생성 헤더, 결함 헤더, 변형 RDL 파일, 호스트 실행 파일을 출력 폴더 아래에 둡니다. 정상 생성 API 호출과 실제 subprocess 호출도 결과에 남깁니다.

## 활용 조건과 한계

레지스터 주소표를 펌웨어·RTL·문서에 각각 옮겨 적으면 주소나 비트 범위가 어긋날 수 있습니다. SystemRDL 같은 명세 언어는 한 입력에서 여러 산출물을 만드는 작업에 사용할 수 있습니다. 이 예제는 그중 C 헤더 생성과 명세 속성 확인을 직접 수행합니다. 특정 제품에서 실제로 사용했다고 주장하는 사례는 아닙니다.

W1C 필드는 일반 RW 필드처럼 읽고 수정한 값을 그대로 다시 쓰면 의도하지 않은 상태 비트를 소거할 수 있습니다. 장치 계약이 W1C라면 소거할 비트의 1 마스크를 쓰는 의미를 별도로 이해해야 합니다. 여기서는 그 계약이 AST에 남는지만 확인합니다. 실제 하드웨어의 동시 갱신·부분 쓰기·버스 응답·리셋 타이밍을 검증하려면 RTL 생성 또는 별도 구현과 버스 테스트벤치가 필요합니다.

이 검사는 단일 주소 공간, 비배열 레지스터 세 개, 32비트 레지스터·접근 폭이라는 작은 입력에 한정합니다. 여러 버스, 주소 재배치, 별도 endian 장치, 64비트 이상 레지스터, C 비트필드 배치, 합성·타이밍·CDC·실기판 동작은 시험하지 않았습니다. 주소와 마스크가 맞는다는 결과를 버스 기능 검증이나 실물 동작 성공으로 확대하지 않습니다.

## 복습 메모

- 필드 초기값 2와 레지스터 비트 패턴 4는 서로 다른 위치 표현입니다.
- RO·RW·W1C는 선언의 의미이며 일반 C 구조체가 그 접근 의미를 강제하지 않습니다.
- 동일 생성기를 두 번 돌린 비교는 결정성을 확인하며, 독립 기대값 비교와 구분합니다.
- 오류 입력 검사는 단순한 예외 발생뿐 아니라 의도한 제약의 진단인지 확인합니다.
- 주소 오프셋의 단위는 바이트이고 필드 범위의 단위는 비트입니다.

## 근거와 작성 범위

레지스터 구성, 기대표, 검사 프로그램과 변형 입력은 이 예제를 위해 직접 작성했습니다. 공식 문서의 예제 명세나 테스트 코드를 복사한 자료가 아닙니다.

- [Accellera SystemRDL 표준 안내](https://www.accellera.org/downloads/standards/systemrdl)는 레지스터 명세와 산출물의 역할을 확인하는 근거입니다.
- [SystemRDL 2.0 공식 명세](https://www.accellera.org/images/downloads/standards/systemrdl/SystemRDL_2.0_Jan2018.pdf)는 접근 속성·쓰기 부작용·우선순위 의미의 기준입니다.
- [SystemRDL Compiler API](https://systemrdl-compiler.readthedocs.io/en/stable/api/compiler.html)와 [속성 참조](https://systemrdl-compiler.readthedocs.io/en/stable/property_reference.html)는 실제 파싱·전개 API와 확인할 속성의 근거입니다.
- [PeakRDL-CHeader API](https://peakrdl-cheader.readthedocs.io/en/latest/api.html)는 헤더 생성 옵션의 근거입니다. [라이선스 안내](https://peakrdl-cheader.readthedocs.io/en/latest/licensing.html)는 생성기와 생성 코드의 적용 범위를 구분합니다. 도구 패키지는 이 폴더에 복사하지 않습니다.
