# 비선형 방정식: 빠른 Newton과 안전한 구간 좁히기

[분야 안내](../README.md) · [실행 예제](../../../예제_examples/심화_advanced/systems/advanced_models.py) · [독립 테스트](../../../예제_examples/심화_advanced/systems/test_advanced_models.py) · [실행 안내](../../../예제_examples/심화_advanced/systems/README.md)

## 한국어

### 잔차가 작다는 말에 조건을 붙입니다

회로의 비선형 동작점이나 센서 보정식에서는 $`f(x)=0`$을 풀어야 합니다. 계산된 $`x`$에서 함수값이 작다고 해서 x의 오차도 무조건 작은 것은 아닙니다. 예를 들어 $`f(x)=10^{-12}(x-1)`$에서는 x가 2여도 잔차는 작습니다. 출력 단위와 함수의 기울기를 함께 봐야 합니다. 단순근 주변에서는 $`f(x)\approx f'(r)(x-r)`$이므로 같은 잔차도 작은 기울기에서 더 큰 위치 오차에 해당합니다.

Newton 방법은 현재 위치에서 접선을 그어 그 접선이 0과 만나는 지점으로 이동합니다. Taylor의 1차 근사에서

```math
0\approx f(x_n)+f'(x_n)(x_{n+1}-x_n),\qquad
x_{n+1}=x_n-\frac{f(x_n)}{f'(x_n)}.
```

