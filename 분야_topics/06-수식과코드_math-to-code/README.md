# 수식과 코드 | Math to Code

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

수식을 코드로 옮길 때는 변수의 뜻과 단위, 값의 범위부터 정합니다. 같은 식이라도 연속 시간 모델인지 표본화된 모델인지, 실수 계산인지 고정소수점 계산인지에 따라 구현이 달라집니다.

## 미분방정식에서 반복문으로

RC 충전 회로는 `dv/dt = (Vin - v)/(RC)`로 표현됩니다. 전진 Euler 방법은 현재 기울기로 다음 값을 계산합니다. `v[n+1] = v[n] + dt*(Vin-v[n])/(RC)`이며 오차는 시간 간격 `dt`와 관련됩니다.

```python
from math import exp

R, C, vin = 1000.0, 1e-6, 3.3
dt, steps = 1e-5, 500
v = 0.0
for _ in range(steps):
    v += dt * (vin - v) / (R * C)
t = dt * steps
exact = vin * (1.0 - exp(-t / (R * C)))
print(f"Euler={v:.6f}, analytic={exact:.6f}, error={abs(v-exact):.6f}")
```

## 부동소수점과 수치 안정성

부동소수점은 유한한 비트로 수를 표현합니다. 크기가 비슷한 두 수를 빼면 유효숫자가 손실될 수 있고, 반복 누적에서는 반올림 오차가 쌓입니다. 선형 연립방정식 `Ax=b`는 역행렬을 직접 계산하기보다 분해 기반 해법으로 푸는 경우가 일반적입니다.

선형대수는 좌표 변환·최소제곱·신경망 연산에, 미적분은 변화율과 최적화에, 확률·통계는 잡음과 추정에 쓰입니다. 그래프 이론은 연결 관계와 경로를 다룹니다. 정보이론의 엔트로피는 확률 분포의 불확실성을 수치화합니다. 실제 계산에서는 이산화 방식과 정밀도, 경계조건이 결과를 좌우합니다.

## 관련 기술

Calculus, Linear Algebra, Probability, Statistics, ODE/PDE, Numerical Analysis, Optimization, Information Theory, Graph Theory

## 참고 자료

- [NumPy documentation](https://numpy.org/doc/)
- [SciPy documentation](https://docs.scipy.org/doc/scipy/)


## 개념·유도·모델·검증

[기초부터 읽기](../../공학기초_foundations/README.md)

- [미분방정식에서 수치해로](해설_notes/미분방정식에서수치해로_differential-equations-numerics.md)
- [선형대수와 최소제곱](해설_notes/선형대수와최소제곱_linear-algebra-least-squares.md)
- [확률, 평균, 추정의 불확실성](해설_notes/확률평균추정의불확실성_probability-estimation.md)
- [단위, 차원, 측정 불확도](해설_notes/단위차원측정불확도_units-dimensional-analysis-uncertainty.md)

## English

Turning an equation into code starts with the meaning, units, and valid range of its variables. Implementation also depends on whether the model uses continuous or sampled time, and whether computation uses floating-point or fixed-point values.

### From a differential equation to a loop

An RC charging circuit follows `dv/dt = (Vin - v)/(RC)`. Forward Euler estimates the next value from the current slope: `v[n+1] = v[n] + dt*(Vin-v[n])/(RC)`. Its error depends on the time step `dt`. The example above iterates this update, calculates the analytical voltage at the same final time, and prints the absolute difference.

### Equivalent equations and numerical behavior

Floating-point numbers use a finite number of bits. Subtracting values that are close together can lose significant digits, and repeated accumulation introduces rounding error. A linear system `Ax=b` is usually solved with a factorization-based method rather than by forming an explicit inverse.

Linear algebra supports coordinate transforms, least squares, and neural-network operations. Calculus describes rates of change and optimization; probability and statistics describe noise and estimation. Graph theory handles connections and paths, while information-theoretic entropy quantifies uncertainty in a probability distribution. Discretization, precision, and boundary conditions connect these mathematical models to executable calculations.


### Concepts, derivations, models, and verification

[Foundations reading guide](../../공학기초_foundations/README.md#english)

- [Differential equations and numerical methods](해설_notes/미분방정식에서수치해로_differential-equations-numerics.md#english)
- [Linear algebra and least squares](해설_notes/선형대수와최소제곱_linear-algebra-least-squares.md#english)
- [Probability and estimation](해설_notes/확률평균추정의불확실성_probability-estimation.md#english)
- [Units, dimensional analysis and uncertainty](해설_notes/단위차원측정불확도_units-dimensional-analysis-uncertainty.md#english)


## 심화 해설 | Advanced article

- [작은 특잇값이 오차를 키울 때: ridge 정규화](해설_notes/정규화와작은특잇값_ridge-spectral-filtering.md) · [English](해설_notes/정규화와작은특잇값_ridge-spectral-filtering.md#english)
