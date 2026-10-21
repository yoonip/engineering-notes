# 등굣길

[Level 3 목록 / Level 3 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

Level 3 · [42898 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/42898)

## 문제와 조건

웅덩이를 피해 오른쪽·아래로만 이동해 집에서 학교로 가는 경로 수를 구합니다.

`1≤m,n≤100; (m,n)≠(1,1); 0≤puddles≤10; modulus=1,000,000,007`

## 풀이를 따라가기

1. 오른쪽·아래로만 이동하므로 현재 칸에 도달하는 경로 수는 위 칸과 왼쪽 칸의 경로 수 합입니다. 웅덩이는 0으로 만듭니다.
2. 예: 가로 4·세로 3에서 (2,2)가 막히면 학교까지 4가지입니다. 입력 좌표는 행·열이 아니라 가로 x·세로 y 순서임에 주의합니다.
3. 시간 O(MN), 추가 공간 O(M + 웅덩이 수). 모든 경로의 이동 횟수는 같으므로 따로 최단 거리를 계산할 필요가 없습니다.

## 왜 이 방법으로 풀 수 있나

오른쪽·아래로만 이동하므로 현재 칸에 도달하는 경로 수는 위 칸과 왼쪽 칸의 경로 수 합입니다. 웅덩이는 0으로 만듭니다.

시간·공간: 시간 O(MN), 추가 공간 O(M + 웅덩이 수). 모든 경로의 이동 횟수는 같으므로 따로 최단 거리를 계산할 필요가 없습니다.

## 다른 방법과 비교

학교에서 집 방향으로 위·왼쪽 경로 수를 재귀로 더합니다. 웅덩이와 경계를 0으로 처리합니다. 반복 DP와 점화식은 같지만 계산 요청 순서가 다릅니다.

| 항목 | 기본 풀이 | 메모이제이션 경로 수 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(MN), 추가 공간 O(M + 웅덩이 수). 모든 경로의 이동 횟수는 같으므로 따로 최단 거리를 계산할 필요가 없습니다. | O(MN), 공간 O(MN) |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[4, 3, [[2, 2]]]` | `4` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Count right/down paths from home to school while avoiding puddles.

`1≤m,n≤100; (m,n)≠(1,1); 0≤puddles≤10; modulus=1,000,000,007`

### Method and correctness

Only right/down movement is allowed, so a cell’s path count is the sum from above and from the left. Puddles reset the count to zero. Use x,y input coordinates carefully rather than reversing them into row,column accidentally. All permitted routes have the same length, so no separate shortest-path search is needed.

Main complexity: O(MN) time, O(M+puddles) extra space.

### Alternative and trade-offs

Memoize path counts backwards from school through the upper and left cells. Boundaries and puddles contribute zero. This evaluates the recurrence on demand rather than iteratively.

Code: [alternative.py](alternative.py).

Complexity: O(MN), space O(MN).

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 등굣길](https://school.programmers.co.kr/learn/courses/30/lessons/42898) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 43개 입력에서 86회 검사를 통과했습니다.

Passed 86 implementation checks across 43 official, boundary and fixed-seed differential inputs.
