# RC 저역통과 회로의 과도·AC 해석과 정확해 비교

[하드웨어 코딩 목차](../../README.md)

입력에서 출력까지 1kΩ 저항을 연결하고 출력과 기준 노드 0 사이에 1µF 커패시터를 둡니다. 직접 작성한 netlist를 실제 ngspice 47로 실행하고, Python은 시뮬레이터가 출력한 표를 독립 해석식과 비교하는 역할만 맡습니다. 회로를 Python으로 대체 계산한 결과를 SPICE 실행으로 표시하지 않습니다.

## 회로와 SPICE의 역할

```text
Vin ─── R1=1kΩ ─── out
                   │
                 C1=1µF
                   │
0 ─────────────────┘
```

R1·C1·Vin은 부품과 연결 관계를 선언합니다. 첫 줄은 회로 제목이며 노드 0은 전압의 기준입니다. 일반 프로그래밍 언어의 위에서 아래로 실행하는 대입문과 다릅니다. ngspice는 이 연결에서 회로 방정식을 구성하고 수치적으로 풉니다. .control 안의 tran·ac·wrdata는 해석 순서와 파일 출력을 제어합니다. [공식 control-language 안내](https://ngspice.sourceforge.io/ngspice-control-language-tutorial.html)는 netlist와 제어 명령의 역할을 구분합니다.

소자값 1k는 1000Ω, 1u는 10⁻⁶F이며 1m는 10⁻³초입니다. SPICE의 m은 milli이므로 mega와 혼동하지 않습니다. 외부 모델이나 제조사 라이브러리가 필요 없는 이상 저항·커패시터·전압원 예제입니다.

## 시간과 주파수의 기준

RC의 시정수 τ=RC=1ms이며 차단 주파수 fc=1/(2πRC)=159.154943Hz입니다. 커패시터의 임피던스 1/(jωC)를 전압 분배에 넣으면 H(jω)=1/(1+jωRC)입니다. 저역통과 응답과 이 식은 [MIT의 The Art of Insight §2.4, 식 2.55](https://ocw.mit.edu/courses/res-6-011-the-art-of-insight-in-science-and-engineering-mastering-complexity-fall-2014/3bca850386a3005c22134fa62fb3bad5_MITRES_6-011F14_art_insfin.pdf)를 참고합니다. 아래 부품값·자극·계산 예는 직접 구성했습니다.

과도 해석에서는 입력이 1ms까지 0V이고 그다음 1µs 동안 1V까지 선형 상승합니다. 펄스의 높은 구간은 20ms로 해석 종료 6ms보다 길어서 이번 범위에 하강은 없습니다. 이상적인 순간 계단으로 근사하지 않고 실제 유한 상승을 기준에 반영합니다.

u=t−1ms, 상승 시간 tr=1µs로 두면 KCL의 τ·dv/dt+v=vin을 풀어 다음과 같이 계산합니다. 시작 전 출력은 0V입니다.

- 0<u<tr에서는 v(u)=(u−τ(1−exp(−u/τ)))/tr입니다.
- u≥tr에서는 v(u)=1−[τ/tr·(1−exp(−tr/τ))]·exp(−(u−tr)/τ)입니다.

Python은 작은 지수 차이의 유효 숫자를 지키기 위해 expm1을 사용합니다. AC의 1V는 소신호 복소 진폭이며 transient의 펄스 크기와 같은 시간 파형을 뜻하지 않습니다. AC는 매 주파수에서 정상상태 복소 응답을 계산하며 0.01fc부터 100fc까지 decade당 10간격, 끝점 포함 41행입니다. [ngspice 공식 RC·AC 설명](https://ngspice.sourceforge.io/ngspice-eeschema.html)은 DC·AC·PULSE 입력과 transient의 차이를 보여줍니다.

## 실제 계산과 독립 대조

2026-10-26에 공식 Windows 64비트 ngspice 47 콘솔을 실제 실행했습니다. 종료 코드 0, stderr 공백, 완료 문구와 두 데이터 파일을 확인했습니다. 버전 출력은 KLU 지원 빌드라고 표시하지만 이번 실제 계산 로그는 SPARSE 1.3을 사용했다고 기록하므로 두 내용을 구분합니다.

과도 해석은 0~6ms를 최대 내부 간격 1µs로 계산하여 실제 6040행을 출력했습니다. tran의 첫 인자 10µs를 모든 출력 행의 균일 간격이라고 가정하지 않습니다. Python은 각 행의 실제 시간에서 정확해를 평가하며, 아래 표도 가장 가까운 실제 행의 시간을 그대로 적습니다.

| 실제 시간 | 입력 | ngspice 출력 | 해석값 | 절대 오차 |
| --- | --- | --- | --- | --- |
| 1.000000000ms | 0.000000V | 0.000000000000V | 0.000000000000V | 0.000e+0V |
| 1.001000000ms | 1.000000V | 0.000499831626V | 0.000499833375V | 1.749e-9V |
| 2.000068304ms | 1.000000V | 0.631961727260V | 0.631961697291V | 2.997e-8V |
| 3.000068304ms | 1.000000V | 0.864606297178V | 0.864606274870V | 2.231e-8V |
| 6.000000000ms | 1.000000V | 0.993258685700V | 0.993258682904V | 2.796e-9V |

모든 6040행의 최대 전압 오차는 2.997762e-8V이며 미리 정한 10⁻⁵V 한도보다 작았습니다. 시간 적분과 수치 허용치의 결과이며 실물 전압 오차를 측정한 값은 아닙니다.

| 실제 주파수 | 전달함수 크기 | 위상 | 해석의 의미 |
| --- | --- | --- | --- |
| 15.915494309Hz | 0.995037190210 | -5.710593137° | 0.1fc의 거의 통과하는 저주파입니다. |
| 159.154943092Hz | 0.707106781187 | -45.000000000° | fc에서 1/√2와 −45°입니다. |
| 1591.549430919Hz | 0.099503719021 | -84.289406863° | 10fc에서 크게 줄어든 진폭입니다. |

AC 41행 모두를 복소수 1/(1+j2πfRC)와 직접 비교했습니다. 최대 복소 오차는 2.288783e-16이며 한도 10⁻¹⁰보다 작았습니다. 크기만 맞고 위상이 틀린 경우도 이 비교에서는 실패합니다. 종료 코드만 보거나 생성 파일의 존재만 보고 통과로 세지 않습니다.

실제 명령·버전·stdout·측정값·기준식과의 오차·소스 SHA는 [example.json](example.json)에 기록합니다. 수천 행의 표는 임시 빌드 폴더에 남기며 공개 메타에는 그 행 수·해시·대표값을 기록합니다.

## 현실 회로와의 차이

ADC 앞의 저역통과, 신호 평활과 센서 입력 대역을 정하는 기본 계산에 연결됩니다. 이 회로는 출력 부하가 없는 이상 모델이며 전압원의 출력 저항도 0입니다. 실제 부하·커패시터 ESR·기생 인덕턴스·부품 오차·노이즈를 넣으면 시정수와 응답이 달라질 수 있습니다. PCB 추출·온도 sweep·실물 측정은 수행하지 않았습니다.

출력을 저항 양단에서 읽으면 같은 회로라도 다른 전달함수가 됩니다. 디지털 RTL의 클록 에지나 펌웨어 명령 주기와도 구분합니다. 여기서 ngspice는 연속 전압·전류 방정식을 수치적으로 풀며 Python은 결과를 읽고 판정합니다.

## 재현 명령

공식 [ngspice 다운로드](https://ngspice.sourceforge.io/download.html)의 Windows 콘솔을 별도 임시 폴더에 준비합니다. 이 예제의 확인 도구는 47이며 바이너리는 저장소에 포함하지 않습니다. 저장소 루트에서 아래와 같이 실행하며 -O는 허용하지 않습니다.

```powershell
$py = 'C:/path/to/python.exe'
& $py -B '하드웨어코딩_hardware-coding/언어확장_language-expansion/03-아날로그회로_spice/check_rc.py' --ngspice 'C:/path/to/Spice64/bin/ngspice_con.exe' --build-dir 'tmp/rc-spice-example'
```

검사기는 원본 netlist를 바이트 그대로 빌드 폴더에 복사하고 ngspice -b -n rc_lowpass.cir를 실행합니다. 60초 실행 상한과 실제 완료 문구를 확인한 뒤 표를 읽습니다. 도구가 없으면 실패하며 Python 해석값만으로 PASS를 만들지 않습니다. 성공 시 실제 결과는 다음과 같습니다.

```text
PASS RC transient_rows=6040 ac_rows=41 transient_error_V=2.998e-08 ac_complex_error=2.289e-16
```

## 전체 소스와 줄별 메모

### rc_lowpass.cir

```spice
RC low-pass: original transient and AC example
* Vin: 0V에서 1V로, 1ms 뒤 1us 동안 선형 상승하는 이상 전압원
Vin in 0 DC 0 AC 1 PULSE(0 1 1m 1u 1u 20m 40m)
* R1: 입력과 출력 사이 1000ohm 저항
R1 in out 1k
* C1: 출력에서 기준 노드 0으로 연결한 1uF 커패시터
C1 out 0 1u
* 소신호 상대 오차와 전압 절대 허용치를 지정
.options reltol=1e-7 vntol=1e-10 abstol=1e-12
* ngspice 제어 명령 구간 시작
.control
* 배치 종료 때 대화형 질문 생략
set noaskquit
* 표를 주파수 또는 시간 한 열과 데이터 열들로 출력
set wr_singlescale
* 첫 행에 열 이름도 기록
set wr_vecnames
* 파일 출력의 십진 유효 자릿수 확보
set numdgt=15
* 0부터 6ms까지, 저장 간격 10us와 내부 최대 간격 1us로 과도 해석
tran 10u 6m 0 1u
* 실제 계산된 시간·입력 전압·출력 전압 저장
wrdata transient.dat v(in) v(out)
* 차단 주파수의 0.01배부터 100배까지 decade당 10개 간격으로 AC 해석
ac dec 10 1.59154943091895 15915.4943091895
* 복소 출력 전압의 실수부 선택
let out_re = real(v(out))
* 복소 출력 전압의 허수부 선택
let out_im = imag(v(out))
* 주파수·실수부·허수부를 독립 비교용 파일로 저장
wrdata ac.dat out_re out_im
* 두 해석과 표 출력까지 도달한 완료 표시
echo PASS ngspice RC analyses complete
* 배치 시뮬레이터 정상 종료
quit
* 제어 명령 구간 끝
.endc
* 회로 정의 끝
.end
```

### check_rc.py

```python
import argparse  # ngspice와 생성물 위치 선택
from datetime import datetime, timezone  # 실제 검증 시각 기록
import hashlib  # 원본 netlist의 바이트 식별
import json  # 측정과 오차를 기계 판독용으로 저장
import math  # 지수 응답과 복소 전달함수 기준
from pathlib import Path  # 원본과 임시 경로 분리
import shutil  # 실행 파일 검색과 동일 바이트 복사
import subprocess  # 실제 ngspice 프로세스 실행
import sys  # assert가 유지되는 실행인지 확인

def rows(path):  # ngspice가 실제로 내보낸 세 열 읽기
    result = []  # 시간 또는 주파수와 두 관측값
    for line in path.read_text(encoding="utf-8").splitlines():  # 머리글까지 순서대로 읽기
        fields = line.split()  # 공백 개수와 관계없이 열 분리
        try:  # 열 이름이 있는 첫 행만 숫자로 바뀌지 않음
            values = [float(value) for value in fields]  # 실제 텍스트 수치를 변환
        except ValueError:  # wr_vecnames의 열 이름 처리
            continue  # 머리글은 측정값에 포함하지 않기
        if len(values) != 3 or not all(math.isfinite(value) for value in values):  # 누락·NaN·무한값 방지
            raise ValueError(f"unexpected data row: {line}")  # 잘못된 출력 형식을 통과로 세지 않기
        result.append(values)  # 정상 측정 행 보관
    if not result:  # 출력 파일만 생기고 데이터가 없는 경우
        raise ValueError(f"no numeric data: {path.name}")  # 미완료 해석 거절
    return result  # 실제 출력 행 반환

def reference_voltage(time):  # 유한 상승 시간까지 반영한 독립 RC 미분방정식 해
    tau, delay, rise = 1e-3, 1e-3, 1e-6  # RC=1ms, 입력 지연=1ms, 상승=1us
    elapsed = time - delay  # 입력 상승 시작부터의 시간
    if elapsed <= 0:  # 입력이 아직 0V인 구간
        return 0.0  # 영 초기조건의 출력도 0V
    if elapsed < rise:  # 입력이 선형으로 증가하는 구간
        return (elapsed + tau * math.expm1(-elapsed / tau)) / rise  # 램프 입력에 대한 정확한 해
    return 1.0 + (tau / rise) * math.expm1(-rise / tau) * math.exp(-(elapsed - rise) / tau)  # 상승 종료 뒤 지수 충전

def main():  # 실제 시뮬레이션 뒤 별도 해석값과 대조
    parser = argparse.ArgumentParser()  # 명령줄 인자 구성
    parser.add_argument("--ngspice", default="ngspice")  # 실행 파일 경로 또는 PATH 이름
    parser.add_argument("--build-dir", type=Path, required=True)  # 생성 데이터와 보고서의 임시 위치
    args = parser.parse_args()  # 실행 환경 읽기
    if sys.flags.optimize:  # 수치 비교가 지워지는 실행 거절
        parser.error("run without -O")  # Python 계산을 생략한 통과 기록 방지
    executable = shutil.which(args.ngspice)  # 실제 실행 가능한 도구 검색
    if not executable:  # Python 계산만 하고 SPICE 완료로 표시하지 않기
        parser.error("ngspice executable not found")  # 도구 부재를 명확한 실행 실패로 처리
    original = Path(__file__).with_name("rc_lowpass.cir")  # 함께 보관한 직접 작성 netlist
    work = args.build_dir.resolve()  # 원본 폴더와 다른 생성물 위치
    if work == original.parent.resolve():  # 게시 소스 폴더를 빌드 폴더로 쓰지 않기
        parser.error("build directory must differ from source directory")  # 원본 주변의 생성물 오염 방지
    work.mkdir(parents=True, exist_ok=True)  # 기존 자료를 지우지 않고 폴더 생성
    shutil.copyfile(original, work / original.name)  # netlist를 동일 바이트로 복사
    argv = [str(Path(executable).resolve()), "-b", "-n", original.name]  # 초기화 파일 없이 배치 해석
    process = subprocess.run(argv, cwd=work, capture_output=True, timeout=60, check=False)  # 실제 ngspice 실행
    stdout = process.stdout.decode("utf-8", errors="replace")  # 시뮬레이터 출력 기록
    stderr = process.stderr.decode("utf-8", errors="replace")  # 경고나 오류도 보존
    (work / "ngspice.stdout.txt").write_text(stdout, encoding="utf-8")  # 원래 실행 로그 저장
    (work / "ngspice.stderr.txt").write_text(stderr, encoding="utf-8")  # 오류 로그 별도 저장
    if process.returncode != 0 or "PASS ngspice RC analyses complete" not in stdout:  # 종료와 실제 완료 지점 모두 필요
        raise RuntimeError(f"ngspice failed: rc={process.returncode}\n{stdout}\n{stderr}")  # 해석 실패 전파
    transient = rows(work / "transient.dat")  # 실제 과도 해석의 출력 행
    ac = rows(work / "ac.dat")  # 실제 소신호 AC 해석의 출력 행
    transient_error = max(abs(voltage - reference_voltage(time)) for time, _, voltage in transient)  # 모든 시간 행을 정확해와 비교
    ac_error = max(abs(complex(real, imag) - 1 / complex(1, 2 * math.pi * frequency * 1e-3)) for frequency, real, imag in ac)  # 모든 주파수에서 H(jw) 비교
    assert transient_error < 1e-5, transient_error  # 수치적 시간 적분의 절대 전압 오차 한도
    assert ac_error < 1e-10, ac_error  # 이상 선형 회로의 복소 전달함수 오차 한도
    assert len(ac) == 41 and transient[0][0] == 0 and abs(transient[-1][0] - 0.006) < 1e-12  # 해석 범위가 실제로 완료됨
    measurements = []  # 문서에서 추적할 대표 시점과 주파수
    for target in (0.001, 0.001001, 0.002, 0.003, 0.006):  # 상승 시작·종료와 충전 경과
        time, vin, voltage = min(transient, key=lambda row: abs(row[0] - target))  # 가장 가까운 실제 계산 행
        expected = reference_voltage(time)  # 선택된 실제 시각의 해석값
        measurements.append({"kind": "transient", "time_s": time, "input_V": vin, "simulated_V": voltage, "analytic_V": expected, "absolute_error_V": abs(voltage - expected)})  # 목표 시각으로 위장하지 않기
    for index in (10, 20, 30):  # 차단 주파수의 0.1배·1배·10배
        frequency, real, imag = ac[index]  # 실제 주파수와 복소 출력
        actual = complex(real, imag)  # 1V AC 입력에서의 전달함수
        expected = 1 / complex(1, 2 * math.pi * frequency * 1e-3)  # 독립 임피던스 해
        measurements.append({"kind": "ac", "frequency_Hz": frequency, "simulated_real": real, "simulated_imag": imag, "magnitude": abs(actual), "phase_deg": math.degrees(math.atan2(imag, real)), "analytic_real": expected.real, "analytic_imag": expected.imag, "complex_error": abs(actual - expected)})  # 크기·위상도 같은 수치에서 계산
    report = {"checked_at": datetime.now(timezone.utc).isoformat(), "status": "passed_actual_ngspice_and_analytic_comparison", "source_sha256": hashlib.sha256(original.read_bytes()).hexdigest(), "command": argv, "cwd": str(work), "returncode": process.returncode, "stdout": stdout, "stderr": stderr, "transient_rows": len(transient), "ac_rows": len(ac), "maximum_transient_absolute_error_V": transient_error, "maximum_ac_complex_error": ac_error, "thresholds": {"transient_absolute_V": 1e-5, "ac_complex": 1e-10}, "measurements": measurements}  # 실물 측정과 구분하는 수치 해석 기록
    (work / "comparison.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")  # 생성물은 실행 폴더에만 저장
    print(f"PASS RC transient_rows={len(transient)} ac_rows={len(ac)} transient_error_V={transient_error:.3e} ac_complex_error={ac_error:.3e}")  # 실제 비교 결과 출력

if __name__ == "__main__":  # import만으로 시뮬레이터를 실행하지 않기
    main()  # 명시 실행에서만 배치 해석과 대조 시작
```

## 출처와 라이선스

- [ngspice 다운로드](https://ngspice.sourceforge.io/download.html)·[버전47 배포 폴더](https://sourceforge.net/projects/ngspice/files/ng-spice-rework/47/)는 실행한 도구의 출처입니다. 다운로드 archive의 SHA도 example.json에 기록합니다.
- [공식 문서](https://ngspice.sourceforge.io/docs.html)·[control-language tutorial](https://ngspice.sourceforge.io/ngspice-control-language-tutorial.html)은 소자·해석·데이터 출력 문법의 근거입니다. 이 netlist는 공식 예제를 복사한 것이 아닙니다.
- [ngspice 개발 안내의 라이선스 설명](https://ngspice.sourceforge.io/devel.html)은 주된 코드를 modified BSD로 설명하며 예외가 있다고 명시합니다. 배포본 COPYING도 KLU·OSDI 등의 별도 라이선스를 구분하므로 프로그램 전체를 단일 BSD 코드라고 요약하지 않습니다. 바이너리·매뉴얼 전문은 이 폴더에 재배포하지 않습니다.
- [MIT의 The Art of Insight](https://ocw.mit.edu/courses/res-6-011-the-art-of-insight-in-science-and-engineering-mastering-complexity-fall-2014/3bca850386a3005c22134fa62fb3bad5_MITRES_6-011F14_art_insfin.pdf)는 RC 전달함수의 근거이며 도서의 CC BY-NC-SA 4.0과 자체 netlist·로컬 결과를 구분합니다. 원문·그림을 복제하지 않았습니다.

공식 자료 열람과 로컬 실행 기준일은 2026-10-26입니다.
