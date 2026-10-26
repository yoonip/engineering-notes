"""유형별 세 언어 예제를 컴파일하고 저장한 입력·출력을 대조하는 실행 도구."""

import argparse  # 실행 환경과 확인할 장을 명령행에서 받기
import ast  # Python 코드를 실행하기 전에 구문 확인
from concurrent.futures import ThreadPoolExecutor, as_completed  # 서로 독립인 컴파일 작업만 병렬 처리
from datetime import datetime, timezone  # 확인 시각을 UTC로 기록
import hashlib  # 검사한 코드의 바이트를 구분할 SHA256 계산
import io  # 주석 토큰을 읽을 문자열 스트림 준비
import json  # 예제 규격과 결과 기록 읽고 쓰기
from pathlib import Path  # 한글 경로를 문자열 조립 없이 처리
import re  # C 계열 문자열 리터럴과 실제 주석을 구분
import shutil  # 사용 가능한 기본 컴파일러 찾기
import subprocess  # 셸 없이 컴파일러와 예제를 실행
import sys  # 현재 Python 실행 경로와 종료 상태 사용
import tempfile  # 실행 파일을 소스 폴더 밖에 저장
import time  # 각 작업의 경과 시간 기록
import tokenize  # Python 주석의 실제 줄 번호 확인

ROOT = Path(__file__).resolve().parent  # 이 파일이 있는 예제 모음 위치
LANGUAGES = ('c', 'cpp', 'python')  # 같은 입력을 확인할 세 언어
SOURCE_NAMES = {'c': 'example.c', 'cpp': 'example.cpp', 'python': 'example.py'}  # 언어별 파일 이름


def digest(data):  # 실제 검사한 바이트의 식별값 계산
    return hashlib.sha256(data).hexdigest()  # 코드 수정 뒤의 결과와 혼동하지 않기


def normalize(text):  # Windows 출력의 줄바꿈만 맞추기
    return text.replace('\r\n', '\n')  # 공백이나 마지막 줄은 지우지 않고 비교


def check_notes(source, language):  # 실행 코드의 각 줄에 설명 주석이 있는지 확인
    if language == 'python':  # 문자열 속 #을 주석으로 잘못 세지 않기
        ast.parse(source)  # 실제 Python 문법으로 먼저 확인
        comments = {t.start[0]: t.string[1:].strip() for t in tokenize.generate_tokens(io.StringIO(source).readline) if t.type == tokenize.COMMENT}  # 실제 주석만 수집
        active = [i for i, line in enumerate(source.splitlines(), 1) if line.strip() and not line.lstrip().startswith('#')]  # 빈 줄과 설명만 있는 줄 제외
    else:  # C와 C++은 문자열 리터럴을 먼저 지우고 줄 주석 확인
        comments, active = {}, []  # 줄 번호별 주석과 실행 줄을 따로 보관
        for i, line in enumerate(source.splitlines(), 1):  # 소스의 모든 줄을 순서대로 확인
            if not line.strip() or line.lstrip().startswith('//'):  # 빈 줄과 설명만 있는 줄이면
                continue  # 실행 줄 목록에 넣지 않기
            active.append(i)  # 전처리·선언·닫는 괄호도 설명 대상에 포함
            cleaned = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', '', line)  # 문자열·문자 리터럴 안의 // 제거
            if '//' in cleaned:  # 실제 줄 주석이 있으면
                comments[i] = cleaned.split('//', 1)[1].strip()  # 주석의 메모 부분만 저장
    missing = [i for i in active if not comments.get(i)]  # 설명이 없는 실행 줄 찾기
    formal = [i for i in active if re.search(r'합니다|때문입니다|됩니다|입니다', comments.get(i, ''))]  # 복습 메모 대신 격식체가 들어간 주석 확인
    if missing or formal:  # 줄별 설명 조건을 만족하지 않으면
        raise ValueError(f'주석 누락={missing}, 메모 문체 확인={formal}')  # 해당 줄을 바로 찾을 수 있게 표시
    return len(active)  # 설명을 확인한 실행 줄 수 반환


def run_process(command, stdin='', timeout=10):  # 한 번의 컴파일 또는 실행을 셸 없이 처리
    result = subprocess.run(command, input=stdin, text=True, encoding='utf-8', errors='replace', capture_output=True, timeout=timeout)  # 표준 입출력만 전달
    if result.returncode:  # 실패한 프로세스의 결과를 성공으로 넘기지 않기
        raise RuntimeError(f'exit={result.returncode}\n{result.stderr[:4000]}')  # 오류 메시지 길이는 제한
    return normalize(result.stdout)  # 실제 표준 출력 반환


