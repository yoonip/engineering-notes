# 학습의 계산과 평가: loss, batch, 학습률, data leakage

## 학습은 점수를 낮추는 과정이며, 평가는 다른 데이터에 대한 질문입니다

학습은 파라미터 $`\theta`$를 바꾸어 훈련 목적함수 $`L(\theta)`$를 줄이는 과정입니다. 목적함수는 모델이 무엇을 맞추도록 할지 수치로 정합니다. 회귀의 제곱 오차, 분류의 cross-entropy처럼 과제와 출력에 맞는 정의가 필요합니다. 훈련 loss가 줄었다는 사실과 새로운 데이터에서 유용하다는 사실은 서로 다른 주장입니다.

먼저 절편이 없는 작은 회귀 모델 $`\hat y=wx`$를 보겠습니다. $`n`$개 표본의 평균 제곱 오차에 편의상 $`1/2`$를 넣으면

```math
L(w)=\frac1{2n}\sum_{i=1}^n(wx_i-y_i)^2,
\qquad\frac{dL}{dw}=\frac1n\sum_i(wx_i-y_i)x_i.
```

도함수는 안쪽 $`wx_i-y_i`$의 미분 $`x_i`$를 곱하는 chain rule에서 나옵니다. $`x_i`$ 중 적어도 하나가 0이 아니어서 $`\sum x_i^2>0`$이면 stationary point는 $`w^*=\sum_i x_iy_i/\sum_i x_i^2`$입니다. 여기서 필요한 조건은 “모든 $`x_i`$가 0인 경우가 아님”이며 일부 표본의 $`x_i=0`$은 허용합니다.

## Gradient와 optimizer

