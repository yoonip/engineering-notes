# 선형대수와 최소제곱 | Linear algebra and least squares

[수식을 코드로](../README.md) · [실행 코드와 검사](../../../예제_examples/공학기초_foundations/math_physics/README.md)

## 한국어

### 여러 측정값에서 한 가지 규칙 찾기

온도 센서의 출력이 실제 온도와 완전히 일치하지 않아 $`y\approx a+bx`$로 교정한다고 하자. $`a`$는 오프셋, $`b`$는 기울기다. 측정점이 두 개라면 직선 하나가 두 점을 지날 수 있다. 점이 많아지고 잡음이 섞이면 모든 점을 정확히 지나는 직선은 보통 없다. 최소제곱은 각 점에서 생긴 잔차를 제곱해 더한 값이 가장 작아지는 계수를 찾는다. 제곱하므로 양·음 잔차가 서로 상쇄되지 않는다.

벡터는 여러 수를 순서대로 모은 것이고, 행렬은 이 수들을 선형 결합하는 규칙이다. $`m`$개 관측값과 $`n`$개 계수를

$$A\in\mathbb R^{m\times n},\quad \theta\in\mathbb R^n,\quad y\in\mathbb R^m,\qquad \hat y=A\theta$$

로 쓴다. 직선이면 $`A`$의 $`i`$번째 행은 $`[1,x_i]`$, $`\theta=[a,b]^T`$다. 열들은 예측을 만드는 기본 모양이고, 계수는 각 모양을 얼마나 섞을지 정한다. 열들이 선형 독립이어야 서로 다른 계수를 구분할 수 있다. 이 관점은 [MIT 18.06, §4.3](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/4d876a9159e32543eb0d73b4d4382f4c_MIT18_06S10ZoomNotes.pdf)와 [Stanford EE263 최소제곱 강의](https://ee263.stanford.edu/archive/ls.pdf)에서 교차 확인할 수 있다.

### 목적함수에서 정규방정식까지

목적함수 $`J(\theta)=\Vert A\theta-y\Vert _2^2`$를 전개하면

$$J=\theta^TA^TA\theta-2\theta^TA^Ty+y^Ty.$$

미분해서 0으로 놓으면

$$\nabla J=2A^T(A\theta-y)=0,\qquad A^TA\hat\theta=A^Ty.$$

따라서 잔차 $`r=A\hat\theta-y`$는 $`A`$의 모든 열과 직교한다. 예측 가능한 방향으로 계수를 조금 움직여도 잔차를 더 줄이지 못하는 상태다. 열 독립이면 $`A^TA`$가 양의 정부호여서 해는 유일하다. 다만 이 식은 유도와 최적성 검사에 유용한 것이지 역행렬을 직접 만들라는 구현 지시가 아니다.

### 실제 계산은 QR로

$`A=QR`$, $`Q^TQ=I`$로 분해하면 최소제곱해는 상삼각 연립방정식

$$R\hat\theta=Q^Ty$$

를 풀어 구한다. 역행렬을 만들 필요가 없다. 열 독립인 행렬에 대해 2-노름 조건수는 $`\kappa_2(A^TA)=\kappa_2(A)^2`$다. 정규방정식을 직접 구성하면 원래 있던 민감도가 더 커질 수 있다. QR 유도는 [Stanford EE263, slides 5–9–5–10](https://ee263.stanford.edu/archive/ls.pdf), 분해와 조건수의 의미는 [Kent State QR 수치해석 강의](https://www.math.kent.edu/~reichel/courses/intr.num.comp.1/fall13/lecture6/lecture6.pdf)와 함께 확인했다.

이 예의 Householder QR은 열 아래 부분을 반사해 0으로 만든다. 반사는 길이를 보존한다. 코드에서는 $`Q`$ 전체를 저장하지 않고 같은 반사를 관측값에도 적용해 $`Q^Ty`$를 얻는다. 조밀한 $`m\times n`$ 행렬, $`m\ge n`$에서 연산량은 $`O(mn^2)`$, 저장량은 $`O(mn)`$이다. 작은 교정 문제를 이해하기 위한 구현이며, 대규모·희소·랭크 부족 문제에는 해당 조건을 다루는 라이브러리 해법을 사용한다.

### 직접 계산해 볼 예

$`(x,y)=(0,1),(1,2),(2,2)`$를 쓰면

$$A=\begin{bmatrix}1&0\\1&1\\1&2\end{bmatrix},\quad y=\begin{bmatrix}1\\2\\2\end{bmatrix},\quad
\hat\theta=\begin{bmatrix}7/6\\1/2\end{bmatrix}.$$

예측은 $`[7/6,5/3,13/6]`$, 잔차는 $`[1/6,-1/3,1/6]`$이다. 잔차의 합과 $`x_i`$를 곱한 잔차의 합은 모두 0이다. 잔차 제곱합은 $`1/6`$이다.

```python
from models import least_squares_qr

# 상수항과 입력값을 서로 다른 열에 배치한다.
theta = least_squares_qr([[1, 0], [1, 1], [1, 2]], [1, 2, 2])
print(theta)
```

### 무엇을 확인해야 하는가

검사는 손으로 구한 직선, 정확한 2차식 계수 복원, 무작위 관측값에서 $`A^Tr\approx0`$, 공통 스케일 변경에 대한 불변성, 종속·거의 종속인 열의 거부를 확인한다. `rtol`은 입력 전체 스케일에 상대적인 수치적 랭크 기준이며 물리적 정확도 보증이 아니다. 열의 단위와 크기가 크게 다르면 중심화·스케일링을 하고, 실제 문제에서는 특이값과 조건수도 살핀다.

이 목적함수는 각 관측값을 같은 무게로 취급한다. 잡음 분산이 다르면 가중 최소제곱을 고려하고, 입력 $`x`$ 자체의 오차가 크면 단순 회귀의 가정도 다시 검토한다. 잔차가 작아도 모델이 올바르다는 보장은 없다. 교정에 쓰지 않은 점에서 오차와 잔차 패턴을 확인해야 곡선 관계나 범위 밖 외삽의 문제를 찾을 수 있다.

## English

### Finding a rule from measurements

Suppose a sensor is calibrated with $`y\approx a+bx`$, where $`a`$ is an offset and $`b`$ a slope. Two points can define a line, but noisy observations usually do not all lie on one line. Least squares chooses coefficients that minimize the sum of squared residuals, preventing positive and negative errors from cancelling.

A vector stores ordered values; a matrix describes linear combinations. With $`m`$ observations and $`n`$ coefficients, $`A\in\mathbb R^{m\times n}`$, $`\theta\in\mathbb R^n`$, $`y\in\mathbb R^m`$, and $`\hat y=A\theta`$. For a line, row $`i`$ is $`[1,x_i]`$ and $`\theta=[a,b]^T`$. Columns are building blocks for predictions. They must be independent to distinguish all coefficients. This formulation is covered by [MIT 18.06, §4.3](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/4d876a9159e32543eb0d73b4d4382f4c_MIT18_06S10ZoomNotes.pdf) and [Stanford EE263](https://ee263.stanford.edu/archive/ls.pdf).

### Derivation and numerical model

Expanding $`J(\theta)=\Vert A\theta-y\Vert _2^2`$ gives $`J=\theta^TA^TA\theta-2\theta^TA^Ty+y^Ty`$. Setting its gradient to zero gives $`A^TA\hat\theta=A^Ty`$, so $`r=A\hat\theta-y`$ is orthogonal to every column of $`A`$. Full column rank makes the minimizer unique. These normal equations characterize the optimum; they do not require forming an inverse.

With a thin QR factorization $`A=QR`$, $`Q^TQ=I`$, solve $`R\hat\theta=Q^Ty`$ by back substitution. Forming normal equations can amplify sensitivity because $`\kappa_2(A^TA)=\kappa_2(A)^2`$ for full column rank. See [Stanford EE263, slides 5–9–5–10](https://ee263.stanford.edu/archive/ls.pdf) and the numerical-analysis discussion of conditioning in [Kent State QR notes](https://www.math.kent.edu/~reichel/courses/intr.num.comp.1/fall13/lecture6/lecture6.pdf).

The implementation uses Householder reflections to eliminate entries below the diagonal. It applies each reflection to the observations as well, obtaining $`Q^Ty`$ without storing a full $`Q`$. Dense work costs $`O(mn^2)`$ and storage $`O(mn)`$ for $`m\ge n`$. This small reference implementation explains calibration-sized problems; large, sparse, or rank-deficient cases need solvers designed for those conditions.

### Worked example and implementation

For $`(x,y)=(0,1),(1,2),(2,2)`$, the design matrix has rows $`[1,0]`$, $`[1,1]`$, and $`[1,2]`$. The fitted coefficients are $`a=7/6`$ and $`b=1/2`$. Predictions are $`[7/6,5/3,13/6]`$, residuals $`[1/6,-1/3,1/6]`$, and their squared sum $`1/6`$. Both the residual sum and its dot product with the input column are zero. The Python example calls `least_squares_qr` on precisely these values.

### Verification and interpretation

Tests check the hand-solved line, recovery of exact quadratic coefficients, $`A^Tr\approx0`$ for random observations, invariance under common scaling, and rejection of dependent or nearly dependent columns. `rtol` sets a numerical rank threshold relative to the overall input scale; it does not guarantee physical accuracy. Centre and scale columns when their units or magnitudes differ strongly, and inspect singular values and conditioning for real applications.

Ordinary least squares weights every observation equally. Different noise variances motivate weighted least squares; substantial error in the inputs requires reconsidering the regression assumptions. A small residual is not proof of a correct physical model. Points excluded from calibration and residual patterns help reveal curvature or unsafe extrapolation beyond the fitted range.

## 출처 / Sources

- MIT 18.06 §4.3: 투영·정규방정식 / projection and normal equations.
- Stanford EE263 slides 5–9–5–10: QR 최소제곱 / least squares via QR.
- Kent State QR notes: 조건수와 수치 계산 / conditioning and numerical computation.

측정점, 수치 예와 검사는 별도로 구성했다. / Measurement points, numerical examples, and tests were constructed for this article.
