# 문자열 압축

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/60057) · Level 2 · Python3

## 문제와 조건 / Task and conditions

소문자 문자열 길이는 1~1000입니다. 앞에서 고정 길이로 나눈 연속 반복만 압축하고 가장 짧은 결과 길이를 반환합니다.

The lowercase string has length 1–1000. Compress consecutive equal fixed-width chunks from the beginning and return the minimum encoded length.

## 풀이 흐름 / Approach

자르는 단위 길이를 하나씩 바꾸며 앞에서부터 같은 조각이 연속으로 몇 번 나오는지 셉니다. 한 번 나온 조각에는 숫자 1을 붙이지 않습니다. 마지막의 짧은 조각도 길이에 포함합니다.

Try every chunk width and count consecutive equal chunks from the beginning. A single chunk has no count prefix. Include any shorter trailing chunk in the encoded length.

## 정답이 되는 이유 / Why it works

압축은 앞에서 고정 길이로 나눈 조각의 연속 묶음으로 결정됩니다. 같은 묶음을 한 번씩 정확히 계산하고 모든 유효한 단위 길이를 비교하므로 최소 길이를 얻습니다.

For a fixed width the run groups are uniquely determined. Counting every group exactly once and taking the minimum over all useful widths yields the optimum.

## 비용 / Complexity

시간 O(n²), 추가 공간 O(n) / Time O(n²), auxiliary space O(n)

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(s):
    # 압축하지 않은 길이로 최솟값 초기화.
    answer = len(s)
    for size in range(1, len(s) // 2 + 1):
        # 끝은 미포함.
        previous = s[:size]
        count, length = 1, 0
        # range(시작,끝,간격)으로 다음 조각 시작점 순회.
        for start in range(size, len(s), size):
            current = s[start:start + size]
            # 이전 조각과 연속 반복인지 검사.
            if current == previous:
                count += 1
            else:
                length += len(previous) + (len(str(count)) if count > 1 else 0)
                # 새 조각으로 기준을 바꾸고 반복 수 1로 초기화.
                previous, count = current, 1
        length += len(previous) + (len(str(count)) if count > 1 else 0)
        # 단위 길이별 결과 비교.
        answer = min(answer, length)
    return answer
```

## 다른 방법: groupby로 실제 압축 문자열 만들기 / Materialize the encoding with groupby

연속 묶음을 라이브러리로 구분하고 압축 문자열을 직접 만듭니다. 이해와 결과 확인이 쉽지만 길이만 세는 주 풀이보다 임시 문자열이 더 많습니다.

Use groupby to identify runs and build the actual compressed string. This makes the encoding visible but allocates more temporary strings than the length-only main solution.

[alternative.py](alternative.py)

```python
from itertools import groupby

def solution(s):
    answer = len(s)
    for width in range(1, len(s) // 2 + 1):
        chunks = [s[i:i + width] for i in range(0, len(s), width)]
        encoded = []
        for chunk, group in groupby(chunks):
            count = sum(1 for _ in group)
            encoded.append((str(count) if count > 1 else '') + chunk)
        answer = min(answer, len(''.join(encoded)))
    return answer
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    "aabbaccc"
  ],
  "output": 7
}
```

## 검증 / Verification

```bash
python verify.py
```

원본 채점 기록과 별도로 로컬 검증 33개를 통과했습니다. 검증 입력·예상 결과는 [cases.json](cases.json), 재현 코드는 [verify.py](verify.py), 실행 기록은 [verification.json](verification.json)에 있습니다.

Separately from the original grading record, 33 local cases passed. Inputs and expected results are in [cases.json](cases.json), the reproducer is [verify.py](verify.py), and the run record is [verification.json](verification.json).

비교 구현은 작은 입력 33개에서 함께 통과했습니다. 큰 입력용 제출 풀이와 전수 탐색 기준 코드는 파일명과 설명으로 구분합니다.

The comparison also passed 33 small-input cases. Exhaustive reference implementations are distinguished from the submission solution in their filenames and descriptions.

원본 채점 기록: 100점. [submitted_original.py](submitted_original.py)는 당시 원본 파일을 그대로 보존하며, `solution.py`는 설명을 정리한 구현입니다.

Original recorded grade: 100/100. [submitted_original.py](submitted_original.py) preserves the original file bytes; `solution.py` contains the documented implementation.

출처: [프로그래머스 문제 60057](https://school.programmers.co.kr/learn/courses/30/lessons/60057), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 60057](https://school.programmers.co.kr/learn/courses/30/lessons/60057), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
