# 다단계 칫솔 판매

[Level 3 목록 / Level 3 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

Level 3 · [77486 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/77486)

## 문제와 조건

판매 이익의 10%를 추천인에게 올리고 나머지를 가지는 조직에서 각 판매원의 최종 수익을 구합니다.

추천인은 가입 순서상 앞선 사람 또는 −입니다. 판매마다 100원×수량을 분배하고 정수 10%를 위로 보냅니다.

`1≤members≤10,000; 1≤sales≤100,000; 1≤amount[i]≤100; unit profit=100; name length≤10`

## 풀이를 따라가기

1. 각 판매의 이익을 본인부터 추천인 방향으로 전달합니다. 금액이 단계마다 1/10이 되어 몇 단계 뒤 0이 됩니다.
2. 예: 1200원은 본인 1080원, 추천인 108원, 그 위 11원, 센터 1원으로 분배됩니다.
3. 판매 금액 최대 10000원이므로 기록당 최대 5단계. 시간 O(가입자 수 + 판매 기록 수), 공간 O(가입자 수).

## 왜 이 방법으로 풀 수 있나

각 판매의 이익을 본인부터 추천인 방향으로 전달합니다. 금액이 단계마다 1/10이 되어 몇 단계 뒤 0이 됩니다.

시간·공간: 시간 O(가입자 수 + 판매 기록 수), 공간 O(가입자 수).

## 다른 방법과 비교

한 거래의 10%를 재귀적으로 추천인에게 올립니다. 거래를 합쳐서 반올림하면 답이 달라지므로 반드시 거래별로 나눕니다. 반복문 대신 재귀로 같은 분배 규칙을 표현합니다.

| 항목 | 기본 풀이 | 거래별 재귀 분배 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(가입자 수 + 판매 기록 수), 공간 O(가입자 수). | O(판매 수·log(최대 매출)), 공간 O(가입자 수+분배 깊이) |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[["john", "mary", "edward", "sam", "emily", "jaimie", "tod", "young"], ["-", "-", "mary", "edward", "mary", "mary", "jaimie", "edward"], ["young", "john", "tod", "emily", "mary"], [12, 4, 2, 5, 10]]` | `[360, 958, 108, 0, 450, 18, 180, 1080]` |
| `[["john", "mary", "edward", "sam", "emily", "jaimie", "tod", "young"], ["-", "-", "mary", "edward", "mary", "mary", "jaimie", "edward"], ["sam", "emily", "jaimie", "edward"], [2, 3, 5, 4]]` | `[0, 110, 378, 180, 270, 450, 0, 0]` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Compute each member’s profit when ten percent of each sale propagates to the referrer and the remainder is retained.

A referrer is an earlier enrollee or −. Distribute each sale’s quantity×100 profit separately, passing its integer ten percent upwards.

`1≤members≤10,000; 1≤sales≤100,000; 1≤amount[i]≤100; unit profit=100; name length≤10`

### Method and correctness

For each sale independently, keep the money minus floor(money/10) and pass that floor amount to the referrer. Continue until the root or a zero share. Rounding is per sale, so combining sales before distributing changes results. Parent names are resolved to indices once.

Main complexity: O(sales·log maximum sale profit) time, O(members) space.

### Alternative and trade-offs

Recursively pass ten percent of each individual sale to the referrer. Never merge sales before rounding, because integer division is per transaction. This expresses propagation recursively rather than iteratively.

Code: [alternative.py](alternative.py).

Complexity: O(sales·log(max sale profit)), space O(members+propagation depth).

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 다단계 칫솔 판매](https://school.programmers.co.kr/learn/courses/30/lessons/77486) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 43개 입력에서 86회 검사를 통과했습니다.

Passed 86 implementation checks across 43 official, boundary and fixed-seed differential inputs.
