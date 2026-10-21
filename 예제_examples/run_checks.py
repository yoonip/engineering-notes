"""기초·추론·확장·심화 모델을 각각 독립 프로세스에서 검사한다."""

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    base = Path(__file__).resolve().parent
    suites = [
        ('공학기초_foundations', [sys.executable, str(base / '공학기초_foundations/run_checks.py')]),
        ('추론_reasoning', [sys.executable, '-m', 'unittest', 'discover', '-s', str(base / '추론_reasoning'), '-t', str(base), '-p', 'test_*.py', '-v']),
    ]
    suites += [(f'확장기초_extended/{group}', [sys.executable, '-m', 'unittest', 'discover', '-s', str(base / '확장기초_extended' / group), '-p', 'test_*.py', '-v'])
               for group in ('hardware', 'systems', 'ai_data')]
    suites += [(f'심화_advanced/{group}', [sys.executable, '-m', 'unittest', 'discover', '-s', str(base / '심화_advanced' / group), '-p', 'test_*.py', '-v'])
               for group in ('hardware', 'systems', 'ai_data', 'math_reasoning')]
    results = []
    for name, command in suites:
        result = subprocess.run(command, cwd=base, env=dict(os.environ, PYTHONUTF8='1'),
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                text=True, encoding='utf-8', errors='replace')
        print(f'[{name}]')
        print(result.stdout, end='')
        count = sum(map(int, re.findall(r'Ran (\d+) tests?', result.stdout)))
        results.append({'suite': name, 'tests': count, 'passed': result.returncode == 0 and count > 0})
    report = {'schema_version': 1, 'review_date': datetime.now(timezone.utc).date().isoformat(),
              'review_date_timezone': 'UTC',
              'python': sys.version.split()[0], 'suites': results,
              'total_tests': sum(row['tests'] for row in results),
              'passed': all(row['passed'] for row in results),
              'scope_ko': '계산·상태·검증 참조 모델의 자동 검사. 실제 보드·계측·EDA·GPU 실행 결과는 각 문서에서 별도로 다룬다.',
              'scope_en': 'Automated checks of computational, state and verification reference models; board, instrument, EDA and GPU execution are addressed separately in the articles.'}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
