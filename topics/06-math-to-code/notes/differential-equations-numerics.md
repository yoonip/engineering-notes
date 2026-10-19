# 미분방정식에서 수치해로 | From differential equations to numerical solutions

[수식을 코드로](../README.md) · [실행 코드와 검사](../../../examples/foundations/math_physics/README.md)

## 한국어

### 변화율을 알면 다음 상태를 예측할 수 있다

물이 담긴 통에서 현재 수위가 높을수록 물이 더 빨리 빠져나간다고 생각해 보자. 지금 수위를 아는 것만으로 미래가 결정되지는 않지만, 수위가 얼마나 빨리 변하는지까지 알면 작은 시간 뒤를 예측할 수 있다. 미분방정식은 이런 변화율의 규칙이다. 이 글의 $y'=-y/\tau$는 감소 속도가 현재 값에 비례하는 가장 단순한 감쇠 모델이다. 실제 배수 현상을 모두 이 식으로 설명한다는 뜻은 아니며, RC 회로에서 평형 전압과의 차이나 일부 선형 완화 현상에 같은 수학 구조가 나타난다.

일반 초기값 문제는 $dy/dt=f(t,y)$, $y(0)=y_0$다. $f$의 단위는 $y$의 단위/시간이다. 방정식뿐 아니라 초기값이 있어야 특정 해를 정할 수 있다. 매끄러움과 해의 존재·유일성 같은 조건을 확인한 뒤 수치해법을 선택한다. 전진 Euler의 정의와 오차 구분은 [MIT 18.330, Chapter 5](https://math.mit.edu/icg/resources/notes330.pdf), 안정성 조건은 [Illinois Tech 수치해석 Chapter 4](https://www.math.iit.edu/~fass/478578_Chapter_4.pdf)와 교차 확인했다.

### Euler 공식을 유도하기

시간 간격 $h>0$에서 Taylor 전개하면

$$y(t+h)=y(t)+hy'(t)+\frac{h^2}{2}y''(\xi),\qquad t<\xi<t+h.$$

$y'=f(t,y)$를 넣고 나머지를 버리면

$$y_{n+1}=y_n+h f(t_n,y_n),\qquad t_n=nh.$$

한 걸음의 값 오차는 충분히 매끄러운 해에서 $O(h^2)$다. 고정된 최종 시간까지 약 $1/h$번 반복하면 적절한 안정성·매끄러움 조건에서 전역 오차는 $O(h)$가 된다. `국소 절단오차`를 $h$로 나눈 잔차로 정의하는 문헌도 있어 그때 표기는 $O(h)$가 된다. 여기서는 한 걸음의 값 오차를 기준으로 쓴다.

### 안정한 모델도 계산은 발산할 수 있다

감쇠 모델의 정확한 해는 변수 분리로 구한다.

$$\frac{dy}{y}=-\frac{dt}{\tau}
\quad\Rightarrow\quad y(t)=y_0e^{-t/\tau},\qquad\tau>0.$$

Euler는 $y_{n+1}=(1-h/\tau)y_n$이다. 오차와 초기값 교란도 같은 계수로 증폭된다. 감쇠하려면 $|1-h/\tau|<1$, 즉 $0<h<2\tau$여야 한다.

| $h/\tau$ | 반복값의 성질 |
|---|---|
| $0<h/\tau<1$ | 부호를 유지하며 감소 |
| $h/\tau=1$ | 한 걸음에 0; 안정하지만 정확해와 다름 |
| $1<h/\tau<2$ | 부호가 번갈아 바뀌며 감소 |
| $h/\tau=2$ | 크기가 줄지 않는 경계 |
| $h/\tau>2$ | 크기가 증가 |

따라서 안정 조건만 통과했다고 정확한 것은 아니다. 실제 $y(t)$가 양수인 농도·에너지 같은 변수라면 번갈아 음수가 되는 수치해도 적절하지 않다. 선형 복소 시험식 $y'=\lambda y$에서는 조건이 $|1+h\lambda|<1$이며, 모든 문제의 안정성을 $h<2\tau$ 하나로 판단할 수 없다.

### 구현, 비용, 비교 기준

```python
from math import exp
from models import decay_euler

exact = exp(-1.0)
for steps in (20, 40, 80):
    # 최종 시간을 고정하고 간격만 줄여 수렴을 확인한다.
    value = decay_euler(initial=1.0, tau=1.0, duration=1.0, steps=steps)
    print(steps, value, abs(value-exact))
```

모델은 최종 시간 $T$를 정확히 $N$개 구간으로 나누어 $h=T/N$을 쓴다. 반복 덧셈으로 시간을 누적해 종료 조건을 비교하지 않는다. 상태 하나만 저장하므로 시간 $O(N)$, 추가 메모리 $O(1)$이다. 전체 궤적이 필요할 때만 별도 저장한다. 이 선형 문제에서 최종값만 필요하면 해석식이 더 효율적이다. 반복 구현의 목적은 다른 방정식에도 이어지는 수치해법의 동작을 확인하는 데 있다.

검사는 $T=\tau=y_0=1$에서 해석해 $e^{-1}$과 비교하고, $N=20,40,80$으로 늘릴 때 오차 비가 약 2인지 확인한다. 초기값 0, 최종 시간 0, 불안정 간격의 거부도 검사한다. 매끈한 그래프 한 장보다 오차 표와 간격 축소 검사가 더 구체적인 근거가 된다.

오차 허용치를 정할 때는 변수 단위에 맞는 절대 허용오차와 크기에 상대적인 허용오차를 함께 생각한다. 간격을 끝없이 줄이면 연산량과 반올림 영향이 커진다. 여러 시간척도가 섞인 stiff 문제에서는 명시적 간격이 안정성에 묶여 비효율적일 수 있어 적응형·암시적 해법을 검토한다. 수치해가 방정식을 잘 푼다는 검증과 그 방정식이 실제 장치를 잘 설명한다는 검증은 별개다.

## English

### Rates of change predict states

A water level and a rule for its rate of change can predict the level a short time later. An ordinary differential equation states such a rule. The simple decay model $y'=-y/\tau$ assumes that the decrease rate is proportional to the current value. It is not a universal model of draining water; the same mathematical form describes deviations from equilibrium in an ideal RC circuit and some linear relaxation processes.

An initial-value problem consists of $dy/dt=f(t,y)$ and $y(0)=y_0$. The units of $f$ are those of $y$ divided by time. The initial state selects a particular trajectory. Existence, uniqueness, and regularity assumptions matter before choosing an integrator. Forward Euler and its error definitions are treated in [MIT 18.330, Chapter 5](https://math.mit.edu/icg/resources/notes330.pdf); stability is cross-checked against [Illinois Tech numerical-analysis Chapter 4](https://www.math.iit.edu/~fass/478578_Chapter_4.pdf).

### Derivation and error

Taylor expansion gives $y(t+h)=y(t)+hy'(t)+h^2y''(\xi)/2$. Substituting the differential equation and dropping the remainder gives $y_{n+1}=y_n+h f(t_n,y_n)$, $t_n=nh$. For a sufficiently smooth solution, one-step value error is $O(h^2)$. Over a fixed time interval, with suitable regularity and stability, the global error is $O(h)$. Some texts define local truncation error after division by $h$, making that quantity $O(h)$ instead. This article uses the one-step value-error convention.

### Stability is not accuracy

Separating variables in the decay equation gives $dy/y=-dt/\tau$ and $y(t)=y_0e^{-t/\tau}$ for $\tau>0$. Euler gives $y_{n+1}=(1-h/\tau)y_n$. Perturbations have the same amplification factor. Decay therefore requires $|1-h/\tau|<1$, or $0<h<2\tau$.

For $0<h/\tau<1$, values decrease without changing sign. At 1, the scheme reaches zero in one step, although the exact solution does not. Between 1 and 2, signs alternate while magnitude decreases. At 2, magnitude no longer decays; above 2 it grows. Thus a stable step need not be accurate or preserve physical positivity. For the complex test equation $y'=\lambda y$, the condition is $|1+h\lambda|<1$. The scalar decay bound cannot replace stability analysis of every other equation.

### Implementation and verification

The example compares `decay_euler` against $e^{-1}$ with 20, 40, and 80 steps. It fixes the final time and changes only the step. The implementation sets $h=T/N$ rather than ending a loop by comparing an accumulated floating-point time. It takes $O(N)$ time and $O(1)$ extra memory, storing only the final state. A full trajectory is stored only when needed. For this particular linear problem, the analytical expression is more efficient if only a final value is required; iteration demonstrates an approach that extends to more general equations.

Tests verify approximately twofold error reduction when the step is halved, zero initial state, zero duration, and rejection of nondecaying unstable steps. An error table and refinement study provide clearer evidence than a smooth plot alone.

Use absolute tolerances in the variable's units alongside relative tolerances. Indefinitely shrinking the step increases work and eventually exposes roundoff. Widely separated timescales can make explicit integration inefficient because stability dictates the step; adaptive or implicit solvers may then be appropriate. Verifying that code solves the selected equation is separate from validating that equation against a physical device.

## 출처 / Sources

- MIT 18.330 Chapter 5: Euler 유도, 국소·전역 오차 / Euler construction and local/global error.
- Illinois Tech Chapter 4: 선형 안정 영역, 감쇠 시험식, stiffness / linear stability, decay test equation, and stiffness.

해석해 비교와 간격 축소 검사는 위 모델에 대해 수행한다. / Analytical comparisons and step refinement apply to the model stated here.
