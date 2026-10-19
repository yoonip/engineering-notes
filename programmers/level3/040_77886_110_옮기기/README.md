# 110 옮기기

Level 3 · [77886 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/77886)

## 문제와 조건

각 이진 문자열에서 110 부분을 꺼내 원하는 위치에 다시 넣는 연산으로 만들 수 있는 사전순 최소 문자열을 구합니다.

`1≤len(s),len(s[i])≤1,000,000; 1≤Σlen(s[i])≤1,000,000`

## 풀이를 따라가기

1. 스택으로 110을 모두 추출한 뒤 남은 문자열의 마지막 0 바로 뒤, 즉 끝에 연속한 1들 앞에 몰아넣습니다.
2. 예: 1110에서 110을 빼면 1. 남은 0이 없으므로 맨 앞에 110을 넣어 1101이 됩니다.
3. 남은 0은 앞에 유지하고 110은 끝의 1보다 앞에 둬야 사전순으로 작아집니다. 시간·공간 O(전체 글자 수).

## 왜 이 방법으로 풀 수 있나

스택으로 110을 모두 추출한 뒤 남은 문자열의 마지막 0 바로 뒤, 즉 끝에 연속한 1들 앞에 몰아넣습니다.

시간·공간: 시간·공간 O(전체 글자 수).

## 다른 방법과 비교

110을 꺼내 다른 모든 위치에 넣은 문자열을 BFS로 모읍니다. 가능한 문자열 중 사전순 최솟값이 답입니다. 스택의 교환 논리를 짧은 문자열에서 직접 확인합니다.

| 항목 | 기본 풀이 | 문자열 상태 그래프 탐색 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간·공간 O(전체 글자 수). | 상태 수 S에서 O(SL²), 아주 짧은 문자열 비교용 |
| 용도 | 기본 제출 구현 | 작은 입력 비교·검증용 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[["1110", "100111100", "0111111010"]]` | `["1101", "100110110", "0110110111"]` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Find the lexicographically smallest binary string reachable by repeatedly moving a 110 block.

`1≤len(s),len(s[i])≤1,000,000; 1≤Σlen(s[i])≤1,000,000`

### Method and correctness

Remove every 110 block with a stack, including blocks newly exposed by a removal. Insert all removed blocks immediately after the last zero of the remaining string, or at the front if no zero remains. The remaining suffix is all ones, and placing 110 before that suffix gives the smallest reachable arrangement.

Main complexity: O(total characters) time and output space.

### Alternative and trade-offs

Explore all strings obtainable by removing a 110 block and reinserting it at every position. The lexicographically smallest reachable string checks the stack argument on short strings.

Code: [alternative.py](alternative.py). Scope: tiny-input oracle; not for maximum-size submissions.

Complexity: states Swith O(SL²), very-short-string oracle.

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 110 옮기기](https://school.programmers.co.kr/learn/courses/30/lessons/77886) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 42개 입력에서 84회 검사를 통과했습니다.

Passed 84 implementation checks across 42 official, boundary and fixed-seed differential inputs.
