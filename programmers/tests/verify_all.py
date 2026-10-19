"""문제별 공개 검증 스크립트를 모아서 실행한다."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse
import json
import os
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]


def check(problem):
    script = ROOT / problem['test']
    start = time.perf_counter()
    process = subprocess.run(
        [sys.executable, '-X', 'utf8', '-B', str(script)],
        cwd=script.parent, capture_output=True, text=True, encoding='utf-8',
        env=dict(os.environ, PYTHONUTF8='1'), timeout=180,
    )
    return dict(
        id=problem['id'], level=problem['level'], language=problem['language'],
        script=problem['test'], passed=process.returncode == 0,
        seconds=round(time.perf_counter() - start, 4),
        output=(process.stdout + process.stderr).strip(),
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    problems = json.loads((ROOT / 'catalog.json').read_text(encoding='utf-8'))['problems']
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        records = list(pool.map(check, problems))
    report = dict(
        python=sys.version.split()[0], total=len(records),
        passed=sum(r['passed'] for r in records), records=records,
    )
    if args.report:
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for record in records:
        if not record['passed']:
            print(json.dumps(record, ensure_ascii=False))
    print(json.dumps({k: v for k, v in report.items() if k != 'records'}))
    return 0 if all(r['passed'] for r in records) else 1


if __name__ == '__main__':
    raise SystemExit(main())
