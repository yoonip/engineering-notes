import argparse  # 컴파일러·링커·생성물 위치 선택
from datetime import datetime, timezone  # 실제 실행 시각 기록
import hashlib  # 게시 소스와 컴파일 입력의 바이트 대조
import json  # 명령과 결과를 기계 판독용으로 저장
from pathlib import Path  # 원본과 임시 작업 경로 분리
import re  # 실제 테스트 수와 비교 수 판정
import shutil  # 도구 검색과 동일 바이트 복사
import subprocess  # 실제 rustc와 호스트 테스트 실행
import tempfile  # 기존 폴더를 지우지 않는 새 빌드 공간

def sha(path):  # 파일 원본의 정확한 바이트 식별
    return hashlib.sha256(path.read_bytes()).hexdigest()  # 줄바꿈을 정규화하지 않고 계산

def execute(argv, work, records):  # 셸 없이 실행하고 실패 로그도 남기기
    record = {"command": [str(value) for value in argv], "cwd": str(work)}  # 재현할 인자 목록
    records.append(record)  # 실행 실패도 보고서에서 빠지지 않기
    try:  # 도구가 멈추거나 시작하지 못한 경우 구분
        process = subprocess.run(record["command"], cwd=work, capture_output=True, timeout=60, check=False)  # 명령별 60초 상한
    except (subprocess.TimeoutExpired, OSError) as error:  # 컴파일·실행 환경 오류
        record["error"] = str(error)  # 실제 오류 보존
        raise RuntimeError(str(error)) from error  # 통과 판정 금지
    record.update(returncode=process.returncode, stdout=process.stdout.decode("utf-8", errors="replace"), stderr=process.stderr.decode("utf-8", errors="replace"))  # 출력과 종료 코드를 함께 저장
    if process.returncode != 0:  # 컴파일이나 테스트가 실패한 경우
        raise RuntimeError(f"command failed: {record['command'][0]} rc={process.returncode}")  # 다음 단계를 성공으로 세지 않기
    return record  # 성공한 단계의 실제 출력

