# 주장의 반례를 계산하기: CNF와 DPLL

[분야 목차](../README.md) · [SAT 구현](../../예제_examples/심화_advanced/math_reasoning/models.py) · [독립 검증](../../예제_examples/심화_advanced/math_reasoning/test_models.py)

## 한국어

### 1. “그럴듯하다”에서 “반례가 없다”로

논증이 타당하다는 것은 전제가 모두 참인데 결론만 거짓인 경우가 없다는 뜻입니다. 결론에 동의하는지나 현실에서 전제가 사실인지는 다른 문제입니다. 명제 논리를 코드로 다루면 이 구분을 분명하게 확인할 수 있습니다. 사람이 놓치기 쉬운 조건 조합을 컴퓨터가 탐색하고, 주장이 성립하지 않으면 구체적인 반례를 돌려줍니다.

전제들의 결합을 $`\Gamma`$, 결론을 $`C`$라 하면

```math
\Gamma\models C
\quad\Longleftrightarrow\quad
\Gamma\land\neg C\text{ 가 만족 불가능하다.}
```

이것은 참인 결론의 예를 여러 개 찾는 것과 다릅니다. 모든 전제와 부정한 결론을 동시에 만족시키는 할당 하나만 발견해도 반례가 됩니다. [CMU 15-414의 SAT·타당성 관계, pp. 1–5](https://www.cs.cmu.edu/~15414/s25/lectures/16-dpll.pdf)와 [Stanford가 제공하는 Abstract DPLL 원논문](https://web.stanford.edu/class/cs357/NOT04.pdf)의 절·전파·분기 체계를 대조했습니다.

### 2. CNF의 구조와 빈 경우

리터럴은 $`p`$ 또는 $`\neg p`$입니다. 절(clause)은 리터럴을 OR로 연결하고, CNF는 여러 절을 AND로 연결합니다. 예를 들어 $`(\neg p\lor q)\land p\land\neg q`$는 세 절을 모두 만족시켜야 합니다. 코드는 $`p=1,q=2`$로 정해 `[[-1,2],[1],[-2]]`로 입력합니다.

빈 절 `[]`은 선택할 참 리터럴이 없으므로 거짓입니다. 반대로 절 목록 전체가 비어 있으면 더 만족시킬 조건이 없으므로 참입니다. 둘을 뒤집으면 알고리즘의 종료 조건이 틀어집니다. 한 절에 $`p`$와 $`\neg p`$가 함께 있으면 그 절은 항상 참이라 제거할 수 있습니다. 서로 다른 절에 두 리터럴이 따로 등장하는 것은 전혀 다른 상황입니다.

이 구현은 CNF를 입력으로 받으며 자연어 문장을 자동으로 논리식으로 바꾸지 않습니다. “모든”, “일부”, “만약”이 들어간 문장을 옮길 때에는 명제의 범위부터 정확히 정해야 합니다. 특히 양화사가 있는 일반적인 일차논리를 유한 개 명제변수로 임의 축약하면 원래 논증과 다른 문제를 풀 수 있습니다.

### 3. 단위 전파를 단계별로 읽습니다

한 절이 $`(\ell)`$만 남았다면 그 리터럴을 참으로 해야 합니다. 나머지 절 중 $`\ell`$이 들어 있는 절은 이미 참이므로 지우고, $`\neg\ell`$은 거짓이므로 해당 절에서 제거합니다. 따라서

```math
F\land\ell\text{ 의 만족성}
\quad\Longleftrightarrow\quad
F[\ell=\mathrm{true}]\land\ell\text{ 의 만족성}.
```

위 예에서는 단위 절 $`p`$를 적용해 $`\neg p\lor q`$가 $`q`$로 줄어듭니다. 이제 $`q`$와 $`\neg q`$를 동시에 만족해야 하므로 빈 절이 생깁니다. 이 가지는 더 탐색할 필요가 없습니다. 그러므로 “$`p\to q`$, $`p`$, 따라서 $`q`$”에는 반례가 없습니다.

반대로 $`p\to q`$와 $`q`$에서 $`p`$를 결론 내리면, $`p`$가 거짓이고 $`q`$가 참인 할당이 남습니다. 실제로 전제는 둘 다 참이고 결론은 거짓입니다. 이 결과가 후건 긍정의 오류를 구체적으로 보여줍니다.

### 4. 결정해야 할 변수가 남으면 분기합니다

단위 전파가 끝났는데 절이 남아 있으면, 아직 결정하지 않은 변수 하나를 참·거짓으로 나누어 탐색합니다. 모든 해는 두 가지 중 하나에 속하므로 양쪽을 빠뜨리지 않으면 완전성이 유지됩니다. 각 분기에서는 변수를 하나 이상 결정하므로 유한 변수에서 종료합니다.

`sat_dpll`은 남은 절에서 자주 나타나는 변수를 먼저 고르고, 같은 빈도이면 변수 번호로 순서를 정합니다. 단위 전파와 이 선택은 불필요한 전수 열거를 줄이지만 최악의 지수 시간은 없애지 못합니다. 작은 예제는 절 집합을 복사해 분기 상태를 분리합니다. 산업용 문제에는 watched literals, clause learning, backjumping과 재시작을 갖춘 검증된 SAT 구현을 사용합니다. 이 예제는 변수 수를 24개 이하로 제한합니다.

```bash
python 예제_examples/심화_advanced/math_reasoning/demo.py
python -m unittest discover -s 예제_examples/심화_advanced/math_reasoning -p "test_*.py" -v
```

### 5. 답을 다시 검증합니다

SAT 결과의 할당은 원래 모든 절에 다시 대입해 확인할 수 있습니다. UNSAT는 만족 할당이 없다는 전칭적 주장이라 같은 방식의 단일 할당 증명이 되지 않습니다. 테스트에서는 변수 1~6개인 무작위 CNF 420개를 모든 진리값 조합으로 독립 확인하고, DPLL의 SAT/UNSAT 결과와 비교합니다. 빈 입력·빈 절·동어반복·잘못된 변수 번호도 검사합니다. 이 작은 검증은 구현의 오류를 찾는 기준이며, 큰 문제의 UNSAT 인증서 검사를 대체하지 않습니다.

이 글의 예는 명제 논리의 계산 예제입니다. 실제 LEET·PSAT 등의 기출 해설은 별도의 공식 문제 출처에 연결된 글에서 다룹니다. 논리식 계산은 반례를 찾는 도구이며, 시험 점수나 일반적인 인지능력의 향상 효과를 수치로 입증하는 실험은 아닙니다.

## English

### 1. Entailment through counterexamples

An argument is valid when no assignment makes every premise true and the conclusion false. Agreement with the conclusion and the empirical truth of the premises are separate questions. With premises $`\Gamma`$ and conclusion $`C`$, entailment is equivalent to unsatisfiability of $`\Gamma\land\neg C`$. A single satisfying assignment refutes entailment; many positive examples cannot establish it. This duality and the propagation/branching rules were compared across [CMU 15-414, pp. 1–5](https://www.cs.cmu.edu/~15414/s25/lectures/16-dpll.pdf) and the [Abstract DPLL paper hosted by Stanford](https://web.stanford.edu/class/cs357/NOT04.pdf).

### 2. Clauses and propagation

A literal is an atom or its negation. A clause is a disjunction of literals; CNF is a conjunction of clauses. Integer literals encode $`(\neg p\lor q)\land p\land\neg q`$ as `[[-1,2],[1],[-2]]`. An empty clause is false, while an empty conjunction of clauses is true. A clause containing both signs of one variable is always true and can be removed. Opposite literals in different clauses do not justify that removal.

The implementation accepts CNF, not unrestricted natural language. Translating scope and quantifiers is a separate modeling task; arbitrary finite propositional substitutions need not preserve a first-order argument.

A unit clause requires its remaining literal to be true. Remove satisfied clauses and remove the opposite literal from other clauses, preserving satisfiability under the unit assignment. In the example, $`p`$ reduces $`\neg p\lor q`$ to $`q`$, conflicting with $`\neg q`$. The empty clause closes this branch, establishing modus ponens by refutation. Reversing the inference from $`p\to q`$ and $`q`$ to $`p`$ leaves the counterexample $`p=\mathrm{false},q=\mathrm{true}`$.

### 3. Search and independent checks

If propagation leaves unresolved clauses, branch on an unassigned variable. Every model belongs to one branch, and each decision reduces the remaining variables, yielding finite termination. `sat_dpll` chooses a most-frequent remaining variable with deterministic tie-breaking. Propagation and ordering prune work without removing exponential worst-case complexity. Copies isolate the small example's branch states; production solvers use techniques such as watched literals, clause learning, backjumping and restarts. This implementation accepts at most 24 variables.

The commands run the example and tests. Returned models are checked against the original clauses. UNSAT is a universal claim and cannot be checked by substituting one assignment. Tests compare 420 random CNFs with exhaustive truth-table enumeration for one to six variables and cover empty inputs, contradictions, tautologies and invalid literals. These bounded checks do not replace proof-certificate verification for large UNSAT instances.

The examples demonstrate logical computation. Official LEET/PSAT past-paper analyses remain in their separately sourced articles. A SAT implementation is a tool for reasoning about counterexamples, not an experiment establishing gains in test scores or general cognition.

## 출처 / Sources

명제의 만족성·타당성, CNF, 단위 전파와 분기 규칙을 대학 자료 및 원논문으로 대조했습니다. / Satisfiability, validity, CNF, propagation and branching were checked against university material and the original formal treatment. 확인 / checked: 2026-10-19.
