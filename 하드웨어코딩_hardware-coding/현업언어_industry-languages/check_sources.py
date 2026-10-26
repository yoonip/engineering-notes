"""현재 소스·문서와 저장된 실행 기록을 대조합니다. 언어 도구는 재실행하지 않습니다."""  # 정적 검사 범위
import argparse  # 보고서 출력 경로
from datetime import datetime, timezone  # 대조한 시각
import hashlib  # 원본 바이트 비교
import json  # 예제 목록과 기록
from pathlib import Path  # 경로 확인
import re  # Markdown 코드와 링크 구분
from urllib.parse import unquote  # 인코딩된 파일 경로

ROOT = Path(__file__).resolve().parent  # 이 자료 묶음

def require(ok, reason):  # 최적화 옵션과 무관한 검사
    if not ok: raise ValueError(reason)  # 불일치를 성공으로 덮지 않기

def within(parent, name):  # 소스 목록의 범위 제한
    target = (parent / name).resolve()  # 실제 경로
    require(target.is_relative_to(parent.resolve()), f'outside directory: {name}')  # 외부 경로 금지
    return target  # 확인한 파일만 사용

def check(root):  # 저장된 결과와 현재 게시 자료 대조
    catalog = json.loads((root / 'catalog.json').read_text(encoding='utf-8'))  # 본문이 있는 예제 목록
    names = [row['directory'] for row in catalog['examples']]  # 폴더 이름
    actual = {p.name for p in root.iterdir() if p.is_dir() and re.match(r'^\d{2}-', p.name)}  # 메타데이터가 없는 번호 폴더도 포함
    recorded = {p.parent.name for p in root.glob('*/example.json')}  # 실제 결과 파일
    require(names and len(names) == len(set(names)) and set(names) == actual == recorded, 'catalog or metadata directory mismatch')  # 누락·중복 확인
    entries = []  # 현재 대조의 결과
    for entry in catalog['examples']:  # 기록이 연결된 예제만 확인
        directory = within(root, entry['directory'])  # 예제 폴더
        metadata = json.loads((directory / 'example.json').read_text(encoding='utf-8'))  # 실제 실행 기록
        hashes = metadata['source_sha256']  # 실행한 소스의 해시
        require(hashes and set(hashes) == set(metadata['sources']) and hashes == entry['source_sha256'], f'source catalog mismatch: {directory.name}')  # 카탈로그와 소스 목록 연결
        body = (directory / 'README.md').read_text(encoding='utf-8')  # 전체 소스를 실은 문서
        fences = re.findall(r'^```[^\n]*\n(.*?)^```[ \t]*$', body, flags=re.M | re.S)  # 코드 블록만 선택
        for name, expected in hashes.items():  # 원본과 검사 소스 모두 확인
            source = within(directory, name)  # 예제 밖 파일 참조 방지
            raw = source.read_bytes()  # 해시에는 개행 변환하지 않기
            require(hashlib.sha256(raw).hexdigest() == expected, f'changed source: {source}')  # 실행 당시 바이트인지 확인
            text = raw.decode('utf-8').replace('\r\n', '\n').strip()  # 표시할 때의 개행만 통일
            require(any(text == block.replace('\r\n', '\n').strip() for block in fences), f'embedded source mismatch: {source}')  # README에 실은 전체 코드 확인
        marker = metadata['expected_marker']  # 실제 완료 출력
        require(marker.startswith('PASS ') and '\n' not in marker and marker == entry['expected_marker'], f'invalid marker: {directory.name}')  # 한 줄의 같은 마커인지 확인
        require(metadata['returncode'] == 0 and any(line.startswith(marker) for line in metadata['stdout'].splitlines()), f'stored result mismatch: {directory.name}')  # 저장된 정상 결과의 종료·완료 줄
        entries.append(dict(directory=directory.name, source_files=len(hashes), source_bytes='match', embedded_sources='match', stored_result='consistent'))  # 도구 재실행과 다른 정적 결과
    broken = []  # 없는 파일의 문서 위치
    links = 0  # 실제 검사한 로컬 파일 연결 수
    for document in root.rglob('*.md'):  # 이 자료 묶음의 문서
        text = re.sub(r'^```.*?^```[^\n]*$', '', document.read_text(encoding='utf-8'), flags=re.M | re.S)  # 코드 안의 괄호 제외
        for match in re.finditer(r'!?\[[^\]\n]*\]\(([^)\n]+)\)', text):  # 일반 Markdown 연결
            target = match.group(1).strip().strip('<>')  # 꺾쇠 파일 링크 처리
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target) or target.startswith('#'): continue  # 웹 주소·제목만의 연결은 별도 대상
            filename = unquote(target.split('#', 1)[0])  # 로컬 파일 경로만 확인
            if filename:  # 파일이 있는 연결
                links += 1  # 실제 대조 수
                if not (document.parent / filename).exists(): broken.append(dict(document=str(document.relative_to(root)), target=target))  # 실패 위치 보존
    require(not broken, f'broken local file links: {broken}')  # 없는 파일 연결은 실패
    return dict(checked_at=datetime.now(timezone.utc).isoformat(), status='passed_source_and_record_checks', tools_reexecuted=False, example_count=len(entries), source_files=sum(row['source_files'] for row in entries), local_file_links_checked=links, local_file_links='all_resolve', entries=entries)  # 이번 대조의 범위

def main():  # 명령행 실행
    parser = argparse.ArgumentParser(description=__doc__)  # 정적 검사임을 안내
    parser.add_argument('--report', type=Path, required=True)  # 결과 경로
    args = parser.parse_args()  # 경로 읽기
    report = check(ROOT)  # 파일과 저장된 출력만 대조
    args.report.parent.mkdir(parents=True, exist_ok=True)  # 보고서 부모 폴더
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')  # 이번 결과 저장
    print(json.dumps({key: report[key] for key in ('status', 'tools_reexecuted', 'example_count', 'source_files', 'local_file_links')}))  # 간단한 결과
    return 0  # 모든 조건을 만족한 경우만 성공

if __name__ == '__main__': raise SystemExit(main())  # import만으로 파일을 쓰지 않기
