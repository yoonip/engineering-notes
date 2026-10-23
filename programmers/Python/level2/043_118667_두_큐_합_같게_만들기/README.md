# 두 큐 합 같게 만들기

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/118667) · Level 2 · Python3

두 양수 큐의 앞 원소를 다른 큐 뒤로 옮겨 합을 같게 하는 최소 횟수를 구합니다.

## 조건과 입출력

입력 매개변수: `queue1, queue2`. 반환값은 정수이며 아래 풀이의 조건을 만족하는 결과입니다.

- 1 ≤ queue1의 길이 = queue2의 길이 ≤ 300,000
- 1 ≤ queue1의 원소, queue2의 원소 ≤ 10^9

## 풀이를 따라가기

전체 합이 홀수면 불가능합니다. 첫 큐 합이 목표보다 크면 첫 큐에서 빼고 작으면 두 번째 큐에서 가져옵니다. 큐 합을 매번 다시 더하지 않고 옮긴 값만 반영합니다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
from collections import deque

def solution(queue1, queue2):
    current = sum(queue1)
    total = current + sum(queue2)
    # 전체 합이 홀수이면 같은 정수 합 두 개로 나눌 수 없다.
    if total % 2:
        return -1
    target = total // 2
    first, second = deque(queue1), deque(queue2)
    for moves in range(2 * (len(queue1) + len(queue2)) + 1):
        if current == target:
            return moves
        # 양수이므로 합이 크면 빼고 작으면 가져온다.
        if current > target:
            value = first.popleft()
            second.append(value)
            current -= value
        else:
            value = second.popleft()
            first.append(value)
            current += value
    return -1
```

## 정답이 되는 이유

양수이므로 목표보다 큰 구간은 왼쪽을 줄여야 하고 작은 구간은 오른쪽을 늘려야 합니다. 두 큐를 원형 연속 구간으로 보면 포인터가 한 방향으로만 움직여 처음 맞춘 이동 수가 최소입니다.

시간 O(N), 공간 O(N) / Time and space O(N); N=두 큐 길이 합 / combined length

주의할 점: 전체 합은 큰 정수가 될 수 있습니다. 탐색 횟수 제한으로 불가능한 순환을 종료합니다.

## 다른 방법: 배열을 복사하지 않는 원형 투 포인터

```python
def solution(queue1,queue2):
    values=queue1+queue2
    n=len(values)
    target=sum(values)
    if target%2: return -1
    target//=2
    left,right=0,len(queue1)
    current=sum(queue1)
    for moves in range(2*n+1):
        if current==target: return moves
        if current>target:
            current-=values[left%n]
            left+=1
        else:
            current+=values[right%n]
            right+=1
    return -1
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 전체 합이 홀수면 불가능합니다. 첫 큐 합이 목표보다 크면 첫 큐에서 빼고 작으면 두 번째 큐에서 가져옵니다. 큐 합을 매번 다시 더하지 않고 옮긴 값만 반영합니다. | 배열을 복사하지 않는 원형 투 포인터 |
| 비용 | 시간 O(N), 공간 O(N) / Time and space O(N); N=두 큐 길이 합 / combined length | 시간 O(N), 공간 O(N) / Time and space O(N) |

## 검증

공식 예제 3개와 생성 입력 80개를 로컬에서 확인했습니다. 생성 입력은 기본 풀이와 대안 풀이를 비교했습니다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함합니다. 제한 상한에 해당하는 크기·수치의 경계 검사도 저장된 테스트에 포함했습니다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Find the fewest front-to-back transfers making two positive-valued queues have equal sums.

### Conditions and input/output

Input arguments: `queue1, queue2`. The return value is an integer satisfying the task described below.

- 1 ≤ len(queue1)=len(queue2) ≤ 300000; 1 ≤ values ≤ 10^9
- use wide integer sums when implementing in fixed-width languages

### Approach

Reject odd totals. If the first queue exceeds half the total, move its front out; otherwise bring in the second queue’s front. Update the running sum by the transferred value.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

With positive values, an oversized interval must shrink left and an undersized one must extend right. Viewing the queues as a circular contiguous interval gives monotone pointers and a minimum first matching transfer count.

시간 O(N), 공간 O(N) / Time and space O(N); N=두 큐 길이 합 / combined length

Boundary cases: The combined sum can be large. A bounded search terminates impossible cyclic cases.

### Alternative: Circular-array two pointers

시간 O(N), 공간 O(N) / Time and space O(N)

### Verification

Local checks covered 3 official examples and 80 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases. Saved tests also include a size or numeric boundary at the stated upper limit.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 두 큐 합 같게 만들기](https://school.programmers.co.kr/learn/courses/30/lessons/118667) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
