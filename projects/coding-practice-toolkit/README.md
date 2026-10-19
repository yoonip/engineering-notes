# Coding Practice Toolkit

C, C++, Python으로 같은 알고리즘을 구현하고 입력·출력을 비교하는 연습 프로젝트다. 자료구조와 탐색, 정렬, 동적 계획법 예제에 한국어 주석을 붙였고, 파일 입력과 언어별 실행 설정을 함께 정리했다. 연습 코드와 입력별 실행 결과를 함께 기록했다.

## 구성

| 경로 | 내용 |
| --- | --- |
| `samples/00_array_function` | 배열과 함수 |
| `samples/00_programmers_function` | 함수 반환형 연습 |
| `samples/01_sum` | 합과 정수 범위 |
| `samples/02_frequency` | 빈도 집계 |
| `samples/03_sort_greedy` | 정렬과 greedy |
| `samples/04_prefix_sum` | 누적합 |
| `samples/05_stack` | stack |
| `samples/06_bfs` | 격자 BFS |
| `samples/07_binary_search` | 이진 탐색 |
| `samples/08_two_pointers` | two pointers |
| `samples/09_dp_coins` | 동전 DP |
| `samples/10_backtracking` | backtracking |
| `samples/11_frequency` | 문자열 빈도 |
| `samples/12_multi_sort` | 여러 기준 정렬 |
| `samples/13_components` | 연결 요소 |
| `samples/mock1_*`, `samples/mock2_*` | 창작 종합 연습 |
| `c_functions/` | 기능개발·의상·구명보트·게임 맵의 C 함수 구현 |
| `scripts/` | 파일 입력·컴파일·실행 도구 |
| `extensions/lig-practice-runner/` | 현재 파일의 언어를 선택하는 VS Code 확장 소스 |

각 예제 폴더에는 `main_explained.c`, `main_explained.cpp`, `main_explained.py`와 `input.txt`, `expected.txt`, `tests.json`이 있다. 주석 없는 중복 사본은 제외했다. `samples/sum_explained.*`는 실행 환경 확인용이다. `c_functions`는 로컬 연습용 함수 인터페이스를 사용한다.

## 실행

Windows에서 Python 3와 GCC의 `gcc.exe`, `g++.exe`를 PATH에 둔다. VS Code의 C/C++ 디버깅에는 `gdb.exe`도 사용한다.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run.ps1 -Source .\samples\06_bfs\main_explained.py
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run.ps1 -Source .\samples\06_bfs\main_explained.c
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run.ps1 -Source .\samples\06_bfs\main_explained.cpp
```

실행기는 코드 옆의 `input.txt`를 먼저 찾고, 없으면 프로젝트 루트의 파일을 읽는다. UTF-8 BOM을 제거한 뒤 표준입력으로 전달하고, 제한 시간을 넘기면 프로세스를 종료한다. `-InputFile`로 다른 입력을 지정할 수 있다. 빌드 결과는 `build/`에 저장한다.

MinGW linker의 한글 출력 경로 문제는 임시 영문 경로에서 링크한 실행 파일을 `build/`로 옮기는 방식으로 처리했다. 기본 임시 경로는 Windows TEMP이며, `PRACTICE_BUILD_TEMP` 환경 변수로 다른 쓰기 가능한 영문 경로를 지정할 수 있다. 한글 경로의 프로젝트에서 세 언어 실행과 C 디버깅용 입력 준비를 확인했다.

## VS Code

`.vscode`에는 Python·C·C++의 파일 입력과 키보드 입력 설정이 있다. Python 및 C/C++ 디버거 확장은 별도로 설치하는 구성이다.

언어 자동 선택 확장은 기존 0.1.2 소스를 바탕으로 정리했다. 고정된 드라이브 경로를 없애고, 현재 workspace의 `scripts/run.ps1`과 `samples` 디렉터리를 확인한다. 선택한 코드의 확장자에 따라 실행 작업과 디버깅 설정을 연결한다. 확장 개발 모드로 `extensions/lig-practice-runner`를 로드해 사용하며, 컴파일된 VSIX는 포함하지 않았다.

2026-10-19에 예제의 세 언어 구현과 테스트 입력, 네 C 함수의 경계 조건, 언어 라우팅 및 실행 명령을 검사했다. VS Code 확장 API 호출은 mock으로 확인했고, PowerShell 실행기는 별도 경로에서 실제 실행했다.

## English

This project implements the same algorithms in C, C++ and Python and compares their input/output behavior. Korean comments explain data structures, searching, sorting and dynamic programming. Fixtures and execution settings keep the exercises easy to rerun.

### Contents

The `samples/` topics cover arrays/functions, function return values, sums/integer ranges, frequency counts, sorting/greedy methods, prefix sums, stacks, grid BFS, binary search, two pointers, coin DP, backtracking, string frequency, multi-key sorting and connected components. `mock1_*` and `mock2_*` combine these concepts into practice tasks. `c_functions/` contains batching, category-combination, greedy-pairing and game-map C functions. `scripts/` handles input, compilation and execution; `extensions/lig-practice-runner/` holds the VS Code language-router source.

Each example directory contains `main_explained.c`, `main_explained.cpp`, `main_explained.py`, `input.txt`, `expected.txt` and `tests.json`. Unannotated duplicate sources are omitted. `samples/sum_explained.*` checks the environment; `c_functions` uses a local exercise interface.

### Running and debugging

On Windows, put Python 3, `gcc.exe` and `g++.exe` on PATH; C/C++ debugging in VS Code also uses `gdb.exe`. The PowerShell examples above run the selected source through `scripts/run.ps1`.

The runner first looks for `input.txt` beside the source, then at the project root. It strips a UTF-8 BOM, supplies standard input and terminates processes that exceed the timeout. `-InputFile` selects another input; build artifacts go in `build/`.

To handle MinGW linking from Korean paths, the runner links to a unique temporary ASCII path and then moves the executable into `build/`. Windows TEMP is the default; `PRACTICE_BUILD_TEMP` selects another writable ASCII path. Three-language execution and C debug-input preparation were checked from a Korean project directory.

`.vscode` provides file-input and keyboard-input configurations for Python/C/C++; debugger extensions are installed separately. The language router is based on version 0.1.2, with fixed drive paths removed. It checks the current workspace's `scripts/run.ps1` and `samples` directories, then routes tasks/debugging by file extension. Load `extensions/lig-practice-runner` in extension development mode; a compiled VSIX is not included.

The October 19, 2026 checks covered three-language exercises and fixtures, boundaries for four C functions, language routing and execution commands. VS Code API calls were mocked; PowerShell execution was tested from a separate path.
