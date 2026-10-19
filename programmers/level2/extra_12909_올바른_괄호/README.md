# 올바른 괄호

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/12909) · Level 2 · Python3

## 문제와 조건 / Task and conditions

괄호 문자열은 1~100000자입니다. 모든 괄호가 올바르게 짝지어지면 True, 아니면 False를 반환합니다.

The parenthesis string has length 1–100000. Return True exactly when all brackets form a valid sequence.

## 풀이 흐름 / Approach

여는 괄호는 잔액을 1 늘리고 닫는 괄호는 1 줄입니다. 중간에 음수가 되면 앞서 연 괄호 없이 닫은 것이므로 즉시 실패합니다. 끝에서 0이어야 남은 괄호도 없습니다.

Increase a balance for an opening bracket and decrease it for a closing bracket. A negative prefix is invalid immediately, and the final balance must be zero.

## 왜 맞는가 / Why it works

올바른 괄호열의 모든 접두부는 닫는 괄호가 더 많지 않아야 하고 전체 수는 같아야 합니다. 두 조건은 괄호를 왼쪽부터 짝짓는 데 충분하기도 합니다.

Every prefix must have at least as many openings as closings, and totals must match. These conditions are also sufficient for greedy left-to-right pairing.

## 비용 / Complexity

시간 O(n), 공간 O(1) / O(n) time, O(1) space

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(s):
    balance = 0
    for ch in s:
        # 여는 괄호면 +1, 닫는 괄호면 -1을 더해 저장.
        balance += 1 if ch == '(' else -1
        if balance < 0:
            return False
    return balance == 0
```

## 다른 방법: 실제 괄호 스택 / Explicit bracket stack

열린 괄호를 스택에 넣고 닫힐 때 하나씩 꺼냅니다. 같은 시간에 공간 O(n)이지만 대응 관계를 눈으로 확인하기 좋습니다.

Push openings and pop one for each closing bracket. It has the same time complexity but O(n) space and makes matching explicit.

[alternative.py](alternative.py)

```python
def solution(s):
    stack = []
    for ch in s:
        if ch == '(':
            stack.append(ch)
        elif not stack:
            return False
        else:
            stack.pop()
    return not stack
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    "()()"
  ],
  "output": true
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

출처: [프로그래머스 문제 12909](https://school.programmers.co.kr/learn/courses/30/lessons/12909), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 12909](https://school.programmers.co.kr/learn/courses/30/lessons/12909), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
