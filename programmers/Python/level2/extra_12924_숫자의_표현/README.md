# 숫자의 표현

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/12924) · Level 2 · Python3

## 문제와 조건 / Task and conditions

1≤n≤10000입니다. 하나 이상의 연속한 양의 정수 합으로 n을 만드는 방법 수를 반환합니다.

1≤n≤10000. Count representations of n as a sum of one or more consecutive positive integers.

## 풀이 흐름 / Approach

연속한 양의 정수의 개수를 length라고 두면 합은 length×시작값+length(length−1)/2입니다. 이 식에서 시작값이 양의 정수로 나오는 길이만 셉니다.

For length consecutive positive integers, the sum is length×start+length(length−1)/2. Count lengths for which solving this equation yields a positive integer start.

## 정답이 되는 이유 / Why it works

최소 합은 1+…+length이므로 이 값이 n보다 큰 길이는 불가능합니다. 가능한 각 길이에 시작값은 하나뿐이므로 나머지가 0인지 확인하는 것만으로 정확히 셉니다.

The minimum sum for a length is 1+…+length, which bounds the search. Each feasible length has a unique starting value, so divisibility counts exactly the representations.

## 비용 / Complexity

시간 O(√n), 공간 O(1) / O(√n) time, O(1) space

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(n):
    # 연속 구간 길이와 가능한 방법 수 초기화.
    length, answer = 1, 0
    while length * (length + 1) // 2 <= n:
        # 증가분을 먼저 빼 시작값 곱만 남김.
        remaining = n - length * (length - 1) // 2
        if remaining % length == 0:
            answer += 1
        length += 1
    return answer
```

## 다른 방법: 양끝 포인터 구간 합 / Sliding window sum

오른쪽 끝을 늘려 합을 키우고 n을 넘으면 왼쪽 끝을 줄입니다. 양의 수이므로 한쪽 이동마다 합이 단조롭게 바뀌며 시간 O(n), 공간 O(1)입니다.

Increase the right endpoint to grow the sum and move the left endpoint while it exceeds n. Positivity makes each adjustment monotone; time is O(n), space O(1).

[alternative.py](alternative.py)

```python
def solution(n):
    left, total, answer = 1, 0, 0
    for right in range(1, n + 1):
        total += right
        while total > n:
            total -= left
            left += 1
        answer += total == n
    return answer
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    15
  ],
  "output": 4
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

출처: [프로그래머스 문제 12924](https://school.programmers.co.kr/learn/courses/30/lessons/12924), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 12924](https://school.programmers.co.kr/learn/courses/30/lessons/12924), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
