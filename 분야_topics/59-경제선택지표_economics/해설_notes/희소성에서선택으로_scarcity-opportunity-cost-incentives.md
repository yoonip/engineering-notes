# 희소성에서 선택으로: 기회비용, 한계와 유인

[경제학](../README.md) · [GDP와 물가](GDP와물가읽기_gdp-inflation-real-values.md)

## 한국어

### 돈이 충분해도 선택은 남는다

하루가 24시간이라는 사실만으로도 선택이 필요하다. 어떤 일을 하는 시간에는 다른 일을 할 수 없고, 같은 공간과 장비를 여러 용도로 동시에 쓰기 어려울 수도 있다. 희소성은 단순히 가난하거나 물건이 드물다는 뜻이 아니라, 가능한 욕구와 목적에 비해 자원에 제약이 있다는 뜻이다.

기회비용은 선택 때문에 포기한 대안 중 가장 가치 있는 것의 가치다. 포기한 대안을 모두 더한 금액이 아니며, 현금 지출만 뜻하지도 않는다. 무료 서비스도 시간이나 주의를 사용한다. 이미 지출했고 회수할 수 없는 매몰비용과, 지금 선택에 따라 달라질 미래 비용은 구분한다. 과거 경험에서 얻은 정보는 유용하지만, 회수 불가능한 지출 자체가 추가 투자의 편익은 아니다. [Rice University OpenStax, Principles of Economics 3e §2.1](https://openstax.org/books/principles-economics-3e/pages/2-1-how-individuals-make-choices-based-on-their-budget-constraint)

### 제약식을 쓰면 포기하는 것이 보인다

다음은 계산을 위한 가상 생산 예다. 실제 작업 시간이나 성능을 측정한 자료가 아니다. 사용 가능한 시간이 12시간이고 A 한 단위에 2시간, B 한 단위에 3시간이 든다고 하자. 준비 시간이나 병행 작업 없이 시간이 선형으로 더해진다는 가정에서

$$2a+3b\le12,\qquad a,b\ge0.$$

경계에서는 $`b=4-(2/3)a`$이므로 A를 한 단위 더 만들려면 B를 $`2/3`$단위 줄여야 한다. 같은 내용을 B 한 단위의 기회비용은 A 1.5단위라고 표현할 수 있다. 실제 물건을 나눌 수 없다면 가능한 정수 조합끼리 비교해야 한다. 예산·시간 제약과 기회비용의 관계는 [MIT 14.01SC의 Budget Constraints](https://ocw.mit.edu/courses/14-01sc-principles-of-microeconomics-fall-2011/pages/unit-2-consumer-theory/budget-constraints/)와도 대조했다.

이 경계는 가능한 생산의 조합을 보여 주지만 무엇이 더 좋은지는 말해 주지 않는다. 모든 효율적 선택이 공정하거나 바람직하다는 뜻도 아니다. 생산가능곡선은 기술과 자원, 두 생산물의 관계를 표현한 모델이다. 자원별 적합성이 다르면 한계 기회비용이 변할 수 있고, 항상 직선이거나 항상 같은 곡률일 필요는 없다. [OpenStax §2.2](https://openstax.org/books/principles-economics-3e/pages/2-2-the-production-possibilities-frontier-and-social-choices)

### 전체 합계보다 다음 한 단위를 비교하기

한계편익은 한 단위를 더 선택했을 때 늘어나는 편익, 한계비용은 그때 추가되는 비용이다. 이미 얻은 전체 편익이 크다는 이유만으로 다음 한 단위도 유리하지는 않다. 순편익을 $`N(q)=B(q)-C(q)`$라고 정의하면

$$N'(q)=B'(q)-C'(q).$$

미분 가능한 내부 최적점에서는 $`B'(q)=C'(q)`$가 필요한 조건이다. 이것만으로 최대라고 보장되지는 않는다. 가능한 범위의 끝점과 다른 후보도 비교해야 하며, $`B`$가 오목하고 $`C`$가 볼록한 등의 조건이 있으면 이 판단이 더 간단해진다. 불연속·정수 선택에는 미분식을 그대로 적용하지 않는다. 한계 비교는 소비 선택에서도 쓰이지만, 효용 숫자를 사람 간 행복의 절대 단위처럼 읽지는 않는다. [OpenStax §6.1](https://openstax.org/books/principles-economics-3e/pages/6-1-consumption-choices)

가상 점수 $`U_A=[0,7,12,15,17,18,18]`$, $`U_B=[0,9,15,19,21]`$를 각각 생산량의 편익으로 정하고 합산 가능하다고 가정해 보자. 이것은 가치 판단을 설명하기 위해 정한 점수이며 관측 자료가 아니다.

```python
benefit_a = [0, 7, 12, 15, 17, 18, 18]
benefit_b = [0, 9, 15, 19, 21]
# 작은 정수 문제는 모든 가능한 조합을 확인해 경계와 끝점을 놓치지 않는다.
plans = [(a, b) for a in range(7) for b in range(5) if 2*a + 3*b <= 12]
best = max(plans, key=lambda pair: benefit_a[pair[0]] + benefit_b[pair[1]])
print(best)  # 최적 조합은 (3, 2)이며 점수는 30이다.
```

이 예에서는 제약을 만족하는 모든 조합을 직접 비교하므로 선택이 점수 정의와 일치하는지 확인할 수 있다. 점수의 합산 방식이나 자원 조건을 바꾸면 답도 달라질 수 있다. 계산의 정확성과 점수에 대한 사회적 동의는 다른 질문이다.

### 유인은 행동을 바꾸지만 결과를 자동 결정하지 않는다

유인은 행동의 예상 편익과 비용을 바꾸는 조건이다. 가격, 보상, 벌칙뿐 아니라 시간, 정보와 사회적 기대도 영향을 준다. 같은 유인이라도 제약과 정보가 다르면 반응이 다를 수 있다. 가격 변화의 효과를 볼 때는 다른 조건도 함께 바뀌었는지 확인한다.

외부효과는 거래 당사자 바깥의 사람에게 미치는 영향을 말한다. 오염 비용이 가격에 반영되지 않으면 개인의 한계비용과 사회적 한계비용이 달라질 수 있다. 단순 모델에서 $`MSC=MPC+MEC`$로 쓴다. 각각 사회적·사적·외부 한계비용이다. 그러나 외부효과가 있다는 말만으로 특정 정책의 효과나 정당성이 입증되지는 않는다. 피해 추정, 집행 비용, 대안과 부담의 분포를 함께 비교한다. [OpenStax §12.1](https://openstax.org/books/principles-economics-3e/pages/12-1-the-economics-of-pollution)

실제 분석에서는 예산·시간·가격의 기준을 기록하고, 고정비와 추가 비용, 개인과 사회의 범위를 나눈다. 이후 자료에서 선택과 결과의 변화를 확인하되, 단순 상관관계를 유인의 인과효과라고 단정하지 않는다. 경제모형은 선택의 조건을 드러내는 도구이며 사람의 목적이나 공정성의 기준을 대신 정하지 않는다.

## English

### Choice remains even without a money shortage

A 24-hour day already creates tradeoffs: time spent on one activity is unavailable for another, and space or equipment may not serve every purpose simultaneously. Scarcity means resources are constrained relative to possible goals, rather than simply that someone is poor or an item is rare.

Opportunity cost is the value of the best alternative forgone. It is neither the sum of every rejected alternative nor merely a cash payment. A free service can still consume time and attention. Separate unrecoverable sunk costs from future costs that change with the present choice. Past experience provides information, but an unrecoverable payment does not itself create a benefit from continuing. [OpenStax §2.1](https://openstax.org/books/principles-economics-3e/pages/2-1-how-individuals-make-choices-based-on-their-budget-constraint)

### A constraint reveals the tradeoff

The following is a hypothetical calculation, not measured production data. Suppose 12 hours are available, A requires two hours per unit, and B requires three. Assuming additive time without setup or parallel work,

$$2a+3b\le12,\qquad a,b\ge0.$$

At the boundary, $`b=4-(2/3)a`$. One more A costs $`2/3`$ of B; one B costs 1.5 A. Indivisible outputs require comparisons among feasible integer combinations. The connection between constraints and opportunity cost is also checked against [MIT 14.01SC, Budget Constraints](https://ocw.mit.edu/courses/14-01sc-principles-of-microeconomics-fall-2011/pages/unit-2-consumer-theory/budget-constraints/).

The boundary identifies feasibility, not desirability. Production efficiency alone does not imply fairness. A production frontier models resources and technology. Different resource suitability can change marginal opportunity cost, so the frontier need not always be straight or have the same curvature. [OpenStax §2.2](https://openstax.org/books/principles-economics-3e/pages/2-2-the-production-possibilities-frontier-and-social-choices)

### Compare the next unit

Marginal benefit is the benefit added by another unit; marginal cost is its additional cost. Large benefits already obtained do not establish that the next unit is worthwhile. With $`N(q)=B(q)-C(q)`$, differentiation gives $`N'(q)=B'(q)-C'(q)`$. A differentiable interior optimum requires equal marginal benefit and cost, but this alone does not prove a maximum. Compare endpoints and other candidates; concave benefits and convex costs provide useful additional conditions. Discrete choices require a discrete comparison. Utility numbers are not automatically interpersonal units of happiness. [OpenStax §6.1](https://openstax.org/books/principles-economics-3e/pages/6-1-consumption-choices)

The code defines hypothetical additive benefit scores $`[0,7,12,15,17,18,18]`$ for A and $`[0,9,15,19,21]`$ for B. These are explanatory assumptions, not observations. Enumerating every feasible integer pair gives $`(3,2)`$ with score 30. This checks consistency with the stated objective, not public agreement with it. Changing the scoring rule or constraints can change the result.

### Incentives influence behavior without uniquely determining outcomes

An incentive changes the expected benefits or costs of an action. Prices, rewards, penalties, time, information, and social expectations can all matter. Responses can differ because constraints and information differ. When examining a price change, check what else changed too.

An externality affects people outside a transaction. Unpriced pollution can create a gap between private and social marginal costs. A simple model writes $`MSC=MPC+MEC`$, adding marginal external cost to private marginal cost. Recognizing an externality does not establish a particular policy's effectiveness or justification. Compare estimated harm, enforcement costs, alternatives, and the distribution of burdens. [OpenStax §12.1](https://openstax.org/books/principles-economics-3e/pages/12-1-the-economics-of-pollution)

Applied analysis records the budget, time and price basis, distinguishes fixed from incremental costs, and separates private from social scope. Subsequent evidence can track choices and outcomes, but correlation alone does not establish an incentive's causal effect. Economic models clarify conditions; they do not choose people's purposes or settle fairness criteria.

## 출처와 대조 / Sources and cross-check

- Rice University OpenStax, *Principles of Economics 3e*, §§2.1–2.2: 기회비용·매몰비용·가능한 조합 / opportunity cost, sunk costs, and feasibility.
- 같은 교재 §6.1: 한계 비교와 효용 해석 / marginal comparison and interpretation of utility.
- 같은 교재 §12.1: 사적 비용과 외부효과 / private costs and externalities.
- MIT 14.01SC, *Budget Constraints*: 시간·예산 제약과 기회비용의 교차 확인 / independent cross-check of time/budget constraints and opportunity cost.

제약·편익·사회적 비용의 범위를 서로 대조했다. 수치 예는 직접 구성하고 가능한 정수 조합을 열거해 검산했다. / Constraint, benefit, and social-cost scopes were checked against each other. Numerical examples are original and checked by enumerating feasible integer pairs. 확인 / checked: 2026-10-19.
