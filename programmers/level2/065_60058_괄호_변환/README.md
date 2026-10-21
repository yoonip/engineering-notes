# 괄호 변환

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/60058) · Level 2 · Python3

## 문제와 조건 / Task and conditions

p는 길이 2~1000인 짝수 길이의 괄호열이며 두 괄호 수가 같습니다. 임의의 올바른 괄호열이 아니라 지정된 절차의 결과를 반환합니다.

p has even length 2–1000 and equal opening/closing counts. Return the result of the specified transformation, not an arbitrary valid sequence.

## 풀이 흐름 / Approach

앞에서부터 여는 괄호와 닫는 괄호의 차이를 셉니다. 처음 0이 되는 가장 짧은 균형 구간 u와 나머지 v로 나눕니다. u가 올바르면 보존하고, 아니면 문제의 변환 순서대로 v를 감싼 뒤 u의 안쪽을 뒤집습니다.

Scan the opening-minus-closing balance and split at its first zero into the shortest balanced prefix u and suffix v. Preserve a valid u; otherwise wrap the converted v and flip the interior of u as required.

## 정답이 되는 이유 / Why it works

가장 짧은 균형 접두부를 찾으므로 분할이 유일합니다. 빈 문자열을 기저로 두면 각 재귀 호출은 더 짧은 v에 공식 변환 규칙을 적용하므로 귀납적으로 요구한 결과를 만듭니다.

The shortest balanced prefix uniquely determines the split. Starting from the empty-string base case, induction on the shorter suffix shows that each recursive call implements the specified transformation.

## 비용 / Complexity

문자열 복사 포함 시간 O(n²), 공간 O(n²) 상한; 재귀 O(n) / O(n²) time and space upper bounds with slicing; O(n) depth

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(p):
    if not p:
        return ''
    balance = 0
    # 최소 균형 접두부가 올바른지 저장.
    correct = True
    for index, character in enumerate(p, 1):
        # 여는 괄호면 +1, 닫는 괄호면 -1을 +=로 누적.
        balance += 1 if character == '(' else -1
        if balance < 0:
            # 현재 u의 위반 여부 기록.
            correct = False
        if balance == 0:
            # 끝은 미포함.
            u, v = p[:index], p[index:]
            if correct:
                return u + solution(v)
            flipped = ''.join(')' if ch == '(' else '(' for ch in u[1:-1])
            return '(' + solution(v) + ')' + flipped
```

## 다른 방법: 명시적 작업 스택 / Explicit work stack

재귀 호출 대신 작업 스택과 출력 조각을 사용합니다. 재귀 깊이 제한을 피하지만 구간을 찾는 과정은 그대로이며, 조각은 마지막에 한 번 합칩니다.

Replace recursive calls with a task stack and output fragments. This avoids recursion-depth limits while keeping the same split rule; fragments are joined once at the end.

[alternative.py](alternative.py)

```python
def solution(p):
    output = []
    tasks = [('convert', p)]
    while tasks:
        action, text = tasks.pop()
        if action == 'literal':
            output.append(text)
            continue
        if not text:
            continue
        balance, valid = 0, True
        for end, ch in enumerate(text, 1):
            balance += 1 if ch == '(' else -1
            valid &= balance >= 0
            if balance == 0:
                break
        u, v = text[:end], text[end:]
        if valid:
            output.append(u)
            tasks.append(('convert', v))
        else:
            output.append('(')
            flipped = ''.join(')' if ch == '(' else '(' for ch in u[1:-1])
            # 나중에 출력할 조각부터 넣어야 원하는 순서로 꺼낸다.
            tasks.append(('literal', ')' + flipped))
            tasks.append(('convert', v))
    return ''.join(output)
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    "(()())()"
  ],
  "output": "(()())()"
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

출처: [프로그래머스 문제 60058](https://school.programmers.co.kr/learn/courses/30/lessons/60058), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 60058](https://school.programmers.co.kr/learn/courses/30/lessons/60058), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
