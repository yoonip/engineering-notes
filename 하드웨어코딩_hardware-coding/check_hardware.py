#!/usr/bin/env python3
"""저장된 소스 해시와 로컬 디지털 시뮬레이션을 다시 확인합니다.

Python 3.10 이상, Icarus Verilog/VVP, GHDL 및 Amaranth 0.5.8이 필요합니다.
Amaranth는 현재 Python에 설치하거나 --python-deps의 임시 설치 경로로 제공합니다.
도구 설치나 온라인 채점은 수행하지 않으며, 누락된 도구도 실패로 기록합니다.
"""

import argparse  # 실행 파일과 출력 위치 선택
import hashlib  # 원본과 임시 복사본의 바이트 대조
import json  # 각 예제의 실행 설정 읽기
import os  # 하위 프로세스의 환경 구성
from pathlib import Path  # 운영체제별 경로 처리
import re  # PASS 집계와 FATAL 원인 구분
import shutil  # 실행 파일 검색과 바이트 복사
import subprocess  # 실제 컴파일러와 시뮬레이터 실행
import sys  # 현재 Python으로 Amaranth 실행
import tempfile  # 기존 폴더를 덮지 않는 작업 공간 생성
from datetime import datetime, timezone  # 이번 실행 시각 기록


ROOT = Path(__file__).resolve().parent  # 이 파일이 있는 하드웨어 자료의 루트
PASS_LINE = re.compile(r"(?:^|:\s+)PASS(?:\s|$)", re.MULTILINE)  # SV 완료 행과 GHDL의 report 접두사 허용


def digest(data):  # 파일이나 출력의 정확한 바이트 해시
    return hashlib.sha256(data).hexdigest()  # 정규화 전 원본으로 계산


def contained(base, relative):  # 메타데이터 경로가 해당 예제 밖으로 나가지 않게 제한
    candidate = (base / relative).resolve()  # 상대 경로와 심볼릭 링크 해석
    if not candidate.is_relative_to(base.resolve()):
        raise ValueError(f"source path escapes example: {relative}")  # 외부 파일 복사 금지
    return candidate  # 확인한 절대 경로 반환


def command(argv, cwd, timeout, env=None):  # 셸 없이 고정 인자 목록 실행
    record = {"argv": [str(x) for x in argv], "cwd": str(cwd)}  # 재현 명령 보관
    try:
        process = subprocess.run(record["argv"], cwd=cwd, env=env,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 timeout=timeout, check=False)  # 프로세스별 대기 상한
        record.update(returncode=process.returncode,
                      stdout=process.stdout.decode("utf-8", errors="replace"),
                      stderr=process.stderr.decode("utf-8", errors="replace"),
                      stdout_sha256=digest(process.stdout))  # 출력 바이트의 해시도 보관
    except subprocess.TimeoutExpired as error:
        record.update(returncode=None, timed_out=True,
                      stdout=(error.stdout or b"").decode("utf-8", errors="replace"),
                      stderr=(error.stderr or b"").decode("utf-8", errors="replace"))  # 멈춤을 성공으로 세지 않기
    except OSError as error:
        record.update(returncode=None, error=str(error), stdout="", stderr="")  # 실행 파일 오류 별도 기록
    return record  # 호출자가 단계별 성공 조건 판정


def executable(value, default):  # 명시 경로를 우선하고 없으면 PATH 검색
    value = value or default  # 도구별 기본 이름
    found = shutil.which(value)  # 확장자를 포함한 Windows 검색도 지원
    return str(Path(found).resolve()) if found else None  # 도구 부재를 숨기지 않기


def metric_values(stdout):  # 테스트벤치가 실제 출력한 집계 해석
    lines = [line for line in stdout.splitlines() if PASS_LINE.search(line)]  # 완료 행만 사용
    if len(lines) != 1:
        return None  # 없거나 중복된 PASS는 모호한 기록
    return {key: int(value) for key, value in re.findall(r"([A-Za-z_]+)=(\d+)", lines[0])}  # 정수 계수


