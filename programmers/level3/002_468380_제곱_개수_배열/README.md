# 제곱 개수 배열

[Level 3 목록 / Level 3 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/468380) · Level 3 · Python3

## 문제와 조건 / Task and conditions

arr 길이·각 값은 1~100000이고 펼친 배열 전체 합은 최대 10¹⁵입니다. 1≤l≤r≤Σarr이며 [l~r 합,같은 길이·합을 가진 구간 수]를 반환합니다.

Array length and values are each 1–100000; the expanded array’s total sum is at most 10¹⁵. With 1≤l≤r≤Σarr, return [sum on l…r,number of windows with equal length and sum].

## 풀이 흐름 / Approach

값 v가 v번 반복되는 큰 배열을 직접 만들지 않습니다. 각 묶음의 길이 합과 값의 합을 저장해 임의 접두부 합을 구합니다. 길이가 같은 창을 움직일 때 양끝이 같은 묶음 안에 있는 구간에서는 합이 등차수열입니다.

Do not materialize the array where value v repeats v times. Prefix lengths and weighted sums support prefix queries. While both window endpoints remain inside fixed runs, moving the window changes its sum by a constant slope.

## 정답이 되는 이유 / Why it works

창을 한 칸 옮길 때 빠지는 값과 들어오는 값은 묶음 경계 전까지 일정합니다. 따라서 해당 구간에서 target=current+slope·offset의 정수해를 세면 모든 시작 위치를 중복 없이 계산합니다.

Outgoing and incoming values stay constant until a run boundary. Counting integer solutions of target=current+slope·offset therefore counts every start position exactly once.

## 비용 / Complexity

묶음 n개에 시간 O(n), 공간 O(n), 이진 탐색 초기화 O(log n) / O(n) time and space, O(log n) initial searches

## 구현 / Implementation

[solution.py](solution.py)

```python
from bisect import bisect_right

def solution(arr, l, r):
    # 각 값 묶음의 끝 위치를 누적 저장.
    lengths = [0]
    sums = [0]
    for value in arr:
        # 값 value가 value번 등장하므로 전체 길이에 value 추가.
        lengths.append(lengths[-1] + value)
        sums.append(sums[-1] + value * value)

    def prefix(count):
        # count가 속하는 묶음을 이진 탐색.
        index = min(len(arr) - 1, bisect_right(lengths, count) - 1)
        return sums[index] + (count - lengths[index]) * arr[index]

    target = prefix(r) - prefix(l - 1)
    # 비교할 모든 구간의 길이.
    window = r - l + 1
    last_start = lengths[-1] - window
    # 시작 위치가 0인 첫 구간의 합.
    current = prefix(window)
    start = left = 0
    # 구간을 오른쪽으로 옮길 때 들어오는 원소의 묶음 번호.
    right = bisect_right(lengths, window) - 1
    answer = 0
    while start < last_start:
        # 나가는 값과 들어오는 값이 모두 일정한 이동 횟수.
        span = min(lengths[left + 1] - start, lengths[right + 1] - start - window, last_start - start)
        slope = arr[right] - arr[left]
        # 변화량 0이면 합이 계속 일정.
        if slope == 0:
            if current == target:
                # span개의 시작 위치를 한꺼번에 추가.
                answer += span
        else:
            difference = target - current
            # 정수 이동 횟수가 현재 구간 안에 있는지 and로 함께 검사.
            if difference % slope == 0 and 0 <= difference // slope < span:
                answer += 1
        current += slope * span
        # 시작점도 span만큼 이동.
        start += span
        if start == lengths[left + 1]:
            left += 1
        # 들어오는 원소도 현재 묶음 끝에 도달했는지 확인.
        if start + window == lengths[right + 1]:
            right += 1
    answer += int(current == target)
    return [target, answer]
```

## 다른 방법: 펼친 배열의 창 합 / Materialized-array sliding window

v를 v번 실제로 넣고 모든 같은 길이 창의 합을 비교합니다. 시간·공간이 Σarr에 비례하므로 작은 값의 무작위 검증에만 사용합니다.

Explicitly repeat v exactly v times and compare all equal-length window sums. Time and space scale with Σarr, so use it only for small-value randomized verification.

[alternative_reference.py](alternative_reference.py)

```python
def solution(arr, l, r):
    expanded = [value for value in arr for _ in range(value)]
    length = r - l + 1
    target = sum(expanded[l - 1:r])
    current = sum(expanded[:length])
    count = int(current == target)
    for end in range(length, len(expanded)):
        current += expanded[end] - expanded[end - length]
        count += current == target
    return [target, count]
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    [
      3,
      2,
      3,
      1,
      1
    ],
    5,
    7
  ],
  "output": [
    8,
    2
  ]
}
```

## 검증 / Verification

```bash
python verify.py
```

원본 채점 기록과 별도로 로컬 검증 34개를 통과했습니다. 검증 입력·예상 결과는 [cases.json](cases.json), 재현 코드는 [verify.py](verify.py), 실행 기록은 [verification.json](verification.json)에 있습니다.

Separately from the original grading record, 34 local cases passed. Inputs and expected results are in [cases.json](cases.json), the reproducer is [verify.py](verify.py), and the run record is [verification.json](verification.json).

비교 구현은 작은 입력 34개에서 함께 통과했습니다. 큰 입력용 제출 풀이와 전수 탐색 기준 코드는 파일명과 설명으로 구분합니다.

The comparison also passed 34 small-input cases. Exhaustive reference implementations are distinguished from the submission solution in their filenames and descriptions.

원본 채점 기록: 100점. [submitted_original.py](submitted_original.py)는 당시 원본 파일을 그대로 보존하며, `solution.py`는 설명을 정리한 구현입니다.

Original recorded grade: 100/100. [submitted_original.py](submitted_original.py) preserves the original file bytes; `solution.py` contains the documented implementation.

출처: [프로그래머스 문제 468380](https://school.programmers.co.kr/learn/courses/30/lessons/468380), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 468380](https://school.programmers.co.kr/learn/courses/30/lessons/468380), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.

큰 입력 검사: 펼치면 100억 원소인 상수 배열 / An implicit constant array of ten billion entries

```bash
python verify_stress.py
```
