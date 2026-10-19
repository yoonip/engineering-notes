# MATLAB 수치해석: 답의 오차와 잔차는 왜 다를까

[MATLAB & Scientific Computing](../README.md) · [실행 모형](../../../예제_examples/확장기초_extended/systems/extended_models.py) · [검증 코드](../../../예제_examples/확장기초_extended/systems/test_extended_models.py)

## 한국어

### 수치해는 입력의 정확도까지 생각해야 한다

연립방정식 $`Ax=b`$는 회로의 노드 전압, 최소제곱 추정과 시뮬레이션의 한 계산 단계에서 나타난다. 정확한 기호식이 있어도 실제 계산은 유한 정밀도와 측정 오차를 가진 입력으로 이루어진다. MATLAB에서 일반적인 선형계 풀이에는 `A\b`를 사용한다. 역행렬을 먼저 계산해 곱하는 것보다 문제 구조에 맞는 분해를 사용하는 경로가 적절하다. 직사각형·특이 행렬의 해석은 정방 비특이 행렬과 다르다. [MathWorks: Systems of Linear Equations](https://www.mathworks.com/help/matlab/math/systems-of-linear-equations.html)

조건수는 입력 변화에 대한 문제 자체의 민감도이고, 알고리즘의 안정성은 계산 과정이 오차를 어떻게 다루는지에 관한 성질이다. 둘을 섞으면 안정적인 알고리즘을 써도 민감한 문제에서 자릿수가 줄어드는 이유를 설명하기 어렵다. 비특이 정방행렬과 유도된 행렬 노름에 대해 $`\kappa(A)=\Vert A\Vert \Vert A^{-1}\Vert `$이다. MATLAB `cond(A)`의 기본값은 2-노름 조건수이며, 여기서 사용하는 $`\kappa_\infty`$와 숫자가 반드시 같지는 않다. [MathWorks cond](https://www.mathworks.com/help/matlab/ref/cond.html)

### 잔차에서 오차 상계까지

계산한 해를 $`\hat{x}`$, 정확한 해를 $`x`$라 하고 잔차를 $`r=b-A\hat{x}`$로 정한다. 그러면 $`A(x-\hat{x})=r`$이고

$$\Vert x-\hat{x}\Vert \le\Vert A^{-1}\Vert \Vert r\Vert ,\qquad
\frac{\Vert x-\hat{x}\Vert }{\Vert x\Vert }\le\kappa(A)\frac{\Vert r\Vert }{\Vert b\Vert }.$$

두 번째 식은 $`b\ne0`$이고 같은 유도 노름을 쓸 때의 상계다. $`\Vert b\Vert =\Vert Ax\Vert \le\Vert A\Vert \Vert x\Vert `$를 이용한다. 잔차가 작아도 조건수가 크면 해의 상대 오차가 클 수 있다. 상계가 항상 실제 오차와 같다는 뜻도 아니다.

가상 예로 $`A=\mathrm{diag}(1,10^{-8})`$, $`b=(1,10^{-8})^T`$이면 $`x=(1,1)^T`$다. 잘못된 후보 $`\hat{x}=(1,2)^T`$의 잔차 무한노름은 $`10^{-8}`$로 작지만 해의 상대 오차는 1이다. $`\kappa_\infty=10^8`$이므로 작은 잔차만 보고 정확하다고 결론 내릴 수 없다. 이 숫자는 장비 측정 결과가 아니라 계산용 예다.

### 크기에 맞춘 점검과 구현

잔차를 입력 크기와 함께 읽기 위한 지표로

$$\eta=\frac{\Vert b-A\hat{x}\Vert _\infty}{\Vert A\Vert _\infty\Vert \hat{x}\Vert _\infty+\Vert b\Vert _\infty}$$

를 사용할 수 있다. 분모가 0인 영 문제는 따로 처리한다. 이는 잔차에 기반한 normwise backward-error 지표이며, 물리 모델이 맞는지나 모든 성분의 상대 정확도까지 입증하는 수치는 아니다. 작은 성분을 중요하게 보는 문제에는 성분별 오차도 확인한다.

```matlab
% 비특이 정방 선형계에서 잔차와 조건수를 함께 본다.
A = [3 1; 1 2];
b = [7; 5];
x = A\b;
r = b - A*x;
kappa = cond(A, Inf);
eta = norm(r, Inf)/(norm(A, Inf)*norm(x, Inf) + norm(b, Inf));
```

예제 Python `solve2`는 2×2 부분 피벗 소거법이다. 피벗이 0인 경우와 비유한 입력을 거부하며, 큰 행렬용 라이브러리를 대체하지 않는다. `condition_inf2`도 작은 교육용 직접 계산이라 극단적인 크기의 입력에서는 determinant 계산 자체가 부정확해질 수 있다. 행렬·단위의 적절한 scaling, 구조에 맞는 분해, 경고 확인이 필요하다.

테스트는 정수 입력에서 Fraction으로 계산한 독립 기준해와 비교하고, 행 교환·특이 행렬·작은 잔차와 큰 전방 오차의 예를 점검한다. Python 모형 테스트를 실행한 것이며 MATLAB 코드의 실행 성공이나 임의 행렬에서의 안정성 보장을 뜻하지 않는다.

## English

### Accuracy depends on the problem as well as the solver

Linear systems appear in circuit analysis, estimation, and simulation. Computation uses finite precision and potentially uncertain input. MATLAB normally solves a system with `A\b`, using an appropriate factorization rather than forming an inverse merely to multiply by it. Rectangular and singular cases differ from nonsingular square systems. [MathWorks linear systems](https://www.mathworks.com/help/matlab/math/systems-of-linear-equations.html)

Conditioning describes sensitivity of the mathematical problem; stability describes how an algorithm handles computation error. For a nonsingular square matrix and an induced norm, $`\kappa(A)=\Vert A\Vert \Vert A^{-1}\Vert `$. MATLAB's default `cond(A)` uses the 2-norm; its value need not equal the infinity-norm condition number here. [cond](https://www.mathworks.com/help/matlab/ref/cond.html)

### From residual to an error bound

With exact solution $`x`$, candidate $`\hat{x}`$, and residual $`r=b-A\hat{x}`$, we have $`A(x-\hat{x})=r`$. Consequently $`\Vert x-\hat{x}\Vert \le\Vert A^{-1}\Vert \Vert r\Vert `$. For $`b\ne0`$, combining this with $`\Vert b\Vert \le\Vert A\Vert \Vert x\Vert `$ gives relative error at most $`\kappa(A)\Vert r\Vert /\Vert b\Vert `$. Use the same induced norm throughout. This is a bound, not an equality.

In the constructed example $`A=\mathrm{diag}(1,10^{-8})`$ and $`b=(1,10^{-8})^T`$, the true solution is $`(1,1)^T`$. Candidate $`(1,2)^T`$ has residual infinity norm $`10^{-8}`$ but relative forward error one. The condition number is $`10^8`$. These are teaching numbers, not experimental results.

### Scaled verification and implementation

The indicator $`\eta=\Vert b-A\hat{x}\Vert _\infty/(\Vert A\Vert _\infty\Vert \hat{x}\Vert _\infty+\Vert b\Vert _\infty)`$ accounts for scale, treating the all-zero denominator separately. It is a normwise backward-error indicator, not proof of physical-model validity or componentwise relative accuracy. Important small components may need separate checks.

The MATLAB snippet examines the solution, residual, infinity-norm condition number, and scaled indicator together. Python `solve2` implements only 2×2 partial-pivot elimination, rejecting singular pivots and nonfinite inputs. `condition_inf2` uses a direct teaching calculation whose determinant can itself become inaccurate at extreme scales. Neither replaces a production solver; scaling, matrix structure, and warnings matter.

Tests compare against independent Fraction solutions for integer data and cover row exchange, singularity, and the small-residual/large-forward-error example. Only the Python model tests were executed; MATLAB execution and universal numerical stability are not claimed.

## 출처 / Sources

MathWorks의 풀이 규약·조건수 정의를 대조하고 잔차 상계는 명시한 가정에서 직접 유도했다. / Solver semantics and conditioning definitions were cross-checked, and the bound was derived under explicit assumptions. 확인 / checked: 2026-10-19.