def passed_simulation(result, marker, expected_checks=None):  # 종료와 실제 완료 출력을 함께 확인
    output = result.get("stdout", "")  # 시뮬레이터의 표준 출력
    if result.get("returncode") != 0 or not PASS_LINE.search(output):
        return False  # 비정상 종료나 미완료를 거절
    if marker and marker not in output:
        return False  # 예제 고유 완료 문구 대조
    actual = metric_values(output)  # 검사 수를 원래 기록과 비교
    return actual is not None and all(actual.get(k) == v for k, v in (expected_checks or {}).items())


def failure_marker(setting):  # 회로의 예상 불일치 원인만 음성 대조로 허용
    if setting.get("failure_marker"):
        return setting["failure_marker"]  # 새 메타데이터가 명시한 원인
    prior = setting.get("simulation", {}).get("stdout", "")  # 기존 실제 FATAL 출력
    match = re.search(r"^FATAL:\s+[^\n]*?:\d+:\s*(.+)$", prior, re.MULTILINE)  # 파일 위치를 뺀 진단
    return match.group(1).strip() if match else None  # 근거가 없으면 예상 실패로 판정하지 않기


def stage_sources(directory, metadata, work):  # 원본을 고치지 않고 복사본만 컴파일
    hashes = metadata.get("source_sha256", {})  # 원래 기록의 바이트 해시
    sources = metadata.get("sources") or (metadata.get("design_files", []) + metadata.get("testbench_files", []))
    if not hashes or not sources or set(sources) != set(hashes):
        raise ValueError("sources and source_sha256 must describe exactly the same nonempty file set")
    checked = {}  # 읽은 원본과 임시 복사본의 대조 결과
    for name in sources:
        source = contained(directory, name)  # 예제 내부 소스만 허용
        data = source.read_bytes()  # 개행까지 그대로 읽기
        observed = digest(data)  # 현재 게시 소스의 실제 해시
        if observed.lower() != str(hashes[name]).lower():
            raise ValueError(f"source SHA-256 mismatch: {name}: {observed}")  # 바뀐 소스로 옛 기록 재사용 금지
        destination = contained(work, name)  # 같은 상대 경로로 임시 복사
        destination.parent.mkdir(parents=True, exist_ok=True)  # include 하위 폴더 지원
        shutil.copyfile(source, destination)  # 텍스트 재인코딩 없이 복사
        if digest(destination.read_bytes()) != observed:
            raise ValueError(f"staged copy mismatch: {name}")  # 실제 컴파일 입력도 확인
        checked[name] = observed  # 확인한 소스별 해시 보관
    return sources, checked  # 순서가 있는 컴파일 입력과 확인 결과


