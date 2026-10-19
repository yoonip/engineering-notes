# H-Index

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/42747) · Level 2 · Python3

## 문제와 조건 / Task and conditions

논문은 1~1000편, 인용 수는 0~10000입니다. 적어도 h편이 h회 이상 인용된 가장 큰 h를 반환합니다.

There are 1–1000 papers with 0–10000 citations. Return the largest h for which at least h papers have at least h citations.

## 풀이 흐름 / Approach

인용 수를 내림차순으로 정렬합니다. 앞에서 count번째 논문의 인용 수가 count 이상이면 앞의 count편 모두 그 기준을 만족합니다. 처음 조건을 어기기 전의 마지막 count가 답입니다.

Sort citations descending. If the count-th paper has at least count citations, the first count papers all satisfy that threshold. The last passing count is the answer.

## 왜 맞는가 / Why it works

내림차순에서 h번째 값이 h 이상인 것과 h편 이상이 h회 이상 인용된 것은 동치입니다. 조건이 한 번 깨지면 이후 값은 더 작고 순번은 더 커져 다시 만족할 수 없습니다.

In descending order, the h-th value being at least h is equivalent to at least h papers having h citations. After failure, values only decrease and ranks increase, so the condition cannot recover.

## 비용 / Complexity

시간 O(n log n), 정렬 공간 O(n) / O(n log n) time, O(n) sorting workspace

## 구현 / Implementation

이 구현은 입력 배열을 제자리에서 정렬하거나 힙으로 바꿉니다.

This implementation sorts or heapifies the input array in place.

[solution.py](solution.py)

```python
def solution(citations):
    # 많이 인용된 논문부터 배치.
    citations.sort(reverse=True)
    answer = 0
    for count, cited in enumerate(citations, 1):
        # 이 논문까지 count편이 count회 이상 인용되는지 검사.
        if cited < count:
            break
        answer = count
    return answer
```

## 다른 방법: 인용 수 버킷 누적 / Citation buckets

H-Index는 논문 수 n을 넘지 않습니다. n 이상 인용은 같은 버킷으로 묶고 뒤에서 누적하면 시간 O(n), 공간 O(n)에 구할 수 있습니다.

The H-index cannot exceed n papers. Cap larger citations at n and accumulate buckets backwards for O(n) time and O(n) space.

[alternative.py](alternative.py)

```python
def solution(citations):
    n = len(citations)
    counts = [0] * (n + 1)
    for value in citations:
        counts[min(value, n)] += 1
    papers = 0
    for h in range(n, -1, -1):
        papers += counts[h]
        if papers >= h:
            return h
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    [
      3,
      0,
      6,
      1,
      5
    ]
  ],
  "output": 3
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

출처: [프로그래머스 문제 42747](https://school.programmers.co.kr/learn/courses/30/lessons/42747), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 42747](https://school.programmers.co.kr/learn/courses/30/lessons/42747), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
