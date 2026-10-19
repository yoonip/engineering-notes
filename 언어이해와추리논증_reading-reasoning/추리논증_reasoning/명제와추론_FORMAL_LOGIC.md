# 명제와 추론: 참인 말에서 따라 나오는 말 | Propositions and inference

[추론·적성](../README.md) · [실행 코드](../../예제_examples/추론_reasoning/README.md)

## 한국어

### 사실과 추론의 모양을 나누기

“조건을 만족하면 승인한다”에서 조건을 만족했다는 것과 승인되었다는 것은 다른 정보입니다. 조건문을 읽으면서 방향을 뒤집으면 그럴듯하지만 잘못된 결론을 얻을 수 있습니다. 먼저 문장 자체가 참인지와, 주어진 전제에서 결론이 반드시 따라오는지를 나눕니다. 이 글은 참·거짓 두 값을 사용하는 고전논리를 다룹니다.

명제는 참이나 거짓으로 판단할 수 있는 서술입니다. 아직 어느 쪽인지 모른다고 명제가 아닌 것은 아닙니다. 술어 $`P(x)`$는 변수와 해석 영역을 정해야 참·거짓이 결정됩니다. “$`x>0`$”은 $`x`$를 정하지 않으면 완결된 명제와 다릅니다. 명제·술어·양화의 구분은 [MIT 6.042 Chapter 1](https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-fall-2010/7853d585044ef21bce5f48ce5fc89d28_MIT6_042JF10_chap01.pdf)을 기준으로 삼았습니다.

### 필요조건과 충분조건

$`p\to q`$는 $`p`$가 참이고 $`q`$가 거짓인 경우만 금지합니다. 따라서 $`p`$는 $`q`$의 충분조건이고, $`q`$는 $`p`$의 필요조건입니다. “오직 q일 때만 p”도 $`p\to q`$입니다. “p이면 그리고 그때에만 q”는 양방향 $`p\leftrightarrow q`$입니다.

| p | q | $`p\to q`$ | $`q\to p`$ |
|---|---|---|---|
| 거짓 | 거짓 | 참 | 참 |
| 거짓 | 참 | 참 | 거짓 |
| 참 | 거짓 | 거짓 | 참 |
| 참 | 참 | 참 | 참 |

$`p`$가 거짓인 두 행에서도 조건문은 참입니다. 이것이 인과관계를 알아냈다는 뜻은 아닙니다. 논리적 조건문은 어떤 조합을 배제하는지 정하고, 원인·시간 순서·실제 규정의 예외는 별도로 모델링합니다.

$$p\to q\equiv\neg p\lor q\equiv\neg q\to\neg p.$$

마지막 식은 대우입니다. 역 $`q\to p`$나 이 $`\neg p\to\neg q`$는 일반적으로 원래 조건문과 같지 않습니다. $`p\to q`$와 $`q`$만으로 $`p`$를 결론 내리는 후건 긍정은 표의 두 번째 행이 반례입니다. $`p\to q`$와 $`p`$에서 $`q`$를 얻는 전건 긍정은 모든 행에서 성립합니다.

### 타당성과 실제 참은 다릅니다

전제 집합 $`\Gamma`$가 결론 $`c`$를 함의한다는 것은, 전제를 모두 참으로 만드는 모든 해석에서 $`c`$도 참이라는 뜻입니다.

$$\Gamma\models c\quad\Longleftrightarrow\quad
\text{전제를 모두 만족하고 }\neg c\text{도 만족하는 해석이 없다.}$$

