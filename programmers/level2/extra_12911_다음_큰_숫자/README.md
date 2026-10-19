# 다음 큰 숫자

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/12911) · Level 2 · Python3

## 문제와 조건 / Task and conditions

1≤n≤1000000입니다. n보다 크고 이진 표현의 1 개수가 같은 수 중 최솟값을 반환합니다.

1≤n≤1000000. Return the smallest integer greater than n with the same binary population count.

## 풀이 흐름 / Approach

가장 낮은 1비트를 더해 오른쪽 끝의 연속 1 묶음에 올림을 만듭니다. 올림으로 사라진 나머지 1들은 가장 낮은 자리로 모읍니다. 같은 1 개수를 유지하는 가장 가까운 큰 수입니다.

Add the lowest set bit to carry through the rightmost run of ones. Move the remaining displaced ones to the lowest positions, obtaining the nearest larger integer with the same one-bit count.

## 왜 맞는가 / Why it works

더 큰 수를 만들 때 바뀌는 최상위 자리는 가능한 낮아야 합니다. 그 자리를 1로 올린 뒤 남은 1을 오른쪽 끝에 배치하면 그 접두부 아래에서 최솟값이 됩니다.

The highest changed bit must be as low as possible to make the smallest increase. Raising that bit and packing the remaining ones at the bottom minimizes the suffix.

## 비용 / Complexity

정수 비트 연산 횟수 O(1), 비트 길이 b의 실제 비용 O(b) / O(1) bit operations; O(b) actual work for b-bit integers

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(n):
    # 예: 78의 1001110에서 10을 추출.
    lowest = n & -n
    raised = n + lowest
    # 올리면서 빠진 나머지 1들을 오른쪽 끝으로 모음.
    tail = ((n ^ raised) >> 2) // lowest
    return raised | tail
```

## 다른 방법: 다음 수부터 1비트 수 비교 / Scan integers by population count

n+1부터 1 개수가 같을 때까지 검사합니다. 비트 공식을 독립적으로 검증하기 쉽지만 답까지의 간격에 따라 반복 횟수가 늘어납니다.

Scan upward from n+1 until the population count matches. It independently checks the bit formula, but the number of iterations depends on the gap to the answer.

[alternative.py](alternative.py)

```python
def solution(n):
    required = n.bit_count()
    candidate = n + 1
    while candidate.bit_count() != required:
        candidate += 1
    return candidate
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    78
  ],
  "output": 83
}
```

## 검증 / Verification

```bash
python verify.py
```

원본 채점 기록과 별도로 로컬 검증 40개를 통과했습니다. 검증 입력·예상 결과는 [cases.json](cases.json), 재현 코드는 [verify.py](verify.py), 실행 기록은 [verification.json](verification.json)에 있습니다.

Separately from the original grading record, 40 local cases passed. Inputs and expected results are in [cases.json](cases.json), the reproducer is [verify.py](verify.py), and the run record is [verification.json](verification.json).

비교 구현은 작은 입력 40개에서 함께 통과했습니다. 큰 입력용 제출 풀이와 전수 탐색 기준 코드는 파일명과 설명으로 구분합니다.

The comparison also passed 40 small-input cases. Exhaustive reference implementations are distinguished from the submission solution in their filenames and descriptions.

원본 채점 기록: 100점. [submitted_original.py](submitted_original.py)는 당시 원본 파일을 그대로 보존하며, `solution.py`는 설명을 정리한 구현입니다.

Original recorded grade: 100/100. [submitted_original.py](submitted_original.py) preserves the original file bytes; `solution.py` contains the documented implementation.

출처: [프로그래머스 문제 12911](https://school.programmers.co.kr/learn/courses/30/lessons/12911), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 12911](https://school.programmers.co.kr/learn/courses/30/lessons/12911), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
