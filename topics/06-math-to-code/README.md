# 수식을 코드로

[전체 목차](../../CATALOG.md) · [처음으로](../../README.md)

수식을 구현할 때는 변수의 뜻, 단위, 정의역부터 정해진다. 같은 식이라도 연속 시간 모델인지 표본화된 모델인지, 실수 계산인지 고정소수점 계산인지에 따라 구현이 달라진다.

## 미분방정식에서 반복문으로

RC 충전 회로는 `dv/dt = (Vin - v)/(RC)`로 표현된다. 전진 Euler 방법은 현재 기울기로 다음 값을 계산한다. `v[n+1] = v[n] + dt*(Vin-v[n])/(RC)`이며 오차는 시간 간격 `dt`와 관련된다.

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

## 수치적으로 같은 식인가

부동소수점은 유한한 비트로 수를 표현한다. 크기가 비슷한 두 수를 빼면 유효숫자가 손실될 수 있고, 반복 누적에서는 반올림 오차가 쌓인다. 선형 연립방정식 `Ax=b`는 역행렬을 직접 계산하기보다 분해 기반 해법으로 푸는 경우가 일반적이다.

선형대수는 좌표 변환·최소제곱·신경망 연산에, 미적분은 변화율과 최적화에, 확률·통계는 잡음과 추정에 쓰인다. 그래프 이론은 연결 관계와 경로를 다룬다. 정보이론의 엔트로피는 확률 분포의 불확실성을 수치화한다. 이산화·정밀도·경계조건이 수학 모델을 실제 계산으로 옮기는 연결점이다.

## 관련 기술

Calculus, Linear Algebra, Probability, Statistics, ODE/PDE, Numerical Analysis, Optimization, Information Theory, Graph Theory

## 참고 자료

- [NumPy documentation](https://numpy.org/doc/)
- [SciPy documentation](https://docs.scipy.org/doc/scipy/)