그런 해석 하나가 반례입니다. 논증이 타당하고 전제가 모두 참이면 건전한 논증이지만, 타당성만으로 현실의 전제가 참이라고 확인되지는 않습니다. 모순된 전제는 만족하는 해석 자체가 없으므로 고전논리에서는 모든 결론을 함의합니다. 따라서 프로그램은 함의 여부와 함께 전제를 만족하는 해석의 개수도 반환합니다. 이 구분은 [Stanford Introduction to Logic, §§3.4–3.6](https://logical.stanford.edu/intrologic/sections/section_03.html?section=1)와 대조했습니다.

### “모든”과 “어떤”의 범위

영역 $`D`$에서 $`\forall x\in D:P(x)`$는 모든 원소가 조건을 만족한다는 뜻이고, $`\exists x\in D:P(x)`$는 적어도 하나가 만족한다는 뜻입니다. 부정하면

$$\neg\forall x:P(x)\equiv\exists x:\neg P(x),\qquad
\neg\exists x:P(x)\equiv\forall x:\neg P(x).$$

“모두 해당하지는 않는다”는 “아무도 해당하지 않는다”가 아니라 반례가 적어도 하나 있다는 말입니다. $`\forall x\exists y:R(x,y)`$에서 각 $`x`$마다 다른 $`y`$를 골라도 되지만, $`\exists y\forall x:R(x,y)`$는 하나의 공통 $`y`$를 요구합니다. 빈 영역에서는 전칭문이 참이고 존재문이 거짓이므로, 현실 문장의 존재 전제도 확인해야 합니다. 양화 부정과 반례 방식은 [MIT Predicate Logic II](https://courses.csail.mit.edu/6.042/spring18/predicate-logic2.pdf)에 근거합니다.

### 계산과 검증

```python
from 예제_examples.추론_reasoning.models import check_entailment, implies

# 전제를 만족해도 결론이 거짓인 배정이 있는지 찾는다.
result = check_entailment(
    ["p", "q"],
    [lambda a: implies(a["p"], a["q"]), lambda a: a["q"]],
    lambda a: a["p"],
)
print(result)
```

결과의 반례는 `p=False, q=True`입니다. 명제 $`n`$개와 평가 비용 $`L`$에 대해 시간은 $`O(2^nL)`$입니다. 진리표 전체를 저장하지 않아 현재 배정·반례 공간은 $`O(n)`$입니다. 예제는 이름 16개 이하의 작은 유한 명제논리를 대상으로 합니다. 이 검사가 자연어 번역이나 무한 영역의 술어논리까지 증명하지는 않습니다.

검사는 조건문의 네 행, 대우, 후건 긍정 반례, 전건 긍정, 모순 전제의 공허한 함의를 확인합니다. 크기 0–4인 유한 영역의 모든 술어 배정에서 양화 부정도 비교합니다. 유한 영역 검사는 해당 크기에서 구현을 확인하는 것이며 일반 정리의 증명은 양화의 정의에 따릅니다.

연역은 전제가 참일 때 결론의 참을 보존하는 추론입니다. 귀납은 관측에서 더 넓은 경향을 추정하고, 가설적 추론(abduction)은 관측을 설명할 후보를 고릅니다. 뒤의 둘은 새로운 정보로 바뀔 수 있습니다. 가설에서 관측이 예상된다고 관측만으로 가설이 논리적으로 확정되는 것은 아닙니다. 구분과 한계는 [Stanford Encyclopedia of Philosophy, Abduction §1.1](https://plato.stanford.edu/entries/abduction/)과 함께 확인했습니다.

## English

### Truth, direction, and validity

“If the condition is met, approval follows” distinguishes meeting a condition from receiving approval. Reversing that direction can produce a plausible but invalid conclusion. Classical logic uses two truth values and separates the truth of a statement from whether a conclusion follows from premises. A proposition is a declarative claim with a truth value, even if that value is unknown. A predicate $`P(x)`$ depends on an assigned value and domain. See [MIT 6.042 Chapter 1](https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-fall-2010/7853d585044ef21bce5f48ce5fc89d28_MIT6_042JF10_chap01.pdf).

The implication $`p\to q`$ excludes exactly $`p`$ true and $`q`$ false. Thus $`p`$ is sufficient for $`q`$, while $`q`$ is necessary for $`p`$. “p only if q” has this same direction. “p if and only if q” requires both directions. The truth table above evaluates both the implication and its converse. False antecedents make the material conditional true; this alone establishes no causal relationship. Causation, time, and exceptions require additional modelling.

Since $`p\to q\equiv\neg p\lor q\equiv\neg q\to\neg p`$, the contrapositive is equivalent. The converse $`q\to p`$ and inverse $`\neg p\to\neg q`$ are not generally equivalent. Affirming the consequent—from $`p\to q`$ and $`q`$ to $`p`$—fails at $`p`$ false, $`q`$ true. Modus ponens—from $`p\to q`$ and $`p`$ to $`q`$—preserves truth.

Premises $`\Gamma`$ entail $`c`$ when every interpretation satisfying them also satisfies $`c`$. Equivalently, no interpretation satisfies all premises and $`\neg c`$. One such interpretation is a counterexample. A valid argument with true premises is sound; validity does not establish real-world premise truth. Inconsistent premises have no satisfying interpretation and classically entail every conclusion. The code therefore reports the count of premise models as well as entailment. [Stanford's logic course §§3.4–3.6](https://logical.stanford.edu/intrologic/sections/section_03.html?section=1) provides this distinction.

### Quantifiers, computation, and inference types

For domain $`D`$, $`\forall x:P(x)`$ means every element satisfies the predicate, and $`\exists x:P(x)`$ means at least one does. Negation exchanges quantifiers: $`\neg\forall x:P(x)\equiv\exists x:\neg P(x)`$ and $`\neg\exists x:P(x)\equiv\forall x:\neg P(x)`$. “Not all” does not mean “none.” In $`\forall x\exists y:R(x,y)`$, the witness may vary with $`x`$; $`\exists y\forall x:R(x,y)`$ requires a common witness. Universal claims over an empty domain are true, existential ones false, so natural-language existence assumptions matter. See [MIT Predicate Logic II](https://courses.csail.mit.edu/6.042/spring18/predicate-logic2.pdf).

The Python example finds the counterexample `p=False, q=True`. With $`n`$ propositions and formula-evaluation cost $`L`$, exhaustive checking takes $`O(2^nL)`$ time. Streaming truth assignments uses $`O(n)`$ assignment/counterexample storage rather than a complete table. The implementation limits names to 16 and checks finite propositional formulas, not the correctness of a natural-language translation or unrestricted predicate logic.

Tests cover all four conditional rows, contrapositive equivalence, the converse fallacy, modus ponens, and vacuous entailment from inconsistency. Every predicate assignment on domains of size 0–4 is checked against quantifier-negation identities. These finite checks verify implementation at those sizes; the general identities follow from quantifier definitions.

Deduction preserves conclusion truth given true premises. Induction extends observations to broader patterns; abduction selects explanatory hypotheses. The latter two remain revisable. A hypothesis predicting an observation is not logically established by that observation alone. These distinctions and limitations are discussed in [Stanford Encyclopedia of Philosophy, Abduction §1.1](https://plato.stanford.edu/entries/abduction/).

## 출처 / Sources

- [MIT 6.042, Chapter 1: Propositions](https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-fall-2010/7853d585044ef21bce5f48ce5fc89d28_MIT6_042JF10_chap01.pdf) — 명제·조건문·술어·양화 / propositions, conditionals, predicates, quantifiers.
- [MIT Predicate Logic II](https://courses.csail.mit.edu/6.042/spring18/predicate-logic2.pdf) — 양화 부정·타당성·반례 / quantifier negation, validity, countermodels.
- [Stanford Introduction to Logic, Lesson 3](https://logical.stanford.edu/intrologic/sections/section_03.html?section=1) — 함의·모순·해석 / entailment, inconsistency, interpretations.
- [Stanford Encyclopedia of Philosophy: Abduction §1.1](https://plato.stanford.edu/entries/abduction/) — 연역·귀납·가설적 추론 / deduction, induction, abduction.

참고일 / Accessed: 2026-10-19. 진리표와 코드는 개념 검증용으로 구성했습니다. / The truth table and code were constructed for conceptual verification.
