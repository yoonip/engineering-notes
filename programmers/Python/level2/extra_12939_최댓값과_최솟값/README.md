# 최댓값과 최솟값

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/12939) · Level 2 · Python3

## 문제와 조건 / Task and conditions

공백으로 구분된 정수가 둘 이상 주어집니다. 수치상 최솟값과 최댓값을 공백 하나로 연결한 문자열을 반환합니다.

At least two space-separated integers are provided. Return the numerical minimum and maximum separated by one space.

## 풀이 흐름 / Approach

공백으로 구분된 숫자를 정수로 바꾼 뒤 최솟값과 최댓값을 찾습니다. 문자열 그대로 비교하면 음수나 자릿수가 다른 수에서 잘못된 순서가 되므로 정수 변환이 필요합니다.

Parse space-separated values as integers, then find the minimum and maximum. Comparing raw strings would misorder negative or differently sized numbers.

## 정답이 되는 이유 / Why it works

정수 비교는 문제의 수 크기와 일치합니다. 모든 입력에 min·max를 적용하고 작은 값부터 문자열로 출력하므로 요구 형식을 만족합니다.

Integer comparison matches numerical order. Taking min and max over every parsed input and formatting the smaller first gives the required result.

## 비용 / Complexity

시간 O(L), 공간 O(L) / O(L) time and space for input length L

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(s):
    # split은 공백으로 문자열 분리, map은 각 원소에 int 정수 변환 적용, list는 결과를 재사용 가능한 리스트로 저장.
    numbers = list(map(int, s.split()))
    return f'{min(numbers)} {max(numbers)}'
```

## 다른 방법: 정렬 후 양 끝 선택 / Sort and take endpoints

정수 목록을 정렬한 뒤 첫 값과 마지막 값을 고릅니다. 시간 O(n log n)이므로 두 최솟값·최댓값 순회보다 많은 일을 하지만 전체 순서를 확인할 수 있습니다.

Sort the integer list and take its endpoints. O(n log n) time does more work than min/max scans, but exposes the complete order.

[alternative.py](alternative.py)

```python
def solution(s):
    numbers = sorted(map(int, s.split()))
    return f'{numbers[0]} {numbers[-1]}'
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    "1 2 3 4"
  ],
  "output": "1 4"
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

출처: [프로그래머스 문제 12939](https://school.programmers.co.kr/learn/courses/30/lessons/12939), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 12939](https://school.programmers.co.kr/learn/courses/30/lessons/12939), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
