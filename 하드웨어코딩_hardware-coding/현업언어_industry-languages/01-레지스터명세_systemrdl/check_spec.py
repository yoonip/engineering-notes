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
