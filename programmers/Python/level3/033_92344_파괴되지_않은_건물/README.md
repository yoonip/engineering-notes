# 파괴되지 않은 건물

Level 3 · [92344 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/92344)

## 문제와 조건

직사각형 공격·회복 스킬을 순서대로 적용한 후 내구도가 양수인 건물 수를 구합니다.

`1≤N,M≤1,000; 1≤durability≤1,000; 1≤K≤250,000; 1≤degree≤500; 0≤r1≤r2<N; 0≤c1≤c2<M`

## 풀이를 따라가기

1. 직사각형을 매번 모두 바꾸는 대신, 변화 시작·취소를 네 꼭짓점에 기록하는 2차원 차분을 사용합니다.
2. 가로·세로 누적합을 각각 한 번 적용하면 각 칸의 총 변화량이 복원됩니다. 중간에 파괴돼도 변화는 계속 누적하며 마지막 내구도>0만 셉니다. 스킬 수 K에 대해 시간 O(K+NM), 공간 O(NM).
3. 예: 공격 4와 회복 2가 겹친 칸의 총 변화량은 -2입니다. 초기 내구도 5이면 최종 3이므로 생존합니다.

## 왜 이 방법으로 풀 수 있나

직사각형을 매번 모두 바꾸는 대신, 변화 시작·취소를 네 꼭짓점에 기록하는 2차원 차분을 사용합니다.

시간·공간: 시간 O(K+NM), 공간 O(NM).

## 다른 방법과 비교

각 스킬의 직사각형을 실제로 모두 갱신합니다. 중간 내구도가 음수여도 회복을 계속 적용합니다. 작은 보드에서 차분 배열의 경계 부호를 검증하는 기준입니다.

| 항목 | 기본 풀이 | 직사각형 직접 갱신 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(K+NM), 공간 O(NM). | O(KNM), 공간 O(NM), 작은 입력 비교용 |
| 용도 | 기본 제출 구현 | 작은 입력 비교·검증용 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[[[5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5]], [[1, 0, 0, 3, 4, 4], [1, 2, 0, 2, 3, 2], [2, 1, 0, 3, 1, 2], [1, 0, 1, 3, 3, 1]]]` | `10` |
| `[[[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[1, 1, 1, 2, 2, 4], [1, 0, 0, 1, 1, 2], [2, 2, 0, 2, 0, 100]]]` | `6` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Count buildings with positive durability after all rectangular attacks and heals.

`1≤N,M≤1,000; 1≤durability≤1,000; 1≤K≤250,000; 1≤degree≤500; 0≤r1≤r2<N; 0≤c1≤c2<M`

### Method and correctness

Record each rectangular durability change at four corners in a two-dimensional difference array. Horizontal and vertical prefix sums reconstruct the total change at every cell. Changes remain additive even when a building is temporarily destroyed and later healed. Count only cells with strictly positive final durability.

Main complexity: O(K+NM) time, O(NM) space.

### Alternative and trade-offs

Update every cell of every skill rectangle. Recovery still applies after durability becomes nonpositive. Tiny boards directly verify the difference-array corner signs.

Code: [alternative.py](alternative.py). Scope: tiny-input oracle; not for maximum-size submissions.

Complexity: O(KNM), space O(NM), small-input checking.

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 파괴되지 않은 건물](https://school.programmers.co.kr/learn/courses/30/lessons/92344) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 43개 입력에서 86회 검사를 통과했습니다.

Passed 86 implementation checks across 43 official, boundary and fixed-seed differential inputs.
