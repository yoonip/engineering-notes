# 더 맵게

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/42626) · Level 2 · Python3

## 문제와 조건 / Task and conditions

음식은 2~1000000개, 값은 0~1000000이고 K는 0~1000000000입니다. 최소 두 값을 a,b로 꺼내 a+2b를 넣으며 최소 혼합 횟수 또는 불가능 시 −1을 반환합니다.

There are 2–1000000 values in [0,1000000], with K in [0,1000000000]. Replace the two smallest values a,b by a+2b; return the mixing count or −1 if impossible.

## 풀이 흐름 / Approach

매번 가장 맵지 않은 두 음식을 꺼내 섞어야 하므로 최소 힙을 사용합니다. 최솟값이 K 이상이면 다른 음식도 모두 조건을 만족합니다. 한 음식만 남았는데 부족하면 불가능합니다.

A min-heap supplies the two least spicy foods at each step. Once the minimum reaches K, all foods qualify. If a single insufficient food remains, the task is impossible.

## 정답이 되는 이유 / Why it works

heap의 뿌리는 항상 남은 음식의 최솟값입니다. 문제에서 정한 혼합을 그대로 반복하며 최솟값으로 종료 조건을 판정하므로 필요한 혼합 횟수가 정확합니다.

The heap root is always the smallest remaining food. Each operation exactly follows the required mixing rule, and the minimum provides the correct stopping test.

## 비용 / Complexity

시간 O(n log n), 공간 O(n); heapify O(n) / O(n log n) time, O(n) space; O(n) heap construction

## 구현 / Implementation

이 구현은 입력 배열을 제자리에서 정렬하거나 힙으로 바꿉니다.

This implementation sorts or heapifies the input array in place.

[solution.py](solution.py)

```python
from heapq import heapify, heappop, heappush

def solution(scoville, K):
    # 인덱스 0이 항상 최솟값.
    heapify(scoville)
    answer = 0
    while scoville[0] < K:
        # 음식이 하나면 더 섞을 수 없음.
        if len(scoville) < 2:
            return -1
        first = heappop(scoville)
        # 남은 것 중 가장 작은 음식, 즉 원래 둘째 음식 꺼내기.
        second = heappop(scoville)
        heappush(scoville, first + second * 2)
        answer += 1
    return answer
```

## 다른 방법: 정렬 배열과 이진 삽입 / Sorted list with binary insertion

정렬한 배열의 앞 두 수를 꺼내고 섞은 수를 정렬 위치에 넣습니다. 같은 규칙을 직접 볼 수 있지만 배열 이동 때문에 시간 O(n²)까지 걸려 작은 입력 검증에만 사용합니다.

Take the first two values from a sorted list and insert the mixture with bisect. It follows the same rule but element shifts make it O(n²), so it is a small-input oracle.

[alternative_reference.py](alternative_reference.py)

```python
from bisect import insort

def solution(scoville, K):
    values = sorted(scoville)
    answer = 0
    while values[0] < K:
        if len(values) < 2:
            return -1
        first, second = values.pop(0), values.pop(0)
        insort(values, first + 2 * second)
        answer += 1
    return answer
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    [
      1,
      2,
      3,
      9,
      10,
      12
    ],
    7
  ],
  "output": 2
}
```

## 검증 / Verification

```bash
python verify.py
```

원본 채점 기록과 별도로 로컬 검증 29개를 통과했습니다. 검증 입력·예상 결과는 [cases.json](cases.json), 재현 코드는 [verify.py](verify.py), 실행 기록은 [verification.json](verification.json)에 있습니다.

Separately from the original grading record, 29 local cases passed. Inputs and expected results are in [cases.json](cases.json), the reproducer is [verify.py](verify.py), and the run record is [verification.json](verification.json).

비교 구현은 작은 입력 29개에서 함께 통과했습니다. 큰 입력용 제출 풀이와 전수 탐색 기준 코드는 파일명과 설명으로 구분합니다.

The comparison also passed 29 small-input cases. Exhaustive reference implementations are distinguished from the submission solution in their filenames and descriptions.

원본 채점 기록: 100점. [submitted_original.py](submitted_original.py)는 당시 원본 파일을 그대로 보존하며, `solution.py`는 설명을 정리한 구현입니다.

Original recorded grade: 100/100. [submitted_original.py](submitted_original.py) preserves the original file bytes; `solution.py` contains the documented implementation.

출처: [프로그래머스 문제 42626](https://school.programmers.co.kr/learn/courses/30/lessons/42626), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 42626](https://school.programmers.co.kr/learn/courses/30/lessons/42626), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.

큰 입력 검사: 100만 개 0의 불가능 판정 / One million zero values remain insufficient

```bash
python verify_stress.py
```
