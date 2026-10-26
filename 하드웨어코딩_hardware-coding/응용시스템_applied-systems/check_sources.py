"""현재 소스·README·저장된 결과를 대조합니다. 계산·파서·컴파일러는 재실행하지 않습니다."""  # 정적 검사 범위
import argparse  # 보고서 경로 읽기
from datetime import datetime, timezone  # 이번 대조 시각
import hashlib  # 원본 바이트의 해시
import json  # 목록과 실행 기록 읽기
from pathlib import Path  # 폴더 안의 경로 확인
import re  # 코드 블록과 Markdown 연결 구분
from urllib.parse import unquote  # 파일 링크의 URL 인코딩 해석

ROOT = Path(__file__).resolve().parent  # 이 자료 묶음의 위치

def require(condition, reason):  # -O에서도 사라지지 않는 판정
    if not condition: raise ValueError(reason)  # 불일치를 성공으로 기록하지 않기

def within(parent, relative):  # 목록에 적힌 파일을 안전하게 해석
    target = (parent / relative).resolve()  # 실제 절대 경로
    require(target.is_relative_to(parent.resolve()), f'outside directory: {relative}')  # 상위 경로 참조 거절
    return target  # 확인한 경로만 사용

def check(root):  # 정적 자료와 저장된 실행 기록 대조
    catalog = json.loads((root / 'catalog.json').read_text(encoding='utf-8'))  # 본문이 있는 예제 목록
    examples = catalog['examples']  # 외부 프로젝트 안내는 실행 예제와 분리
    names = [entry['directory'] for entry in examples]  # 중복 확인용 이름
    require(names and len(names) == len(set(names)), 'empty or duplicate catalog')  # 빈 목록·중복 금지
    actual = {p.name for p in root.iterdir() if p.is_dir() and re.match(r'^\d{2}-', p.name)}  # 번호가 있는 예제 폴더 자체를 확인
    recorded = {p.parent.name for p in root.glob('*/example.json')}  # 실제 메타데이터가 있는 폴더
    require(set(names) == actual == recorded, 'catalog differs from example directories or metadata')  # 메타데이터와 목록이 함께 빠진 폴더도 거절
    entries = []  # 예제별 결과
    for entry in examples:  # 실제 실행 기록이 있는 항목만 대조
        directory = within(root, entry['directory'])  # 예제 폴더 확인
        record = json.loads((directory / 'example.json').read_text(encoding='utf-8'))  # 원래 결과
        hashes = record['source_sha256']  # 당시 실행 소스의 해시
        require(hashes and set(hashes) == set(record['sources']), f'source list: {directory.name}')  # 목록과 해시 누락 확인
        require(hashes == entry['source_sha256'], f'catalog hash: {directory.name}')  # 카탈로그와 실행 기록 연결
        body = (directory / 'README.md').read_text(encoding='utf-8')  # 줄 설명을 담은 문서
        fences = re.findall(r'^```[^\n]*\n(.*?)^```[ \t]*$', body, flags=re.M | re.S)  # 전체 코드 블록만 추출
        for name, expected in hashes.items():  # 코드 생성 입력과 검사 코드도 포함
            source = within(directory, name)  # 소스가 예제 바깥을 가리키지 않게 제한
            raw = source.read_bytes()  # 해시는 개행을 정규화하지 않기
            require(hashlib.sha256(raw).hexdigest() == expected, f'source bytes: {source}')  # 실행 당시와 현재 바이트 비교
            code = raw.decode('utf-8').replace('\r\n', '\n').strip()  # 표시 코드의 개행만 통일
            require(any(code == fence.replace('\r\n', '\n').strip() for fence in fences), f'embedded source: {source}')  # README 전체 코드 일치
        marker = record['expected_marker']  # 원래 정상 실행의 완료 문자열
        require(marker.startswith('PASS ') and '\n' not in marker, f'invalid marker: {directory.name}')  # 한 줄의 완료 마커인지 확인
        require(marker == entry['expected_marker'], f'catalog marker: {directory.name}')  # 다른 결과 연결 방지
        if 'results' in record:  # 정상·의도한 오류를 함께 실행한 예제
            outcomes = record['results']  # 실행 결과를 별도 상태로 유지
            normal = [r for r in outcomes if r['name'] == 'normal']  # 정상 결과 선택
            require(len(normal) == 1 and normal[0]['actual_returncode'] == 0, f'normal result: {directory.name}')  # 정상 종료 확인
            require(any(line.startswith(marker) for line in normal[0]['stdout'].splitlines()), f'normal marker: {directory.name}')  # 실제 완료 줄의 시작을 확인
            require(all(r['actual_returncode'] == r['expected_returncode'] for r in outcomes), f'negative result: {directory.name}')  # 의도한 실패를 정상 통과와 구분
            require(all(r['actual_returncode'] != 0 and any(line.startswith('FAIL ') for line in r['stderr'].splitlines()) for r in outcomes if r['name'] != 'normal'), f'negative failure: {directory.name}')  # 실제 기능 실패 줄의 근거
        else:  # 단일 검사 프로세스의 기록
            require(record['returncode'] == 0 and any(line.startswith(marker) for line in record['stdout'].splitlines()), f'execution result: {directory.name}')  # 완료 상태와 실제 출력 줄 확인
            require(not record['stderr'], f'unexpected stderr: {directory.name}')  # 기록과 다른 오류 출력 확인
        entries.append(dict(directory=directory.name, source_files=len(hashes), stored_result='consistent', source_bytes='match', embedded_sources='match'))  # 현재 정적 대조 결과
    links = 0  # 실제 대조한 로컬 파일 연결 수
    broken = []  # 실패한 문서와 대상
    for document in root.rglob('*.md'):  # 이 자료 묶음의 문서만 읽기
        text = re.sub(r'^```.*?^```[^\n]*$', '', document.read_text(encoding='utf-8'), flags=re.M | re.S)  # 코드 안의 괄호는 제외
        for match in re.finditer(r'!?\[[^\]\n]*\]\(([^)\n]+)\)', text):  # 일반 Markdown 연결
            target = match.group(1).strip().strip('<>')  # 꺾쇠 파일 링크도 해석
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target) or target.startswith('#'): continue  # 외부 주소·문서 내 제목은 별도 대상
            filename = unquote(target.split('#', 1)[0])  # URL 인코딩된 파일명 처리
            if filename:  # 파일 경로가 있는 연결만 검사
                links += 1  # 실제 검사 수
                if not (document.parent / filename).exists(): broken.append(dict(document=str(document.relative_to(root)), target=target))  # 없는 파일 기록
    require(not broken, f'broken local file links: {broken}')  # 파일 부재를 통과로 표시하지 않기
    return dict(checked_at=datetime.now(timezone.utc).isoformat(), status='passed_source_and_record_checks', tools_reexecuted=False, example_count=len(entries), source_files=sum(r['source_files'] for r in entries), local_file_links_checked=links, local_file_links='all_resolve', entries=entries)  # 현재 정적 대조 범위

def main():  # 명령행 진입점
    parser = argparse.ArgumentParser(description=__doc__)  # 새 실행과 정적 대조의 차이 안내
    parser.add_argument('--report', type=Path, required=True)  # 출력할 JSON 경로
    args = parser.parse_args()  # 사용자 인자 읽기
    report = check(ROOT)  # 소스와 문서만 대조
    args.report.parent.mkdir(parents=True, exist_ok=True)  # 보고서 부모 폴더 준비
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')  # 이번 정적 검사 결과 저장
    print(json.dumps({k: report[k] for k in ('status', 'tools_reexecuted', 'example_count', 'source_files', 'local_file_links')}))  # 간단한 결과
    return 0  # 모든 조건을 만족한 경우만 성공

if __name__ == '__main__': raise SystemExit(main())  # import만으로 파일을 쓰지 않기
