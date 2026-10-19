# 숫자 타자 대회

Level 3 · [136797 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/136797)

## 문제와 조건

처음 4·6에 놓인 두 손가락으로 숫자 문자열을 입력하는 최소 가중 이동 비용을 구합니다. 두 손은 같은 키에 놓일 수 없습니다.

`1≤len(numbers)≤100,000; digits∈{0,…,9}`

## 풀이를 따라가기

1. 두 손가락의 위치가 같을 수 없다는 조건을 지키며, 다음 숫자를 왼손·오른손으로 누르는 두 선택을 DP로 비교합니다.
2. 이동 비용은 가능한 대각선을 3씩, 나머지 직선을 2씩 더하며 같은 키는 1입니다. 각 글자 직후에는 한 손이 그 글자 위에 있어 가능한 상태 수가 제한됩니다. 전체 시간 O(100L), 상태 공간 O(100) 이내입니다.
3. 예: 이미 오른손이 6에 있을 때 6을 누르면 반드시 오른손으로 비용 1을 지불합니다. 다른 손을 6으로 옮기는 선택은 금지합니다.

## 왜 이 방법으로 풀 수 있나

두 손가락의 위치가 같을 수 없다는 조건을 지키며, 다음 숫자를 왼손·오른손으로 누르는 두 선택을 DP로 비교합니다.

시간·공간: 시간 O(100L), 상태 공간 O(100) 이내입니다.

## 다른 방법과 비교

다음 숫자와 양손 위치를 재귀 상태로 둡니다. 남은 문자열의 최저 비용을 반환하므로 앞에서부터 비용을 누적하는 기본 DP와 방향이 반대입니다. 긴 문자열의 제출에는 반복 DP가 안전합니다.

| 항목 | 기본 풀이 | 메모이제이션 재귀 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(100L), 상태 공간 O(100) 이내입니다. | O(100L), 공간 O(100L), 짧은 문자열 비교용 |
| 용도 | 기본 제출 구현 | 작은 입력 비교·검증용 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `["1756"]` | `10` |
| `["5123"]` | `8` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Find the minimum weighted cost of typing digits with fingers initially on 4 and 6; fingers may not occupy the same key.

`1≤len(numbers)≤100,000; digits∈{0,…,9}`

### Method and correctness

DP states are the positions of the left and right fingers. For each digit, either finger may press it unless the other finger already occupies that key. Staying costs one; diagonal moves cost three and remaining straight moves cost two each. Keep only the smallest cost per finger pair, since future costs depend only on those positions.

Main complexity: O(100L) time, O(100) states.

### Alternative and trade-offs

Memoize the minimum future cost by index and both finger positions. This runs backwards conceptually compared with forward DP; the iterative version avoids recursion depth problems on long inputs.

Code: [alternative.py](alternative.py). Scope: tiny-input oracle; not for maximum-size submissions.

Complexity: O(100L), space O(100L), short-string oracle.

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 숫자 타자 대회](https://school.programmers.co.kr/learn/courses/30/lessons/136797) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 44개 입력에서 88회 검사를 통과했습니다.

Passed 88 implementation checks across 44 official, boundary and fixed-seed differential inputs.
