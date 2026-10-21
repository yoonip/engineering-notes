# [1차] 셔틀버스

[Level 3 목록 / Level 3 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

Level 3 · [17678 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/17678)

## 문제와 조건

제한 좌석 셔틀을 타고 출근할 수 있는 콘의 가장 늦은 도착 시각을 구합니다.

09:00부터 t분 간격으로 n대가 출발합니다. 콘은 같은 도착 시각의 크루보다 뒤에 섭니다.

`1≤n≤10; 1≤t≤60; 1≤m≤45; crew≤2,000; timetable∈[00:01,23:59]`

## 풀이를 따라가기

1. 크루를 도착 순서로 정렬한 뒤 실제 버스 탑승을 시뮬레이션합니다. 마지막 버스에 자리가 남으면 출발 시각, 만석이면 마지막 탑승자보다 1분 먼저 도착합니다.
2. 예: 마지막 버스의 마지막 크루가 09:10이면 콘은 09:09까지 와야 합니다. 이전 버스를 앞당겨 타야 하는 경우도 같은 경계 시각으로 처리됩니다.
3. 크루 C명, 버스 N대일 때 시간 O(C log C+N), 공간 O(C). 크루는 한 번만 탑승 처리됩니다.

## 왜 이 방법으로 풀 수 있나

크루를 도착 순서로 정렬한 뒤 실제 버스 탑승을 시뮬레이션합니다. 마지막 버스에 자리가 남으면 출발 시각, 만석이면 마지막 탑승자보다 1분 먼저 도착합니다.

시간·공간: 시간 O(C log C+N), 공간 O(C). 크루는 한 번만 탑승 처리됩니다.

## 다른 방법과 비교

00:00부터 마지막 버스 시각까지 콘을 실제 대기열에 넣어 탑승 여부를 확인합니다. 같은 시각 크루가 먼저 타므로 콘은 동점에서 뒤에 둡니다.

| 항목 | 기본 풀이 | 콘 도착시각 전수 시뮬레이션 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(C log C+N), 공간 O(C). 크루는 한 번만 탑승 처리됩니다. | O(시각 수·(C log C+N)), 작은 크루 수 비교용 |
| 용도 | 기본 제출 구현 | 작은 입력 비교·검증용 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[1, 1, 5, ["08:00", "08:01", "08:02", "08:03"]]` | `"09:00"` |
| `[2, 10, 2, ["09:10", "09:09", "08:00"]]` | `"09:09"` |
| `[2, 1, 2, ["09:00", "09:00", "09:00", "09:00"]]` | `"08:59"` |
| `[1, 1, 5, ["00:01", "00:01", "00:01", "00:01", "00:01"]]` | `"00:00"` |
| `[1, 1, 1, ["23:59"]]` | `"09:00"` |
| `[10, 60, 45, ["23:59", "23:59", "23:59", "23:59", "23:59", "23:59", "23:59", "23:59", "23:59", "23:59", "23:59", "23:59", "23:59", "23:59", "23:59", "23:59"]]` | `"18:00"` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Find Con’s latest arrival time that still boards a capacity-limited shuttle.

There are n departures from 09:00 at t-minute intervals. Con joins behind crews with the same arrival time.

`1≤n≤10; 1≤t≤60; 1≤m≤45; crew≤2,000; timetable∈[00:01,23:59]`

### Method and correctness

Sort crew arrival times and simulate every bus’s limited seats. If the final bus has a free seat, Con may arrive at its departure time. If full, Con must arrive one minute before its final boarding crew member, since equal-time crews take priority. Each crew member is boarded only once.

Main complexity: O(C log C+n) time, O(C) space.

### Alternative and trade-offs

Insert Con into the queue for every candidate minute. Crews arriving at the same time precede Con. This directly checks the last-seat boundary formula by simulation.

Code: [alternative.py](alternative.py). Scope: tiny-input oracle; not for maximum-size submissions.

Complexity: O(candidate minutes·(C log C+N)), small-crew oracle.

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: [1차] 셔틀버스](https://school.programmers.co.kr/learn/courses/30/lessons/17678) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 47개 입력에서 94회 검사를 통과했습니다.

Passed 94 implementation checks across 47 official, boundary and fixed-seed differential inputs.
