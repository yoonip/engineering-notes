# 카운트 다운

Level 3 · [131129 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/131129)

## 문제와 조건

다트로 target을 정확히 만드는 최소 발수를 구하고, 같은 발수면 싱글·불을 최대한 많이 맞힌 결과를 반환합니다.

`1≤target≤100,000`

## 풀이를 따라가기

1. 점수를 1부터 target까지 늘리며 마지막 다트의 점수를 모두 비교하는 DP입니다. 우선 다트 수를 최소화하고, 다트 수가 같을 때만 싱글·불을 최대화합니다.
2. 동일한 점수를 싱글로도 낼 수 있으면 더블·트리플보다 항상 유리하므로 점수별 최선의 종류만 남깁니다. 서로 다른 점수 수 C≤43에 대해 시간 O(target×C), 공간 O(target).
3. 예: 21은 트리플 7 한 발이라 [1,0]. 58은 불 50+싱글 8 두 발이므로 [2,2]입니다.

## 왜 이 방법으로 풀 수 있나

점수를 1부터 target까지 늘리며 마지막 다트의 점수를 모두 비교하는 DP입니다. 우선 다트 수를 최소화하고, 다트 수가 같을 때만 싱글·불을 최대화합니다.

시간·공간: 시간 O(target×C), 공간 O(target).

## 다른 방법과 비교

점수를 정점으로 두고 비용을 (다트 수, 싱글·불 수의 음수)로 표현합니다. 튜플 비교로 두 우선순위를 함께 처리합니다. 기본 DP보다 힙 비용이 들지만 우선순위를 명확히 확인할 수 있습니다.

| 항목 | 기본 풀이 | 사전식 비용 최단경로 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(target×C), 공간 O(target). | O(target·C log target), 공간 O(target) |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[21]` | `[1, 0]` |
| `[58]` | `[2, 2]` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Reach target exactly with the fewest darts, maximizing single/bull hits among equal-length solutions.

`1≤target≤100,000`

### Method and correctness

DP compares the final dart for every target subtotal. Minimize dart count first, then maximize single-or-bull hits among equal-count solutions. If the same numeric score has multiple dart types, retain its most favorable single/bull flag. Every scoring sequence ends with one listed score, so considering all final darts covers all possibilities.

Main complexity: O(target·C) time, O(target) space; C≤43.

### Alternative and trade-offs

Treat scores as vertices with lexicographic costs (throws, negative single/bull hits). Tuple comparison encodes both priorities; Dijkstra adds heap overhead compared with score-ordered DP.

Code: [alternative.py](alternative.py). Scope: alternative implementation.

Complexity: O(target·C log target), space O(target).

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 카운트 다운](https://school.programmers.co.kr/learn/courses/30/lessons/131129) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 45개 입력에서 90회 검사를 통과했습니다.

Passed 90 implementation checks across 45 official, boundary and fixed-seed differential inputs.
