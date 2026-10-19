# [3차] 파일명 정렬

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/17686) · Level 2 · Python3

## 문제와 조건 / Task and conditions

파일은 최대 1000개, 길이는 최대 100자입니다. 영문자로 시작해 숫자를 포함하며 HEAD는 대소문자 무시, NUMBER는 최대 5자리 정수입니다. 두 키 동률이면 원래 순서를 유지합니다.

There are at most 1000 filenames of at most 100 characters, starting with a letter and containing digits. Compare HEAD case-insensitively, NUMBER as an integer of at most five digits, and preserve input order on ties.

## 풀이 흐름 / Approach

파일명 앞부분 HEAD는 대소문자를 무시하고 비교합니다. 이어지는 최대 다섯 자리 NUMBER는 정수로 비교합니다. 나머지 TAIL은 정렬 기준이 아니며 동률은 원래 순서를 유지합니다.

Compare the leading HEAD case-insensitively, then the following NUMBER of at most five digits numerically. TAIL is not part of the key; ties retain their original order.

## 정답이 되는 이유 / Why it works

정렬 키가 문제의 우선순위인 (소문자 HEAD, 정수 NUMBER)와 정확히 같습니다. Python의 안정 정렬은 두 키가 같을 때 입력 순서를 보존합니다.

The key is exactly the required pair (lowercase HEAD, integer NUMBER). Python’s stable sort preserves the input order when both components tie.

## 비용 / Complexity

최대 파일 길이 d에 시간 O(nd log n), 공간 O(nd) / O(nd log n) time, O(nd) space

## 구현 / Implementation

[solution.py](solution.py)

```python
from re import match

def solution(files):
    def key(filename):
        # () 캡처를 groups로 꺼내 언패킹.
        head, number = match(r'(\D+)(\d{1,5})', filename).groups()
        return (head.lower(), int(number))
    return sorted(files, key=key)
```

## 다른 방법: 직접 파싱과 두 번의 안정 정렬 / Manual parsing and two stable sorts

정규식 없이 처음 숫자 위치를 찾고 다섯 자리까지 읽습니다. NUMBER로 먼저, HEAD로 나중에 안정 정렬하면 같은 복합 키 순서를 얻습니다.

Find the first digit manually and read at most five digits. Stable sorting by NUMBER and then by HEAD produces the same compound order.

[alternative.py](alternative.py)

```python
def solution(files):
    parsed = []
    for filename in files:
        start = next(i for i, ch in enumerate(filename) if '0' <= ch <= '9')
        end = start
        while end < len(filename) and end < start + 5 and filename[end].isdigit():
            end += 1
        parsed.append((filename[:start].lower(), int(filename[start:end]), filename))
    parsed.sort(key=lambda item: item[1])
    parsed.sort(key=lambda item: item[0])
    return [item[2] for item in parsed]
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    [
      "img12.png",
      "img10.png",
      "img02.png",
      "img1.png",
      "IMG01.GIF",
      "img2.JPG"
    ]
  ],
  "output": [
    "img1.png",
    "IMG01.GIF",
    "img02.png",
    "img2.JPG",
    "img10.png",
    "img12.png"
  ]
}
```

## 검증 / Verification

```bash
python verify.py
```

원본 채점 기록과 별도로 로컬 검증 30개를 통과했습니다. 검증 입력·예상 결과는 [cases.json](cases.json), 재현 코드는 [verify.py](verify.py), 실행 기록은 [verification.json](verification.json)에 있습니다.

Separately from the original grading record, 30 local cases passed. Inputs and expected results are in [cases.json](cases.json), the reproducer is [verify.py](verify.py), and the run record is [verification.json](verification.json).

비교 구현은 작은 입력 30개에서 함께 통과했습니다. 큰 입력용 제출 풀이와 전수 탐색 기준 코드는 파일명과 설명으로 구분합니다.

The comparison also passed 30 small-input cases. Exhaustive reference implementations are distinguished from the submission solution in their filenames and descriptions.

원본 채점 기록: 100점. [submitted_original.py](submitted_original.py)는 당시 원본 파일을 그대로 보존하며, `solution.py`는 설명을 정리한 구현입니다.

Original recorded grade: 100/100. [submitted_original.py](submitted_original.py) preserves the original file bytes; `solution.py` contains the documented implementation.

출처: [프로그래머스 문제 17686](https://school.programmers.co.kr/learn/courses/30/lessons/17686), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 17686](https://school.programmers.co.kr/learn/courses/30/lessons/17686), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