def sv_runs(directory, metadata, work, sources, tools, timeout):  # Icarus 설정별 독립 실행
    if not tools["iverilog"] or not tools["vvp"]:
        raise ValueError("Icarus Verilog and VVP are required; supply --iverilog and --vvp or PATH")
    top = metadata.get("top") or metadata.get("testbench_top")  # 최상위 테스트벤치 이름
    if not top or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_$]*", top):
        raise ValueError("a valid testbench top is required")  # 외부 템플릿의 이름 확인
    settings = metadata.get("runs") or metadata.get("results")  # 두 설정 목록 이름 지원
    settings = settings or [{"name": "normal", "parameters": {}, "expected": "pass"}]  # HDLBits 기본 실행
    outcomes = []  # 정상과 음성 대조를 서로 다른 행으로 기록
    for index, setting in enumerate(settings):
        run_dir = work / f"run_{index:02d}"  # 설정별 생성물 충돌 방지
        run_dir.mkdir()  # 새 작업 폴더만 생성
        for name in sources:
            target = contained(run_dir, name)  # 소스의 상대 경로 유지
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(contained(work, name), target)  # 확인한 복사본에서 다시 복사
        argv = [tools["iverilog"], "-g2012", "-gstrict-expr-width", "-Wall", "-s", top]
        for key, value in setting.get("parameters", {}).items():
            if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_$]*", key) or not isinstance(value, (int, str)):
                raise ValueError(f"invalid parameter: {key}")  # 셸은 쓰지 않지만 파라미터 형식도 제한
            argv.append(f"-P{top}.{key}={value}")  # 메타데이터의 실제 설정 적용
        argv += ["-o", "sim.vvp", *sources]  # 분석 순서와 top을 명시
        compiled = command(argv, run_dir, timeout)  # 컴파일 단계 자체를 먼저 확인
        outcome = {"name": setting.get("name", str(index)), "parameters": setting.get("parameters", {}),
                   "expected": setting.get("expected", "pass"), "compile": compiled, "status": "failed"}
        if compiled.get("returncode") == 0:
            simulated = command([tools["vvp"], "-n", "sim.vvp"], run_dir, timeout)  # 실제 시뮬레이션 실행
            outcome["simulation"] = simulated  # 실패 출력도 그대로 보관
            if outcome["expected"] == "pass":
                if passed_simulation(simulated, metadata.get("expected_marker"), setting.get("checks")):
                    outcome["status"] = "passed"  # exit0·PASS·집계가 함께 일치
            elif outcome["expected"] == "functional_failure":
                marker = failure_marker(setting)  # 알려진 DUT 불일치 원인
                outcome["expected_failure_marker"] = marker
                text = simulated.get("stdout", "") + simulated.get("stderr", "")
                if (simulated.get("returncode") not in (None, 0) and marker
                        and "FATAL:" in text and marker in text and "watchdog" not in text.lower()):
                    outcome["status"] = "expected_functional_failure"  # 도구 오류·멈춤과 구분
            else:
                outcome["error"] = "unknown expected outcome"  # 모르는 기준으로 성공을 만들지 않기
        outcomes.append(outcome)  # 설정 하나의 결과 보관
    return outcomes  # 하나라도 실패하면 상위 결과도 실패


def vhdl_runs(metadata, work, sources, tools, timeout):  # VHDL-2008 분석·전개·실행
    if not tools["ghdl"]:
        raise ValueError("GHDL is required; supply --ghdl or PATH")  # 도구 누락을 명시
    top = metadata.get("testbench_top")  # 메타데이터의 테스트벤치
    if not top:
        raise ValueError("VHDL testbench_top is required")
    commands = [[tools["ghdl"], "-a", "--std=08", *sources],
                [tools["ghdl"], "-e", "--std=08", top],
                [tools["ghdl"], "-r", "--std=08", top, "--assert-level=error"]]  # 상대 파일명으로 한글 경로 문제 회피
    outcome = {"name": "normal", "expected": "pass", "commands": [], "status": "failed"}
    for argv in commands:
        result = command(argv, work, timeout)  # 앞 단계가 성공한 경우에만 다음 단계 수행
        outcome["commands"].append(result)
        if result.get("returncode") != 0:
            return [outcome]  # 분석 실패를 시뮬레이션 성공으로 세지 않기
    verification = metadata.get("verification", {})  # 기록된 검사 수와 주기
    expected = {key: verification[key] for key in ("cycles",) if key in verification}
    if "assertions" in verification:
        expected["checks"] = verification["assertions"]  # TB의 출력 키와 연결
    if passed_simulation(outcome["commands"][-1], metadata.get("expected_marker"), expected):
        outcome["status"] = "passed"  # 종료와 완료 문구·계수 일치
    return [outcome]


