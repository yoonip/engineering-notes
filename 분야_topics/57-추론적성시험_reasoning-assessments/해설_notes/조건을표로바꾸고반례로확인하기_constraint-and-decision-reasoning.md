# 조건을 표로 바꾸고 반례로 확인하기 | Constraint and decision reasoning

[추론·적성](../README.md) · [실행 코드](../../../예제_examples/추론_reasoning/README.md)

## 한국어

### 조건을 기억하는 대신 표현하기

여러 대상의 순서나 배치를 정할 때 문장을 머릿속에만 쌓으면 빠뜨리기 쉽다. “A는 B보다 앞선다”는 관계와 “A는 첫 위치가 아니다”라는 조건을 따로 적으면 각 조건이 무엇을 지우는지 보인다. 상황판단형 조건 해석에서도 먼저 주체·행동·범위·예외를 분리하고, 문장에 없는 제한을 추가하지 않는 것이 중요하다. 아래 표와 숫자는 개념 교육을 위한 작은 모델이다.

제약 충족 문제(CSP)는 변수 $`X_i`$, 가능한 값의 집합인 도메인 $`D_i`$, 허용 조합을 정하는 제약 $`C_j`$로 표현한다. 해는 모든 변수에 값을 배정하고 모든 제약을 동시에 만족한 결과다. “무엇이 가능하다”와 “무엇이 반드시 그렇다”는 다른 질문이다. 이 정의는 [CMU 15-281 CSP notes](https://www.cs.cmu.edu/~15281-s24/coursenotes/constraints/index.html)와 [Berkeley AIMA Chapter 5 slides](https://aima.cs.berkeley.edu/4th-ed/slides-pdf/chapter05.pdf)를 대조했다.

| 문장의 역할 | 수학 모델 | 표에서 할 일 |
|---|---|---|
| A의 가능한 위치 | $`X_A\in\{1,2,3\}`$ | 후보를 적는다 |
| A는 마지막이 아님 | $`X_A\ne3`$ | 도메인에서 3을 지운다 |
| A가 B보다 앞섬 | $`X_A<X_B`$ | 두 변수의 관계를 유지한다 |
| 서로 다른 위치 | $`X_i\ne X_j`$ | 같은 값을 함께 쓰지 못하게 한다 |
| 조건부 규칙 | $`p\to q`$ | $`p`$일 때 $`q`$를 요구하며 역을 추가하지 않는다 |

위치는 순서를 나타내는 무차원 정수다. 실제 시간 길이와는 다르다. 문장에서 “바로 앞”이라면 $`X_B=X_A+1`$이며 단순한 $`X_A<X_B`$보다 강하다. 순위가 작은 수일수록 먼저인지도 모델에서 정한다.

### 제약 전파: 짝이 없는 후보 지우기

이항 제약 $`C(X,Y)`$에서 $`X`$의 후보 $`x`$를 살리려면 $`Y`$의 남은 후보 중 적어도 하나가 $`C(x,y)`$를 만족해야 한다.

$$D_X\leftarrow\{x\in D_X:\exists y\in D_Y,\ C(x,y)\}.$$

$`X`$의 도메인이 줄면 $`X`$를 참고하던 이웃을 다시 검사한다. AC-3는 이 의존 관계를 큐에 넣어 전파한다. 이웃을 검사하려고 매번 모든 변수 조합을 훑는 대신 실제 관계가 있는 쌍을 기록한다. [CMU의 AC-3 설명](https://www.cs.cmu.edu/~15281-s24/coursenotes/constraints/index.html)과 [AIMA의 arc consistency](https://aima.cs.berkeley.edu/4th-ed/slides-pdf/chapter05.pdf)가 이 원리를 제공한다.

개념 예로 세 위치에서 $`X_A<X_B<X_C`$라면 처음에는 모두 $`\{1,2,3\}`$이다. 관계를 양방향으로 전파하면 결국 $`D_A=\{1\}`$, $`D_B=\{2\}`$, $`D_C=\{3\}`$만 남는다. 반대로 세 변수가 각각 $`\{0,1\}`$이고 모두 서로 달라야 한다면, 각 쌍에는 다른 값을 가진 짝이 있어도 세 변수 전체에는 해가 없다. 따라서 arc consistency는 모든 모순을 발견하는 완전한 판정법이 아니다.

### 경우를 나누고 되돌아오기

전파 뒤에도 후보가 둘 이상이면 하나를 가정해 분기하고 다시 전파한다. 도메인이 비면 그 분기는 버린다. MRV(minimum remaining values)는 남은 후보 수가 가장 작은 변수부터 정하는 순서다. 제약을 바꾸지 않고 실패를 빨리 만날 기회를 높인다. 이미 정한 조건을 잊고 다른 분기에 섞지 않도록 구현은 분기별 도메인을 따로 유지한다.

유한 도메인의 모든 값을 빠짐없이 분기하고, 전파가 실제 가능한 해를 지우지 않는다면 탐색은 완전하다. 제약을 만족하는 완성 배정만 반환하므로 건전성도 확인할 수 있다. 하지만 변수 $`n`$개에 후보가 최대 $`d`$개면 가능한 완성 배정이 최대 $`d^n`$개다. 제약 전파가 이를 늘 다항 시간으로 바꾸는 것은 아니다. 코드의 이항 관계 검사 비용을 $`C`$라 두면 AC-3 한 번의 표준 상한은 $`O(ed^3C)`$이며, $`e`$는 방향 있는 관계 수다. 도메인 복사를 유지하는 깊이 우선 재귀의 보수적인 저장 상한은 $`O(n^2d+e)`$다. 모든 해를 리스트로 모으면 출력 크기만큼 더 든다.

```python
from 예제_examples.추론_reasoning.models import iter_solutions

domains = {name: [1, 2, 3] for name in "ABC"}
rules = [("A", "B", lambda a, b: a < b),
         ("B", "C", lambda b, c: b < c)]
# 가능한 배정을 하나씩 받으며 원래 입력 도메인은 바꾸지 않는다.
print(list(iter_solutions(domains, rules)))
```

예상 결과는 `A=1, B=2, C=3`이다. 이 구현은 정수의 유한 도메인과 이항 제약을 다룬다. 단항 조건은 도메인을 미리 줄인다. 모든 값이 다르다는 조건은 쌍별 부등식으로 표현할 수 있지만, 전용 global all-different 전파가 더 강한 가지치기를 할 수 있다. 세 변수 이상인 임의 조건을 이항 함수 하나로 옮겼다고 가정해서는 안 된다.

### 가능성, 필연성, 최적화

주장 $`q`$가 가능한지 보려면 제약 $`C\land q`$의 해 하나를 찾으면 된다. 반드시 참인지 보려면 $`C`$ 자체가 일관되는지도 확인하고, $`C\land\neg q`$에 해가 없는지 검사한다. 해를 못 찾은 이유가 실제 무해인지, 시간 제한이나 탐색 중단인지 구분해야 한다.

최적화는 여기에 목적함수를 추가한다. 구현의 `minimize_cost`는 변수별 비용의 합 $`f(x)=\sum_i c_i(x_i)`$를 최소화한다. 남은 도메인에서

$$L=\sum_i\min_{v\in D_i}c_i(v)$$

는 실제 가능한 해의 비용 이하인 안전한 하한이다. 각 변수가 다른 제약을 무시하고 가장 싼 값을 고르게 해 제한을 완화했기 때문이다. 이미 찾은 해의 비용이 $`U`$이고 $`L\ge U`$면 더 좋은 해가 없는 가지를 버릴 수 있다. 비용이 음수여도 이 하한은 성립한다. 이 구현은 동률인 최적해 모두가 아니라 하나를 반환한다. A와 B를 서로 다른 두 위치에 놓고 비용을 A:{1:3,2:1}, B:{1:2,2:5}로 두면 비용 8과 3 중 3인 `A=2,B=1`을 고른다.

검사는 80개 고정 시드의 작은 무작위 이항 모델을 독립적인 전체 배정 검사와 비교해 해 집합과 최소 비용을 확인한다. 순서 예, 국소적으로 일관되지만 전체 해가 없는 삼각 관계, 같은 쌍의 여러 제약, 반대 방향 관계, 빈 문제, 음수 비용·동률도 검사한다. 올바른 solver도 잘못 옮긴 문장의 의미까지 고쳐 주지는 않는다. 조건표와 원문의 대응이 계산 검증의 출발점이다.

## English

### Represent conditions explicitly

Keeping many ordering rules only in memory invites omissions. Separating “A precedes B” from “A is not first” shows which possibilities each rule removes. Situation-based reasoning also requires explicit actors, actions, scope, and exceptions, without inventing restrictions. The tables and numbers here are small conceptual models.

A constraint satisfaction problem consists of variables $`X_i`$, finite domains $`D_i`$, and constraints specifying allowed combinations. A solution assigns every variable while satisfying every constraint. Possibility and necessity ask different questions. These definitions are cross-checked against [CMU CSP notes](https://www.cs.cmu.edu/~15281-s24/coursenotes/constraints/index.html) and [Berkeley AIMA Chapter 5](https://aima.cs.berkeley.edu/4th-ed/slides-pdf/chapter05.pdf).

The table maps possible positions to domains, exclusions to deleted values, precedence to $`X_A<X_B`$, and distinct positions to inequalities. A conditional $`p\to q`$ does not add its converse. Positions are dimensionless integers, not elapsed times. “Immediately before” requires $`X_B=X_A+1`$, a stronger condition than precedence; the numerical direction of order must be defined.

### Propagation and search

For binary relation $`C(X,Y)`$, retain $`x\in D_X`$ only if some $`y\in D_Y`$ satisfies $`C(x,y)`$. Thus $`D_X\leftarrow\{x\in D_X:\exists y\in D_Y,C(x,y)\}`$. A shrinking domain requires rechecking affected neighbours. AC-3 queues these relationships rather than repeatedly scanning every unrelated pair. See the linked CMU and AIMA treatments of arc consistency.

With domains $`\{1,2,3\}`$ and $`X_A<X_B<X_C`$, propagation leaves A=1, B=2, C=3. By contrast, three pairwise-distinct variables each having domain $`\{0,1\}`$ have pairwise support but no global solution. Arc consistency alone is therefore incomplete.

When propagation leaves multiple candidates, branch on a value and propagate again, abandoning empty-domain branches. MRV selects the variable with fewest remaining values. It changes search order, not constraints. Separate branch domains prevent assumptions leaking across branches. Exhaustive branching over finite remaining domains is complete when propagation removes no possible solutions; returning only satisfying full assignments establishes soundness.

The worst case still has $`d^n`$ complete assignments. With $`e`$ directed relations, maximum domain size $`d`$, and relation-evaluation cost $`C`$, a standard AC-3 bound is $`O(ed^3C)`$ per call. Domain-copying depth-first recursion has a conservative storage bound $`O(n^2d+e)`$, plus any collected outputs. The Python example returns A=1, B=2, C=3 without mutating the caller's domains. Unary rules are encoded by initial domain restriction. Pairwise inequalities represent distinctness, but a global all-different propagator may prune more strongly. Arbitrary higher-order constraints are not automatically binary relations.

### Decisions and optimization

Possibility of $`q`$ requires one solution of $`C\land q`$. Necessity requires checking that $`C`$ is consistent and that $`C\land\neg q`$ has no solution. Exhaustion must be distinguished from timeout or interrupted search.

Optimization adds an objective. `minimize_cost` minimizes the separable sum $`f(x)=\sum_i c_i(x_i)`$. The lower bound $`L=\sum_i\min_{v\in D_i}c_i(v)`$ relaxes constraints by letting each variable choose its cheapest remaining value independently. Every feasible completion costs at least $`L`$. With incumbent cost $`U`$, a branch with $`L\ge U`$ cannot improve the incumbent and can be pruned. This remains valid with negative costs. The implementation returns one optimum, not all tied optima. For distinct positions 1 and 2 with A costs {1:3,2:1} and B costs {1:2,2:5}, it selects A=2, B=1 at cost 3 rather than 8.

Tests compare full solution sets and minimum costs against independent exhaustive enumeration for 80 seeded small random binary models. They also cover the ordering example, the globally impossible triangle, multiple and reversed relations on a pair, empty models, negative costs, and ties. A correct solver cannot repair a mistranslated condition; correspondence between the source wording and the formal rules remains essential.

## 출처 / Sources

- [Carnegie Mellon University 15-281: Constraint Satisfaction Problems](https://www.cs.cmu.edu/~15281-s24/coursenotes/constraints/index.html) — 변수·도메인·제약, backtracking, AC-3, MRV, 복잡도 / formulation, backtracking, AC-3, MRV, complexity.
- [UC Berkeley AIMA, Chapter 5 slides](https://aima.cs.berkeley.edu/4th-ed/slides-pdf/chapter05.pdf) — 제약 충족과 비용 최적화의 구분, 전파와 탐색 / satisfaction versus cost optimization, propagation and search.

참고일 / Accessed: 2026-10-19. 도메인·비용 예와 독립 검사는 개념 설명용으로 구성했다. / Domain/cost examples and independent checks were constructed to explain the concepts.
