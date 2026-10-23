# [PCCP 기출문제] 4번 / 수식 복원하기

[Level 3 목록 / Level 3 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/340210) · Level 3 · Python3

## 문제와 조건 / Task and conditions

수식은 2~100개, 진법은 2~9입니다. A,B는 음이 아닌 최대 두 자리, 결과는 최대 세 자리 또는 X이며 X가 하나 이상 있습니다. 가능한 진법이 여럿이면 결과가 같은 경우만 복원하고 나머지는 ?입니다.

There are 2–100 equations in an unknown base 2–9. Operands have at most two nonnegative digits and results at most three digits or X, with at least one X. Restore a result only if all possible bases agree; otherwise use ?.

## 풀이 흐름 / Approach

숫자에 등장한 최댓값보다 큰 2~9진법만 후보입니다. 답이 알려진 수식을 모두 만족하는 진법을 남깁니다. X의 계산 결과를 각 후보 진법으로 다시 표현해 문자열이 모두 같을 때만 확정합니다.

Only bases 2–9 greater than every written digit are possible. Keep bases satisfying every known equation. For X expressions, encode the result in each remaining base and accept it only if all strings agree.

## 정답이 되는 이유 / Why it works

올바른 진법은 모든 알려진 등식을 만족하므로 후보에서 빠지지 않습니다. 가능한 모든 후보의 결과가 같을 때만 값이 유일하게 결정되고, 서로 다르면 정보가 부족하므로 ?입니다.

The true base satisfies every known equation and remains in the candidate set. A missing result is uniquely determined exactly when every remaining base produces the same encoded string; otherwise it is ambiguous.

## 비용 / Complexity

수식 수 e, 자릿수 d에 시간 O(8ed), 공간 O(ed) / O(8ed) time, O(ed) space

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(expressions):
    # 리스트 내포와 split()으로 각 수식을 단어 목록으로 분리.
    parsed = [expression.split() for expression in expressions]
    minimum = max(2, 1 + max(int(char) for expression in expressions for char in expression if char.isdigit()))

    def calculate(a, operator, b, base):
        # int(문자열,진법)은 해당 진법의 문자열을 정수로 해석.
        first, second = int(a, base), int(b, base)
        return first + second if operator == '+' else first - second

    bases = []
    for base in range(minimum, 10):
        # X는 건너뛰고 알려진 결과가 맞는지 확인.
        if all(c == 'X' or calculate(a, operator, b, base) == int(c, base) for a, operator, b, _, c in parsed):
            bases.append(base)

    def encode(value, base):
        # 0은 반복에서 문자가 생기지 않으므로 따로 처리.
        if value == 0:
            return '0'
        digits = []
        while value:
            value, remainder = divmod(value, base)
            # 나머지가 현재 가장 낮은 자릿수.
            digits.append(str(remainder))
        return ''.join(reversed(digits))

    answer = []
    for a, operator, b, _, c in parsed:
        if c != 'X':
            continue
        # {} 집합 내포로 진법별 결과 문자열의 중복 제거.
        results = {encode(calculate(a, operator, b, base), base) for base in bases}
        result = results.pop() if len(results) == 1 else '?'
        # 원래 순서대로 결과 수식 추가.
        answer.append(f'{a} {operator} {b} = {result}')
    return answer
```

## 다른 방법: 자리별 수동 진법 계산 / Manual positional-base evaluation

int(문자열,진법) 대신 value=value×base+digit로 직접 해석합니다. 각 진법에서 복원 수식을 따로 모은 뒤 위치별로 비교해 라이브러리 진법 변환과 대조합니다.

Evaluate digits manually with value=value×base+digit instead of int(text,base). Build the restored results independently for each base, then compare corresponding outputs.

[alternative.py](alternative.py)

```python
def solution(expressions):
    equations = [text.split() for text in expressions]
    minimum = max(2, 1 + max(int(ch) for text in expressions for ch in text if ch.isdigit()))
    def parse(text, base):
        value = 0
        for ch in text:
            value = value * base + int(ch)
        return value
    def encode(value, base):
        if value < base:
            return str(value)
        return encode(value // base, base) + str(value % base)
    options = []
    for base in range(minimum, 10):
        restored, valid = [], True
        for a, operator, b, _, c in equations:
            value = parse(a, base) + (1 if operator == '+' else -1) * parse(b, base)
            if c == 'X':
                restored.append(encode(value, base))
            elif value != parse(c, base):
                valid = False
        if valid:
            options.append(restored)
    missing = [parts for parts in equations if parts[4] == 'X']
    output = []
    for i, (a, operator, b, _, _) in enumerate(missing):
        values = {option[i] for option in options}
        output.append(f'{a} {operator} {b} = {next(iter(values)) if len(values) == 1 else "?"}')
    return output
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    [
      "14 + 3 = 17",
      "13 - 6 = X",
      "51 - 5 = 44"
    ]
  ],
  "output": [
    "13 - 6 = 5"
  ]
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

출처: [프로그래머스 문제 340210](https://school.programmers.co.kr/learn/courses/30/lessons/340210), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 340210](https://school.programmers.co.kr/learn/courses/30/lessons/340210), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
