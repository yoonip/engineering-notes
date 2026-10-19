# 매출 하락 최소화

Level 4 · `72416` · Python3 · [공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/72416)

[기본 풀이](solution.py) · [다른 풀이](alternative.py) · [예제 입력과 정답](examples.json) · [검증 코드](test_solution.py)

## 문제와 조건

각 팀에서 한 명 이상 참석시키면서 참석자 매출 합을 최소화한다. 팀장은 자기 팀과 상위 팀에 동시에 속할 수 있다.

입력 범위와 상수는 다음과 같다. 기호는 코드의 매개변수에 맞췄다.

`2≤employees≤300000; sales:0..10000; rooted management tree, CEO=1; each manager-and-direct-report team needs an attendee; result≤2^31−1.`

## 풀이를 따라가기

직원마다 참석·불참 두 비용을 저장한다. 자식별 더 싼 상태를 기본으로 고르고, 직원이 불참하면서 자식도 모두 불참이라면 자식 한 명을 참석으로 바꾸는 최소 추가 비용을 더한다.

하위 팀 조건은 각 자식 상태에 이미 반영된다. 현재 팀 조건만 최소한으로 보완하면 되므로 이 두 상태로 충분하다. 반복문 후위 순서를 사용해 긴 일자 조직에서도 Python 재귀 깊이에 기대지 않는다.

## 다른 방법과 비교

대안은 참석자 부분집합을 모두 만들고 모든 팀 조건을 직접 검사한다. 직원 20명 이하에서 최적 비용을 독립적으로 확인한다.

| 구분 | 시간 | 추가 공간 |
|---|---|---|
| 기본 풀이 | `O(n)` | `O(n)` |
| 대안 풀이 | `O(2^n · n)` | `O(n)` |

## 코드와 검증

`solution.py`에는 상태의 뜻과 경계조건을 한국어 주석으로 적었다. `alternative.py`는 별도의 풀이이며, `test_solution.py`에서 공식 예제와 생성 입력을 비교한다. 실행 기록은 [validation.json](validation.json)에 있다. 원본 제출 파일은 [submitted_original.py](submitted_original.py)에 그대로 보관했다.

```bash
python test_solution.py
```

## English

### Problem and constraints

Choose at least one attendee from each manager-and-direct-report team while minimizing lost sales. A manager can belong to both a parent team and their own team.

Input limits and constants, using the parameter names in the code:

`2≤employees≤300000; sales:0..10000; rooted management tree, CEO=1; each manager-and-direct-report team needs an attendee; result≤2^31−1.`

### Following the solution

Store attending and absent costs per employee. Start from cheaper child states; if an absent manager leaves every child absent, add the smallest cost of forcing one child to attend.

Child states already satisfy lower teams, leaving only the current team to enforce. Iterative postorder avoids recursion-depth failures in long management chains.

### Alternative and comparison

The alternative enumerates attendee subsets and checks every team, independently establishing optima for at most twenty employees.

The primary solution takes `O(n)` time and `O(n)` additional space. The alternative takes `O(2^n · n)` time. Its additional space is `O(n)`.

### Code and verification

Read `solution.py` for the primary implementation and `alternative.py` for the comparison. Comments explain states and boundary cases in Korean. Run `python test_solution.py` for the official examples and generated comparisons; [validation.json](validation.json) records the execution. The submitted source is preserved byte for byte in [submitted_original.py](submitted_original.py).

## 출처 / Source

- [Programmers — 매출 하락 최소화](https://school.programmers.co.kr/learn/courses/30/lessons/72416): 문제 조건·입출력 예 확인 / problem constraints and examples checked on 2026-10-19.
