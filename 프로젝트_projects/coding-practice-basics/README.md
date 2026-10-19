# 기초 알고리즘 연습: C · C++ · Python

6개 학습 주제를 세 언어로 구현한 표준 입력·출력 예제 18개입니다. 입력을 읽어 결과를 출력하는 독립 실행 프로그램으로 구성되어 있습니다.

같은 입력을 세 언어로 처리하면서 자료형, 표준 입출력, 자료구조 표현의 차이를 비교합니다.

## 주제

| 번호 | 예제 | 개념 |
|---|---|---|
| 01 | 센서 기록 요약 | 배열 / 최솟값·최댓값 / 누적합 |
| 02 | 숫자별 빈도 | 문자 코드 / 빈도 배열 |
| 03 | 오름차순 정렬 | 정렬 / 비교 함수 |
| 04 | 격자 최단 경로 | 큐 / BFS |
| 05 | 계단 최소 비용 | DP / 점화식 |
| 06 | 정렬된 기록 검색 | 이분 탐색 / lower_bound |

## 입출력

- `01_sensor_summary`: N과 정수 N개를 받아 최솟값, 최댓값, 합계를 출력합니다.
- `02_digit_frequency`: 숫자 문자열을 받아 0~9의 개수를 순서대로 출력합니다.
- `03_sort_values`: N과 정수 N개를 받아 중복을 유지하며 오름차순으로 출력합니다.
- `04_grid_bfs`: N×M의 0/1 격자에서 시작·도착을 포함한 최단 칸 수를 출력합니다. 도달 불가는 -1입니다.
- `05_stair_cost_dp`: 0번 계단부터 N-1번까지 1칸 또는 2칸씩 이동하며 밟는 비용의 최솟값을 출력합니다.
- `06_lower_bound`: 정렬된 정수 N개와 Q개 질의를 받아 첫 인덱스(0부터)를 출력합니다. 없는 값은 -1입니다.

공백으로 구분되는 입력을 사용하며, 격자는 줄마다 하나의 0/1 문자열로 입력합니다. 입력은 형식에 맞는 유효한 값으로 가정합니다. N, Q는 양수이며 숫자 문자열은 비어 있지 않습니다. 센서 값과 계단 비용의 합은 C/C++의 `long long` 범위에 들어가야 합니다. 숫자 문자열은 최대 200,000자이고 격자는 최대 1,000×1,000입니다.

## 자료구조와 계산 비용

숫자별 빈도는 가능한 값이 10개로 고정되어 있어 길이 10의 배열로 바로 집계합니다. BFS는 먼저 발견한 칸부터 처리하는 큐가 필요하며, Python의 `deque.popleft()`는 맨 앞 원소를 꺼낼 때 나머지 원소를 옮기지 않습니다. 계단 문제는 이전 두 상태의 최솟값을 저장해 같은 경로를 반복해서 계산하지 않습니다. 정렬된 기록은 질의마다 전체를 훑는 대신 `lower_bound`로 탐색 범위를 절반씩 줄입니다.

| 예제 | 계산 비용 |
| --- | --- |
| 센서 요약·숫자 빈도 | 입력을 한 번씩 처리해 O(N) |
| 정렬 | Python·C++ 구현은 O(N log N) 비교 정렬; C `qsort`의 최악 시간 보장은 라이브러리 구현에 따름 |
| 격자 BFS | 각 칸과 인접 간선을 한 번씩 확인해 O(NM), 거리·큐 공간 O(NM) |
| 계단 DP | 시간 O(N), 현재 구현의 상태 배열 O(N) |
| 정렬된 기록 검색 | 입력을 읽은 뒤 질의 하나당 O(log N), Q개 질의 O(Q log N) |

## 구성

- `c/`, `cpp/`, `python/`: 주제별 소스 코드
- `fixtures/`: 주제별 입력과 기대 출력
- `catalog.json`: 주제, 소스 및 fixture 경로
- `verify.py`: 컴파일 및 실행 결과 비교 도구
- `VALIDATION.json`: 로컬 검증 기록
- `SHA256SUMS`: 파일별 SHA256 목록
- `PROVENANCE.md`: 구성과 파일 기록

## 실행과 검증

Python 3.8 이상, C11 및 C++17 컴파일러를 사용합니다. Python 스크립트와 검증 도구는 표준 라이브러리만 사용합니다. 다음 명령은 이 프로젝트 디렉터리에서 실행합니다.

