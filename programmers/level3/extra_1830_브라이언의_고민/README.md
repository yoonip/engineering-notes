# 브라이언의 고민

Level 3 · [1830 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/1830)

## 문제와 조건

글자 사이 기호 삽입과 단어 양끝 기호 삽입 규칙으로 암호화한 광고 문장을 원래 대문자 단어 문장으로 복원합니다.

기호 재사용은 금지됩니다. 여러 원문이 가능하면 그중 하나를 반환하고 불가능하면 invalid입니다.

`sentence length≤1,000; sentence∈[A-Za-z]+`

## 풀이를 따라가기

1. 하나의 단어 구간은 대문자만, 규칙1(대문자·기호 번갈아), 규칙2(기호로 감싸기), 두 규칙의 결합 중 하나다. 같은 기호의 전체 출현이 한 구간 안에서만 쓰이는지 검사한다.
2. previous[end]에 앞부분을 유효하게 해석한 마지막 단어를 저장하는 DP를 사용한다. 가능한 경계를 모두 확인하므로 규칙1·2로 둘 다 해석되는 경우도 처리한다.
3. 기호 재사용·기호 교차·두 규칙 중복은 구간 검사에서 거절한다. 길이 L≤1000, 시간·저장 문자열을 포함한 공간 O(L²). 가능한 원문 중 하나를 반환한다.

## 왜 이 방법으로 풀 수 있나

하나의 단어 구간은 대문자만, 규칙1(대문자·기호 번갈아), 규칙2(기호로 감싸기), 두 규칙의 결합 중 하나다. 같은 기호의 전체 출현이 한 구간 안에서만 쓰이는지 검사한다.

시간·공간: 시간·저장 문자열을 포함한 공간 O(L²). 가능한 원문 중 하나를 반환한다.

## 다른 방법과 비교

각 구간이 원래 단어·규칙 1·규칙 2·두 규칙 결합인지 직접 검사하고 유효한 구간을 이어 붙입니다. 모든 소문자의 출현이 한 규칙에 온전히 들어가야 하며 재사용과 교차를 막습니다.

| 항목 | 기본 풀이 | 단어 후보 그래프 DFS |
|---|---|---|
| 코드 | [solution.cpp](solution.cpp) | [alternative.py](alternative.py) |
| 비용 | 시간·저장 문자열을 포함한 공간 O(L²). 가능한 원문 중 하나를 반환한다. | O(L³), 공간 O(L²), 짧은 문장 비교용 |
| 용도 | 기본 제출 구현 | 작은 입력 비교·검증용 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `["HaEaLaLaObWORLDb"]` | `"HELLO WORLD"` |
| `["SpIpGpOpNpGJqOqA"]` | `"SIGONG JOA"` |
| `["AxAxAxAoBoBoB"]` | `"invalid"` |

Python 대안은 examples.json과 별도 경계·무작위 입력으로 로컬 검증합니다. C++ 제출본의 실행 결과는 전체 검증 기록에서 구분합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.cpp)

## English

### Task and constraints

Decode an advertising sentence formed by interleaving lowercase markers and/or wrapping words with markers back into uppercase words.

Marker reuse is forbidden. Any valid decoded sentence is accepted; return invalid if none exists.

`sentence length≤1,000; sentence∈[A-Za-z]+`

### Method and correctness

A valid word interval is plain uppercase, alternating uppercase/one marker, wrapped by one marker, or a combination of the two rules. Validate that every occurrence of each marker belongs to that single rule use. DP records one valid prefix decomposition per endpoint. If the end is reachable, backtrack words; otherwise return invalid. Any valid decoded sentence is acceptable.

Main complexity: O(L²) time and stored substring space.

### Alternative and trade-offs

Validate each candidate interval as a plain word, rule 1, rule 2, or their combination, then search a path of valid word intervals. Every lowercase marker must be wholly contained in one rule use, preventing reuse or crossing.

Code: [alternative.py](alternative.py). Scope: tiny-input oracle; not for maximum-size submissions.

Complexity: O(L³), space O(L²), short-sentence oracle.

### Verification

The Python alternative is checked with examples.json and separate edge/random cases; C++ execution is recorded separately in the repository validation report.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 브라이언의 고민](https://school.programmers.co.kr/learn/courses/30/lessons/1830) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 33개 입력에서 33회 검사를 통과했습니다.

Passed 33 implementation checks across 33 official, boundary and fixed-seed differential inputs.

## 제출본과 현재 구현 / Submission and current implementation

저장된 제출본은 이미 저장한 끝점에도 부분 문자열을 새로 만들 수 있어 최악 시간은 O(L³)입니다. 현재 코드는 끝점이 아직 저장되지 않았을 때만 부분 문자열을 만들어 후보 검사와 복사의 합을 O(L²)로 줄였습니다. 저장 원본의 주석보다 이 분석을 따릅니다.

The saved submission can construct substrings even for already-filled endpoints, giving O(L³) worst-case time. The current implementation constructs them only for previously unset endpoints, reducing total candidate checks and copying to O(L²). This analysis corrects the original submission’s complexity comment.

[Python 비교 원본 / Stored Python comparison source](submitted_original.py)
