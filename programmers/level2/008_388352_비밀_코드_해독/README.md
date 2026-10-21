# 비밀 코드 해독

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/388352) · Level 2 · Python3

다섯 숫자로 된 비밀 코드 후보 중 모든 시도별 일치 개수를 만족하는 후보 수를 셉니다.

## 조건과 입출력

입력 매개변수: `n, q, ans`. 반환값은 정수이며 아래 풀이의 조건을 만족하는 결과입니다.

- 10 ≤ n ≤ 30
- 1 ≤ (q의 길이 = m) ≤ 10
- q[i]는 i+1번째 시도에서 입력한 5개의 서로 다른 정수를 담고 있으며, 오름차순으로 정렬되어 있습니다.
- 1 ≤ q[i][j] ≤ n
- 0 ≤ ans[i] ≤ 5

## 풀이를 따라가기

1부터 n까지 중 다섯 개를 조합으로 고릅니다. 각 시도와 공통으로 가진 숫자 수를 확인하고 하나라도 다르면 후보를 버립니다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
from itertools import combinations


def solution(n, q, ans):
    attempts = [set(attempt) for attempt in q]
    answer = 0

    # 다섯 숫자의 순서 없는 모든 후보를 한 번씩 만든다.
    for candidate in combinations(range(1, n + 1), 5):
        code = set(candidate)
        valid = True
        for attempt, matched in zip(attempts, ans):
            # 각 시도에서 알려 준 공통 숫자 수와 정확히 같아야 한다.
            if len(code & attempt) != matched:
                valid = False
                break
        if valid:
            answer += 1

    return answer
```

## 정답이 되는 이유

조합은 순서 없는 다섯 원소 집합을 중복 없이 모두 만듭니다. 모든 관측 조건을 동시에 만족하는 후보만 세므로 필요충분합니다.

시간 O(C(n,5)Q), 공간 O(Q+n) / Time O(C(n,5)Q), space O(Q+n)

주의할 점: 일치 개수 0과 5도 그대로 검사합니다. 코드는 순서가 아니라 포함된 숫자의 집합입니다.

## 다른 방법: 숫자 선택 DFS + 남은 일치 수 가지치기

```python
def solution(n, q, ans):
    attempts = [set(row) for row in q]
    answer = 0
    def visit(start, chosen):
        nonlocal answer
        need = 5-len(chosen)
        for attempt, target in zip(attempts, ans):
            matched = len(chosen & attempt)
            possible = sum(v >= start for v in attempt)
            if matched > target or matched + min(need, possible) < target:
                return
        if need == 0:
            answer += 1
            return
        for value in range(start, n-need+2):
            visit(value+1, chosen | {value})
    visit(1, set())
    return answer
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 1부터 n까지 중 다섯 개를 조합으로 고릅니다. 각 시도와 공통으로 가진 숫자 수를 확인하고 하나라도 다르면 후보를 버립니다. | 숫자 선택 DFS + 남은 일치 수 가지치기 |
| 비용 | 시간 O(C(n,5)Q), 공간 O(Q+n) / Time O(C(n,5)Q), space O(Q+n) | 최악 O(C(n,5)Qn), 공간 O(Q+n) / Worst-case O(C(n,5)Qn), space O(Q+n) |

## 검증

공식 예제 2개와 생성 입력 12개를 로컬에서 확인했습니다. 생성 입력은 기본 풀이와 대안 풀이를 비교했습니다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함합니다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Count five-number secret codes matching the reported intersection size for every attempt.

### Conditions and input/output

Input arguments: `n, q, ans`. The return value is an integer satisfying the task described below.

- 10 ≤ n ≤ 30; 1 ≤ len(q)=len(ans) ≤ 10
- each attempt contains 5 distinct sorted integers in [1,n]; 0 ≤ ans[i] ≤ 5
- at least one valid secret code exists

### Approach

Enumerate combinations of five values from 1 through n. Compare intersection sizes against every attempt and reject a candidate as soon as one count differs.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Combinations enumerate every unordered five-element set exactly once. Keeping precisely those satisfying all observations is both necessary and sufficient.

시간 O(C(n,5)Q), 공간 O(Q+n) / Time O(C(n,5)Q), space O(Q+n)

Boundary cases: Handle match counts of both zero and five. A code is a set of values, not an ordering.

### Alternative: Selection DFS with intersection bounds

최악 O(C(n,5)Qn), 공간 O(Q+n) / Worst-case O(C(n,5)Qn), space O(Q+n)

### Verification

Local checks covered 2 official examples and 12 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 비밀 코드 해독](https://school.programmers.co.kr/learn/courses/30/lessons/388352) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
