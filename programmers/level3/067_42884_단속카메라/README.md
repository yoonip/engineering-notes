# 단속카메라

[Level 3 목록 / Level 3 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

Level 3 · [42884 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/42884)

## 문제와 조건

모든 차량이 진입·진출 구간 안에서 카메라를 적어도 한 번 만나도록 필요한 최소 카메라 수를 구합니다.

`1≤N≤10,000; −30,000≤entry≤exit≤30,000`

## 풀이를 따라가기

1. 진출 지점 순으로 정렬하고 아직 카메라를 만나지 않은 차량의 진출 지점에 새 카메라를 둡니다. 가능한 가장 뒤쪽에 두는 그리디 방식입니다.
2. 예: -15에 첫 카메라를 놓아 첫째·셋째 차량을, -5에 둘째 카메라를 놓아 둘째·넷째 차량을 단속합니다. 끝점도 포함하므로 >로 비교합니다.
3. 차량 수 N일 때 시간 O(N log N), 정렬 결과를 포함한 공간 O(N).

## 왜 이 방법으로 풀 수 있나

진출 지점 순으로 정렬하고 아직 카메라를 만나지 않은 차량의 진출 지점에 새 카메라를 둡니다. 가능한 가장 뒤쪽에 두는 그리디 방식입니다.

시간·공간: 시간 O(N log N), 정렬 결과를 포함한 공간 O(N).

## 다른 방법과 비교

차량의 진출 지점들 중 카메라를 둘 위치를 골라 모든 구간을 덮는지 검사합니다. 최적 카메라는 어느 구간의 오른쪽 끝으로 옮길 수 있다는 성질을 사용합니다.

| 항목 | 기본 풀이 | 카메라 후보 부분집합 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(N log N), 정렬 결과를 포함한 공간 O(N). | O(2^N N²), 작은 차량 수 비교용 |
| 용도 | 기본 제출 구현 | 작은 입력 비교·검증용 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[[[-20, -15], [-14, -5], [-18, -13], [-5, -3]]]` | `2` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Place the fewest cameras so every vehicle route contains at least one camera.

`1≤N≤10,000; −30,000≤entry≤exit≤30,000`

### Method and correctness

Sort routes by exit position. If the current camera lies before a route’s entry, install a new one at that route’s exit. Choosing the latest possible point covering the earliest-ending uncovered interval cannot reduce coverage of later intervals. Endpoints are inclusive.

Main complexity: O(N log N) time, O(N) sorting space.

### Alternative and trade-offs

Enumerate subsets of exit-point candidates and check interval coverage. An optimal camera can be shifted to an interval’s right endpoint without losing coverage.

Code: [alternative.py](alternative.py). Scope: tiny-input oracle; not for maximum-size submissions.

Complexity: O(2^N N²), small-route oracle.

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 단속카메라](https://school.programmers.co.kr/learn/courses/30/lessons/42884) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 42개 입력에서 84회 검사를 통과했습니다.

Passed 84 implementation checks across 42 official, boundary and fixed-seed differential inputs.
