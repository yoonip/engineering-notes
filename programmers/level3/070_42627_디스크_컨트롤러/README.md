# 디스크 컨트롤러

Level 3 · [42627 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/42627)

## 문제와 조건

지정된 비선점 우선순위로 디스크 작업을 실행했을 때 요청부터 완료까지 걸린 시간의 평균을 구합니다.

대기 중 소요시간·요청시각·작업번호 순으로 우선하고 작업 도중 중단하지 않습니다. 평균 반환시간의 정수 부분을 구합니다.

`1≤jobs≤500; 0≤request≤1,000; 1≤duration≤1,000`

## 풀이를 따라가기

1. 요청을 작업 N개에서 시간 O(N log N), 공간 O(N)
2. 예: [0,3],[1,9],[3,5]는 작업 0→2→1 순서로 실행되어 반환 시간이 3·5·16, 평균의 정수 부분은 8입니다.
3. 현재 지문의 요청 시각·작업 번호 동점 조건까지 튜플에 반영합니다. 시간 O(N log N), 공간 O(N).

## 왜 이 방법으로 풀 수 있나

요청을 작업 N개에서 시간 O(N log N), 공간 O(N)

시간·공간: 작업 N개에서 시간 O(N log N), 공간 O(N)

## 다른 방법과 비교

매번 도착한 미처리 작업 중 (소요시간, 요청시각, 번호)가 가장 작은 것을 고릅니다. 현재 지문의 우선순위를 그대로 따르며 힙 없이 구현합니다.

| 항목 | 기본 풀이 | 대기 작업 직접 선택 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 작업 N개에서 시간 O(N log N), 공간 O(N) | O(N²), 공간 O(N) |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[[[0, 3], [1, 9], [3, 5]]]` | `8` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Simulate the specified nonpreemptive disk priority policy and return average request-to-completion time.

Prioritize waiting jobs by duration, request time, and job index; execution is nonpreemptive. Return the integer part of average turnaround.

`1≤jobs≤500; 0≤request≤1,000; 1≤duration≤1,000`

### Method and correctness

Sort jobs by request time and push newly arrived jobs into a heap ordered by duration, request time, then original index. Execute the top job without interruption. If no job is waiting, jump to the next request time. Accumulate completion minus request times and return the integer part of their average.

Main complexity: O(N log N) time, O(N) space.

### Alternative and trade-offs

Scan all arrived unfinished jobs and choose the minimum (duration, request time, job index). This follows the specified priority directly without a heap.

Code: [alternative.py](alternative.py).

Complexity: O(N²), space O(N).

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 디스크 컨트롤러](https://school.programmers.co.kr/learn/courses/30/lessons/42627) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 42개 입력에서 84회 검사를 통과했습니다.

Passed 84 implementation checks across 42 official, boundary and fixed-seed differential inputs.
