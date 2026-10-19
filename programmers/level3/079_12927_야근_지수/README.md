# 야근 지수

Level 3 · [12927 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/12927)

## 문제와 조건

매시간 작업량 하나를 1씩 줄일 수 있을 때 n시간 후 남은 작업량 제곱합을 최소화합니다.

`1≤W≤20,000; 1≤works[i]≤50,000; 1≤n≤1,000,000`

## 풀이를 따라가기

1. 작업 총량이 n 이하라면 전부 끝낼 수 있으므로 답은 0입니다.
2. 작업량을 큰 순서로 정렬합니다. 현재 가장 높은 작업들을 다음 작업의 높이까지 한 묶음으로 낮추는 데 드는 횟수는 (현재 높이−다음 높이)×묶음 크기입니다.
3. 남은 시간이 충분하면 그 높이까지 낮췄다고 보고 묶음을 하나 늘립니다. 각 원소를 실제로 갱신하지 않아도 다음 높이와 묶음 크기만 알면 됩니다.
4. 충분하지 않으면 남은 시간을 묶음 크기로 나눕니다. 몫만큼 모두 낮추고 나머지 개만 한 번 더 낮춘 뒤 제곱합을 계산합니다. 나머지 낮은 작업은 그대로 합칩니다.

## 왜 이 방법으로 풀 수 있나

작업량 x를 1 줄이면 제곱합은 2x−1만큼 줄어듭니다. 가장 높은 작업부터 줄이는 선택이 항상 가장 큰 이득입니다. 높이가 같은 작업들에는 가능한 한 균등하게 횟수를 나눠야 하므로 일괄 낮추기와 몫·나머지 배분은 이 선택을 여러 번 한 것과 같은 결과입니다.

시간·공간: 작업 W개에서 O(W log W) 시간·O(W) 공간

## 다른 방법과 비교

대안은 최대 힙에서 가장 큰 작업을 매시간 하나씩 줄입니다. n이 작으면 간단하고 충분히 빠르지만 n이 크면 반복 힙 연산이 많아집니다. 기본 코드는 높이 차이를 한꺼번에 처리해 n에 비례한 반복을 없앴습니다.

| 항목 | 기본 풀이 | 다른 방법 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 작업 W개에서 O(W log W) 시간·O(W) 공간 | 최대 힙: O(W+n log W) 시간·O(W) 공간 |

## 예제와 검증

[공식 예제 입력·결과](examples.json) · [고정 검증 입력](test_cases.json) · [실제 제출 원본](submitted_original.py)

저장된 제출본은 100점 채점을 받은 코드입니다. 현재 기본 구현은 효율을 높인 별도 구현이며, 공식 예제·경계 입력·독립 대안 비교를 합쳐 44개 입력에서 88회 로컬 검사를 통과했습니다.

```bash
python test_solution.py
```

## English

### Task and constraints

Minimize the squared remaining workloads after n one-unit reductions.

`1≤W≤20,000; 1≤works[i]≤50,000; 1≤n≤1,000,000`

### Method

If n covers all work, return zero. Sort workloads descending and lower the current highest group to the next height at cost (current−next)×group size. If affordable, enlarge the group; only the height and group size matter, so individual updates are unnecessary. Otherwise distribute remaining reductions evenly by quotient and remainder, then add the untouched lower workloads’ squared values.

### Correctness and complexity

Reducing x by one decreases fatigue by 2x−1, so reducing a current maximum gives the greatest benefit. Equal-height tasks must be reduced as evenly as possible. Bulk leveling and quotient/remainder allocation reproduce exactly those repeated greedy reductions.

Main complexity: O(W log W) time and O(W) space.

### Alternative and trade-offs

The alternative reduces one maximum workload per hour with a heap. It is simple and suitable when n is small, but performs many heap operations for large n. Bulk leveling removes the n-proportional loop.

Alternative complexity: O(W+n log W) time and O(W) space.

### Verification

The saved original submission received 100 points. The current main solution is a separate, more efficient implementation, locally verified by 88 checks on 44 official, boundary and independent differential inputs. Run `python test_solution.py`; inputs and results are in [examples.json](examples.json) and [test_cases.json](test_cases.json).

## 출처 / Sources

- [프로그래머스 공식 문제: 야근 지수](https://school.programmers.co.kr/learn/courses/30/lessons/12927) — 조건·예제 / task rules and examples. 확인 / checked: 2026-10-19.
