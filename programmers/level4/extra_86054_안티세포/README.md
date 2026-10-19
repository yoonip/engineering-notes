# 안티세포

Level 4 · `86054` · Python3 · [공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/86054)

[기본 풀이](solution.py) · [다른 풀이](alternative.py) · [예제 입력과 정답](examples.json) · [검증 코드](test_solution.py)

## 문제와 조건

양수 배열을 왼쪽부터 처리합니다. 새 원소가 든 세포와 바로 왼쪽 세포의 합이 같으면 합칠지 멈출지 고를 수 있습니다. 이 과정에서 남기는 서로 다른 합성 기록의 수를 구합니다.

입력 범위와 상수는 다음과 같습니다. 기호는 코드의 매개변수에 맞췄습니다.

`1≤len(a)≤200000; values:1..10^9; 1≤len(s)≤len(a); positive segment lengths summing to len(a); modulus 1000000007.`

## 풀이를 따라가기

같은 질량끼리 합치므로 오른쪽 세포의 질량은 두 배씩 커집니다. prefix sum과 그 위치를 저장하고, 앞 세포가 필요한 합성 깊이를 만들 수 있는지를 depth로 확인합니다.

양수 배열에서는 주어진 끝점과 질량에 대응하는 시작점이 유일합니다. 만들 수 있는 마지막 세포의 시작 위치마다 앞부분 dp를 더합니다. 각 세포 내부의 반반 질량 분할도 유일하므로 기록을 중복해서 세지 않습니다.

## 다른 방법과 비교

대안은 실제 세포 질량 스택에서 합치지 않는 분기·합치는 분기를 전부 따라갑니다. 구간 길이 14 이하의 과정 자체를 비교하며 큰 입력을 처리하는 풀이와 구분합니다.

| 구분 | 시간 | 추가 공간 |
|---|---|---|
| 기본 풀이 | `O(N log S), S=전체 질량/total mass` | `O(N)` |
| 대안 풀이 | `O(S·N)` | `O(S·N)` |

대안 비용에서 S는 저장되는 실제 스택 상태 수, N은 구간 길이입니다. 스택 튜플을 복사하고 해시하는 비용까지 포함하면 시간과 저장 공간의 상한은 O(S·N)입니다.

## 코드와 검증

`solution.py`에는 상태의 뜻과 경계조건을 한국어 주석으로 적었습니다. `alternative.py`는 별도의 풀이이며, `test_solution.py`에서 공식 예제와 생성 입력을 비교합니다. 실행 기록은 [validation.json](validation.json)에 있습니다. 원본 제출 파일은 [submitted_original.py](submitted_original.py)에 그대로 보관했습니다.

```bash
python test_solution.py
```

## English

### Problem and constraints

Process positive arrays from left to right. A current cell may merge with its immediate left neighbor only when their masses match. Count distinct merge-index records.

Input limits and constants, using the parameter names in the code:

`1≤len(a)≤200000; values:1..10^9; 1≤len(s)≤len(a); positive segment lengths summing to len(a); modulus 1000000007.`

### Following the solution

Repeated equal-mass merges double the current mass. Prefix-sum positions locate matching boundaries; depth records whether the preceding cell can realize the required merge level.

Positivity makes a boundary unique for a fixed endpoint and mass. Sum prefix DP counts for every feasible final cell. Its equal-mass internal split is also unique, preventing duplicate histories.

### Alternative and comparison

The alternative follows the actual mass stack and branches on merge versus stop. It is an independent process enumeration limited to segments of length fourteen.

The primary solution takes `O(N log S), S=total mass` time and `O(N)` additional space. The alternative takes `O(S·N)` time. Its additional space is `O(S·N)`.

For the alternative, S counts memoized stack states and N is segment length. Including tuple copying and hashing gives O(S·N) time and storage.

### Code and verification

Read `solution.py` for the primary implementation and `alternative.py` for the comparison. Comments explain states and boundary cases in Korean. Run `python test_solution.py` for the official examples and generated comparisons; [validation.json](validation.json) records the execution. The submitted source is preserved byte for byte in [submitted_original.py](submitted_original.py).

## 출처 / Source

- [Programmers — 안티세포](https://school.programmers.co.kr/learn/courses/30/lessons/86054): 문제 조건·입출력 예 확인 / problem constraints and examples checked on 2026-10-19.
