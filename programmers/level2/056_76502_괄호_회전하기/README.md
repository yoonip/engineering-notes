# 괄호 회전하기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/76502) · Level 2 · Python3

문자열을 각 위치에서 회전했을 때 올바른 괄호 문자열이 되는 경우 수를 센다.

## 조건과 입출력

입력 매개변수: `s`. 반환값은 정수이며 아래 풀이의 조건을 만족하는 결과다.

- s의 길이는 1 이상 1,000 이하입니다.

## 풀이를 따라가기

각 시작점을 기준으로 회전 문자열을 만든다. 여는 괄호는 스택에 넣고 닫는 괄호는 맨 위와 짝이 맞아야 꺼낸다. 끝에서 스택이 비면 유효하다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
def solution(s):
    pairs = {')': '(', ']': '[', '}': '{'}
    answer = 0
    for offset in range(len(s)):
        stack = []
        for character in s[offset:] + s[:offset]:
            # 가장 최근의 여는 괄호부터 닫혀야 한다.
            if character in '([{':
                stack.append(character)
            # 짝이 맞지 않거나 여는 괄호가 없으면 이 회전은 실패다.
            elif not stack or stack.pop() != pairs[character]:
                break
        else:
            if not stack:
                answer += 1
    return answer
```

## 왜 맞는가

올바른 중첩에서는 마지막으로 열린 괄호부터 닫혀야 한다. 스택은 이 순서를 강제하고 남은 여는 괄호도 거부하므로 필요충분하다.

시간 O(N²), 공간 O(N) / Time O(N²), space O(N)

주의할 점: 여는 괄호가 없는데 닫는 괄호를 만나면 바로 실패다. 홀수 길이는 어떤 회전도 유효하지 않다.

## 다른 방법: 맞붙은 괄호쌍 반복 제거 · 비교용

이 대안은 작은 입력에서 원리를 비교하는 검증용이다. 최대 제한에 제출할 기본 풀이와 구분한다.

```python
def solution(s):
    answer=0
    for offset in range(len(s)):
        current=s[offset:]+s[:offset]
        while current:
            following=current.replace('()','').replace('[]','').replace('{}','')
            if following==current: break
            current=following
        answer+=not current
    return answer
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 각 시작점을 기준으로 회전 문자열을 만든다. 여는 괄호는 스택에 넣고 닫는 괄호는 맨 위와 짝이 맞아야 꺼낸다. 끝에서 스택이 비면 유효하다. | 맞붙은 괄호쌍 반복 제거 · 비교용 |
| 비용 | 시간 O(N²), 공간 O(N) / Time O(N²), space O(N) | 시간 O(N³), 공간 O(N) / Time O(N³), space O(N) |

## 검증

공식 예제 4개와 생성 입력 80개를 로컬에서 확인했다. 생성 입력은 기본 풀이와 대안 풀이를 비교했다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함한다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행한다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분한다.

## English

Count rotations that form a valid bracket string.

### Conditions and input/output

Input arguments: `s`. The return value is an integer satisfying the task described below.

- 1 ≤ len(s) ≤ 1000; six bracket characters

### Approach

Try each rotation. Push opening brackets; a closing bracket must match the stack top. Accept only if the stack is empty at the end.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Valid nesting closes the most recently opened bracket first. The stack enforces this order and rejects unmatched openings, making the test necessary and sufficient.

시간 O(N²), 공간 O(N) / Time O(N²), space O(N)

Boundary cases: Reject a closing bracket with an empty stack. No rotation of an odd-length string can be valid.

### Alternative: Repeated elimination of adjacent pairs

This alternative is for understanding and checking small inputs; use the main implementation for the full constraints. 시간 O(N³), 공간 O(N) / Time O(N³), space O(N)

The main approach follows the steps described above. The alternative uses repeated elimination of adjacent pairs; compare its intermediate state and cost with the main implementation before choosing it.

### Verification

Local checks covered 4 official examples and 80 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 괄호 회전하기](https://school.programmers.co.kr/learn/courses/30/lessons/76502) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
