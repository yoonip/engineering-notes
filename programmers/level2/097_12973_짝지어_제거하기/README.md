# 짝지어 제거하기

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/12973) · Level 2 · Python3

## 문제와 조건 / Task and conditions

소문자 문자열 길이는 1~1000000입니다. 같은 글자 인접 쌍을 반복 제거해 전부 없앨 수 있으면 1, 아니면 0을 반환합니다.

The lowercase string has length 1–1000000. Repeatedly remove equal adjacent pairs; return 1 if everything can be removed, otherwise 0.

## 풀이 흐름 / Approach

지금까지 지운 뒤 남은 문자열을 스택으로 관리합니다. 새 글자가 맨 위와 같으면 한 쌍을 지우고, 다르면 쌓습니다. 마지막에 스택이 비었는지 확인합니다.

Maintain the reduced prefix as a stack. Remove its top when the next character matches it; otherwise push the character. Success means the final stack is empty.

## 정답이 되는 이유 / Why it works

이미 처리한 접두부 내부에는 지울 같은 인접 쌍이 없습니다. 새 문자 때문에 생길 수 있는 쌍은 스택의 끝뿐이므로 한 번의 비교로 접두부의 올바른 축약 상태를 유지합니다.

The reduced prefix has no equal adjacent pair. Adding one character can create a pair only at its end, so a single top comparison preserves a fully reduced prefix.

## 비용 / Complexity

시간 O(n), 공간 O(n) / Time O(n), space O(n)

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(s):
    stack = []
    # 문자를 왼쪽부터 순회.
    for character in s:
        if stack and stack[-1] == character:
            stack.pop()
        else:
            # append로 새 문자를 스택 끝에 추가.
            stack.append(character)
    return int(not stack)
```

## 다른 방법: 같은 인접 쌍을 반복 삭제 / Repeated adjacent-pair deletion

문자열에서 첫 같은 쌍을 찾아 직접 지우고 다시 시작합니다. 문자 복사가 반복돼 시간 O(n²)이며 작은 문자열 검증용입니다.

Find and delete the first equal adjacent pair, then restart. Repeated copying makes it O(n²), suitable as a small-string reference.

[alternative_reference.py](alternative_reference.py)

```python
def solution(s):
    while True:
        for i in range(len(s) - 1):
            if s[i] == s[i + 1]:
                s = s[:i] + s[i + 2:]
                break
        else:
            return int(not s)
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    "baabaa"
  ],
  "output": 1
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

출처: [프로그래머스 문제 12973](https://school.programmers.co.kr/learn/courses/30/lessons/12973), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 12973](https://school.programmers.co.kr/learn/courses/30/lessons/12973), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.

큰 입력 검사: 100만 글자에서 인접 쌍 없음 / No removable pair in one million characters

```bash
python verify_stress.py
```