def main():  # no_std 빌드와 표준 라이브러리 호스트 테스트 분리 실행
    parser = argparse.ArgumentParser()  # 실행 환경 인자 구성
    parser.add_argument("--rustc", default="rustc")  # 명시한 컴파일러 또는 PATH 이름
    parser.add_argument("--linker", default="auto", help="auto, default, or a linker executable path")  # 호스트 링커 정책 선택
    parser.add_argument("--out", type=Path)  # 보고서 위치를 지정하지 않으면 새 빌드 폴더 사용
    parser.add_argument("--build-dir", type=Path, required=True)  # 새 임시 작업 공간을 둘 부모 폴더
    args = parser.parse_args()  # 사용자 선택 읽기
    rustc = shutil.which(args.rustc)  # 실제 실행 가능한 컴파일러 검색
    if not rustc:  # 도구 부재를 완료로 표시하지 않기
        parser.error("rustc executable not found")  # 설치 경로 오류 알림
    rustc = str(Path(rustc).resolve())  # 작업 폴더를 바꿔도 같은 도구 사용
    source = Path(__file__).resolve().parent  # 확정된 소스의 위치
    original_hashes = {name: sha(source / name) for name in ("lib.rs", "tests.rs", "run.py")}  # 변경 전 세 파일의 식별값
    args.build_dir.mkdir(parents=True, exist_ok=True)  # 기존 파일 삭제 없이 빌드 부모 준비
    work = Path(tempfile.mkdtemp(prefix="rust-fw-", dir=args.build_dir)).resolve()  # 고유한 새 작업 폴더
    output = args.out.resolve() if args.out else work / "validation.json"  # 보고서는 명시한 위치 또는 생성물 옆에 저장
    if output.suffix.lower() != ".json" or output.name == "example.json":  # 예제 원본 메타데이터와 실행 결과 구분
        parser.error("--out must be a separate .json execution report")  # 원본 메타데이터 덮어쓰기 방지
    report = {"checked_at": datetime.now(timezone.utc).isoformat(), "status": "failed", "source_sha256": original_hashes, "build_directory": str(work), "commands": [], "scope": {"no_std_rlib_compile": True, "host_standard_library_tests": True, "mcu_execution": False, "mmio_execution": False, "cross_target_compile": False}}  # 실행 범위를 명확히 기록
    result_code = 1  # 모든 단계가 확인되기 전에는 실패가 기본
    try:  # 오류가 나도 실행 보고서를 남기는 범위
        for name in ("lib.rs", "tests.rs"):  # 확정한 Rust 소스만 임시 폴더에 복사
            shutil.copyfile(source / name, work / name)  # 원본 바이트를 그대로 사용
            if sha(work / name) != original_hashes[name]:  # 실제 컴파일 입력도 대조
                raise RuntimeError(f"staged copy mismatch: {name}")  # 손상된 복사본 거절
        version = execute([rustc, "--version", "--verbose"], work, report["commands"])  # 실제 도구 버전과 호스트 확인
        sysroot = execute([rustc, "--print", "sysroot"], work, report["commands"])["stdout"].strip()  # 배포 링커를 찾을 도구 루트
        host_match = re.search(r"^host: (\S+)$", version["stdout"], re.MULTILINE)  # 컴파일러가 대상으로 삼은 기본 호스트
        if not host_match:  # 호스트 확인이 안 된 상태로 GNU 옵션을 추측하지 않기
            raise RuntimeError("rustc verbose output has no host")  # 버전 출력 오류
        host = host_match.group(1)  # 실제 호스트 triple
        linker_options = []  # 다른 호스트에서는 기본 링커를 그대로 사용
        selected_linker = None  # 명시 또는 자동 선택된 링커
        if args.linker == "auto" and host == "x86_64-pc-windows-gnu":  # 확인한 Windows GNU의 경로 문제 우회
            selected_linker = Path(sysroot) / "lib" / "rustlib" / host / "bin" / "rust-lld.exe"  # 같은 Rust 배포에 포함된 LLD
            if not selected_linker.is_file():  # 자동 선택한 실행 파일 존재 확인
                raise RuntimeError("bundled rust-lld missing; choose --linker default or an explicit linker")  # 조용한 대체 금지
        elif args.linker not in ("auto", "default"):  # 사용자가 명시한 링커
            found = shutil.which(args.linker)  # 파일 경로 또는 PATH 검색
            if not found:  # 존재하지 않는 링커 경로
                raise RuntimeError("specified linker executable not found")  # 명확한 실패 기록
            selected_linker = Path(found).resolve()  # 작업 폴더와 무관한 절대 경로
        if selected_linker:  # 기본값 외의 링커를 선택한 경우
            linker_options += ["-C", f"linker={selected_linker}"]  # rustc가 실제로 사용할 실행 파일
            if host == "x86_64-pc-windows-gnu" and "lld" in selected_linker.stem:  # 이 호스트의 직접 LLD 호출 방식
                linker_options += ["-C", "linker-flavor=ld.lld", "-C", "link-self-contained=yes"]  # 배포본의 GNU 지원 파일과 함께 링크
        report["linker"] = {"requested": args.linker, "selected": str(selected_linker) if selected_linker else "target default", "codegen_options": linker_options}  # 다른 호스트와의 선택 차이 보관
        execute([rustc, "--edition", "2024", "--crate-name", "firmware_fields", "--crate-type", "rlib", "-D", "warnings", "lib.rs", "-o", "libfirmware_fields.rlib"], work, report["commands"])  # no_std 라이브러리 자체 컴파일
        test_binary = "tests.exe" if "windows" in host else "tests"  # 호스트의 실행 파일 이름
        execute([rustc, "--edition", "2024", "--test", "-D", "warnings", *linker_options, "tests.rs", "--extern", "firmware_fields=libfirmware_fields.rlib", "-o", test_binary], work, report["commands"])  # 표준 라이브러리 테스트 실행 파일 별도 빌드
        tested = execute([str(work / test_binary), "--test-threads=1", "--nocapture"], work, report["commands"])  # 정해진 순서로 실제 호스트 테스트 실행
        fields = re.search(r"PASS fields checks=(\d+)", tested["stdout"])  # 테스트가 실제 출력한 필드 비교 수
        frames = re.search(r"PASS frames checks=(\d+)", tested["stdout"])  # 테스트가 실제 출력한 프레임 비교 수
        if not fields or not frames or (int(fields.group(1)), int(frames.group(1))) != (21652, 10179):  # 예상 범위가 실제로 실행됨
            raise RuntimeError("expected assertion counts were not observed")  # 미완료나 축소된 실행 거절
        if not re.search(r"test result: ok\. 2 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out", tested["stdout"]):  # 두 테스트 모두 실제 완료
            raise RuntimeError("host tests did not complete with the required result")  # 종료 코드만으로 완료 추정 금지
        report["checks"] = {"fields": int(fields.group(1)), "frames": int(frames.group(1)), "total": 31831, "tests_passed": 2}  # 실제 집계
        report["artifacts_sha256"] = {name: sha(work / name) for name in ("libfirmware_fields.rlib", test_binary)}  # 이번 컴파일 산출물의 식별값
        report["status"] = "passed_no_std_compile_and_host_tests"  # MCU 동작과 구분한 완료 상태
        result_code = 0  # 필요한 단계가 모두 확인됨
    except (OSError, RuntimeError) as error:  # 도구·파일·기능 실패를 보고서에 보존
        report["error"] = str(error)  # 실패 원인을 숨기지 않기
    after_hashes = {name: sha(source / name) for name in original_hashes}  # 실행 후 게시 소스 다시 읽기
    report["source_sha256_after"] = after_hashes  # 원본 보존 대조 근거
    report["source_bytes_unchanged"] = after_hashes == original_hashes  # 실행 전후 바이트 일치
    if not report["source_bytes_unchanged"]:  # 실행 중 외부 수정까지 구분
        report["status"] = "failed_source_changed"  # 옛 소스 근거로 통과를 기록하지 않기
        result_code = 1  # 실패 종료
    output.parent.mkdir(parents=True, exist_ok=True)  # 보고서 부모 위치 준비
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")  # 실제 실행 보고서 저장
    print(f"{report['status']} fields={report.get('checks', {}).get('fields', 0)} frames={report.get('checks', {}).get('frames', 0)} source_bytes_unchanged={report['source_bytes_unchanged']}")  # 간단한 실제 결과 표시
    return result_code  # 자동 실행에서도 실패를 전달

if __name__ == "__main__":  # import만으로 도구나 파일을 실행하지 않기
    raise SystemExit(main())  # 실제 결과를 프로세스 종료 코드로 연결
