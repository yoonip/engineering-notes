"""도메인별 독립 프로세스에서 기초 모델 검사를 실행한다."""

import argparse
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
    root = Path(__file__).resolve().parent
    groups = ['math_physics', 'circuits_hardware', 'systems', 'signals_ai']
    results = []
    environment = dict(os.environ, PYTHONUTF8='1')
    for group in groups:
        command = [sys.executable, '-m', 'unittest', 'discover', '-s', str(root / group), '-p', 'test_*.py', '-v']
        if group == 'signals_ai':
            command.extend(['-t', str(root)])
        completed = subprocess.run(command, cwd=root, env=environment, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
        print(f'[{group}]')
        print(completed.stdout, end='')
        match = re.search(r'Ran (\d+) tests?', completed.stdout)
        count = int(match.group(1)) if match else 0
        results.append({'group': group, 'tests': count, 'passed': completed.returncode == 0 and count > 0})
    report = {'schema_version': 1, 'python': sys.version.split()[0],
              'scope_ko': '기초 참조 모델의 계산 검증. 실제 장치 측정과 GPU benchmark는 별도 범위다.',
              'scope_en': 'Foundational reference-model verification; physical measurements and GPU benchmarks are separate.',
              'groups': results, 'total_tests': sum(x['tests'] for x in results),
              'passed': all(x['passed'] for x in results)}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