def verify_one(directory, metadata, language, commands, build):  # 한 언어의 한 예제를 확인
    started = time.perf_counter()  # 이 작업만의 경과 시간 시작
    source = directory / SOURCE_NAMES[language]  # 실행할 언어의 소스 선택
    raw = source.read_bytes()  # 원본 바이트 해시를 위해 그대로 읽기
    text = raw.decode('utf-8')  # 한국어 주석을 UTF-8로 해석
    note_lines = check_notes(text, language)  # 각 실행 줄의 복습 주석 확인
    if language == 'python':  # Python은 현재 선택한 인터프리터로 실행
        command = [commands['python'], '-B', str(source)]  # 캐시 파일은 만들지 않기
        compile_command = None  # 네이티브 컴파일과 구분
    else:  # C와 C++은 먼저 실행 파일 생성
        binary = build / f'{metadata["chapter"]:02d}_{language}.exe'  # 장과 언어가 겹치지 않는 이름
        standard = '-std=c17' if language == 'c' else '-std=c++17'  # 예제의 언어 표준 선택
        compile_command = commands[language] + [standard, '-O0', '-Wall', '-Wextra', '-Werror', str(source), '-o', str(binary)]  # 경고도 수정 대상으로 확인
        run_process(compile_command, timeout=180)  # 새 실행 파일을 만들 때만 컴파일
        command = [str(binary)]  # 만들어진 실행 파일을 바로 실행
    cases = []  # 기본 예제와 경계 입력의 결과 보관
    for case in metadata['cases']:  # 저장한 모든 입력을 같은 순서로 확인
        stdout = run_process(command, case['stdin'])  # 예제 프로그램에 실제 표준 입력 전달
        expected = normalize(case['stdout'])  # 예상 출력도 줄바꿈만 정규화
        if stdout != expected:  # 다른 공백이나 값은 그대로 오류로 처리
            raise AssertionError(f'{case["name"]}: expected={expected!r}, actual={stdout!r}')  # 차이가 난 값을 표시
        cases.append({'name': case['name'], 'stdout': stdout, 'passed': True})  # 통과한 입력만 기록
    return {'chapter': metadata['chapter'], 'language': language, 'source': source.relative_to(ROOT).as_posix(), 'source_sha256': digest(raw), 'metadata_sha256': digest((directory / 'example.json').read_bytes()), 'cases_sha256': digest(json.dumps(metadata['cases'], ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')), 'annotated_lines': note_lines, 'native_compilation': language != 'python', 'cases': cases, 'seconds': round(time.perf_counter() - started, 4), 'passed': True}  # 검사 범위와 결과 반환


def main():  # 경로·컴파일러·확인 범위를 준비해 검사 시작
    parser = argparse.ArgumentParser(description=__doc__)  # 사용법과 선택 항목 제공
    parser.add_argument('--zig')  # 한 실행 파일로 C와 C++을 빌드할 때의 경로
    parser.add_argument('--cc')  # 별도 C 컴파일러 경로
    parser.add_argument('--cxx')  # 별도 C++ 컴파일러 경로
    parser.add_argument('--python', default=sys.executable)  # 기본은 이 도구를 실행한 Python
    parser.add_argument('--chapters', nargs='*', type=int)  # 일부 장만 재확인할 때 사용
    parser.add_argument('--languages', nargs='+', choices=LANGUAGES, default=LANGUAGES)  # 수정한 언어만 다시 확인할 때 선택
    parser.add_argument('--jobs', type=int, default=2)  # 동시에 실행할 컴파일 작업 수
    parser.add_argument('--build-dir')  # 실행 파일 저장 위치를 직접 정할 때 사용
    parser.add_argument('--report', required=True)  # 결과 JSON을 저장할 위치
    args = parser.parse_args()  # 명령행 인자 해석
    if args.zig:  # Zig 경로가 있으면 두 언어의 드라이버를 함께 구성
        commands = {'c': [args.zig, 'cc'], 'cpp': [args.zig, 'c++'], 'python': args.python}  # 셸 문자열 대신 인자 리스트 사용
    else:  # 일반적인 C·C++ 컴파일러를 각각 찾기
        cc = args.cc or shutil.which('cc') or shutil.which('gcc') or shutil.which('clang')  # C 컴파일러 선택
        cxx = args.cxx or shutil.which('c++') or shutil.which('g++') or shutil.which('clang++')  # C++ 컴파일러 선택
        if ('c' in args.languages and not cc) or ('cpp' in args.languages and not cxx):  # 선택한 언어의 컴파일러가 없으면
            parser.error('--zig 또는 --cc와 --cxx로 컴파일러를 지정해야 합니다.')  # 실행 환경을 분명하게 안내
        commands = {'c': [cc], 'cpp': [cxx], 'python': args.python}  # 선택한 실행 경로 보관
    build = Path(args.build_dir).resolve() if args.build_dir else Path(tempfile.mkdtemp(prefix='algorithm-examples-'))  # 소스와 분리된 빌드 위치
    build.mkdir(parents=True, exist_ok=True)  # 실행 파일을 저장할 폴더 준비
    entries = []  # 검사할 예제와 규격을 함께 보관
    for file in sorted(ROOT.glob('*/example.json')):  # 각 유형 폴더의 실행 규격 찾기
        metadata = json.loads(file.read_text(encoding='utf-8'))  # JSON을 실제 값으로 읽기
        if args.chapters and metadata['chapter'] not in args.chapters:  # 선택하지 않은 장이면
            continue  # 이번 실행에서는 제외
        if len(metadata['trace']) < 4 or len(metadata['language_differences']) < 3 or len(metadata['cases']) < 3:  # 문서·경계 입력의 최소 구성 확인
            raise ValueError(f'{file}: 실행 흐름·차이·입력 사례가 부족함')  # 누락한 예제의 위치 표시
        if not any(c['stdin'] == metadata['input'] and c['stdout'] == metadata['expected_stdout'] for c in metadata['cases']):  # 대표 입력도 검사에 포함되어야 함
            raise ValueError(f'{file}: 대표 입력이 검사 목록에 없음')  # 설명과 실행 검사가 갈라지지 않게 막기
        entries.append((file.parent, metadata))  # 세 언어가 공유할 입력 규격 추가
    if not entries:  # 잘못된 선택으로 아무 예제도 검사하지 않는 상황 방지
        raise ValueError('검사할 예제가 없음')  # 빈 실행을 통과로 표시하지 않기
    found = {metadata['chapter'] for _, metadata in entries}  # 실제로 찾은 장 번호 모으기
    if args.chapters and found != set(args.chapters):  # 요청한 장 중 파일이 없는 장도 확인
        raise ValueError(f'예제가 없는 장: {sorted(set(args.chapters) - found)}')  # 일부만 실행하고 전체 요청을 통과로 표시하지 않기
    results, failures = [], []  # 성공과 실패를 분리해서 보관
    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:  # 독립 예제끼리만 병렬 처리
        tasks = {pool.submit(verify_one, directory, metadata, language, commands, build): (metadata['chapter'], language) for directory, metadata in entries for language in args.languages}  # 선택한 장과 언어의 작업 생성
        for future in as_completed(tasks):  # 완료된 작업부터 결과 기록
            chapter, language = tasks[future]  # 어느 예제의 결과인지 확인
            try:  # 한 예제의 실패로 나머지 결과를 잃지 않기
                result = future.result()  # 컴파일·실행이 끝난 결과 받기
                results.append(result)  # 성공 기록 보관
                print(json.dumps({'chapter': chapter, 'language': language, 'cases': len(result['cases']), 'passed': True}), flush=True)  # 긴 실행에서도 진행 상태 표시
            except Exception as error:  # 실제 실패 원인을 그대로 기록
                failures.append({'chapter': chapter, 'language': language, 'error': str(error)})  # 실패를 통과 수에 넣지 않기
                print(json.dumps({'chapter': chapter, 'language': language, 'error': str(error)}, ensure_ascii=True), flush=True)  # 콘솔 문자 인코딩에 의존하지 않기
    report = {'checked_at': datetime.now(timezone.utc).isoformat(), 'scope': 'Local standalone teaching examples only; no online grading', 'standards': {'c': 'C17', 'cpp': 'C++17', 'python': sys.version.split()[0]}, 'selected_chapters': sorted(m['chapter'] for _, m in entries), 'selected_languages': list(args.languages), 'programs_passed': len(results), 'case_executions_passed': sum(len(r['cases']) for r in results), 'results': sorted(results, key=lambda r: (r['chapter'], r['language'])), 'failures': failures, 'passed': not failures}  # 실제 실행한 범위만 집계
    target = Path(args.report).resolve()  # 결과 파일의 절대 위치 정하기
    target.parent.mkdir(parents=True, exist_ok=True)  # 결과 저장 폴더 준비
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')  # UTF-8 JSON으로 보관
    print(json.dumps({'programs_passed': len(results), 'case_executions_passed': report['case_executions_passed'], 'failures': len(failures), 'passed': report['passed']}), flush=True)  # 마지막 합계 출력
    return 0 if report['passed'] else 1  # 실패가 있으면 실행 상태에도 반영


if __name__ == '__main__':  # 가져오기 때는 검사하지 않고 직접 실행할 때만 시작
    raise SystemExit(main())  # 검사 결과를 프로세스 종료 상태로 전달
