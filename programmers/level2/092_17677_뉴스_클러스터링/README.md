# [1차] 뉴스 클러스터링

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/17677) · Level 2 · Python3

## 문제와 조건 / Task and conditions

두 문자열 길이는 2~1000입니다. 영문자 인접 두 글자만 대소문자 없이 다중집합으로 사용합니다. 교집합/합집합×65536의 내림값이며 두 집합이 비면 65536입니다.

Both strings have length 2–1000. Form case-insensitive multisets of adjacent English-letter pairs. Return floor(intersection/union×65536), or 65536 when both are empty.

## 풀이 흐름 / Approach

영문자 두 글자로 된 인접 조각만 소문자로 모읍니다. 같은 조각이 여러 번 나온 횟수도 중요하므로 집합이 아니라 Counter를 씁니다. 교집합은 빈도의 최솟값, 합집합은 최댓값의 합입니다.

Collect lowercase adjacent two-letter fragments containing only English letters. Use multiplicities rather than a set. Multiset intersection sums minimum counts; union sums maximum counts.

## 왜 맞는가 / Why it works

각 조각별 min·max가 다중집합 교집합·합집합의 정의입니다. 독립 조각의 빈도를 합쳐 비율을 구하며, 합집합이 비면 문제의 특별 규칙으로 65536을 반환합니다.

Per-fragment minima and maxima are exactly multiset intersection and union multiplicities. Sum them and scale the ratio; an empty union follows the special result 65536.

## 비용 / Complexity

시간 O(|s₁|+|s₂|), 공간 O(1): 영문자 쌍 최대 676종 / Linear time, O(1) space over at most 676 letter pairs

## 구현 / Implementation

[solution.py](solution.py)

```python
from collections import Counter

def solution(str1, str2):
    def pairs(text):
        # 대소문자 구분 제거.
        text = text.lower()
        return Counter(text[i:i + 2] for i in range(len(text) - 1) if 'a' <= text[i] <= 'z' and 'a' <= text[i + 1] <= 'z')
    first, second = pairs(str1), pairs(str2)
    # values는 개수, sum은 합계.
    intersection = sum((first & second).values())
    union = sum((first | second).values())
    return 65536 if union == 0 else intersection * 65536 // union
```

## 다른 방법: 정렬한 조각의 두 포인터 / Two pointers over sorted fragments

조각을 정렬하고 같은 값이면 두 목록에서 동시에, 다르면 작은 쪽만 진행합니다. 빈도표 대신 정렬을 사용해 시간 O(n log n), 공간 O(n)입니다.

Sort fragments and merge them with two pointers, advancing both on equality and the smaller side otherwise. This replaces a frequency map with O(n log n) sorting and O(n) space.

[alternative.py](alternative.py)

```python
def solution(str1, str2):
    def chunks(text):
        text = text.lower()
        return sorted(text[i:i + 2] for i in range(len(text) - 1)
                      if all('a' <= ch <= 'z' for ch in text[i:i + 2]))
    a, b = chunks(str1), chunks(str2)
    i = j = overlap = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            overlap += 1
            i += 1
            j += 1
        elif a[i] < b[j]:
            i += 1
        else:
            j += 1
    union = len(a) + len(b) - overlap
    return 65536 if union == 0 else overlap * 65536 // union
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    "FRANCE",
    "french"
  ],
  "output": 16384
}
```

## 검증 / Verification

```bash
python verify.py
```

원본 채점 기록과 별도로 로컬 검증 32개를 통과했습니다. 검증 입력·예상 결과는 [cases.json](cases.json), 재현 코드는 [verify.py](verify.py), 실행 기록은 [verification.json](verification.json)에 있습니다.

Separately from the original grading record, 32 local cases passed. Inputs and expected results are in [cases.json](cases.json), the reproducer is [verify.py](verify.py), and the run record is [verification.json](verification.json).

비교 구현은 작은 입력 32개에서 함께 통과했습니다. 큰 입력용 제출 풀이와 전수 탐색 기준 코드는 파일명과 설명으로 구분합니다.

The comparison also passed 32 small-input cases. Exhaustive reference implementations are distinguished from the submission solution in their filenames and descriptions.

원본 채점 기록: 100점. [submitted_original.py](submitted_original.py)는 당시 원본 파일을 그대로 보존하며, `solution.py`는 설명을 정리한 구현입니다.

Original recorded grade: 100/100. [submitted_original.py](submitted_original.py) preserves the original file bytes; `solution.py` contains the documented implementation.

출처: [프로그래머스 문제 17677](https://school.programmers.co.kr/learn/courses/30/lessons/17677), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 17677](https://school.programmers.co.kr/learn/courses/30/lessons/17677), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
