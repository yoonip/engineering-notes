# 최적의 행렬 곱셈

[Level 3 목록 / Level 3 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

Level 3 · [12942 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/12942)

## 문제와 조건

행렬의 순서는 유지하면서 괄호 위치를 정해 스칼라 곱셈 횟수를 최소화합니다.

모든 인접 행렬의 차원이 곱셈 가능한 형태입니다. 행렬 순서는 바꾸지 않습니다.

`3≤matrix count≤200; 1≤rows,columns≤200`

## 풀이를 따라가기

1. 최종 곱셈은 어떤 경계 k를 기준으로 (i~k 결과)×(k+1~j 결과)로 나뉩니다. 두 부분의 최적 비용과 마지막 곱셈 비용을 합쳐 최소를 고릅니다.
2. 예: 5×3,3×10,10×6은 뒤 두 행렬부터 곱하면 3×10×6+5×3×6=270으로, 앞부터 곱한 450보다 작습니다.
3. 구간을 짧은 순서로 계산하면 필요한 두 부분의 값이 이미 있습니다. 시간 O(N³), 공간 O(N²).

## 왜 이 방법으로 풀 수 있나

최종 곱셈은 어떤 경계 k를 기준으로 (i~k 결과)×(k+1~j 결과)로 나뉩니다. 두 부분의 최적 비용과 마지막 곱셈 비용을 합쳐 최소를 고릅니다.

시간·공간: 시간 O(N³), 공간 O(N²).

## 다른 방법과 비교

마지막 곱셈의 경계를 재귀로 고르고 부분 구간의 답을 캐시합니다. 짧은 구간부터 반복하는 기본 DP와 계산 순서가 다릅니다.

| 항목 | 기본 풀이 | 메모이제이션 구간 분할 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(N³), 공간 O(N²). | O(N³), 공간 O(N²) |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[[[5, 3], [3, 10], [10, 6]]]` | `270` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Parenthesize an unchanged matrix sequence to minimize scalar multiplications.

Adjacent matrix dimensions are compatible; matrix order cannot be changed.

`3≤matrix count≤200; 1≤rows,columns≤200`

### Method and correctness

The final multiplication of matrices i…j splits after some k. Add the optimal left cost, optimal right cost, and row[i]×col[k]×col[j]. Fill intervals in increasing length so both subproblems are already available. Testing every final split proves optimality.

Main complexity: O(N³) time, O(N²) space.

### Alternative and trade-offs

Recursively choose the final multiplication split and cache interval costs. It evaluates the same optimal-substructure recurrence on demand rather than by increasing interval length.

Code: [alternative.py](alternative.py).

Complexity: O(N³), space O(N²).

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 최적의 행렬 곱셈](https://school.programmers.co.kr/learn/courses/30/lessons/12942) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 41개 입력에서 82회 검사를 통과했습니다.

Passed 82 implementation checks across 41 official, boundary and fixed-seed differential inputs.