근이 단순하고 함수가 충분히 매끄러우며 초기점이 충분히 가까운 조건에서 빠른 국소 수렴을 기대합니다. 기울기가 0에 가깝거나 초기점이 멀면 구간 밖으로 크게 벗어날 수 있습니다. NIST DLMF는 Newton의 전제와 초기점 의존성을 구분합니다. [NIST DLMF §3.8](https://dlmf.nist.gov/3.8)

### 존재를 보장하는 조건과 계산 규칙

닫힌 구간 $`[a,b]`$에서 f가 연속이고 양 끝 함수값의 부호가 다르면 중간값 정리에 따라 적어도 한 근이 있습니다. 불연속인 $`1/x`$는 0 양쪽에서 부호가 달라도 그 안에 근이 없으므로 연속성 전제를 빼면 안 됩니다. 부호 변화가 없다는 것이 근이 없다는 뜻도 아닙니다. $`x^2`$의 0은 부호를 바꾸지 않습니다.

예제는 bracket을 유지하며 Newton 후보가 현재 구간의 가운데 80% 안에 있을 때만 받아들입니다. 그렇지 않으면 중점을 사용합니다. 후보에서 0을 얻으면 종료하고, 아니면 같은 부호인 끝점을 교체합니다. 따라서 보존되는 구간은 매번 이전 너비의 최대 90%가 됩니다. 중점만 쓰는 bisection이라면 매번 절반입니다. Newton의 빠른 수렴 가능성과 구간의 보수적인 축소 조건을 함께 둔 작은 알고리즘입니다.

MATLAB `fzero` 역시 구간과 부호 변화를 활용하지만 bisection, secant, inverse quadratic interpolation을 조합합니다. 여기의 코드가 `fzero`와 동일하다고 보지는 않습니다. 실제 MATLAB에서는 `x=fzero(@(x)x.^2-2,[0,2])`처럼 사용할 수 있고 함수값, exit flag, 반복 정보도 함께 확인합니다. [MathWorks fzero](https://www.mathworks.com/help/matlab/ref/fzero.html)

### 종료 조건이 주는 정보

예제는 현재 구간 너비의 절반이 요청 tolerance 이하면 중점을 반환합니다. 정확한 실수 계산과 유효한 bracket이라는 전제에서는 반환점과 그 구간 안 어떤 근 사이의 거리가 너비의 절반 이합니다. 부동소수점에서는 함수 평가·반올림이 부호 판정을 바꿀 수 있으므로 형식적인 interval arithmetic 증명은 아닙니다. 중점이 끝점과 같아지는 stagnation, NaN·무한대, 반복 상한도 명시적인 실패로 처리합니다.

부호 차이를 `f(a)*f(b)<0`로 검사하면 곱셈 overflow가 생길 수 있어 부호 Boolean을 비교합니다. 반환 객체에는 x, 양 끝점, 잔차와 반복 수가 있습니다. 잔차 하나만 남기지 않고 “어떤 구간으로 판단했는가”를 함께 보여 줍니다. 한 반복의 함수·미분 계산 비용이 상수라면 시간은 반복 수에 비례하고 상태 공간은 상수입니다.

### 독립적인 수치 비교

테스트는 $`x^2-n=0`$의 양의 근을 Python `Decimal` 70자리 제곱근과 비교합니다. 미분이 0을 반환하도록 만든 경우에는 bisection 경로를 확인하며 부호 변화가 없는 함수, 비유한 함수값과 부족한 반복 수를 거부합니다. 이는 선택한 함수에서의 수치 검사입니다. MATLAB 실행이나 임의의 비선형 함수 전체의 수렴 검증은 아닙니다. 서로 다른 해법을 비교할 때에는 tolerance, 함수 평가 수, 정의역과 종료 이유를 같은 기준으로 읽어야 합니다.

저장소 루트에서 실행합니다. 첫 명령은 입력과 계산 결과를 출력하고, 두 번째 명령은 이 디렉터리의 전체 테스트를 실행합니다.

```sh
python "예제_examples/심화_advanced/systems/demo.py" root
python "예제_examples/심화_advanced/systems/test_advanced_models.py" -v
```

## English

### A small residual needs context

Nonlinear operating points and sensor-calibration equations require solving $`f(x)=0`$. A small function value does not universally imply a small error in x: for $`f(x)=10^{-12}(x-1)`$, x=2 still has a small residual. Units and slope matter. Near a simple root, $`f(x)\approx f'(r)(x-r)`$, so the same residual corresponds to a larger position error when the slope is small.

Newton's method finds where a local tangent reaches zero. First-order Taylor expansion gives

```math
0\approx f(x_n)+f'(x_n)(x_{n+1}-x_n),\qquad
x_{n+1}=x_n-\frac{f(x_n)}{f'(x_n)}.
```

Fast local convergence requires a sufficiently smooth function, a simple root, and a sufficiently close starting point. A near-zero derivative or distant initial point can produce a large step. NIST DLMF distinguishes these assumptions and initialization sensitivity. [NIST DLMF §3.8](https://dlmf.nist.gov/3.8)

### Separate root existence from an update rule

A continuous function on $`[a,b]`$ with opposite endpoint signs has at least one root by the intermediate value theorem. The discontinuous function $`1/x`$ changes sign across zero without having a root there. Conversely, a root such as zero of $`x^2`$ need not change sign.

The example maintains a bracket and accepts a Newton proposal only inside its central 80%; otherwise it uses the midpoint. An exact zero terminates; otherwise the endpoint with matching sign is replaced. Retained width is at most 90% of the previous width. Pure bisection halves it. This combines an opportunity for fast steps with explicit conservative contraction.

MATLAB `fzero` also uses sign-changing intervals, but combines bisection, secant, and inverse quadratic interpolation. It is not the same algorithm as this example. In MATLAB, `x=fzero(@(x)x.^2-2,[0,2])` is an applicable call; function value, exit flag, and iteration information should be interpreted together. [MathWorks fzero](https://www.mathworks.com/help/matlab/ref/fzero.html)

### Interpret the stopping condition

The implementation returns the midpoint when half the interval width is within tolerance. Under exact arithmetic and a valid bracket, its distance from any enclosed root is at most that half-width. Floating-point function evaluation can alter signs, so this is not a formal interval-arithmetic certificate. Midpoint stagnation, nonfinite evaluations, and an iteration limit are explicit failures.

Comparing sign Booleans avoids overflowing a product such as `f(a)*f(b)`. The returned object includes x, endpoints, residual, and iteration count, preserving the reason for accepting the answer. With constant-cost function and derivative evaluations, time is proportional to iteration count and working state is constant-sized.

### Use an independent numerical reference

Tests compare positive roots of $`x^2-n=0`$ with 70-digit Decimal square roots. A zero derivative exercises the bisection fallback. Missing sign changes, nonfinite values, and an insufficient iteration budget are rejected. These tests cover selected functions; they neither execute MATLAB nor prove convergence for arbitrary nonlinear functions. Comparisons between solvers need aligned tolerances, evaluation counts, domains, and stopping reasons.

Run the following commands from the repository root. The first prints the input and computed observations; the second runs the complete test suite in this example directory.

```sh
python "예제_examples/심화_advanced/systems/demo.py" root
python "예제_examples/심화_advanced/systems/test_advanced_models.py" -v
```

## 출처 / Sources

- [NIST DLMF §3.8](https://dlmf.nist.gov/3.8): Newton 수렴·근의 conditioning / Newton convergence and root conditioning
- [MathWorks fzero](https://www.mathworks.com/help/matlab/ref/fzero.html): bracket·구현 알고리즘·종료 정보 / brackets, algorithm, termination information
