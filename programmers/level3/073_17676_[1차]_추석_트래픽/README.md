# [1차] 추석 트래픽

Level 3 · [17676 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/17676)

## 문제와 조건

임의의 1초 구간에 처리 중인 요청이 최대 몇 개인지 밀리초 로그에서 구합니다.

요청 구간은 시작·종료를 모두 포함하고 밀리초 단위입니다. 로그는 종료 시각순입니다.

`1≤logs≤2,000; date=2016-09-15; duration∈[0.001s,3s]; window=1s`

## 풀이를 따라가기

1. 각 요청을 양 끝 포함 정수 밀리초 구간으로 바꾸고, 어떤 요청의 종료 시각부터 시작하는 1000ms 창과 겹치는 요청 수를 센다.
2. 임의의 최적 창도 겹치는 요청 중 가장 이른 종료 시각까지 오른쪽으로 밀어 요청을 잃지 않을 수 있어 종료 시각만 검사하면 충분하다.
3. 창의 끝은 시작+1000이 아니라 시작+999다. 예제 1·2의 1ms 차이로 답이 1·2로 달라진다. 시간 O(N²), 공간 O(N).

## 왜 이 방법으로 풀 수 있나

각 요청을 양 끝 포함 정수 밀리초 구간으로 바꾸고, 어떤 요청의 종료 시각부터 시작하는 1000ms 창과 겹치는 요청 수를 센다.

시간·공간: 시간 O(N²), 공간 O(N).

## 다른 방법과 비교

요청 [s,e]가 겹칠 1초 창의 시작점은 [s−999,e]입니다. 이 시작점 구간들의 최대 겹침을 차분 이벤트로 계산합니다. 끝점 전수 비교보다 빠릅니다.

| 항목 | 기본 풀이 | 정수 밀리초 이벤트 스윕 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(N²), 공간 O(N). | O(N log N), 공간 O(N) |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

예제 입력과 결과는 [공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/17676)에서 확인할 수 있습니다.

[examples.json](examples.json) contains the official example inputs and expected outputs, including narrative-format examples.

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Find the maximum concurrent request count over any one-second window from millisecond logs.

Request intervals include both endpoints at millisecond resolution. Logs are ordered by end time.

`1≤logs≤2,000; date=2016-09-15; duration∈[0.001s,3s]; window=1s`

### Method and correctness

Convert each log into a closed integer-millisecond interval, with start=end−duration+1. Test 1000-ms windows beginning at request end times and count intersecting requests. Any optimal window can shift right to the earliest end among its intersecting requests without losing them. A window ending at start+999 includes exactly 1000 ms.

Main complexity: O(N²) time, O(N) space.

### Alternative and trade-offs

A closed request interval [s,e] overlaps a 1000-ms window starting at t exactly for t in [s−999,e]. Sweep these feasible start intervals with integer difference events.

Code: [alternative.py](alternative.py).

Complexity: O(N log N), space O(N).

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: [1차] 추석 트래픽](https://school.programmers.co.kr/learn/courses/30/lessons/17676) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 43개 입력에서 86회 검사를 통과했습니다.

Passed 86 implementation checks across 43 official, boundary and fixed-seed differential inputs.