기본 SGD 갱신은 $`w_{t+1}=w_t-\eta_tg_t`$입니다. Gradient는 어느 방향으로 loss가 증가하는지 나타내므로 부호를 반대로 움직입니다. `optimizer`는 gradient로 실제 파라미터를 바꾸는 규칙입니다. Momentum이나 Adam은 상태와 갱신 규칙을 추가하며, 이름만 바꾼 같은 계산이 아닙니다. 이 예제는 momentum 없는 SGD만 계산합니다. [PyTorch SGD 정의](https://docs.pytorch.org/docs/2.14/generated/torch.optim.SGD.html)

위 회귀의 곡률은 $`a=\frac1n\sum x_i^2>0`$입니다. 정확한 full-batch gradient와 고정 학습률이면

```math
w_{t+1}-w^*=(1-\eta a)(w_t-w^*).
```

따라서 이 1차원 이차함수에서 수렴 조건은 $`0<\eta a<2`$입니다. 너무 큰 보폭은 최적점을 넘나들며 발산할 수 있습니다. 이 식을 모든 비선형 신경망의 전역 수렴 보장으로 확장할 수는 없습니다.

## Batch 크기와 가중치

Mini-batch는 전체 데이터의 일부로 gradient를 추정합니다. 같은 파라미터에서 두 batch의 평균 gradient가 $`g_1,g_2`$, 표본 수가 $`n_1,n_2`$라면 전체 gradient는

```math
g=\frac{n_1g_1+n_2g_2}{n_1+n_2}.
```

마지막 batch가 작을 때 batch 평균을 단순 평균하면 표본 가중치가 달라집니다. 또한 batch마다 파라미터를 갱신한 여러 SGD step은 같은 파라미터에서 합친 full-batch step과 같지 않습니다. Gradient accumulation으로 큰 batch를 모사할 때도 loss reduction과 표본 수를 맞춰야 합니다. Batch 크기는 메모리, gradient의 변동, step당 비용을 바꾸므로 “크면 항상 좋다”는 한 줄로 정할 수 없습니다.

## 학습률 스케줄과 데이터 분리

한 번 감소하는 cosine schedule을 $`0\le t\le T`$에서

```math
\eta_t=\eta_{min}+\frac{\eta_{max}-\eta_{min}}2[1+\cos(\pi t/T)]
```

로 정의하면 시작은 $`\eta_{max}`$, 마지막은 $`\eta_{min}`$입니다. $`t`$가 optimizer update 수인지 epoch 수인지 정해야 같은 schedule을 재현합니다. 이 예제는 종료 구간 안의 값만 정의하며 restart를 구현하지 않습니다. [PyTorch cosine schedule](https://docs.pytorch.org/docs/2.14/generated/torch.optim.lr_scheduler.CosineAnnealingLR.html)

Train은 파라미터 학습, validation은 설정 선택, test는 선택을 마친 뒤의 평가에 씁니다. 동일한 사람·장비·연속 frame·미래 정보가 양쪽에 섞이면 독립적인 성능 추정이 어려워집니다. 평균·표준편차 같은 전처리 통계도 train에서 추정하고 나머지 데이터에 적용해야 합니다. Test를 반복해서 보고 설정을 고르면 test 역시 선택 과정에 들어갑니다. Google의 교육 자료도 중복과 반복적인 평가 재사용을 경고합니다. [Google dataset separation](https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets)

## 구현과 검증

[`linear_loss_gradient`, `cosine_learning_rate`](../../../예제_examples/확장기초_extended/ai_data/models.py)는 위 정의를 직접 구현합니다. [검증](../../../예제_examples/확장기초_extended/ai_data/test_models.py)은 중앙 유한차분 $`\{L(w+h)-L(w-h)\}/(2h)`$와 해석적 gradient를 비교합니다. $`y=2x`$의 독립적인 최적점 $`w^*=2`$로 수렴하는지, 작은 step 뒤 loss가 줄어드는지, 불균등 batch 가중 평균, schedule 양끝과 단조 감소도 확인합니다. 이는 작은 회귀 계산의 검증이며 실제 신경망의 학습 정확도·속도·일반화 측정 결과가 아닙니다.

## English

### Optimization and evaluation answer different questions

Training changes parameters to reduce a specified objective. Squared error for regression and cross-entropy for classification encode different output assumptions. Lower training loss and useful performance on new observations are different claims.

For the no-intercept model $`\hat y=wx`$, the equations above define half the mean squared error and its derivative. The derivative follows from the chain rule, multiplying the residual by $`x_i`$. When $`\sum x_i^2>0`$, setting it to zero gives $`w^*=\sum x_iy_i/\sum x_i^2`$. Some inputs may be zero; they must not all be zero.

### The update rule

Basic SGD updates $`w_{t+1}=w_t-\eta_tg_t`$. The negative gradient moves opposite the local direction of increasing loss. An optimizer specifies the actual update; momentum and Adam add different states and rules. The executable example uses only SGD without momentum. [PyTorch SGD](https://docs.pytorch.org/docs/2.14/generated/torch.optim.SGD.html)

This quadratic has curvature $`a=\sum x_i^2/n>0`$. With exact full-batch gradients and constant learning rate, the error obeys $`w_{t+1}-w^*=(1-\eta a)(w_t-w^*)`$. Convergence follows when $`0<\eta a<2`$; a larger step can diverge. This is a result for the specified one-dimensional quadratic, not a global guarantee for nonlinear neural networks.

### Batch accounting

At the same parameters, combining batch mean gradients requires sample weights: $`g=(n_1g_1+n_2g_2)/(n_1+n_2)`$. Averaging the two means equally is wrong when the final batch is smaller. Updating parameters between batches also makes several SGD steps different from one combined full-batch step. Gradient accumulation must match the intended loss reduction and sample counts. Batch size changes memory, gradient variation and update cost; larger is not universally better.

### Schedules and leakage

The cosine formula is defined on $`0\le t\le T`$, starts at $`\eta_{max}`$ and ends at $`\eta_{min}`$. Reproduction must state whether $`t`$ counts optimizer updates or epochs. The model implements a single decay interval without restarts. [CosineAnnealingLR](https://docs.pytorch.org/docs/2.14/generated/torch.optim.lr_scheduler.CosineAnnealingLR.html)

Training fits parameters, validation selects settings and testing evaluates the completed selection. Shared people, devices, adjacent frames or future information can invalidate independent evaluation. Fit preprocessing statistics on training data, then apply them to the other splits. Repeatedly choosing settings from test results makes the test part of selection. Google's material discusses duplicates and repeated reuse of evaluation sets. [Dataset separation](https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets)

### Implementation and checks

The linked functions implement the stated loss, derivative and schedule. Tests compare the gradient with an independent central finite difference, check convergence toward the known $`w^*=2`$ for $`y=2x`$, and verify loss reduction after a small step, unequal-batch weighting, schedule endpoints and monotonicity. They establish the arithmetic of a small regression problem, not measured neural-network accuracy, training speed or generalization.

## Sources

- [PyTorch SGD](https://docs.pytorch.org/docs/2.14/generated/torch.optim.SGD.html): gradient update conventions.
- [PyTorch CosineAnnealingLR](https://docs.pytorch.org/docs/2.14/generated/torch.optim.lr_scheduler.CosineAnnealingLR.html): closed-form decay and step convention.
- [Google ML Crash Course, dataset separation](https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets): validation/test roles, duplicated observations and repeated selection. Reference date: 2026-10-19.
