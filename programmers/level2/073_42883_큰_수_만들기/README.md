# 큰 수 만들기

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/42883) · Level 2 · Python3

## 문제와 조건 / Task and conditions

숫자는 2~1000000자리이고 1≤k<자릿수입니다. 남은 숫자의 순서는 바꿀 수 없으며 정확히 k자리를 지운 가장 큰 수를 문자열로 반환합니다.

The number has 2–1000000 digits and 1≤k<length. Preserve relative order, remove exactly k digits, and return the largest remaining number as text.

## 풀이 흐름 / Approach

앞자리 숫자가 클수록 전체 숫자가 커집니다. 새 숫자가 스택 마지막보다 크고 삭제 기회가 남아 있으면 작은 앞자리를 지웁니다. 끝까지 삭제가 남으면 뒤에서 지웁니다.

Earlier digits dominate the resulting number. While deletions remain, remove smaller stack-tail digits before appending a larger digit; remove any leftover deletions from the end.

## 정답이 되는 이유 / Why it works

같은 길이의 수는 첫 다른 자리로 대소가 정해집니다. 뒤의 큰 숫자를 앞으로 당길 수 있는데 작은 앞자리를 남기는 선택은 최적일 수 없습니다. 각 숫자는 한 번 들어가고 최대 한 번 나옵니다.

Equal-length numbers are ordered by their first differing digit. Keeping a smaller earlier digit when a larger one can replace it cannot be optimal. Each digit is pushed once and popped at most once.

## 비용 / Complexity

시간 O(n), 공간 O(n) / Time O(n), space O(n)

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(number, k):
    stack = []
    # 숫자 문자를 왼쪽부터 순회.
    for digit in number:
        while k > 0 and stack and stack[-1] < digit:
            stack.pop()
            k -= 1
        # 같은 자리 문자 비교는 숫자 크기 순서와 같음.
        stack.append(digit)
    if k > 0:
        stack = stack[:-k]
    return ''.join(stack)
```

## 다른 방법: 선택 가능한 구간의 최댓값 / Greedy maximum in each selectable window

남겨야 할 다음 자리마다 뒤에 필요한 자릿수를 확보하는 범위에서 가장 큰 숫자를 고릅니다. 스택보다 직관적이지만 반복 최댓값 탐색으로 시간 O(n²)까지 걸려 작은 입력 대조에 적합합니다.

Choose the largest feasible next digit while leaving enough suffix digits. This is intuitive but repeated scans can take O(n²), so it is a small-input comparison.

[alternative_reference.py](alternative_reference.py)

```python
def solution(number, k):
    keep = len(number) - k
    start = 0
    output = []
    for remaining in range(keep, 0, -1):
        stop = len(number) - remaining + 1
        best = max(range(start, stop), key=number.__getitem__)
        output.append(number[best])
        start = best + 1
    return ''.join(output)
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    "1924",
    2
  ],
  "output": "94"
}
```

## 검증 / Verification

```bash
python verify.py
```

원본 채점 기록과 별도로 로컬 검증 31개를 통과했습니다. 검증 입력·예상 결과는 [cases.json](cases.json), 재현 코드는 [verify.py](verify.py), 실행 기록은 [verification.json](verification.json)에 있습니다.

Separately from the original grading record, 31 local cases passed. Inputs and expected results are in [cases.json](cases.json), the reproducer is [verify.py](verify.py), and the run record is [verification.json](verification.json).

비교 구현은 작은 입력 31개에서 함께 통과했습니다. 큰 입력용 제출 풀이와 전수 탐색 기준 코드는 파일명과 설명으로 구분합니다.

The comparison also passed 31 small-input cases. Exhaustive reference implementations are distinguished from the submission solution in their filenames and descriptions.

원본 채점 기록: 100점. [submitted_original.py](submitted_original.py)는 당시 원본 파일을 그대로 보존하며, `solution.py`는 설명을 정리한 구현입니다.

Original recorded grade: 100/100. [submitted_original.py](submitted_original.py) preserves the original file bytes; `solution.py` contains the documented implementation.

출처: [프로그래머스 문제 42883](https://school.programmers.co.kr/learn/courses/30/lessons/42883), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 42883](https://school.programmers.co.kr/learn/courses/30/lessons/42883), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.

큰 입력 검사: 100만 자리의 앞부분 제거 / Remove the first half of a million-digit input

```bash
python verify_stress.py
```
