# 작은 MLP로 역전파를 끝까지 계산하기

[실행 코드](../../../예제_examples/심화_advanced/ai_data/advanced_ai_models.py) · [CLI](../../../예제_examples/심화_advanced/ai_data/demo.py) · [독립 검증](../../../예제_examples/심화_advanced/ai_data/test_advanced_ai.py)

## 선형 모델 다음에 필요한 것

한 개의 직선으로 나눌 수 없는 데이터가 있습니다. 두 입력의 부호가 다를 때만 1인 XOR가 작은 예입니다. 입력을 직선으로 분류하는 대신 여러 중간 특징을 만들고 이를 조합하면 경계를 구부릴 수 있습니다. MLP의 은닉층은 이런 중간 특징을 계산합니다. 역전파는 그 특징을 만드는 가중치까지 손실의 변화량을 전달합니다.

여기서는 입력 2개, tanh 은닉 unit 3개, 출력 2개를 사용합니다. 복잡한 모델의 성능을 주장하기 위한 데이터가 아니라 모든 매개변수의 계산을 펼쳐 볼 수 있는 크기입니다. 학습할 수는 입력 가중치 6개, 은닉 bias 3개, 출력 가중치 6개, 출력 bias 2개로 총 17개입니다. 비선형 함수를 빼면 두 affine 층의 합성도 다시 하나의 affine 변환이므로 은닉층 개수만 늘린 효과를 얻지 못합니다. [Stanford CS231n의 계산 그래프](https://cs231n.github.io/optimization-2/), [CS224n 신경망 강의](https://web.stanford.edu/class/cs224n/readings/cs224n-2019-notes03-neuralnets.pdf)

## 순전파와 손실

열벡터 입력을 $`x\in\mathbb R^2`$라 하고 $`W_1\in\mathbb R^{3\times2}`$, $`W_2\in\mathbb R^{2\times3}`$로 둡니다. 코드의 weight 행도 각 출력 unit에 대응합니다. 라이브러리의 저장 방향을 식과 맞추는 과정이 필요합니다. PyTorch Linear의 weight도 출력×입력 형태입니다. [Linear 정의](https://docs.pytorch.org/docs/2.9/generated/torch.nn.Linear.html)

```math
a=W_1x+b_1,\qquad h=\tanh(a),\qquad z=W_2h+b_2.
```

$`z`$는 class별 logit입니다. 정답 class $`y`$의 cross-entropy를 $`L=\ln\sum_c e^{z_c}-z_y`$로 계산합니다. 최대 logit $`m`$을 빼면 $`L=m+\ln\sum_c e^{z_c-m}-z_y`$가 되어 큰 지수의 overflow를 피합니다. Softmax 역시 같은 이동을 사용합니다. 출력 확률을 먼저 반올림한 뒤 log를 취하는 방식과 수치 경로가 다릅니다.

## Chain rule을 층별로 연결하기

Softmax의 미분은 $`\partial p_i/\partial z_j=p_i(\delta_{ij}-p_j)`$입니다. 손실에 적용하면 $`g_z=p-e_y`$로 정리됩니다. $`e_y`$는 정답 위치만 1인 벡터입니다. 출력 logit 하나의 변화가 loss에 미치는 값을 알면 각 곱셈을 거꾸로 따라갈 수 있습니다.

```math
g_{W_2}=g_z h^T,\quad g_{b_2}=g_z,\quad
g_h=W_2^Tg_z.
```

다음으로 tanh의 국소 미분 $`1-h_j^2`$를 곱합니다.

```math
g_a=g_h\odot(1-h\odot h),\qquad
g_{W_1}=g_a x^T,\qquad g_{b_1}=g_a.
```

여러 출력으로 갈라졌던 은닉 unit에는 모든 출력 경로의 기여가 더해집니다. 이 합을 마지막 경로의 미분으로 덮어쓰면 차원은 맞아도 계산은 틀립니다. Bias 미분은 연결된 logit 미분이며, 표본 평균 loss를 쓰면 전체 gradient도 표본별 gradient의 평균입니다. 같은 매개변수에서 계산한 평균과 표본마다 갱신한 여러 step은 서로 다른 연산입니다.

## 실제 실행

저장소 루트에서 실행합니다.

```bash
python "예제_examples/심화_advanced/ai_data/demo.py" mlp
python -m unittest discover -s "예제_examples/심화_advanced/ai_data" -p "test_*.py" -v
```

CLI는 seed 7로 초기화하고 네 XOR 표본에 full-batch gradient descent를 600회 적용합니다. Python 3.12.14 실행에서 평균 loss는 약 0.80027에서 0.01501로 감소했습니다. 이것은 코드가 실제 매개변수를 갱신하며 계산한 네 표본의 훈련 결과입니다. 새로운 데이터의 일반화 성능이나 특정 반도체·영상 과제의 정확도로 해석하지 않습니다. 결과 JSON에는 각 표본의 두 출력 확률과 반복 횟수도 있습니다.

## 코드와 다른 경로로 검증하기

17개 매개변수 각각을 $`\pm10^{-5}`$만큼 바꿔 중앙 차분을 계산하고 해석적 gradient와 비교합니다. 은닉층은 미분 가능한 tanh이므로 ReLU의 꺾이는 지점을 피하는 조건은 이 예제에 필요하지 않습니다. 반면 tanh가 포화하면 미분이 작아지므로 너무 큰 초기 가중치에서 수치 검사가 둔감해질 수 있습니다. 유한차분의 step을 지나치게 줄이면 반올림 오차가 커집니다.

큰 출력 logit $`(1000,-1000)`$에서 손실 2000을 안정적으로 계산하는지, batch 평균이 맞는지, Adam으로 같은 비선형 표본을 학습했을 때 loss와 분류가 맞는지도 따로 검사합니다. 계산량은 표본 수 $`B`$, 입력 폭 $`D`$, 은닉 폭 $`H`$, 출력 폭 $`C`$에서 대략 $`O(B(DH+HC))`$입니다. 이 Python 구현은 학습 구조를 드러내는 CPU 기준선이며 tensor kernel의 처리량을 대신하지 않습니다. 실제 배포는 전처리, 데이터 분리, 수치 형식과 task별 평가를 추가합니다.

## English

### Why add a hidden layer?

XOR labels two inputs as one only when their signs differ. One affine decision boundary cannot express it. An MLP creates intermediate nonlinear features, and backpropagation transfers loss derivatives to the parameters that create those features. Without the nonlinearity, composing affine layers still gives one affine map. This example has two inputs, three tanh units and two output classes: six input weights, three hidden biases, six output weights and two output biases, totaling 17 parameters. [CS231n](https://cs231n.github.io/optimization-2/) and [CS224n](https://web.stanford.edu/class/cs224n/readings/cs224n-2019-notes03-neuralnets.pdf) provide the graph and chain-rule foundations.

The small XOR set exposes calculations rather than establishing performance on an application dataset.

### Forward computation and derivatives

For column input $`x\in\mathbb R^2`$, use $`W_1:3\times2`$ and $`W_2:2\times3`$. Each weight row produces one output unit, consistent with the output-by-input storage described by [PyTorch Linear](https://docs.pytorch.org/docs/2.9/generated/torch.nn.Linear.html). The forward equations above compute affine hidden inputs, tanh activations and output logits.

Cross-entropy is $`L=\ln\sum_c e^{z_c}-z_y`$. Subtracting the maximum logit before exponentiation produces the equivalent stable expression. Softmax uses the same shift. This differs numerically from taking a logarithm after a probability has rounded to zero.

Its Jacobian is $`\partial p_i/\partial z_j=p_i(\delta_{ij}-p_j)`$, yielding $`g_z=p-e_y`$. Following the output affine map backward gives $`g_{W_2}=g_z h^T`$, $`g_{b_2}=g_z`$ and $`g_h=W_2^Tg_z`$. The tanh derivative then gives $`g_a=g_h\odot(1-h\odot h)`$, followed by $`g_{W_1}=g_a x^T`$ and $`g_{b_1}=g_a`$.

A hidden unit receives contributions from every outgoing path. Accumulate them; replacing one contribution with another can preserve shapes while breaking the derivative. For mean sample loss, average gradients at the same parameters. Sequential per-sample updates are a different operation.

### Executed example and independent checks

Run the two commands above from the repository root. The CLI initializes with seed seven and performs 600 full-batch gradient-descent updates on four XOR samples. A Python 3.12.14 execution reduced mean training loss from approximately 0.80027 to 0.01501. The JSON also contains sample probabilities and update count. These are executed training calculations on the specified four observations, not generalization or accuracy claims for a semiconductor or vision task.

Tests perturb each of the 17 parameters by $`\pm10^{-5}`$ and compare centered differences with the analytic derivative. Tanh is differentiable, so the ReLU kink issue is absent. Saturation can make derivatives small and checks less informative; excessively small difference steps amplify rounding error. Separate checks cover logits $`(1000,-1000)`$ with loss 2000, correct batch averaging and loss/classification after Adam updates on the nonlinear sample.

For batch size $`B`$, input width $`D`$, hidden width $`H`$ and class width $`C`$, work is approximately $`O(B(DH+HC))`$. The implementation is a readable CPU reference, not a tensor-kernel throughput claim. Deployment additionally needs preprocessing, independent data splits, numerical-format agreement and task-specific evaluation.

## 출처 / Sources

- [Stanford CS231n, Backpropagation](https://cs231n.github.io/optimization-2/): local derivatives, accumulated branches and matrix gradients.
- [Stanford CS224n, Neural Networks and Backpropagation](https://web.stanford.edu/class/cs224n/readings/cs224n-2019-notes03-neuralnets.pdf): multilayer chain rule and classification loss.
- [PyTorch 2.9 Linear](https://docs.pytorch.org/docs/2.9/generated/torch.nn.Linear.html): weight dimensions and affine convention. 확인 / checked: 2026-10-19.
