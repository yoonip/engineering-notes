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
