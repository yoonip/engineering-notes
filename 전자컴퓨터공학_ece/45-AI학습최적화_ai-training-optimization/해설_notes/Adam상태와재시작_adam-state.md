# Adam의 상태, bias correction과 학습 재개

[Optimizer 구현](../../../예제_examples/심화_advanced/ai_data/advanced_ai_models.py) · [CLI](../../../예제_examples/심화_advanced/ai_data/demo.py) · [독립 검증](../../../예제_examples/심화_advanced/ai_data/test_advanced_ai.py)

## 현재 기울기만으로는 다음 step이 정해지지 않습니다

SGD의 기본 형태는 현재 gradient에 학습률을 곱해 이동합니다. Adam은 gradient의 최근 방향과 제곱 크기를 누적하므로 현재 매개변수가 같고 현재 gradient가 같아도 과거 상태가 다르면 다음 값이 달라질 수 있습니다. “가중치만 저장했다”와 “같은 학습을 재개한다”가 다른 이유입니다.

이 글은 momentum 계수 $`0\le\beta_1,\beta_2\lt1`$, 양의 학습률과 epsilon을 사용하는 기본 Adam입니다. AMSGrad, weight decay, AdamW의 분리 감쇠, 혼합 정밀도의 loss scaling은 넣지 않습니다. 같은 이름의 optimizer라도 이런 설정과 epsilon 위치가 다르면 수치가 달라집니다. [Adam 원 논문 Algorithm 1](https://arxiv.org/pdf/1412.6980), [PyTorch Adam](https://docs.pytorch.org/docs/2.9/generated/torch.optim.Adam.html)

## 모멘트를 쌓고 0 초기화의 영향을 보정합니다

Gradient $`g_t`$에 대해 상태를 0에서 시작합니다.

```math
m_t=\beta_1m_{t-1}+(1-\beta_1)g_t,\qquad
v_t=\beta_2v_{t-1}+(1-\beta_2)g_t^2.
```

제곱과 나눗셈은 성분별 연산입니다. v는 gradient의 두 번째 raw moment 추정이며, 평균을 뺀 분산과 같은 정의가 아닙니다. 평균 gradient가 일정한 $`\mu`$라고 가정해 첫 식의 기댓값을 전개하면 유한 기하급수로

```math
E[m_t]=(1-\beta_1)\mu\sum_{k=0}^{t-1}\beta_1^k
=(1-\beta_1^t)\mu
```

가 됩니다. 초기 0 때문에 작아진 배율을 나누는 것이 bias correction입니다. 제곱 gradient에도 같은 초기화 보정을 적용합니다.

```math
\hat m_t=\frac{m_t}{1-\beta_1^t},\qquad
\hat v_t=\frac{v_t}{1-\beta_2^t},\qquad
\theta_t=\theta_{t-1}-\eta\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}.
```

실제 학습의 gradient는 위치에 따라 달라지므로 위 정상 평균 유도가 매 step의 진짜 gradient를 정확히 복원한다는 뜻은 아닙니다. 보정은 0 초기화 배율을 다루며, 신경망의 전역 최적점 수렴을 보장하지 않습니다.

## 첫 두 step을 손으로 계산합니다

한 성분, $`m_0=v_0=0`$, $`g_1=2`$, $`\beta_1=\beta_2=0.5`$면 $`m_1=1,v_1=2`$입니다. 보정 후는 $`\hat m_1=2,\hat v_1=4`$이므로 step 크기는 $`\eta\,2/(2+\epsilon)`$입니다.

다음 gradient가 -1이면 $`m_2=0,v_2=1.5`$입니다. 두 번째 step은 m이 0이어서 매개변수가 움직이지 않습니다. 현재 gradient가 -1인데도 움직이지 않는 이 예는 최근 방향 평균이 작동함을 보여 줍니다. 테스트는 epsilon=0.1을 써 분모에서 epsilon의 위치도 드러냅니다. 너무 작은 epsilon으로만 검사하면 잘못된 위치가 거의 같은 숫자를 낼 수 있습니다.

## Gradient clipping의 위치

큰 gradient의 전역 2-노름을 제한하려면 $`r=\Vert g\Vert_2`$를 구하고, 상한 c에 대해 $`g'=g\min(1,c/r)`$로 둡니다. r=0이면 그대로 둡니다. 벡터 방향은 유지하며 큰 gradient의 크기만 줄입니다. 각 성분을 따로 잘라내는 elementwise clipping과는 다릅니다.

이 예제는 clipping한 gradient를 Adam에 전달해 m,v가 그 값을 누적합니다. Adam 상태를 만든 뒤 파라미터 step만 clipping하는 방법과 다른 알고리즘입니다. `math.hypot`으로 노름을 계산해 단순 제곱합에서 불필요한 overflow를 줄이지만 모든 극단적 입력에서 Adam의 모든 중간 연산이 안전하다는 보장은 하지 않습니다. 실학습에서는 비유한 loss·gradient와 데이터 스케일도 함께 점검합니다.

## 실행과 상태 복원 검증

```bash
python "예제_examples/심화_advanced/ai_data/demo.py" adam
python -m unittest discover -s "예제_examples/심화_advanced/ai_data" -p "test_*.py" -v
```

CLI는 $`L(\theta)=\Vert\theta\Vert_2^2/2`$의 gradient $`g=\theta`$를 사용합니다. 시작 (1,-2), 학습률 0.05, clipping 상한 1에서 200회 실제 갱신한 뒤 loss가 2.5에서 약 $`3.19\times10^{-9}`$로 줄었습니다. 정한 이차함수의 실행 결과이며 모든 비선형 학습 문제에서 같은 수렴을 기대하는 근거는 아닙니다.

JSON에는 매개변수, m,v, step_count와 설정이 포함됩니다. 테스트는 두 step 뒤 상태를 JSON으로 저장·복원한 객체의 다음 결과가 중단 없이 진행한 객체와 같은지 검사합니다. 같은 가중치로 새 optimizer를 만들어 m,v,t를 초기화한 경우에는 결과가 다름을 확인합니다. 첫 두 step의 해석적 값, clipping의 노름과 방향, 0 gradient도 별도 기준입니다.

실제 checkpoint는 optimizer 외에도 model, scheduler, 데이터 순서, 난수 생성기, mixed-precision scaler 상태를 포함할 수 있습니다. 라이브러리·장치·kernel 차이는 bit 재현성에 추가 조건을 만듭니다. 이 예제의 정확한 상태 재개는 Python 숫자 모델의 동일 연산 경로에 관한 결과입니다.

## English

### History is part of the optimizer

Basic SGD uses the current gradient. Adam also stores moving direction and squared magnitude, so equal parameters and a current gradient do not determine the next step without the past state. Saving weights alone is not the same as resuming the same training process.

The implementation is basic Adam with betas in [0,1), positive learning rate and epsilon. It excludes AMSGrad, weight decay, decoupled AdamW and mixed-precision scaling. Epsilon placement and options matter. [Original Algorithm 1](https://arxiv.org/pdf/1412.6980) and [PyTorch Adam](https://docs.pytorch.org/docs/2.9/generated/torch.optim.Adam.html) define the reference convention.

### Derive correction for zero initialization

The equations above update m from gradients and v from elementwise squared gradients. The latter estimates a raw second moment, not centered variance. Under a constant expected gradient μ, expanding the recurrence yields $`E[m_t]=(1-\beta_1^t)\mu`$. Dividing by that geometric-series factor removes the zero-initialization shrinkage. The same correction applies to the squared-gradient state.

Updates use $`\hat m_t=m_t/(1-\beta_1^t)`$, $`\hat v_t=v_t/(1-\beta_2^t)`$ and denominator $`\sqrt{\hat v_t}+\epsilon`$. Nonstationary training gradients do not make this a reconstruction of the exact current gradient, and correction is not a global convergence guarantee.

For beta1=beta2=0.5 and first gradient two, the raw states are one and two, corrected states two and four. The first step has magnitude $`\eta\,2/(2+\epsilon)`$. A next gradient of minus one makes m zero and v 1.5, so the second parameter step is zero. Tests use epsilon 0.1 to expose its denominator placement.

### Clip before accumulating state

Global clipping rescales g by $`\min(1,c/\Vert g\Vert_2)`$, leaving a zero vector unchanged. It preserves direction, unlike clipping components independently. The example feeds this clipped vector into Adam, so moments accumulate clipped values. Clipping only a final parameter step would define a different algorithm.

Using `math.hypot` reduces avoidable overflow in the norm, without guaranteeing every Adam intermediate for arbitrarily extreme inputs. Real training also needs finite-value and scale checks.

### Executed updates and resumption

The commands optimize $`\Vert\theta\Vert_2^2/2`$, whose gradient is θ, from (1,-2). With rate 0.05, norm cap one and 200 updates, loss changed from 2.5 to about $`3.19\times10^{-9}`$. This is an executed quadratic example, not a result for every neural-network objective.

JSON includes parameters, moments, counter and settings. Tests serialize/restore after two updates and compare the next result with uninterrupted execution. Restarting a fresh optimizer at the same weights produces a different result. Analytic first/second steps, clipping direction/norm and zero vectors provide separate checks.

A production checkpoint can also require model, scheduler, data-order, random-generator and mixed-precision-scaler states. Runtime, device and kernel differences add conditions for bitwise replay. The demonstrated exact resumption concerns the same Python arithmetic path.

## 출처 / Sources

- [Kingma & Ba, Adam](https://arxiv.org/pdf/1412.6980): exponential moments and initialization-bias correction.
- [PyTorch 2.9 Adam](https://docs.pytorch.org/docs/2.9/generated/torch.optim.Adam.html): update convention, epsilon and optimizer state. 확인 / checked: 2026-10-19.
