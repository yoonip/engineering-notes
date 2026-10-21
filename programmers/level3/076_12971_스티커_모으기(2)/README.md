# 스티커 모으기(2)

[Level 3 목록 / Level 3 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

Level 3 · [12971 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/12971)

## 문제와 조건

원형으로 이웃한 스티커를 함께 고를 수 없을 때 얻을 수 있는 최대 점수 합을 구합니다.

`1≤N≤100,000; 1≤sticker[i]≤100`

## 풀이를 따라가기

1. 일직선에서는 dp[i]=max(dp[i-1],dp[i-2]+현재 값)입니다. 원형에서는 첫 칸·마지막 칸 중 적어도 하나를 빼야 하므로 두 일직선 문제로 나눕니다.
2. 예제 1은 첫 칸을 제외하고 6+11+9+10=36을 고릅니다. 두 경우 모두 첫 칸·마지막 칸을 선택하지 않는 경우도 자연스럽게 포함됩니다.
3. 각 DP에서 이전 값 두 개만 필요합니다. 시간 O(N), 추가 공간 O(1).

## 왜 이 방법으로 풀 수 있나

일직선에서는 dp[i]=max(dp[i-1],dp[i-2]+현재 값)입니다. 원형에서는 첫 칸·마지막 칸 중 적어도 하나를 빼야 하므로 두 일직선 문제로 나눕니다.

시간·공간: 시간 O(N), 추가 공간 O(1).

## 다른 방법과 비교

선택할 스티커 집합을 모두 만들고 인접 선택을 배제합니다. 첫 칸·마지막 칸의 연결까지 직접 검사하므로 원형 DP의 분리를 확인합니다.

| 항목 | 기본 풀이 | 독립 집합 전수검사 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(N), 추가 공간 O(1). | O(2^N N), 작은 원형 배열 비교용 |
| 용도 | 기본 제출 구현 | 작은 입력 비교·검증용 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[[14, 6, 5, 11, 3, 9, 2, 10]]` | `36` |
| `[[1, 3, 2, 5, 4]]` | `8` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Maximize selected sticker values on a circle without selecting neighboring stickers.

`1≤N≤100,000; 1≤sticker[i]≤100`

### Method and correctness

For a line, update best[i]=max(best[i−1],best[i−2]+value[i]). In a circle at least one of the first and last stickers must be absent, so solve the line excluding the first and the line excluding the last. Their maximum covers every valid circular selection. Handle a single sticker separately.

Main complexity: O(N) time, O(1) extra space.

### Alternative and trade-offs

Enumerate sticker subsets and reject adjacent selections, including the first–last edge. This directly checks the circular split used by the linear DPs.

Code: [alternative.py](alternative.py). Scope: tiny-input oracle; not for maximum-size submissions.

Complexity: O(2^N N), small-circle oracle.

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 스티커 모으기(2)](https://school.programmers.co.kr/learn/courses/30/lessons/12971) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 43개 입력에서 86회 검사를 통과했습니다.

Passed 86 implementation checks across 43 official, boundary and fixed-seed differential inputs.
