"""E8M7 MAX-EX Python 단위시험을 실제 실행하고 JSON 증거를 저장한다.

모델에 기대 결과를 다시 주입하는 도구가 아니다. 표준 unittest가 실행한
시험 수, 실패, 오류와 전체 로그를 기록하며 실패하면 종료 코드도 1이다.
--output으로 다른 위치에 저장하면 과거 실행 증거를 보존할 수 있다.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import platform
import sys
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


class RecordedResult(unittest.TextTestResult):
    """실제로 완료한 시험 이름과 상태를 JSON에서도 확인할 수 있게 한다."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.successful_test_ids: list[str] = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.successful_test_ids.append(test.id())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path,
                        default=ROOT / 'build/reports/e8m7_maxex_python_verification.json')
    args = parser.parse_args()
    source_paths = ('model/e8m7.py', 'model/e8m7_maxex.py',
                    'model/test_e8m7_maxex.py', 'tools/verify_e8m7_maxex_python.py')
    source_sha256 = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                     for name in source_paths}
    log = io.StringIO()
    started = datetime.now(timezone.utc).isoformat()
    before = time.perf_counter()
    # 이름을 지정해 로딩하므로 다른 프로젝트 시험을 실수로 섞지 않는다.
    # import 오류가 발생하면 unittest의 _FailedTest도 실제 errors에 기록된다.
    suite = unittest.defaultTestLoader.loadTestsFromName('model.test_e8m7_maxex')
    result = unittest.TextTestRunner(stream=log, verbosity=2,
                                    resultclass=RecordedResult).run(suite)
    elapsed = time.perf_counter() - before
    successful = set(result.successful_test_ids)
    roundtrip_id = ('model.test_e8m7_maxex.MaxExTests.'
                    'test_all_finite_word_roundtrips_without_float_intermediate')
    midpoint_id = ('model.test_e8m7_maxex.MaxExTests.'
                   'test_every_adjacent_finite_midpoint_ties_to_even')
    # 이 숫자는 해당 실제 시험이 성공했을 때만 포함한다. roundtrip 시험은
    # 내부 count==65,280도 assert한다. midpoint 시험의 range(0x7f7f)는
    # 양수 32,639개이며 각 반복에서 양수·음수 두 개를 실제 비교한다.
    report = {
        'passed': result.wasSuccessful() and result.testsRun > 0,
        'test_count': result.testsRun,
        'failures': len(result.failures),
        'errors': len(result.errors),
        'skipped': len(result.skipped),
        'expected_failures': len(result.expectedFailures),
        'unexpected_successes': len(result.unexpectedSuccesses),
        'wall_seconds': round(elapsed, 6),
        'started_at_utc': started,
        'python_version': platform.python_version(),
        'runner': 'stdlib unittest.TextTestRunner',
        'execution_argv': [sys.executable, str(Path(__file__).resolve()), *sys.argv[1:]],
        'finite_scalar_roundtrip_words': 65280 if roundtrip_id in successful else 0,
        'positive_negative_midpoint_checks': 2 * 0x7F7F if midpoint_id in successful else 0,
        'successful_test_ids': sorted(successful),
        'failure_details': [{'test': test.id(), 'traceback': trace}
                            for test, trace in result.failures],
        'error_details': [{'test': test.id(), 'traceback': trace}
                          for test, trace in result.errors],
        'description_ko': '정확한 Fraction 변환, MAX-EX 정렬 손실, 특수값, 폭 및 G506/G512 회귀를 실제 실행했습니다. 좁은 G16/G32에서 수학적 합 0의 상쇄가 절삭으로 깨지는 반례를 포함합니다. 모든 16lane 조합의 전수시험은 아닙니다.',
        'source_sha256': source_sha256,
        'output': log.getvalue(),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')
    print(log.getvalue(), end='')
    print(f'실제 시험 {result.testsRun}개 / 실패 {len(result.failures)} / 오류 {len(result.errors)}')
    print(f'결과 보고서: {args.output.resolve()}')
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
