"""현재 게시 소스·문서와 저장된 실행 기록을 대조합니다. 실행 도구는 다시 호출하지 않습니다."""  # 정적 대조의 범위
import argparse  # 보고서 경로 선택
from datetime import datetime, timezone  # 이번 대조 시각
import hashlib  # 바이트 그대로의 SHA-256
import json  # 예제 목록과 원래 실행 기록
from pathlib import Path  # 예제 안의 경로 확인
import re  # Markdown의 로컬 파일 연결 구분
import sys  # 종료 코드와 최적화 옵션 검사
ROOT = Path(__file__).resolve().parent  # 이 자료 묶음의 위치
def sha(data): return hashlib.sha256(data).hexdigest()  # 개행을 바꾸기 전 바이트 비교
def check(root):  # 호출자가 지정한 자료 묶음 대조
    catalog = json.loads((root / 'catalog.json').read_text(encoding='utf-8'))  # 실제 본문이 있는 목록
    assert catalog['examples']  # 빈 목록으로 성공을 만들지 않기
    entries = []  # 자료별 대조 결과
    for example in catalog['examples']:  # 연결된 예제만 확인
        directory = (root / example['directory']).resolve()  # 예제 디렉터리의 실제 위치
        assert directory.is_relative_to(root.resolve())  # 목록이 바깥 파일을 가리키지 않게 제한
        metadata = json.loads((directory / 'example.json').read_text(encoding='utf-8'))  # 원래 실행 기록 읽기
        recorded = metadata.get('source_sha256') or {row['file']: row['sha256'] for row in metadata['source_files']}  # 예제별 메타 형식 연결
        assert recorded == example['source_sha256']  # 목록과 실행 기록의 소스가 같은지 확인
        body = (directory / 'README.md').read_text(encoding='utf-8').replace('\r\n', '\n')  # 코드 표시에 사용할 개행만 정규화
        for name, expected in recorded.items():  # 실행에 연결된 소스·제약 예시 파일
            source = (directory / name).resolve()  # 예제 안의 파일로 해석
            assert source.is_relative_to(directory)  # 소스 목록의 외부 경로 금지
            raw = source.read_bytes()  # 해시 검사는 원본 개행으로 수행
            assert sha(raw) == expected, str(source)  # 게시 코드가 실행 당시 코드와 다르면 실패
            assert raw.decode('utf-8').replace('\r\n', '\n').strip() in body, f'code fence mismatch: {source}'  # README에 실은 전체 코드 대조
        if example['number'] == 1:  # 실제 QEMU에서 정상 실행과 의도한 명령 결함 확인
            assert metadata['returncode'] == 0 and metadata['expected_marker'] in metadata['stdout']  # 정상 CPU 실행의 완료 확인
            assert metadata['results'][1]['returncode'] == 1 and metadata['results'][1]['result'] == 'EXPECTED_FUNCTIONAL_FAILURE'  # 부호 확장 결함의 기능 실패
        elif example['number'] == 2:  # 실제 HDL 시뮬레이터와 cocotb의 결과
            normal, negative = metadata['runs']  # 정상과 결함 대조를 분리
            assert normal['returncode'] == 0 and negative['returncode'] == 1  # 프로세스 종료 상태 대조
            assert all(marker in normal['stdout'] for marker in metadata['expected']['normal_markers'])  # 카운터·버퍼 완료 확인
            assert metadata['expected']['negative_assertion'] in negative['stdout'] + negative['stderr']  # 원하는 assertion으로 실패했는지 확인
        elif example['number'] == 3:  # 실제 아날로그 계산과 독립 해석값의 비교
            result = metadata['verification']['comparison']  # ngspice 출력 자료의 비교 기록
            assert result['returncode'] == 0 and result['status'] == 'passed_actual_ngspice_and_analytic_comparison'  # 해석 완료 확인
            assert result['maximum_transient_absolute_error_V'] < metadata['expected']['maximum_transient_absolute_error_V_less_than']  # 전압 오차 한도
            assert result['maximum_ac_complex_error'] < metadata['expected']['maximum_ac_complex_error_less_than']  # 복소 전달함수 오차 한도
        elif example['number'] == 4:  # Rust 라이브러리·호스트 테스트 기록
            result = metadata['verification']  # no_std와 호스트 테스트를 나눈 명령 목록
            assert all(row['returncode'] == 0 for row in result['commands'])  # 도구 버전·컴파일·실행 모두 확인
            assert metadata['expected']['total_assertions'] == 31831 and result['source_bytes_unchanged']  # 기록한 집계와 원본 보존
        elif example['number'] == 5:  # 일반 구조 변환과 SDC 생성 기록
            assert [row['status'] for row in metadata['settings']].count('passed_generic_structure_and_sdc_generation') == 2  # 정상 주기 두 경우
            assert [row['status'] for row in metadata['settings']].count('expected_configuration_rejection') == 7  # 구성 오류 일곱 경우
            assert metadata['scope']['sta'] is False  # 실행하지 않은 타이밍 분석을 통과로 합치지 않기
            assert (directory / 'constraints.sdc').read_text(encoding='utf-8') == metadata['settings'][0]['sdc_text']  # 게시한 SDC가 실제 10ns 출력인지 대조
            dependency = (directory / metadata['dependency']['path']).resolve()  # 기존 버퍼 원본의 읽기 전용 연결
            assert dependency.is_relative_to(root.parent.resolve()) and sha(dependency.read_bytes()) == metadata['dependency']['sha256']  # 외부 예제의 원본도 같은 바이트인지 확인
        elif example['number'] == 6:  # SystemC 이벤트 커널과 검사기 대조
            assert metadata['source_copy_matches_published_source']  # 실제 컴파일 입력의 동일성
            for row in metadata['execution']['cases']:  # 느린 소비·빠른 소비·잘못된 기대값
                assert row['actual_returncode'] == row['expected_returncode'] and row['expected_stdout_matched']  # 종료 코드와 기대 출력 함께 확인
        else: raise ValueError('unsupported example number')  # 모르는 기록을 조용히 성공으로 처리하지 않기
        entries.append(dict(directory=example['directory'], source_files=len(recorded), stored_execution_record='consistent', current_source_bytes='match', embedded_sources='match'))  # 현재 대조 결과
    broken = []  # 이 자료 안에서 연결한 로컬 파일 검사
    for document in root.rglob('*.md'):  # 실제 문서만 대상으로 하기
        text = re.sub(r'```.*?```', '', document.read_text(encoding='utf-8'), flags=re.S)  # 코드 안의 괄호는 링크로 읽지 않기
        for match in re.finditer(r'!?\[[^\]\n]*\]\(([^)\n]+)\)', text):  # 현재 문서의 일반 Markdown 연결
            target = match.group(1).strip().strip('<>')  # 파일명 연결의 꺾쇠 처리
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target) or target.startswith('#'): continue  # 웹 주소와 문서 내 제목 제외
            filename = target.split('#', 1)[0]  # 파일 존재와 제목 anchor는 별도로 보기
            if filename and not (document.parent / filename).exists(): broken.append(dict(document=str(document.relative_to(root)), target=target))  # 없는 파일의 위치 기록
    assert not broken, broken  # 연결한 파일 부재를 성공으로 기록하지 않기
    return dict(checked_at=datetime.now(timezone.utc).isoformat(), status='passed_source_and_record_checks', tools_reexecuted=False, entries=entries, example_count=len(entries), source_files=sum(row['source_files'] for row in entries), local_file_links='all_resolve')  # 확인 범위가 분명한 보고서
def main():  # 단독 실행의 CLI
    parser = argparse.ArgumentParser(description=__doc__)  # 실행 검사와 정적 대조의 차이 안내
    parser.add_argument('--report', type=Path, required=True)  # 이번 결과를 남길 파일
    args = parser.parse_args()  # 경로 읽기
    if sys.flags.optimize: parser.error('run without -O: assertions must remain enabled')  # 검사를 제거하는 옵션 거절
    report = check(ROOT)  # 파일과 기록 대조
    args.report.parent.mkdir(parents=True, exist_ok=True)  # 출력 부모 준비
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')  # 현재 대조를 별도 JSON으로 기록
    print(json.dumps({key: report[key] for key in ('status', 'tools_reexecuted', 'example_count', 'source_files', 'local_file_links')}))  # 짧은 결과 출력
    return 0  # 모든 검사 통과 시 정상 종료
if __name__ == '__main__': raise SystemExit(main())  # import로는 실행하거나 파일을 쓰지 않기
