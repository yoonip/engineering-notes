# 금과 은 운반하기

Level 3 · [86053 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/86053)

## 문제와 조건

도시별 트럭으로 필요한 금 a와 은 b를 운반하는 최소 시간을 구합니다. 돌아오는 시간도 필요하지만 마지막 배달 후에는 돌아오지 않아도 됩니다.

`0≤a,b,g[i],s[i]≤10^9; 1≤cities≤10^5; 1≤w[i]≤10^2; 1≤t[i]≤10^5; a≤Σg; b≤Σs`

## 풀이를 따라가기

1. 주어진 도시 N개·시간 탐색 상한 T에서 시간 O(N log T), 추가 공간 O(1)
2. 시간이 늘면 운반 가능량이 줄지 않으므로 이진 탐색으로 최소 시간을 찾습니다. 마지막 운반은 편도만 필요합니다. 도시 수 N·시간 상한 T에 대해 시간 O(N log T), 추가 공간 O(1).
3. 예: 편도 10·적재량 7인 트럭은 10,30,50에 각각 배달합니다. 금·은 합계 20을 운반하려면 세 번 필요해 답은 50입니다.

## 왜 이 방법으로 풀 수 있나

주어진 도시 N개·시간 탐색 상한 T에서 시간 O(N log T), 추가 공간 O(1)

시간·공간: 도시 N개·시간 탐색 상한 T에서 시간 O(N log T), 추가 공간 O(1)

## 다른 방법과 비교

시간별로 각 도시가 실을 수 있는 금·은 조합을 직접 만들고 도시들을 합칩니다. 세 가지 용량 부등식의 충분성을 작은 화물량에서 대조합니다.

| 항목 | 기본 풀이 | 도시별 화물 배분 DP |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 도시 N개·시간 탐색 상한 T에서 시간 O(N log T), 추가 공간 O(1) | O(T·도시 수·(a+1)²(b+1)²), 작은 입력 비교용 |
| 용도 | 기본 제출 구현 | 작은 입력 비교·검증용 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[10, 10, [100], [100], [7], [10]]` | `50` |
| `[90, 500, [70, 70, 0], [0, 0, 500], [100, 100, 2], [4, 8, 1]]` | `499` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Find the earliest time to deliver a gold and b silver using city trucks. Return trips are needed between deliveries, but not after the final delivery.

`0≤a,b,g[i],s[i]≤10^9; 1≤cities≤10^5; 1≤w[i]≤10^2; 1≤t[i]≤10^5; a≤Σg; b≤Σs`

### Method and correctness

Binary-search the earliest feasible time. For each city, count deliveries including the final one-way trip and obtain maximum gold, maximum silver, and maximum combined cargo. Feasibility requires all three totals to cover the requested amounts; separate gold and silver tests alone would double-count shared truck capacity. More time never reduces capacity.

Main complexity: O(cities·log T) time, O(1) extra space.

### Alternative and trade-offs

At each candidate time, explicitly enumerate feasible gold/silver allocations per city and combine them. Tiny cargos independently check the three capacity inequalities.

Code: [alternative.py](alternative.py). Scope: tiny-input oracle; not for maximum-size submissions.

Complexity: O(T·cities·(a+1)²(b+1)²), small-input checking.

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 금과 은 운반하기](https://school.programmers.co.kr/learn/courses/30/lessons/86053) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 14개 입력에서 26회 검사를 통과했습니다.

Passed 26 implementation checks across 14 official, boundary and fixed-seed differential inputs.
