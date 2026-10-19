"""C++ 제출 구현을 컴파일해 공식 입출력 예를 실행한다."""
from pathlib import Path
import argparse
import json
import os
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def literal(value):
    if isinstance(value, list):
        return '{' + ','.join(map(literal, value)) + '}'
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=True)
    return str(value).lower()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--compiler', default=shutil.which('g++') or shutil.which('clang++') or shutil.which('zig'))
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    if not args.compiler:
        parser.error('g++, clang++, zig 중 하나의 경로를 --compiler로 지정하세요.')
    rows = json.loads((ROOT / 'tests/cpp_cases.json').read_text(encoding='utf-8'))
    records = []
    with tempfile.TemporaryDirectory(prefix='programmers-cpp-') as directory:
        build = Path(directory)
        include = build / 'include/bits'
        include.mkdir(parents=True)
        headers = 'algorithm array bitset cassert cctype climits cmath cstdint cstdio cstdlib deque functional iomanip iostream limits map memory numeric queue set sstream stack string tuple unordered_map unordered_set utility vector'
        (include / 'stdc++.h').write_text('#pragma once\n' + ''.join(f'#include <{h}>\n' for h in headers.split()), encoding='utf-8')
        for row in rows:
            source = '#include <bits/stdc++.h>\n' + (ROOT / row['source']).read_text(encoding='utf-8')
            source += '''
template<class T> void emit(const T& value){std::cout<<value;}
void emit(const std::string& value){std::cout<<std::quoted(value);}
template<class T> void emit(const std::vector<T>& value){std::cout<<"[";bool first=true;for(const auto& x:value){if(!first)std::cout<<",";first=false;emit(x);}std::cout<<"]";}
int main(){
'''
            for case in row['cases']:
                source += 'emit(solution(' + ','.join(map(literal, case['args'])) + '));std::cout<<"\\n";\n'
            source += '}\n'
            path = build / f"{row['id']}.cpp"
            path.write_text(source, encoding='utf-8')
            executable = build / (f"{row['id']}.exe" if os.name == 'nt' else str(row['id']))
            command = [args.compiler]
            if Path(args.compiler).stem == 'zig':
                command += ['c++']
                if os.name == 'nt':
                    command += ['-target', 'x86_64-windows-gnu']
            command += ['-std=c++17', '-O2', '-I', str(include.parent), str(path), '-o', str(executable)]
            subprocess.run(command, check=True, capture_output=True, timeout=180)
            process = subprocess.run([str(executable)], check=True, capture_output=True, text=True, encoding='utf-8', timeout=60)
            actual = [json.loads(line) for line in process.stdout.splitlines() if line.strip()]
            expected = [case['expected'] for case in row['cases']]
            assert actual == expected, (row['id'], actual, expected)
            records.append(dict(id=row['id'], examples=len(expected), passed=True))
    report = dict(problems=len(records), examples=sum(r['examples'] for r in records), records=records)
    if args.report:
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
