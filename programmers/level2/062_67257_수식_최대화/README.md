# 수식 최대화

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/67257) · Level 2 · Python3

세 연산자의 우선순위를 바꾸어 수식 결과 절댓값을 최대화한다.

## 조건과 입출력

입력 매개변수: `expression`. 반환값은 정수이며 아래 풀이의 조건을 만족하는 결과다.

- expression은 길이가 3 이상 100 이하인 문자열입니다.
- expression의 피연산자(operand)는 0 이상 999 이하의 숫자입니다.
- 즉, "100-2145*458+12"처럼 999를 초과하는 피연산자가 포함된 수식은 입력으로 주어지지 않습니다.
- expression은 적어도 1개 이상의 연산자를 포함하고 있습니다.
- 연산자 우선순위를 어떻게 적용하더라도, expression의 중간 계산값과 최종 결괏값은 절댓값이 2^63 - 1 이하가 되도록 입력이 주어집니다.

## 풀이를 따라가기

수식을 숫자와 연산자 토큰으로 나눈다. 여섯 우선순위를 모두 시도하며 높은 연산자부터 왼쪽에서 찾아 축약한다. 마지막 정수의 절댓값 최댓값을 고른다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
from itertools import permutations
from re import split
from operator import add, sub, mul

def solution(expression):
    original = split(r'([+*-])', expression)
    functions = {'+': add, '-': sub, '*': mul}
    answer = 0
    # 세 연산자의 여섯 우선순위를 모두 확인한다.
    for order in permutations('+-*'):
        tokens = original[:]
        for operation in order:
            while operation in tokens:
                # 같은 연산자는 왼쪽부터 계산한다.
                index = tokens.index(operation)
                value = functions[operation](int(tokens[index - 1]), int(tokens[index + 1]))
                tokens[index - 1:index + 2] = [str(value)]
        answer = max(answer, abs(int(tokens[0])))
    return answer
```

## 왜 맞는가

서로 다른 세 연산자의 순서는 최대 3!가지다. 같은 우선순위는 왼쪽부터 축약하므로 각 순서가 정의한 계산을 그대로 수행하고 모든 경우를 비교한다.

시간 O(6L²), 공간 O(L) / Time O(6L²), space O(L); L=토큰 수 / token count

주의할 점: 원래 수식에 없는 연산자도 순열에 있어도 무방하다. eval 대신 직접 산술 연산을 적용한다.

## 다른 방법: 두 스택으로 선형 평가

기본 풀이와 같은 결과를 구하되 중간 상태와 계산 방식이 다르다.

```python
from itertools import permutations
import re

def solution(expression):
    tokens=re.findall(r'\d+|[+*-]',expression)
    answer=0
    def calculate(a,b,op):
        return a+b if op=='+' else a-b if op=='-' else a*b
    for order in permutations('+-*'):
        rank={op:i for i,op in enumerate(order)}
        values=[]
        operators=[]
        def reduce_top():
            b,a=values.pop(),values.pop()
            values.append(calculate(a,b,operators.pop()))
        for token in tokens:
            if token.isdigit(): values.append(int(token))
            else:
                while operators and rank[operators[-1]]>=rank[token]: reduce_top()
                operators.append(token)
        while operators: reduce_top()
        answer=max(answer,abs(values[0]))
    return answer
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 수식을 숫자와 연산자 토큰으로 나눈다. 여섯 우선순위를 모두 시도하며 높은 연산자부터 왼쪽에서 찾아 축약한다. 마지막 정수의 절댓값 최댓값을 고른다. | 두 스택으로 선형 평가 |
| 비용 | 시간 O(6L²), 공간 O(L) / Time O(6L²), space O(L); L=토큰 수 / token count | 시간 O(6L), 공간 O(L) / Time O(6L), space O(L) |

## 검증

공식 예제 2개와 생성 입력 80개를 로컬에서 확인했다. 생성 입력은 기본 풀이와 대안 풀이를 비교했다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함한다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행한다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분한다.

## English

Maximize the absolute result by changing precedence among the three operators.

### Conditions and input/output

Input arguments: `expression`. The return value is an integer satisfying the task described below.

- 3 ≤ len(expression) ≤ 100; operands 0 … 999; operators +,−,*
- valid infix expression; no unary minus; absolute answer ≤ 2^63−1

### Approach

Tokenize numbers and operators. For each of six precedence orders, repeatedly reduce the highest-precedence remaining operator from the left. Maximize the absolute final integer.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

There are at most 3! strict orders. Leftmost reduction preserves left associativity within each operator and evaluates every possible precedence assignment.

시간 O(6L²), 공간 O(L) / Time O(6L²), space O(L); L=토큰 수 / token count

Boundary cases: Permutations may include absent operators harmlessly. Apply arithmetic directly instead of using eval.

### Alternative: Linear evaluation with operator and operand stacks

It computes the same result using different intermediate states or evaluation steps. 시간 O(6L), 공간 O(L) / Time O(6L), space O(L)

The main approach follows the steps described above. The alternative uses linear evaluation with operator and operand stacks; compare its intermediate state and cost with the main implementation before choosing it.

### Verification

Local checks covered 2 official examples and 80 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 수식 최대화](https://school.programmers.co.kr/learn/courses/30/lessons/67257) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
