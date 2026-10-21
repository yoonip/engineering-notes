# JadenCase 문자열 만들기

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/12951) · Level 2 · Python3

## 문제와 조건 / Task and conditions

문자열 길이는 1~200입니다. 영문·숫자·공백으로 이루어지고 숫자는 단어 첫 위치에만 있습니다. 연속 공백을 유지하면서 각 단어 첫 글자는 대문자, 나머지는 소문자로 만듭니다.

Length is 1–200 with letters, digits and spaces; digits occur only at word starts. Preserve repeated spaces, uppercase each first character and lowercase the rest.

## 풀이 흐름 / Approach

공백 한 개를 구분자로 나누면 연속 공백 사이의 빈 단어도 보존됩니다. 각 단어의 첫 글자는 대문자, 뒤는 소문자로 바꾸고 같은 공백으로 다시 합칩니다.

Splitting on the literal space preserves empty words between repeated spaces. Capitalize the first character and lowercase the rest of each word, then join with the same spaces.

## 정답이 되는 이유 / Why it works

명시적 공백 구분은 공백 개수와 위치를 보존합니다. capitalize는 숫자로 시작할 때도 나머지 문자를 소문자로 바꾸므로 문제의 단어 변환 규칙과 일치합니다.

Literal-space splitting preserves the number and location of spaces. capitalize also lowercases the remaining characters when a word begins with a digit, matching the specified rule.

## 비용 / Complexity

시간 O(n), 공간 O(n) / Time O(n), space O(n)

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(s):
    # 인수를 생략한 split()과 달리 연속·앞뒤 공백을 빈 원소로 보존.
    words = s.split(' ')
    changed = [word.capitalize() for word in words]
    return ' '.join(changed)
```

## 다른 방법: 단어 시작 상태를 문자별 추적 / Character-level word-start state

문자열을 나누지 않고 직전 문자가 공백인지 추적합니다. 공백을 그대로 출력하면서 단어 시작 문자만 대문자로 바꿉니다.

Track whether the previous character was a space without splitting. Emit spaces unchanged and uppercase only word-initial characters.

[alternative.py](alternative.py)

```python
def solution(s):
    output, first = [], True
    for ch in s:
        output.append(ch.upper() if first else ch.lower())
        first = ch == ' '
    return ''.join(output)
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    "3people unFollowed me"
  ],
  "output": "3people Unfollowed Me"
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

출처: [프로그래머스 문제 12951](https://school.programmers.co.kr/learn/courses/30/lessons/12951), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 12951](https://school.programmers.co.kr/learn/courses/30/lessons/12951), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