```sh
python -B verify.py --cc gcc --cxx g++
```

검증 도구는 C/C++ 실행 파일을 임시 폴더에 만들고, 각 언어의 6개 예제에 대응하는 fixture를 한 번씩 실행합니다. 공백을 정규화한 출력과 기대값을 비교하며 컴파일러가 없으면 실패를 보고합니다. 컴파일러·IDE의 다운로드나 설치는 수행하지 않습니다.

Python 예제 한 개의 파일 입력 실행은 다음과 같습니다.

```sh
python python/01_sensor_summary.py < fixtures/01_sensor_summary.in
```

위 `<` 리디렉션 예시는 Bash와 Windows Command Prompt 기준입니다. PowerShell에서는 다음 형태를 사용합니다.

```powershell
Get-Content fixtures/01_sensor_summary.in | python python/01_sensor_summary.py
```

C/C++ 개별 빌드 예시입니다.

```sh
gcc -std=c11 -O2 c/01_sensor_summary.c -o sensor_c
g++ -std=c++17 -O2 cpp/01_sensor_summary.cpp -o sensor_cpp
```

## 검증 범위

기록된 검증은 C 6개·C++ 6개 빌드와 Python 6개 구문 검사, 총 18회의 예제 실행입니다. 최대 입력 성능, 잘못된 입력 처리, 모든 경계 조건을 검증하지 않습니다. C/C++ 코드가 사용하는 동적 메모리와 자료형은 위 입력 조건을 전제로 합니다.

## English

Six topics are implemented in C, C++ and Python as eighteen standalone standard-input/output programs. Running the same input across languages makes differences in types, I/O and data-structure representation easier to compare.

### Topics and input/output

| Example | Concept and output |
| --- | --- |
| `01_sensor_summary` | Arrays, min/max and accumulation; reads N integers and prints minimum, maximum and sum |
| `02_digit_frequency` | Character codes/frequency arrays; prints the counts of digits 0–9 |
| `03_sort_values` | Sorting/comparators; prints N values in ascending order, preserving duplicates |
| `04_grid_bfs` | Queue/BFS; prints shortest path length in an N×M binary grid, counting both endpoints, or −1 |
| `05_stair_cost_dp` | Recurrence/DP; finds the minimum cost from stair 0 to N−1 with one- or two-step moves |
| `06_lower_bound` | Binary search; returns the first zero-based index for each of Q queries, or −1 |

Input is whitespace-separated, except that each grid row is a binary string. Inputs must satisfy the stated format: N and Q are positive, digit strings are nonempty and at most 200,000 characters, and grids are at most 1,000×1,000. Sensor sums and stair costs must fit C/C++ `long long`.

### Data structures and cost

Digit counts use a ten-element array because the value range is fixed. BFS needs a FIFO queue; Python's `deque.popleft()` removes the front item without shifting the remaining elements. Stair DP stores preceding results to avoid recomputing paths. Sorted-record queries halve the search range with lower_bound instead of rescanning the array.

Aggregation/counting takes O(N). Python/C++ sorting takes O(N log N); C `qsort` has implementation-dependent worst-case guarantees. Grid BFS takes O(NM) time and O(NM) distance/queue space. Stair DP uses O(N) time and an O(N) state array. After reading input, binary search takes O(log N) per query, or O(Q log N) for Q queries.

### Files and execution

`c/`, `cpp/` and `python/` hold sources; `fixtures/` holds input/expected output. `catalog.json` maps topics to files, `verify.py` compiles and checks outputs, `VALIDATION.json` records local checks, `SHA256SUMS` stores hashes and `PROVENANCE.md` describes the file set.

Use Python 3.8+, a C11 compiler and a C++17 compiler. Python code uses only the standard library. Run the listed `verify.py` command from this project directory. It builds native executables in a temporary directory and runs one fixture for each of the eighteen implementations, normalizing whitespace before comparison. Missing compilers cause failure; the verifier does not install tools.

The examples above show direct Python execution and individual C/C++ builds. The `<` redirection form is for Bash or Windows Command Prompt; the PowerShell example pipes `Get-Content` into Python.

Recorded checks cover six C builds, six C++ builds, six Python syntax checks and eighteen executions. Maximum-size performance, malformed input and every boundary condition are outside those fixture checks; allocation and integer types rely on the input contract above.
