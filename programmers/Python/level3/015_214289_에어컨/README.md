# 에어컨

Level 3 · [214289 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/214289)

## 문제와 조건

승객이 탄 모든 시각에 실내온도를 쾌적 범위 안에 두면서 전력 소비를 최소화합니다. 0분의 실내온도는 실외온도와 같습니다.

실외온도는 쾌적 범위 밖입니다. 탑승 표시는 0·1이고 최소 한 번 탑승하며, 조건을 지키는 제어가 가능한 입력입니다.

`−10≤temperature≤40; −10≤t1<t2≤40; 1≤a,b≤100; 2≤len(onboard)≤1,000; onboard[0]=0`

## 풀이를 따라가기

1. DP 상태는 현재 시각의 온도별 최소 소비전력입니다. 매 분 전원 끄기(무료 자연 변화), 유지(b), 1도 상승·하강(a)을 모두 비교합니다.
2. 탑승 시각의 다음 온도가 쾌적 범위 밖이면 제외합니다. 마지막 시각 이후의 비용은 더하지 않습니다. 시간 O(51T), 공간 O(51).
3. 예: 28도에서 26도까지 두 번 냉방한 뒤 계속 유지할 수도 있지만, 24도까지 더 냉방하고 전원을 꺼 자연 상승시키면 첫 예제에서 총 40이 됩니다.

## 왜 이 방법으로 풀 수 있나

DP 상태는 현재 시각의 온도별 최소 소비전력입니다. 매 분 전원 끄기(무료 자연 변화), 유지(b), 1도 상승·하강(a)을 모두 비교합니다.

시간·공간: 시간 O(51T), 공간 O(51).

## 다른 방법과 비교

시간과 온도를 정점으로 만들고 다익스트라로 최소 소비전력을 찾습니다. 기본 풀이는 매 분 모든 온도를 검사하고, 대안은 비용이 낮은 상태부터 꺼냅니다.

| 항목 | 기본 풀이 | 시간·온도 최단경로 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(51T), 공간 O(51). | O(51T log(51T)), 공간 O(51T) |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[28, 18, 26, 10, 8, [0, 0, 1, 1, 1, 1, 1]]` | `40` |
| `[-10, -5, 5, 5, 1, [0, 0, 0, 0, 0, 1, 0]]` | `25` |
| `[11, 8, 10, 10, 1, [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1]]` | `20` |
| `[11, 8, 10, 10, 100, [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1]]` | `60` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Minimize energy while keeping every occupied minute within the comfort range. At minute zero, inside and outside temperatures are equal.

The outside temperature is outside the comfort interval. Occupancy is binary, contains a passenger minute, and a feasible control schedule is guaranteed.

`−10≤temperature≤40; −10≤t1<t2≤40; 1≤a,b≤100; 2≤len(onboard)≤1,000; onboard[0]=0`

### Method and correctness

Let dp[t] be the minimum energy required to reach temperature t at the current minute. For each next minute, try switching off, holding temperature, heating one degree, and cooling one degree. Reject temperatures outside the comfort range when a passenger is present. Keep only the cheapest route to each temperature because future choices depend only on that temperature and time. There is no charge after the final observed minute.

Main complexity: O(51T) time, O(51) space.

### Alternative and trade-offs

Dijkstra searches a time–temperature graph. The main DP scans each time layer; this alternative expands states in increasing energy cost.

Code: [alternative.py](alternative.py).

Complexity: O(51T log(51T)), space O(51T).

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 에어컨](https://school.programmers.co.kr/learn/courses/30/lessons/214289) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 46개 입력에서 92회 검사를 통과했습니다.

Passed 92 implementation checks across 46 official, boundary and fixed-seed differential inputs.
