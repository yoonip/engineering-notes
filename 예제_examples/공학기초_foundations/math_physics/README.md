# 수학·물리 참조 모델 | Mathematics and physics reference models

[구현](models.py) · [검사](test_models.py)

외부 패키지 없이 실행하는 작은 모델입니다. 단위를 통일한 실수 입력을 사용하며, 각 모델의 가정과 유도는 연결된 글에 설명합니다.

| 함수 | 본문 | 계산 비용 |
|---|---|---|
| `resistance_uncertainty` | [단위·차원·불확도](../../../전자컴퓨터공학_ece/06-수식과코드_math-to-code/해설_notes/단위차원측정불확도_units-dimensional-analysis-uncertainty.md) | 시간·추가 공간 O(1) |
| `least_squares_qr` | [선형대수·최소제곱](../../../전자컴퓨터공학_ece/06-수식과코드_math-to-code/해설_notes/선형대수와최소제곱_linear-algebra-least-squares.md) | 조밀한 m×n, m≥n에서 시간 O(mn²), 공간 O(mn) |
| `mean_variance`, `normal_mean_interval` | [확률·추정](../../../전자컴퓨터공학_ece/06-수식과코드_math-to-code/해설_notes/확률평균추정의불확실성_probability-estimation.md) | 평균·분산은 시간 O(n), 추가 공간 O(1); 구간 계산은 O(1) |
| `decay_euler` | [미분방정식·수치해](../../../전자컴퓨터공학_ece/06-수식과코드_math-to-code/해설_notes/미분방정식에서수치해로_differential-equations-numerics.md) | N단계에서 시간 O(N), 추가 공간 O(1) |
| `oscillator_verlet` | [역학·진동](../../../전자컴퓨터공학_ece/56-물리기초_physics-foundations/해설_notes/역학에너지진동_mechanics-energy-oscillation.md) | N단계에서 시간 O(N), 생성기 상태 O(1) |
| `heat_ftcs` | [열전도·확산](../../../전자컴퓨터공학_ece/56-물리기초_physics-foundations/해설_notes/열전도와확산_heat-diffusion.md) | N단계·M+1점에서 시간 O(NM), 추가 공간 O(M) |

저장소 최상위 폴더에서 실행합니다.

```bash
python -m unittest discover -s 예제_examples/공학기초_foundations/math_physics -p "test_*.py" -v
```

2026-10-19, CPython 3.12.14에서 24개 검사를 통과했습니다. 수치해를 해석해, 독립 손계산, 표준 라이브러리 통계, 불변식과 비교하며 경계값·잘못된 입력도 검사합니다. 오차는 다음과 같습니다. 마지막 자릿수는 실행 환경에 따라 조금 달라질 수 있습니다.

| 검사 사례 | 결과 |
|---|---|
| $y'=-y$, $y(0)=1$, T=1; Euler N=20, 40, 80 | 절대오차 0.00939352, 0.00464700, 0.00231130 |
| 열방정식, L=α=1, T=0.05, 초기 sin(πx); M=20, 40 | 최대 절대오차 0.000248242, 0.0000619745 |
| 무감쇠 진동자 m=1, k=4, x₀=0.3, v₀=0; T=100, N=10000 | 최대 에너지 상대오차 약 0.000100000 |
| V=2, I=0.01, uV=0.002, uI=0.00001, 독립 | R=200 Ω, uR≈0.282843 Ω |
| (0,1), (1,2), (2,2)의 직선 교정 | 절편 7/6, 기울기 1/2 |

신뢰구간 함수는 알려진 모집단 표준편차를 쓰는 독립 정규 표본 모델입니다. 표본 표준편차로 바꿔 넣으면 t 구간이 되지 않습니다. QR은 열 독립인 조밀한 실수 행렬을 위한 구현이며 랭크가 부족하거나 수치적으로 분리되지 않는 입력을 거부합니다. Fourier 법칙의 상수 계수 막대, 무감쇠 선형 스프링 등 단순화된 모델을 검사한 결과이며 실제 기기 측정 결과는 아닙니다. 극단적인 크기의 입력에서는 유한 정밀도와 중간 연산의 표현 범위를 추가로 고려해야 합니다.

## English

These small models use only Python's standard library. Inputs are real values in consistent units; linked articles state the assumptions and derivations. The table maps each implementation to its explanation and computational cost. Mean and variance use one pass; QR handles dense full-column-rank matrices; the oscillator is a generator; heat diffusion exchanges two buffers without keeping a complete time history.

Run the command above from the repository root. All 24 tests passed on 2026-10-19 with CPython 3.12.14. They compare numerical calculations with analytical solutions, independent hand calculations, standard-library statistics, and invariants, including boundary and invalid-input checks. The table reports absolute Euler errors for N=20/40/80, maximum heat-grid errors for M=20/40, maximum relative oscillator-energy error, a resistance uncertainty calculation, and fitted line coefficients. Final digits may vary slightly by runtime.

The interval function assumes independent normal observations and known population standard deviation. Substituting a sample standard deviation does not turn it into a t interval. QR requires dense real full-column-rank input and rejects deficient or numerically unresolved columns. The results verify simplified mathematical models, including a constant-coefficient conductive rod and an undamped linear spring; they are not instrument measurements. Extreme input magnitudes additionally require attention to finite precision and representable intermediate values.
