# Structured Text의 스캔과 온도 표시 상태 | Scan-based temperature indication in ST

[현업 언어 목차](../README.md) · [실제 실행 기록](example.json)

## ST를 사용하는 위치

Structured Text(ST)는 PLC의 프로그램과 함수 블록을 작성하는 IEC 61131-3 언어입니다. C로 같은 계산을 쓸 수 있다는 사실과 ST 프로젝트를 C 소스라고 부르는 것은 다릅니다. [IEC 61131-3:2025의 공식 개요](https://webstore.iec.ch/en/publication/68533)는 ST, LD, FBD와 프로그램 구조를 위한 SFC 요소를 구분합니다. 이 공개 개요를 읽은 것이 표준 전문을 검토했다는 뜻은 아닙니다.

[Phoenix Contact PLCnext Engineer의 IEC 프로그래밍 안내](https://engineer.plcnext.help/latest/iecprogramming.htm)는 실제 제품의 ST·FBD·LD 편집, 프로그램 인스턴스와 태스크 설정을 설명합니다. 이 예제는 그 제품을 실행한 결과가 아니라 [Beremiz 1.6.0 공식 Windows 번들](https://github.com/beremiz/beremiz/releases/tag/v1.6.0)에 동봉된 matiec로 직접 작성한 ST를 번역·실행한 기록입니다.

## 입력과 상태의 약속

실험용 온도 표시등을 모형으로 사용합니다. 모터·히터·장비 출력을 제어하지 않습니다. `Temperature10`은 섭씨 0.1도 단위의 `DINT` 정수 입력이며 여기에는 센서 통신·유효성 판단이 없습니다. 극단 정수 입력은 형식의 경계 검사이고 실제 온도 자료가 아닙니다.

| 입력 조건 | 이번 호출 뒤 Lit |
| --- | --- |
| Enable=FALSE | 이전 상태와 온도에 관계없이 FALSE입니다. |
| Enable=TRUE, 온도≥300 | TRUE입니다. |
| Enable=TRUE, 온도≤250 | FALSE입니다. |
| Enable=TRUE, 250<온도<300 | 이전 출력 상태를 유지합니다. |

30.0도에서 켜고 25.0도에서 끄는 이력 특성인 히스테리시스를 둡니다. 중간 구간에서 직전 상태를 기억하면 문턱 근처의 작은 변화마다 표시 상태가 반복해서 바뀌는 일을 줄일 수 있습니다. 이 임계값은 직접 정한 교육용 조건이며 장비의 운용값이 아닙니다.

`FUNCTION_BLOCK`의 인스턴스가 상태를 보관합니다. 새 인스턴스는 `Lit=FALSE`이고, 호스트가 입력을 넣고 생성된 body 함수를 한 번 호출할 때 상태를 한 번 갱신합니다. 여기서 한 호출은 한 스캔의 논리 계산을 흉내 내는 단위이며 실제 10ms 같은 시간 주기가 아닙니다. PLC의 입력 이미지·태스크 스케줄러·출력 이미지·재시작·RETAIN 처리는 구현하지 않았습니다.

## 입력부터 출력까지

```mermaid
flowchart LR
    ST[ST 함수 블록] --> M[matiec 파싱·C 생성]
    M --> C[생성 C와 호스트 검사 컴파일]
    C --> I[입력 고정]
    I --> S[body 한 번 호출]
    S --> O[갱신된 Lit 비교]
    O --> I
```

| 호출 | Enable | Temperature10 | Lit | 읽는 순서 |
| --- | --- | --- | --- | --- |
| 초기화 | — | — | FALSE | 새 인스턴스의 초기값입니다. |
| 1 | TRUE | 240 | FALSE | 낮은 구간입니다. |
| 2 | TRUE | 290 | FALSE | 유지 구간이므로 꺼진 상태를 유지합니다. |
| 3 | TRUE | 300 | TRUE | 높은 문턱의 등호를 포함합니다. |
| 4 | TRUE | 270 | TRUE | 같은 유지 구간이어도 이전 상태가 켜져 있습니다. |
| 5 | TRUE | 250 | FALSE | 낮은 문턱의 등호를 포함합니다. |
| 6 | TRUE | 300 | TRUE | 다시 켭니다. |
| 7 | FALSE | 400 | FALSE | 사용 중단이 높은 온도보다 우선합니다. |
| 8 | TRUE | 275 | FALSE | 사용 중단 때 지운 상태를 이어받습니다. |

## 실행과 독립 비교

2026-10-26에 실제 matiec의 ST 번역, Zig 0.16.0/Clang 21.1.0의 C 컴파일, 생성 코드의 호스트 실행을 수행했습니다. matiec의 자체 버전 출력은 `0.1`이며 changeset은 비어 있습니다. 이를 최근 버전 번호로 추정하지 않고 배포 번들 1.6.0·컴파일러 SHA·표준 헤더 SHA를 기록합니다.

온도 입력 10개와 Enable 두 값의 20가지 조합을 길이 3의 모든 순서로 만들었습니다. 8,000개의 새 인스턴스 초기값 8,000번, 세 번씩 호출한 출력 24,000번, 고정 예제 흐름 8번을 합해 32,008개 조건을 비교했습니다. 기대 출력은 생성된 C의 내부 상태 대신 이전 기대 출력과 입력으로 계산한 별도 논리식 및 고정 상태표에서 구합니다. 온도 입력은 DINT 최솟값·최댓값, 부호와 250·300의 양쪽 경계를 포함합니다.

복사본에만 `<= 250`을 `< 250`으로 바꾼 뒤 실제 번역·컴파일·실행을 반복했습니다. 낮은 문턱에서 꺼져야 할 출력이 켜져 남아 `sequence=155, scan=2`에서 기능 비교가 실패했습니다. 컴파일 실패를 결함 검출로 세지 않았습니다.

```text
PASS plc sequences=8000 scans=24008 checks=32008
FAIL plc sequence=155 scan=2 expected=0 actual=1
PASS structured-text normal_checks=32008 negative_boundary=detected
```

첫 줄은 정상 검사, 둘째 줄은 의도한 경계 결함 실행, 셋째 줄은 두 결과를 판정한 실행기의 출력입니다. C 표준은 C11이고 직접 작성한 검사에는 `-Wall -Wextra -Werror`를 적용합니다. 생성된 표준 FB의 미사용 함수 경고만 `#pragma` 구간에서 제외하고 의존 헤더는 `-isystem`으로 지정합니다. 표준 라이브러리 전체를 경고 없이 검증했다는 주장은 아닙니다.

저장소 루트에서 실행합니다. `--build-dir`은 아직 없는 폴더를 지정하며, `iec2c`와 그 번들의 `lib`를 함께 둡니다. 새 환경에서 다른 matiec 판본을 사용하면 생성된 C의 자료형·인터페이스도 달라질 수 있으므로 이 검사와 맞는지 먼저 확인합니다.

```bash
python -B 하드웨어코딩_hardware-coding/현업언어_industry-languages/04-PLC스캔_structured-text/run_checks.py --matiec /path/to/matiec/iec2c --zig /path/to/zig --build-dir /path/to/new-plc-build --report /path/to/plc-result.json
```

실행기는 원본을 변경하지 않고 새 작업 폴더에서 C를 생성합니다. 생성된 `POUS.c`·`POUS.h`와 표준 헤더의 해시, 실제 명령·종료 코드·stdout·stderr는 `example.json`에 있습니다. 외부 컴파일러·지원 라이브러리는 직접 작성한 소스와 구분하며, 각 파일의 GPL·LGPL 고지를 따릅니다. [matiec 프로젝트 안내](https://openplcproject.gitlab.io/matiec/)의 오래된 표준 기반 설명을 IEC 61131-3:2025 전체 지원으로 읽지 않습니다.

## C·RTL과 비교

ST의 `:=`는 대입이고 `=`는 비교입니다. `VAR_INPUT`·`VAR_OUTPUT`과 `FUNCTION_BLOCK`은 호출 인터페이스와 인스턴스 상태를 표현합니다. C에서는 구조체와 갱신 함수를 직접 연결해 같은 논리를 만들 수 있지만, 여기의 C 파일은 ST를 시험하는 호스트 드라이버입니다. 업무의 작성 언어가 C로 바뀌었다는 뜻이 아닙니다.

RTL의 여러 레지스터가 같은 클록 에지에서 갱신되는 모델과 PLC 프로그램을 태스크에서 순서대로 호출하는 모델은 구분해야 합니다. 이 함수 블록은 물리 회로를 합성하지 않으며, 한 호출의 성공은 실제 PLC의 주기·지터·I/O·기능 안전을 확인한 결과가 아닙니다.

## 풀이 요약

출력의 초기값을 정하고 사용 중단을 먼저 처리합니다. 높은 구간과 낮은 구간에서만 상태를 쓰고 중간에서는 이전 상태를 남깁니다. 매 호출 직후 결과를 비교하면 스캔을 한 번 늦게 적용한 오류와 경계의 등호 오류를 구분해서 찾을 수 있습니다.

## indicator.st의 전체 코드

```iecst
FUNCTION_BLOCK TempIndicator (* 호출 사이에 표시 상태를 기억할 블록 *)
VAR_INPUT (* 매 스캔에 전달할 입력 *)
    Enable : BOOL; (* 표시 기능의 사용 여부 *)
    Temperature10 : DINT; (* 온도 0.1도 단위의 정수 표본 *)
END_VAR (* 입력 선언 끝 *)
VAR_OUTPUT (* 호출 뒤 읽을 출력 *)
    Lit : BOOL := FALSE; (* 시작할 때 표시등은 꺼 두기 *)
END_VAR (* 출력 선언 끝 *)
IF NOT Enable THEN (* 사용하지 않으면 이전 상태보다 우선 *)
    Lit := FALSE; (* 표시 상태 지우기 *)
ELSIF Temperature10 >= 300 THEN (* 30.0도부터 켜기 *)
    Lit := TRUE; (* 높은 구간에서 켜진 상태 저장 *)
ELSIF Temperature10 <= 250 THEN (* 25.0도까지 내려오면 끄기 *)
    Lit := FALSE; (* 낮은 구간에서 꺼진 상태 저장 *)
END_IF; (* 중간 구간에서는 대입하지 않아 직전 상태 유지 *)
END_FUNCTION_BLOCK (* 한 번 호출이 한 번의 상태 갱신 *)
```

## check_driver.c의 전체 코드

```c
#include <stdio.h> /* 실행 결과와 실패 위치 출력 */
#include <stdint.h> /* 32비트 정수 경계 */
#include "iec_std_lib.h" /* matiec의 BOOL·DINT·접근 매크로 */
#include "accessor.h" /* 생성 블록의 선언·읽기·쓰기 매크로 */
#include "POUS.h" /* 실제 ST에서 생성한 블록 자료형 */
#pragma GCC diagnostic push /* 생성된 표준 블록의 경고 범위만 분리 */
#pragma GCC diagnostic ignored "-Wunused-function" /* 이 예제에서 쓰지 않는 표준 FB */
#include "POUS.c" /* 실제 ST에서 생성한 초기화·한 스캔 함수 */
#pragma GCC diagnostic pop /* 직접 작성한 검사에는 원래 경고 적용 */
TIME __CURRENT_TIME = {0, 0}; /* 타이머를 쓰지 않는 호스트 검사 */
static unsigned checks = 0; /* 실제 판정한 조건 수 */
static int compare(TEMPINDICATOR_data__ *block, int expected, unsigned sequence, unsigned scan) { /* 출력 한 번 대조 */
    int actual = __GET_VAR(block->LIT); /* 생성 구조체의 접근자로 출력 읽기 */
    ++checks; /* 성공과 실패 모두 판정 수에 포함 */
    if (actual != expected) { /* 독립 기대값과 다른지 확인 */
        fprintf(stderr, "FAIL plc sequence=%u scan=%u expected=%d actual=%d\n", sequence, scan, expected, actual); /* 재현 위치 */
        return 0; /* 불일치를 호출자에게 전달 */
    } /* 실패 처리 끝 */
    return 1; /* 같은 출력이면 통과 */
} /* 출력 대조 끝 */
static void step(TEMPINDICATOR_data__ *block, int enabled, int32_t temperature10) { /* 입력을 고정한 뒤 한 번 호출 */
    __SET_VAR(block->, ENABLE, , enabled); /* 이번 스캔의 사용 여부 */
    __SET_VAR(block->, TEMPERATURE10, , temperature10); /* 이번 스캔의 정수 표본 */
    TEMPINDICATOR_body__(block); /* 갱신 횟수 한 번이며 실제 시간이 아님 */
} /* 호스트의 한 스캔 호출 끝 */
int main(void) { /* 실행 가능한 검사의 시작 */
    const int32_t temperatures[] = {INT32_MIN, -1, 249, 250, 251, 275, 299, 300, 301, INT32_MAX}; /* 부호·경계·유지 구간 */
    for (unsigned sequence = 0; sequence < 8000; ++sequence) { /* 입력 20가지의 길이3 모든 순서 */
        TEMPINDICATOR_data__ block; /* 서로 영향을 주지 않는 새 인스턴스 */
        TEMPINDICATOR_init__(&block, 0); /* 초기 출력 FALSE와 기본 EN 설정 */
        if (!compare(&block, 0, sequence, 0)) return 1; /* 초기 상태 자체도 확인 */
        unsigned encoded = sequence; /* 20진수 자릿수로 입력 선택 */
        int expected = 0; /* 생성 코드와 독립인 이전 출력 */
        for (unsigned scan = 1; scan <= 3; ++scan) { /* 한 호출씩 상태를 이어가기 */
            unsigned choice = encoded % 20; /* 이번 입력 번호 */
            encoded /= 20; /* 다음 입력 번호로 이동 */
            int enabled = (int)(choice % 2); /* 같은 온도에서 FALSE·TRUE 모두 사용 */
            int32_t temperature10 = temperatures[choice / 2]; /* 입력 표의 정수 값 */
            expected = enabled && (temperature10 >= 300 || (expected && temperature10 > 250)); /* 명세의 유지 조건을 논리식으로 계산 */
            step(&block, enabled, temperature10); /* 실제 번역된 ST 한 번 실행 */
            if (!compare(&block, expected, sequence, scan)) return 1; /* 매 호출 직후 외부 출력 비교 */
        } /* 길이3 입력 순서 끝 */
    } /* 전 순서 대조 끝 */
    TEMPINDICATOR_data__ trace; /* 사람이 따라갈 별도 실행 */
    TEMPINDICATOR_init__(&trace, 0); /* 꺼진 상태에서 시작 */
    const int enabled[] = {1, 1, 1, 1, 1, 1, 0, 1}; /* 사용 중단과 재개 포함 */
    const int32_t input[] = {240, 290, 300, 270, 250, 300, 400, 275}; /* 상승·유지·하강·중단 입력 */
    const int expected[] = {0, 0, 1, 1, 0, 1, 0, 0}; /* 상태표에서 직접 적은 결과 */
    for (unsigned i = 0; i < 8; ++i) { /* 예제 입력을 순서대로 전달 */
        step(&trace, enabled[i], input[i]); /* 입력을 넣고 한 번 갱신 */
        if (!compare(&trace, expected[i], 8000, i + 1)) return 1; /* 별도 고정 기대표 비교 */
        printf("TRACE scan=%u enabled=%d temperature10=%d lit=%d\n", i + 1, enabled[i], (int)input[i], __GET_VAR(trace.LIT)); /* 입력과 결과 */
    } /* 흐름 출력 끝 */
    printf("PASS plc sequences=8000 scans=24008 checks=%u\n", checks); /* 실제 집계 출력 */
    return 0; /* 모든 조건을 만족한 경우만 정상 종료 */
} /* 호스트 검사 끝 */
```

## run_checks.py의 전체 코드

```python
"""실제 ST 번역과 호스트 실행을 수행하고 정상·경계 결함 결과를 따로 기록합니다."""  # 실행 검사의 범위
import argparse  # 도구와 출력 경로
import hashlib  # 실행 소스와 생성 파일의 바이트 해시
import json  # 결과 저장
from pathlib import Path  # 경로를 명시적으로 다루기
import shutil  # 직접 작성한 소스만 작업 폴더로 복사
import subprocess  # 실제 컴파일러와 검사 실행

ROOT = Path(__file__).resolve().parent  # 원본 소스 폴더

def run(command, cwd, records):  # 실행 사실과 출력을 함께 남기기
    result = subprocess.run([str(x) for x in command], cwd=cwd, capture_output=True, text=True, encoding='utf-8', errors='replace')  # 셸 없이 인자 전달
    row = dict(command=[str(x) for x in command], cwd=str(cwd), returncode=result.returncode, stdout=result.stdout, stderr=result.stderr)  # 원래 출력 보존
    records.append(row)  # 실행 순서 유지
    return row  # 호출자가 기대 상태를 판정

def require(ok, reason):  # -O에서도 유지되는 검사
    if not ok: raise ValueError(reason)  # 오류를 성공 결과로 덮지 않기

def main():  # 재현 가능한 명령행
    parser = argparse.ArgumentParser(description=__doc__)  # 입력 안내
    parser.add_argument('--matiec', type=Path, required=True)  # 실제 iec2c 실행 파일
    parser.add_argument('--zig', type=Path, required=True)  # 생성 C를 컴파일할 Zig
    parser.add_argument('--build-dir', type=Path, required=True)  # 아직 없는 작업 폴더
    parser.add_argument('--report', type=Path, required=True)  # 결과 파일
    args = parser.parse_args()  # 경로 읽기
    compiler, zig, build = args.matiec.resolve(), args.zig.resolve(), args.build_dir.resolve()  # 실행 중 경로 기준 고정
    require(not build.is_relative_to(ROOT), 'build directory must be outside the source directory')  # 소스 옆 생성물 방지
    require(compiler.is_file() and zig.is_file(), 'compiler executable not found')  # 없는 도구로 통과하지 않기
    library = compiler.parent / 'lib'  # 사용한 번들의 표준 선언 위치
    require((library / 'C/accessor.h').is_file(), 'matiec library directory not found')  # 다른 판본의 헤더 혼합 방지
    build.mkdir(parents=True, exist_ok=False)  # 이전 생성물을 재사용하지 않기
    commands = []  # 실제 명령 전체
    require(run([compiler, '-v'], build, commands)['returncode'] == 0, 'matiec version failed')  # 도구가 시작되는지 확인
    require(run([zig, 'cc', '--version'], build, commands)['returncode'] == 0, 'C compiler version failed')  # 실제 C 도구 판본
    results = []  # 정상·결함을 분리할 목록
    for name in ('normal', 'negative_boundary'):  # 같은 검사에 서로 다른 ST 입력 사용
        work = build / name  # 독립 생성 위치
        work.mkdir()  # 다른 실행의 C를 섞지 않기
        original = (ROOT / 'indicator.st').read_bytes()  # 원본 그대로 읽기
        source = original if name == 'normal' else original.replace(b'<= 250', b'< 250')  # 복사본에만 낮은 경계 결함 주입
        require(name == 'normal' or source != original, 'mutation was not applied')  # 결함이 실제로 바뀌었는지 확인
        (work / 'indicator.st').write_bytes(source)  # 이번 번역의 정확한 입력
        shutil.copyfile(ROOT / 'check_driver.c', work / 'check_driver.c')  # 같은 독립 검사 사용
        translated = run([compiler, '-I', library, '-T', work, work / 'indicator.st'], work, commands)  # 실제 ST 파서·코드 생성
        require(translated['returncode'] == 0, f'ST translation failed: {name}')  # 번역 실패를 기능 결함 검출로 세지 않기
        generated = {p: hashlib.sha256((work / p).read_bytes()).hexdigest() for p in ('POUS.c', 'POUS.h')}  # 실제 생성물과 연결
        executable = work / 'check.exe'  # 검사 프로그램 출력
        compiled = run([zig, 'cc', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror', '-isystem', library / 'C', '-I', work, work / 'check_driver.c', '-o', executable], work, commands)  # 생성 C와 호스트 검사 연결
        require(compiled['returncode'] == 0, f'C compilation failed: {name}')  # 컴파일 오류는 별도 실패
        executed = run([executable], work, commands)  # 실제 생성 코드 실행
        if name == 'normal':  # 정상 명세의 기대 결과
            require(executed['returncode'] == 0 and any(line == 'PASS plc sequences=8000 scans=24008 checks=32008' for line in executed['stdout'].splitlines()), 'normal behavior failed')  # 종료·집계 모두 확인
        else:  # 경계 결함은 기능 비교에서 실패해야 함
            require(executed['returncode'] == 1 and executed['stderr'].startswith('FAIL plc sequence='), 'boundary fault was not detected')  # 런타임의 실제 불일치 근거
        results.append(dict(name=name, expected_returncode=0 if name == 'normal' else 1, **{k: executed[k] for k in ('returncode', 'stdout', 'stderr')}, input_sha256=hashlib.sha256(source).hexdigest(), generated_sha256=generated))  # 실행별 소스·결과
    hashes = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in ('indicator.st', 'check_driver.c', 'run_checks.py')}  # 게시 소스 바이트
    dependencies = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((library / 'C').glob('*.h'))}  # 사용한 표준 헤더의 판본 연결
    report = dict(status='passed_actual_st_translation_and_host_checks', source_sha256=hashes, compiler_sha256=hashlib.sha256(compiler.read_bytes()).hexdigest(), library_header_sha256=dependencies, commands=commands, results=results, checks=32008, sequences=8000, scans=24008, scope=dict(actual_st_translation=True, generated_c_execution=True, cyclic_scheduler=False, real_plc=False, physical_io=False, safety_validation=False))  # 실제 확인 범위
    args.report.parent.mkdir(parents=True, exist_ok=True)  # 보고서 부모 준비
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')  # 결과 보존
    print('PASS structured-text normal_checks=32008 negative_boundary=detected')  # 바깥 실행의 완료 출력
    return 0  # 모든 비교를 마친 경우만 성공

if __name__ == '__main__': raise SystemExit(main())  # import만으로 도구를 실행하지 않기
```
