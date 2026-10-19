# 추론을 계산으로 확인하기 | Verifying reasoning with computation

[코드](models.py) · [검사](test_models.py) · [검증 기록 / Verification](VERIFICATION.json) · [추론·적성](../../추론과시험_reasoning/57-추론적성시험_reasoning-assessments/README.md)

명제논리의 반례, 가중평균과 Bayes 계산, 유한 이항 제약의 해와 최소 비용을 확인하는 표준 라이브러리 예제입니다. 저장소 최상위 폴더에서 실행합니다.

```bash
python -m unittest 예제_examples.추론_reasoning.test_models -v
```

| 구현 | 범위와 비용 |
|---|---|
| `check_entailment` | 명제 16개 이하. 전제 모형 수·함의·첫 반례를 반환. n개 명제와 식 평가 비용 L에서 시간 O(2ⁿL), 배정·반례 공간 O(n) |
| `weighted_mean` | 비음수 가중치와 양의 가중치 합. O(n)개의 유리수 연산, 일정 개수 누산기 |
| `relative_change` | 양의 기준값을 쓰는 상대 변화 |
| `bayes_binary` | P(H), P(E\|H), P(E\|¬H)를 입력. P(E)=0이면 거부 |
| `iter_solutions` | 유한 정수 도메인·이항 제약, AC-3와 MRV 탐색. 해를 하나씩 반환 |
| `minimize_cost` | 변수별 유리수 비용의 합 최소화. 독립 최소 비용 하한으로 가지치기하며 최적해 하나를 반환 |

유리수 연산 수와 비트 연산 비용은 다릅니다. 분자·분모가 커지면 각 연산 비용도 늘어납니다. 십진수를 정확히 표현하려면 float로 바꾸기 전에 문자열이나 `Fraction`으로 전달합니다. 제약 탐색은 전파와 가지치기를 써도 최악에는 지수적으로 커질 수 있습니다. 자세한 가정과 계산 비용은 각 본문에 있습니다.

2026-10-19, CPython 3.12.14에서 19개 검사를 통과했습니다. 작은 제약 모델 80개의 해 집합과 최저 비용을 별도의 전체 배정 검사와 비교했습니다. 가중평균은 100개의 집단 예를 원래 관측값으로 펼친 평균과 비교하고, Bayes는 직접 센 사건 수와 비교합니다. 논리 검사는 진리표, 반례와 모순 전제, 유한 영역 양화 부정을 확인합니다. 이 예제는 자연어 의미를 자동 판정하거나 실제 시험의 점수를 예측하는 도구가 아닙니다.

## English

These standard-library examples check propositional countermodels, weighted means, Bayes calculations, and solutions/minimum costs of finite binary constraint models. Run the command above from the repository root.

The table states each implementation's scope. Truth-table checking uses at most 16 propositions and streams assignments. Weighted means use a constant number of accumulators and O(n) rational operations. Relative changes require a positive baseline. Binary Bayes rejects zero-probability evidence. Constraint solving uses AC-3 propagation and MRV search; optimization uses a separable-cost lower bound and returns one optimum.

Rational-operation counts differ from bit complexity: larger numerators and denominators increase per-operation cost. Pass exact decimal strings or `Fraction` values before conversion to binary float. Constraint search can remain exponential despite propagation and pruning. Linked articles state the detailed assumptions and costs.

All 19 tests passed on 2026-10-19 with CPython 3.12.14. An independent exhaustive checker verifies complete solution sets and minimum costs for 80 small seeded constraint models. Weighted means are compared with 100 expanded-population examples; Bayes uses direct event counts. Logic tests cover truth tables, countermodels, contradictory premises, and finite-domain quantifier negation. This is not an automatic judge of natural-language meaning or a predictor of assessment scores.
