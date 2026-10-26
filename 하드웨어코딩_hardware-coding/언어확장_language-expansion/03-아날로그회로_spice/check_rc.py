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
