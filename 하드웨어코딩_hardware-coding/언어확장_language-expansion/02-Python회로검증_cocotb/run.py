import argparse  # 도구와 빌드 위치 선택
import logging  # 실제 컴파일·VVP 명령을 실행 로그에 표시
import os  # Icarus 실행 경로와 Python 환경 연결
from pathlib import Path  # 원본과 임시 경로 구분
import shutil  # 원본을 바이트 그대로 복사
import sys  # 시뮬레이터의 Python 모듈 검색 경로
import xml.etree.ElementTree as ET  # cocotb의 실제 테스트 결과 확인
from cocotb_tools.runner import get_runner  # 고정 버전의 공식 Python 실행기

def main():  # 두 회로의 실제 Icarus 연동 실행
    parser = argparse.ArgumentParser()  # 명령줄 인자 구성
    parser.add_argument("--build-dir", type=Path, required=True)  # 생성물은 명시한 임시 폴더로 한정
    parser.add_argument("--iverilog-bin", type=Path)  # PATH에 없는 Icarus 설치도 선택
    parser.add_argument("--drop-on-stall", action="store_true")  # 음성 대조에서만 기존 DUT의 의도한 결함 선택
    args = parser.parse_args()  # 사용자 입력 읽기
    if sys.flags.optimize:  # assert가 지워진 Python 실행 거절
        parser.error("run without -O")  # 검사 생략을 통과로 기록하지 않기
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")  # 실제 도구 명령을 보존할 로거
    if args.iverilog_bin:  # 두 실행 파일을 같은 설치에서 찾기
        os.environ["PATH"] = str(args.iverilog_bin.resolve()) + os.pathsep + os.environ["PATH"]  # 도구 경로 우선
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"  # 게시 소스에 캐시를 만들지 않기
    os.environ.pop("PYTHONOPTIMIZE", None)  # 내장 Python에서도 assert 유지
    source = Path(__file__).resolve().parent  # 이 예제의 소스 폴더
    base = args.build_dir.resolve()  # 기존 파일을 지우지 않는 생성물 위치
    base.mkdir(parents=True, exist_ok=True)  # 빌드 부모 폴더 준비
    for name, rtl, top, test in [("counter", "counter.sv", "mod10_counter", "test_counter"), ("buffer", "elastic_buffer.sv", "elastic_buffer", "test_buffer")]:  # DUT별 독립 빌드
        work = base / name  # 두 회로의 결과 충돌 방지
        work.mkdir(exist_ok=True)  # 해당 작업 공간 준비
        for filename in (rtl, test + ".py"):  # 필요한 RTL과 테스트만 복사
            shutil.copyfile(source / filename, work / filename)  # 개행·인코딩을 바꾸지 않는 복사
        sys.path.insert(0, str(work))  # 시뮬레이터 안에서 테스트 모듈 찾기
        runner = get_runner("icarus")  # 실제 Icarus/VPI 실행기 선택
        parameters = {"BUG_DROP_ON_STALL": 1} if name == "buffer" and args.drop_on_stall else {}  # 정상 DUT와 명시한 결함 대조 분리
        runner.build(sources=[work / rtl], hdl_toplevel=top, build_dir=work, always=True, build_args=["-g2012"], parameters=parameters)  # SystemVerilog 회로 컴파일
        results = runner.test(hdl_toplevel=top, test_module=test, build_dir=work, test_dir=work, results_xml="results.xml", seed=20261026)  # 고정 시드의 내장 Python 테스트
        root = ET.parse(results).getroot()  # 종료 코드 외에 실제 테스트 행 확인
        cases = list(root.iter("testcase"))  # 완료한 cocotb 테스트 목록
        assert len(cases) == 1 and not any(list(root.iter(tag)) for tag in ("failure", "error", "skipped")), name  # 실패·오류·건너뜀 없는 한 테스트 완료
        print(f"PASS integration dut={name} tests={len(cases)}")  # 회로별 통합 완료 표시

if __name__ == "__main__":  # import로 빌드를 시작하지 않기
    main()  # 명시적으로 실행한 경우만 도구 호출
