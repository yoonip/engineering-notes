# 선입 선출 스케줄링

[Level 3 목록 / Level 3 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

Level 3 · [12920 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/12920)

## 문제와 조건

일이 코어가 비는 순서로 배정되고 동시에 비면 작은 번호가 먼저 받을 때 n번째 일을 받는 코어 번호를 구합니다.

`2≤cores≤10,000; 1≤core time≤10,000; n≤50,000`

## 풀이를 따라가기

1. 코어 C개·시간 상한 U에서 시간 O(C log U), 추가 공간 O(1)
2. 예: n=6, [1,2,3]은 0시각 세 개, 1시각 한 개, 2시각 1·2번 코어가 두 개를 받아 마지막은 2번입니다.
3. 최초 배정 시각 직전의 작업 수를 빼고 동시에 비는 코어를 번호순으로 셉니다. 코어 C개, 탐색 상한 U일 때 시간 O(C log U), 공간 O(1).

## 왜 이 방법으로 풀 수 있나

코어 C개·시간 상한 U에서 시간 O(C log U), 추가 공간 O(1)

시간·공간: 코어 C개·시간 상한 U에서 시간 O(C log U), 추가 공간 O(1)

## 다른 방법과 비교

처음 모든 코어에 하나씩 주고, 그다음부터 (다음 빈 시각, 코어 번호)를 힙에서 꺼냅니다. 동시 시각에 작은 번호가 먼저 받는 규칙을 직접 따릅니다.

| 항목 | 기본 풀이 | 코어 배정 이벤트 힙 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 코어 C개·시간 상한 U에서 시간 O(C log U), 추가 공간 O(1) | O(C+n log C), 공간 O(C) |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[6, [1, 2, 3]]` | `2` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Return the core receiving job n when jobs are assigned to the first free core, breaking simultaneous availability by smaller core index.

`2≤cores≤10,000; 1≤core time≤10,000; n≤50,000`

### Method and correctness

Jobs start on every core at time zero; by time T the started-job count is core_count+sum(floor(T/duration)). Binary-search the first assignment time containing job n. Subtract jobs assigned strictly earlier, then scan cores in index order among those becoming free at that time. The desired event is an assignment time, not the final completion time.

Main complexity: O(C log U) time, O(1) extra space.

### Alternative and trade-offs

Initially assign one job to each core, then pop (next free time, core index) events. The heap directly enforces the smaller-index priority at simultaneous completion times.

Code: [alternative.py](alternative.py).

Complexity: O(C+n log C), space O(C).

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 선입 선출 스케줄링](https://school.programmers.co.kr/learn/courses/30/lessons/12920) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 42개 입력에서 84회 검사를 통과했습니다.

Passed 84 implementation checks across 42 official, boundary and fixed-seed differential inputs.
