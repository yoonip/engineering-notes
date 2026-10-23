# 롤케이크 자르기

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/132265) · Level 2 · Python3

자른 양쪽의 토핑 종류 수가 같은 분할 위치를 셉니다.

## 조건과 입출력

입력 매개변수: `topping`. 반환값은 정수이며 아래 풀이의 조건을 만족하는 결과입니다.

- 1 ≤ topping의 길이 ≤ 1,000,000
- 1 ≤ topping의 원소 ≤ 10,000

## 풀이를 따라가기

오른쪽은 전체 토핑 빈도, 왼쪽은 빈 집합으로 시작합니다. 한 토핑씩 왼쪽으로 옮기며 오른쪽 빈도가 0이면 키를 지웁니다. 두 집합 크기가 같으면 셉니다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
from collections import Counter

def solution(topping):
    right = Counter(topping)
    left = set()
    answer = 0
    for value in topping:
        left.add(value)
        right[value] -= 1
        # 오른쪽에서 사라진 종류의 키도 지워 종류 수를 맞춘다.
        if right[value] == 0:
            del right[value]
        # 개수가 아니라 서로 다른 토핑 종류 수를 비교한다.
        if len(left) == len(right):
            answer += 1
    return answer
```

## 정답이 되는 이유

매 이동 뒤 왼쪽 집합은 잘린 앞부분의 종류, 오른쪽 키는 뒷부분의 종류와 정확히 같습니다. 따라서 크기 비교가 곧 조건 검사입니다.

평균 시간 O(N), 공간 O(U) / Expected time O(N), space O(U)

주의할 점: 총 토핑 수가 아니라 종류 수를 비교합니다. 마지막 오른쪽 빈 구간은 왼쪽과 종류 수가 같을 수 없습니다.

## 다른 방법: 접두·접미 종류 수 배열

```python
def solution(topping):
    n=len(topping)
    suffix=[0]*(n+1)
    seen=set()
    for i in range(n-1,-1,-1):
        seen.add(topping[i])
        suffix[i]=len(seen)
    seen=set()
    answer=0
    for i in range(n-1):
        seen.add(topping[i])
        answer+=len(seen)==suffix[i+1]
    return answer
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 오른쪽은 전체 토핑 빈도, 왼쪽은 빈 집합으로 시작합니다. 한 토핑씩 왼쪽으로 옮기며 오른쪽 빈도가 0이면 키를 지웁니다. 두 집합 크기가 같으면 셉니다. | 접두·접미 종류 수 배열 |
| 비용 | 평균 시간 O(N), 공간 O(U) / Expected time O(N), space O(U) | 시간 O(N), 공간 O(N+U) / Time O(N), space O(N+U) |

## 검증

공식 예제 2개와 생성 입력 70개를 로컬에서 확인했습니다. 생성 입력은 기본 풀이와 대안 풀이를 비교했습니다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함합니다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Count cut positions giving both pieces the same number of distinct toppings.

### Conditions and input/output

Input arguments: `topping`. The return value is an integer satisfying the task described below.

- 1 ≤ len(topping) ≤ 1000000; 1 ≤ topping[i] ≤ 10000

### Approach

Initialize all frequencies on the right and an empty set on the left. Move toppings one at a time, deleting a right key when its count reaches zero; compare distinct counts.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

After each move, the left set and right keys exactly represent the topping types in the two pieces.

평균 시간 O(N), 공간 O(U) / Expected time O(N), space O(U)

Boundary cases: Compare distinct-type counts, not item counts. An empty final right piece cannot match the nonempty left piece.

### Alternative: Prefix and suffix distinct-count arrays

시간 O(N), 공간 O(N+U) / Time O(N), space O(N+U)

### Verification

Local checks covered 2 official examples and 70 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 롤케이크 자르기](https://school.programmers.co.kr/learn/courses/30/lessons/132265) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
