"""Compile the 12 native examples and run one fixture for each of 18 programs."""
import argparse
import ast
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parent


def executable(value):
    resolved = shutil.which(value)
    if resolved:
        return resolved
    path = Path(value)
    if path.is_file():
        return str(path.resolve())
    raise RuntimeError('Required compiler was not found: ' + Path(value).name)


def compare_output(actual, expected):
    return actual.split() == expected.split()


def verify(cc, cxx):
    cc, cxx = executable(cc), executable(cxx)
    environment = dict(os.environ)
    # Compiler runtime DLLs on Windows may live alongside the compiler.
    environment['PATH'] = os.pathsep.join([str(Path(cc).parent), str(Path(cxx).parent),
                                           environment.get('PATH', '')])
    environment['PYTHONDONTWRITEBYTECODE'] = '1'
    catalog = json.loads((ROOT / 'catalog.json').read_text(encoding='utf-8'))
    versions = {}
    for label, compiler in [('c', cc), ('cpp', cxx)]:
        completed = subprocess.run([compiler, '--version'], env=environment, capture_output=True,
                                   text=True, encoding='utf-8', errors='replace', timeout=10)
        if completed.returncode != 0:
            raise RuntimeError('Could not read compiler version: ' + label)
        versions[label] = completed.stdout.splitlines()[0]
    records = []
    with tempfile.TemporaryDirectory(prefix='coding-practice-basics-') as scratch:
        temporary = Path(scratch)
        for entry in catalog:
            raw_input = (ROOT / entry['fixture_input']).read_bytes()
            expected = (ROOT / entry['fixture_output']).read_text(encoding='utf-8')
            for language in ['c', 'cpp', 'python']:
                relative = entry['sources'][language]
                source = ROOT / relative
                if language == 'python':
                    ast.parse(source.read_text(encoding='utf-8-sig'), filename=relative,
                              feature_version=(3, 8))
                    command = [sys.executable, '-B', str(source)]
                    check = 'python_syntax'
                else:
                    output = temporary / (language + '_' + entry['id'] + ('.exe' if os.name == 'nt' else ''))
                    compiler = cc if language == 'c' else cxx
                    standard = '-std=c11' if language == 'c' else '-std=c++17'
                    completed = subprocess.run([compiler, standard, '-O2', '-Wall', '-Wextra', '-Werror',
                                                str(source), '-o', str(output)], env=environment,
                                               capture_output=True, timeout=30)
                    if completed.returncode:
                        # Keep error summaries portable and free of machine paths.
                        raise RuntimeError('Compilation failed: ' + relative)
                    command = [str(output)]
                    check = 'native_compile'
                completed = subprocess.run(command, input=raw_input, env=environment,
                                           capture_output=True, timeout=10)
                actual = completed.stdout.decode('utf-8', errors='replace')
                passed = completed.returncode == 0 and compare_output(actual, expected)
                records.append({'source': relative, 'language': language,
                                'build_or_syntax': check, 'fixture': entry['fixture_input'],
                                'passed': passed, 'exit_code': completed.returncode})
    return {
        'schema_version': 1,
        'status': 'passed' if all(record['passed'] for record in records) else 'failed',
        'runtime': {'python': platform.python_version(), 'compilers': versions},
        'source_count': len(records),
        'native_builds_passed': sum(record['build_or_syntax'] == 'native_compile' for record in records),
        'python_syntax_checks_passed': sum(record['build_or_syntax'] == 'python_syntax' for record in records),
        'fixture_runs_passed': sum(record['passed'] for record in records),
        'fixture_runs_total': len(records),
        'command': 'python -B verify.py --cc gcc --cxx g++',
        'output_comparison': 'whitespace-token normalized',
        'records': records,
        'limitations': ['One valid fixture per implementation.',
                       'No maximum-input performance or memory testing.',
                       'Malformed input handling is outside the validation scope.',
                       'No online judge submission or company assessment is verified.'],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cc', default='gcc')
    parser.add_argument('--cxx', default='g++')
    parser.add_argument('--report', type=Path, help='Optional JSON output file')
    args = parser.parse_args()
    try:
        report = verify(args.cc, args.cxx)
    except (OSError, RuntimeError, SyntaxError, subprocess.TimeoutExpired) as error:
        report = {'schema_version': 1, 'status': 'failed', 'error_type': type(error).__name__,
                  'message': 'Compiler, syntax, or execution check could not complete.'}
    text = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
    if args.report:
        args.report.write_text(text, encoding='utf-8')
    print(text, end='')
    return 0 if report['status'] == 'passed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