def amaranth_runs(metadata, work, sources, tools, timeout, deps):  # Python 회로 모델과 RTLIL 생성
    environment = os.environ.copy()  # 사용자 환경을 기본으로 사용
    environment.pop("PYTHONOPTIMIZE", None)  # assert를 지우는 환경 옵션 제거
    environment.update(PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")  # 소스 폴더 캐시·인코딩 변화 방지
    if deps:
        environment["PYTHONPATH"] = str(deps) + os.pathsep + environment.get("PYTHONPATH", "")  # 임시 패키지 경로 우선
    version = command([sys.executable, "-B", "-c", "import amaranth; print(amaranth.__version__)"], work, timeout, environment)
    tools["amaranth"] = version  # 실제 사용한 라이브러리 버전 보관
    expected_version = metadata.get("tool", {}).get("version")
    if version.get("returncode") != 0 or (expected_version and version["stdout"].strip() != expected_version):
        raise ValueError(f"Amaranth {expected_version or 'library'} is required; install it or supply --python-deps")
    test_files = metadata.get("testbench_files", [])  # 실행할 독립 테스트벤치
    design_files = metadata.get("design_files", [])  # RTLIL을 내보낼 회로 정의
    if len(test_files) != 1 or len(design_files) != 1:
        raise ValueError("Amaranth example needs one design file and one testbench file")
    simulated = command([sys.executable, "-B", test_files[0]], work, timeout, environment)  # -O 없는 Python 실행
    verification = metadata.get("verification", {})
    expected = {"cycles": verification["cycles"], "checks": verification["assertions"]}  # 모델 TB의 집계 대조
    outcome = {"name": "normal", "expected": "pass", "simulation": simulated, "status": "failed"}
    if passed_simulation(simulated, metadata.get("expected_marker"), expected):
        outcome["status"] = "passed"  # 실제 Simulator 완료 확인
    generated = command([sys.executable, "-B", design_files[0], "--rtlil"], work, timeout, environment)  # 변환만 별도로 실행
    rtl_text = generated.get("stdout", "").replace("\r\n", "\n")  # 비교용 줄바꿈 정규화본
    rtl_sha = digest(rtl_text.encode("utf-8"))  # raw 출력 해시와 분리
    recorded_sha = metadata.get("rtl_generation", {}).get("sha256")
    rtl_pass = (generated.get("returncode") == 0 and "module \\mod10_counter" in rtl_text
                and "$dff" in rtl_text and (not recorded_sha or recorded_sha in (generated.get("stdout_sha256"), rtl_sha)))
    rtl_path = work / "generated.il"  # 생성물을 작업 폴더에만 보관
    rtl_path.write_text(rtl_text, encoding="utf-8", newline="\n")
    generation = {"name": "rtlil_generation", "expected": "generation", "generation": generated,
                  "normalized_lf_sha256": rtl_sha, "recorded_sha256": recorded_sha,
                  "artifact": str(rtl_path), "status": "passed" if rtl_pass else "failed",
                  "scope": "RTLIL generation only; no generated-RTL simulation or synthesis"}
    return [outcome, generation]  # 모델 시뮬레이션과 변환을 같은 증거로 취급하지 않기


def main():  # CLI와 전체 자료 자동 수집
    parser = argparse.ArgumentParser(description=__doc__)  # 설치 전제도 --help에 표시
    parser.add_argument("--iverilog", help="Icarus Verilog executable; default: PATH")
    parser.add_argument("--vvp", help="VVP executable; default: PATH")
    parser.add_argument("--ghdl", help="GHDL executable; default: PATH")
    parser.add_argument("--python-deps", type=Path, help="temporary pip --target directory containing Amaranth")
    parser.add_argument("--out", type=Path, default=ROOT / "validation.json", help="new execution report")
    parser.add_argument("--build-dir", type=Path, help="parent for a new unique temporary build directory")
    parser.add_argument("--timeout", type=float, default=60.0, help="seconds per compiler/simulator command")
    arguments = parser.parse_args()  # 사용자 경로와 대기 상한 읽기
    if arguments.timeout <= 0:
        parser.error("--timeout must be positive")
    if sys.flags.optimize:
        parser.error("run without -O: Python assertions must remain enabled")  # 검사를 생략하는 실행 금지
    if arguments.build_dir:
        arguments.build_dir.mkdir(parents=True, exist_ok=True)  # 기존 내용은 지우지 않기
    work_root = Path(tempfile.mkdtemp(prefix="hardware-check-", dir=arguments.build_dir)).resolve()  # 충돌 없는 새 폴더
    tools = {name: executable(getattr(arguments, name), name) for name in ("iverilog", "vvp", "ghdl")}
    report = {"schema_version": 1, "checked_at": datetime.now(timezone.utc).isoformat(),
              "root": str(ROOT), "build_directory": str(work_root), "python": sys.version,
              "scope": {"source_bytes_and_staged_copies": True, "local_digital_simulation": True,
                        "online_grading": False, "formal_proof": False, "synthesis": False,
                        "static_timing_analysis": False, "board_measurement": False},
              "tools": tools, "entries": []}  # 확인하지 않은 하드웨어 범위 구분
    for name in ("iverilog", "vvp", "ghdl"):
        if tools[name]:
            flag = "--version" if name == "ghdl" else "-V"  # 실제 실행 파일의 버전 기록
            report.setdefault("tool_versions", {})[name] = command([tools[name], flag], work_root, arguments.timeout)
    metadata_paths = sorted((ROOT / "예제_examples").glob("*/example.json"))  # 현재 보관된 예제 수집
    metadata_paths += sorted((ROOT / "HDLBits").rglob("problem.json"))  # 나중에 추가되는 문제도 자동 수집
    if not metadata_paths:
        report["error"] = "no example.json or problem.json found"  # 빈 자료를 통과로 기록하지 않기
    for index, metadata_path in enumerate(metadata_paths):
        relative = metadata_path.parent.relative_to(ROOT).as_posix()  # 저장소 안의 재현 대상
        entry = {"directory": relative, "metadata": metadata_path.relative_to(ROOT).as_posix(), "status": "failed"}
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8-sig"))  # UTF-8 BOM도 허용
            entry["id"] = metadata.get("id", metadata_path.parent.name)
            work = work_root / f"example_{index:03d}"  # 비ASCII 제목을 생성 파일명에서 제거
            work.mkdir()  # 독립 컴파일 작업 공간
            sources, checked = stage_sources(metadata_path.parent, metadata, work)  # 원본·복사본 해시 확인
            entry["source_sha256"] = checked
            language = metadata.get("language", "SystemVerilog").lower()
            if "amaranth" in language:
                entry["runs"] = amaranth_runs(metadata, work, sources, tools, arguments.timeout,
                                                arguments.python_deps.resolve() if arguments.python_deps else None)
            elif "vhdl" in language:
                entry["runs"] = vhdl_runs(metadata, work, sources, tools, arguments.timeout)
            elif "verilog" in language:
                entry["runs"] = sv_runs(metadata_path.parent, metadata, work, sources, tools, arguments.timeout)
            else:
                raise ValueError(f"unsupported language: {language}")  # 알 수 없는 언어를 조용히 건너뛰지 않기
            if entry["runs"] and all(run["status"] in ("passed", "expected_functional_failure") for run in entry["runs"]):
                entry["status"] = "passed"  # 해당 자료의 모든 설정이 기준 충족
        except (OSError, ValueError, KeyError, TypeError) as error:
            entry["error"] = str(error)  # 다른 자료도 계속 검사하고 최종 실패로 기록
        report["entries"].append(entry)
        print(f"{entry['status'].upper()}: {relative}")  # 실행 도중의 간단한 진행 표시
    runs = [run for entry in report["entries"] for run in entry.get("runs", [])]  # 세부 실행의 실제 개수
    report["summary"] = {"entries": len(report["entries"]),
                         "entries_passed": sum(entry["status"] == "passed" for entry in report["entries"]),
                         "runs": len(runs), "normal_passed": sum(run["status"] == "passed" and run["expected"] == "pass" for run in runs),
                         "negative_controls_detected": sum(run["status"] == "expected_functional_failure" for run in runs),
                         "generations_passed": sum(run["status"] == "passed" and run["expected"] == "generation" for run in runs)}
    passed = bool(metadata_paths) and all(entry["status"] == "passed" for entry in report["entries"])
    report["status"] = "passed_local_checks" if passed else "failed_local_checks"  # 온라인 정답과 분리
    output = arguments.out.resolve()  # 보고서의 실제 저장 위치
    if output.suffix.lower() != ".json" or output.name in ("example.json", "problem.json"):
        parser.error("--out must name a separate .json report, not source metadata")  # 메타데이터 덮어쓰기 방지
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(report["summary"], ensure_ascii=False))  # 정상·음성·생성 수를 각각 표시
    return 0 if passed else 1  # 자동 실행에서도 실패를 놓치지 않기


if __name__ == "__main__":  # import만으로 컴파일이나 파일 생성을 하지 않기
    raise SystemExit(main())  # 전체 검사 결과를 프로세스 종료 코드로 전달
