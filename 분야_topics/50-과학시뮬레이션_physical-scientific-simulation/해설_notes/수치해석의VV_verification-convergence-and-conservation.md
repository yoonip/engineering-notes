# 수치해석의 V&V: 수렴, 잔차, 보존을 따로 확인하기

## 그럴듯한 그림만으로는 정확성을 알 수 없습니다

시뮬레이션은 물리 현상을 모델로 만들고, 모델의 방정식을 이산화해 코드로 계산한 결과입니다. 그림이 부드럽거나 solver가 종료됐다고 이 모든 단계가 옳은 것은 아닙니다. Verification은 선택한 수학 모델을 제대로 계산했는지, validation은 그 모델과 계산이 관측한 물리 현실을 충분히 설명하는지 묻습니다. NASA도 해석해 비교와 실험 비교를 구분합니다. [NASA V&V overview](https://www.grc.nasa.gov/www/wind/valid/tutorial/overview.html)

이 글은 무차원 1차원 예제로 verification을 다룹니다. 실제 재료의 열전도율이나 실험 장치에 대한 validation 결과를 주장하지 않습니다. 반복 오차, 공간 이산화 오차, 시간 이산화 오차, 모델·입력의 불확실성은 서로 다른 원인입니다.

## 답을 정하고 방정식을 만드는 manufactured solution

구간 $`0\le x\le1`$에서 $`u(0)=u(1)=0`$인 Poisson 문제를 보겠습니다.

$$-u''(x)=f(x).$$

정답을 $`u_*(x)=\sin(\pi x)`$로 정하면 두 번 미분해 $`f(x)=\pi^2\sin(\pi x)`$를 얻습니다. 정답을 알고 있으므로 구현의 오차를 직접 계산할 수 있습니다. 이는 실제 측정에 맞춘 보정과 다릅니다. 코드는 정한 방정식을 제대로 푸는지 검사합니다.

균일 격자 $`x_i=ih`$, $`h=1/N`$에서 Taylor 전개를 양쪽으로 더하면

$$u(x+h)-2u(x)+u(x-h)=h^2u''(x)+\frac{h^4}{12}u^{(4)}(x)+O(h^6).$$

따라서 (-u'')의 중심 차분은 $`O(h^2)`$의 절단 오차를 가집니다. 이 문제의 이산식은

$$-u_{i-1}+2u_i-u_{i+1}=h^2f_i,\qquad i=1,\ldots,N-1.$$

계수 행렬은 삼중 대각이고, 이 예제의 Dirichlet 문제에서는 양의 정부호입니다. Thomas 소거법으로 메모리와 연산량 (O(N))에 풀 수 있습니다. 일반적인 모든 삼중 대각 행렬에서 pivot 없는 소거가 안전하다는 뜻은 아닙니다.

## 잔차가 작다는 것과 격자가 충분하다는 것은 다릅니다

격자 해의 잔차는 $`r_i=(-u_{i-1}+2u_i-u_{i+1})/h^2-f_i`$입니다. 잔차는 이산 방정식을 얼마나 잘 풀었는지 보여 주지만 연속 방정식과의 오차를 직접 없애지 않습니다. 아주 거친 격자에서도 이산식을 정확히 풀면 잔차가 작을 수 있습니다. NASA verification 자료도 반복 수렴, 보존, 격자 수렴, 시간 수렴을 별도 항목으로 둡니다. [NASA verification assessment](https://www.grc.nasa.gov/www/wind/valid/tutorial/verassess.html)

정답과의 최대 오차를 $`e_h=\max_i\vert u_i-u_*(x_i)\vert `$라 하겠습니다. 점근 구간에서 $`e_h\approx Ch^p`$이면 격자를 절반으로 줄였을 때 $`e_h/e_{h/2}\approx2^p`$, 관측 차수는 $`p_{obs}=\log_2(e_h/e_{h/2})`$입니다. 이 예제의 기대 차수는 2라서 비율은 약 4입니다. 매우 미세한 격자에서는 반올림이나 solver 오차가 지배해 이 비율이 유지되지 않을 수 있습니다.

별도의 해석적 검사도 가능합니다. 격자에서 $`\sin(\pi ih)`$는 이산 연산자의 고유모드이고 고유값은 $`\lambda_h=4\sin^2(\pi h/2)/h^2`$입니다. 따라서 정확한 “이산 해”는 $`u_i^h=(\pi^2/\lambda_h)\sin(\pi ih)`$입니다. 이것과 비교하면 solver 구현 오류와 연속 문제의 이산화 오차를 분리할 수 있습니다.

## 보존식은 독립적인 균형 검사입니다

면 flux를 $`J_{i+1/2}=-(u_{i+1}-u_i)/h`$로 정의하면 이산식은 $`(J_{i+1/2}-J_{i-1/2})/h=f_i`$입니다. 내부 점 전체를 더하면 중간 flux가 서로 지워져

$$J_{N-1/2}-J_{1/2}=h\sum_{i=1}^{N-1}f_i.$$

이 식은 내부 격자 영역의 이산 균형입니다. 경계 바로 바깥까지의 연속 적분을 정확히 계산했다는 뜻은 아닙니다. 국소 항의 부호나 경계 처리를 잘못했을 때 전역 균형이 오류를 드러낼 수 있습니다. 반대로 전역 합만 맞고 국소 값이 틀릴 수도 있으므로 보존만 검사하지 않습니다.

시간 수렴은 별도로 확인합니다. $`y'=-y,y(0)=1`$을 Euler로 풀면 $`y_{n+1}=(1-\Delta t)y_n`$이고 정확해는 $`e^{-t}`$입니다. $`0<\Delta t<2`$는 이 문제의 절대 안정 구간이지만, 작은 오차를 보장하는 조건과 같지 않습니다. 같은 종료 시각에서 $`\Delta t`$를 절반씩 줄여 1차 방법의 오차 비율 약 2를 확인합니다.

## 구현과 검증

[`poisson_sine`, `decay_euler`](../../../예제_examples/확장기초_extended/ai_data/models.py)와 [테스트](../../../예제_examples/확장기초_extended/ai_data/test_models.py)는 이산 고유모드 비교, 16·32·64 구간의 공간 수렴, 면 flux 균형, 시간 step 40·80·160의 수렴을 각각 확인합니다. 이 결과는 명시한 방정식의 계산 검증입니다. 물리 validation에는 독립 실험, 측정 불확실성, 적용 범위와 모델 가정의 비교가 더 필요합니다. [NASA validation assessment](https://www.grc.nasa.gov/www/wind/valid/tutorial/valassess.html)

## English

### A smooth plot is not sufficient

Simulation passes from physical assumptions to equations, discretization and code. Solver termination or a smooth plot cannot validate every stage. Verification asks whether the chosen mathematical model is calculated correctly; validation asks whether it adequately represents observed reality. NASA distinguishes comparisons with analytical solutions from comparisons with experiments. [V&V overview](https://www.grc.nasa.gov/www/wind/valid/tutorial/overview.html)

This dimensionless one-dimensional example performs verification, not validation of a physical material or apparatus. Iteration error, spatial and temporal discretization error, and model/input uncertainty have different origins.

### Constructing a known answer

For $`-u''=f`$ on ([0,1]) with zero Dirichlet boundaries, choosing $`u_* = \sin(\pi x)`$ gives $`f=\pi^2\sin(\pi x)`$. This manufactured solution makes the answer known before running the solver. It tests equation implementation rather than calibration against measurements.

Adding Taylor expansions at $`x\pm h`$ gives the central-difference formula above and a second-order truncation error. The resulting tridiagonal equations have diagonal two and neighboring coefficients minus one after multiplication by $`h^2`$. This Dirichlet matrix is positive definite. Thomas elimination solves it with (O(N)) work and memory; that does not make pivot-free elimination safe for every tridiagonal matrix.

### Distinct checks for distinct errors

Residuals measure satisfaction of the discrete equations, not distance from the continuous solution. A coarse-grid solution can have a tiny residual. NASA lists iterative convergence, consistency/conservation, grid convergence and temporal convergence separately. [Verification assessment](https://www.grc.nasa.gov/www/wind/valid/tutorial/verassess.html)

If $`e_h\approx Ch^p`$, halving the spacing gives $`e_h/e_{h/2}\approx2^p`$. The expected ratio here is four. Roundoff or solver error may dominate at extremely small spacing. An independent exact discrete solution follows from the sine eigenmode: $`\lambda_h=4\sin^2(\pi h/2)/h^2`$, so $`u_i^h=(\pi^2/\lambda_h)\sin(\pi ih)`$. This separates solver error from discretization error.

Defining face flux $`J_{i+1/2}=-(u_{i+1}-u_i)/h`$ turns the discrete equation into flux divergence. Summing cancels interior faces and yields the balance above. This is a discrete interior-domain identity, not an exact continuous integral to the outer boundary. Global balance can catch signs and boundary errors, but correct global totals can coexist with incorrect local values.

Time refinement is separate. Euler applied to $`y'=-y,y(0)=1`$ gives $`y_{n+1}=(1-\Delta t)y_n`$, compared with $`e^{-t}`$. Its absolute-stability interval $`0<\Delta t<2`$ does not guarantee small error. At fixed final time, halving steps should asymptotically halve the first-order global error.

### Implementation and checks

The linked models and tests compare against the discrete eigenmode, check spatial refinement on 16, 32 and 64 intervals, verify flux balance and check temporal refinement with 40, 80 and 160 steps. These establish calculations for the specified equations. Physical validation additionally requires independent experiments, measurement uncertainty, applicability and examination of model assumptions. [Validation assessment](https://www.grc.nasa.gov/www/wind/valid/tutorial/valassess.html)

## Sources

- [NASA Glenn, Overview of CFD V&V](https://www.grc.nasa.gov/www/wind/valid/tutorial/overview.html): verification/validation distinction.
- [NASA Glenn, Verification Assessment](https://www.grc.nasa.gov/www/wind/valid/tutorial/verassess.html): analytic comparisons, convergence and conservation as separate checks.
- [NASA Glenn, Validation Assessment](https://www.grc.nasa.gov/www/wind/valid/tutorial/valassess.html): comparison with physical observations and applicability. Reference date: 2026-10-19.
