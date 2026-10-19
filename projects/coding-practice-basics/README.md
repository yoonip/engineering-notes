# 기초 알고리즘 연습: C · C++ · Python

6개 학습 주제를 세 언어로 구현한 표준 입력·출력 예제 18개입니다. 입력을 읽어 결과를 출력하는 독립 실행 프로그램으로 구성되어 있습니다.

AI를 활용해 작성한 기초 알고리즘 학습 예제입니다. 같은 입력을 세 언어로 처리하고 결과를 비교합니다.

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

## 구성

- `c/`, `cpp/`, `python/`: 주제별 소스 코드
- `fixtures/`: 주제별 입력과 기대 출력
- `catalog.json`: 주제, 소스 및 fixture 경로
- `verify.py`: 컴파일 및 실행 결과 비교 도구
- `VALIDATION.json`: 로컬 검증 기록
- `SHA256SUMS`: 파일별 SHA256 목록
- `PROVENANCE.md`: 작성 경위와 공개 범위

## 실행과 검증

Python 3.8 이상, C11 및 C++17 컴파일러를 사용합니다. Python 스크립트와 검증 도구는 표준 라이브러리만 사용합니다. 다음 명령은 저장소 루트에서 실행합니다.

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

## English overview

Six algorithm exercises are implemented in C, C++, and Python: aggregation, digit counting, sorting, grid BFS, dynamic programming, and binary search. All 18 programs use standard input and output. The standard-library verification script compiles the native programs and checks one fixture per implementation.
