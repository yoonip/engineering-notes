# 채널별 정수 양자화와 오차의 크기

[정수 연산 모델](../../../예제_examples/심화_advanced/ai_data/advanced_ai_models.py) · [실행 CLI](../../../예제_examples/심화_advanced/ai_data/demo.py) · [독립 검증](../../../예제_examples/심화_advanced/ai_data/test_advanced_ai.py)

## 작은 수를 큰 자와 함께 재면

몸집이 다른 물체를 같은 눈금자로 재면 작은 물체의 차이를 구별하기 어렵다. 신경망에서도 한 출력 채널의 가중치는 0.01 정도이고 다른 채널은 5 정도일 수 있다. 두 채널에 같은 정수 눈금을 쓰면 작은 채널의 가중치가 전부 0으로 반올림될 수 있다.

Per-channel, 또는 per-axis 양자화는 정해진 축을 따라 scale을 여러 개 둔다. 여기서는 행렬 W의 행 하나가 출력 채널 하나인 선형층 $`y=Wx`$다. 입력은 벡터 하나에 scale 하나, 가중치는 출력 행마다 scale 하나를 쓴다. 이 배치는 모든 convolution·배포 연산자의 축과 같다는 뜻은 아니다. 실제 tensor layout과 연산자 규약을 확인해야 한다. [LiteRT int8 규약](https://developers.google.com/edge/litert/conversion/tensorflow/quantization/quantization_spec), [ONNX QuantizeLinear](https://onnx.ai/onnx/operators/onnx__QuantizeLinear.html)

## 실수 눈금과 정수 표현

일반적인 affine 표현은 $`r=s(q-z)`$다. s는 양의 scale, z는 실수 0을 나타내는 정수 zero point다. 예제는 z=0인 대칭 표현과 정수 범위 [-127,127]을 입력·가중치 모두에 사용한다. 입력도 -128을 제외하는 이 선택은 교육 모델의 계약이며 모든 int8 backend의 입력 범위와 같지는 않다.

입력의 최대 절댓값을 a, 출력 행 j의 최대 절댓값을 b라 하면

```math
s_x=\frac{\max_i|x_i|}{127},\qquad
s_{w,j}=\frac{\max_i|w_{ji}|}{127},
\qquad
q_{x,i}=\mathrm{clip}\!\left(\mathrm{round}(x_i/s_x),-127,127\right).
```

가중치도 행 scale로 같은 연산을 한다. 최대 절댓값이 0인 벡터나 행은 scale=1을 사용한다. 그 값은 정확히 0으로 양자화되므로 출력에 영향을 주지 않는다. 반올림은 Python의 nearest, ties-to-even이다. 중간값의 tie 규칙은 ONNX의 설명과 일치하지만, 실제 변환기 전체와 bit 단위로 같다는 주장은 아니다.

이 예제의 입력 scale은 호출 때 전달된 실제 입력 벡터로 계산한다. 고정 calibration 데이터로 scale을 정해 새 입력을 처리하는 static 양자화와 다르다. 현재 벡터에는 절댓값 범위 밖 값이 없어 clipping 오차가 생기지 않는다. 고정 scale을 쓰는 배포에서는 범위를 벗어난 입력의 clipping을 별도로 다뤄야 한다.

## 행별 scale을 정수 내적 밖으로 꺼낸다

복원된 입력과 가중치를 선형식에 대입하면 한 출력 채널 안에서는 scale이 상수다.

```math
\tilde y_j
=\sum_i(s_{w,j}q_{w,ji})(s_xq_{x,i})
=s_xs_{w,j}\underbrace{\sum_iq_{w,ji}q_{x,i}}_{A_j}.
```

$`A_j`$는 정수 곱의 합이다. 출력 채널마다 마지막 실수 환산 계수만 달라진다. 이 구조 때문에 채널별 가중치 scale을 써도 각 곱마다 서로 다른 실수 scale을 적용할 필요는 없다.

예제는 bias를 넣지 않고 정수 누산 뒤 실수 출력으로 복원한다. int8 출력으로 다시 양자화하는 multiplier·shift·saturation, int32 bias 변환, fused activation은 포함하지 않는다. LiteRT의 특정 선형 연산에서 bias scale은 입력 scale과 해당 가중치 scale의 곱으로 정해진다. 입력 scale을 매번 바꾸면 고정 정수 bias를 그대로 쓸 수 없는 이유도 이 식에서 보인다.

## 공통 scale과 채널별 scale의 차이

첫 행이 [0.01, 0.002, -0.005, 0.001], 둘째 행이 [3, -2, 5, 0.1]이면 공통 absmax scale은 5/127이다. 첫 행의 최대값도 그 반 눈금보다 작아 전부 0으로 반올림된다. 행별 scale을 쓰면 첫 행은 0.01/127, 둘째 행은 5/127로 서로 다른 해상도를 갖는다.

이는 해당 행의 표현 오차가 줄어드는 예다. 최종 task accuracy가 항상 좋아진다는 증명은 아니다. 여러 층의 오차, activation 범위, calibration 분포, 연산자 지원, clipping과 재양자화가 실제 결과를 좌우한다.

## 출력 오차의 상계를 유도한다

원래 입력과 가중치가 양자화 범위 안에 있고 nearest 반올림을 쓰면 복원 오차의 크기는 $`\epsilon_x=s_x/2`$, $`\epsilon_{w,j}=s_{w,j}/2`$ 이하로 둘 수 있다. 복원값을 $`x+\delta x`$, $`w+\delta w`$로 적고 곱을 전개한다.

```math
(w+\delta w)(x+\delta x)-wx
=w\delta x+x\delta w+\delta w\delta x.
```

삼각부등식을 항마다 적용하면

```math
|\tilde y_j-y_j|
\le\sum_i\left(
|w_{ji}|\epsilon_x+|x_i|\epsilon_{w,j}
+\epsilon_x\epsilon_{w,j}\right).
```

상계는 실제 오차보다 느슨할 수 있다. 양·음 오차가 상쇄되는 효과를 모두 절댓값으로 세기 때문이다. Clipping된 값에는 반 눈금 상계만 적용할 수 없으므로, 이 식의 전제는 중요하다. 부동소수점 연산의 작은 잔차는 테스트 허용오차로 분리한다.

## 실제 실행과 누산 범위

```bash
python "예제_examples/심화_advanced/ai_data/demo.py" quantization
python -m unittest discover -s "예제_examples/심화_advanced/ai_data" -p "test_*.py" -v
```

입력 [0.3, -0.8, 1, 0.01]과 위 두 행, 0으로 된 셋째 행을 계산한다.

| 출력 행 | 실수 내적 | 정수 누산 후 복원 | 절대오차 |
|---|---:|---:|---:|
| 1 | -0.003590 | -0.00362019 | 0.00003019 |
| 2 | 7.501000 | 7.50883502 | 0.00783502 |
| 3 | 0 | 0 | 0 |

테스트는 실수 내적을 독립 기준으로 계산하고 위 해석적 상계 안에 복원 오차가 드는지 확인한다. 0 입력·0 행, scale 값과 정수 범위도 검사한다. 실제 모델의 정확도 평가나 기기별 kernel 벤치마크가 아니라, 작은 정수 선형층의 수치 검증이다.

길이가 n인 내적에서 각 항의 절댓값은 최대 $`127^2`$이므로 $`|A_j|\le n\,127^2`$다. Signed int32에 저장하려면 이 상계와 bias 등을 합쳐 $`2^{31}-1`$을 넘지 않는 조건이 필요하다. Python 정수는 임의 정밀도라 여기서 int32 overflow가 재현되지 않는다. 실제 backend가 사용하는 중간 폭·포화 규칙·누산 순서는 별도 규약이다. 연산량은 입력 차원 n, 출력 채널 C에 대해 O(Cn), 가중치 저장은 O(Cn)이며, 이 stdlib 계산 시간은 정수 가속기의 속도를 나타내지 않는다.

## English

### Give channels a useful resolution

A common ruler can hide a small object beside a large one. Likewise, one output channel may have weights around 0.01 while another reaches five. A single integer scale can round every weight in the small channel to zero.

Per-channel or per-axis quantization assigns multiple scales along a specified tensor axis. Here each row of W is one output channel of $`y=Wx`$: the input vector uses one scale and each weight row has its own scale. This layout is not a universal statement about convolution or deployment operators; the axis and tensor layout are part of the contract. [LiteRT's int8 specification](https://developers.google.com/edge/litert/conversion/tensorflow/quantization/quantization_spec) and [ONNX QuantizeLinear](https://onnx.ai/onnx/operators/onnx__QuantizeLinear.html) define concrete conventions.

### Quantization and an integer accumulator

The general affine relation is $`r=s(q-z)`$, with positive scale s and integer zero point z. This model uses z=0 and [-127,127] for both inputs and weights. Excluding -128 for inputs is an explicit educational choice, not every backend's input convention.

The input scale is its absolute maximum divided by 127; each row scale is that row's absolute maximum divided by 127. Divide, round to nearest with ties to even, and clip to the integer range. An all-zero input or row uses scale one, yielding exact zeros. The tie convention agrees with ONNX, without claiming bit-exact equivalence to an entire deployment converter.

Input scaling is dynamic: it is computed from the current input vector on every call, not fixed from a calibration set. These particular values lie within their chosen ranges, so no saturation error occurs. Static deployment scales must also account for future out-of-range inputs.

Substituting the reconstructed values into the linear layer factors the scales out of each row's dot product:
$`\tilde y_j=s_xs_{w,j}A_j`$, where $`A_j=\sum_iq_{w,ji}q_{x,i}`$ is an integer accumulator. Different output-row scales do not require a floating-point scale at every multiply.

The implementation has no bias and reconstructs floating-point outputs. It omits int8 output requantization, multiplier/shift approximations, int32 bias conversion and fused activations. In specific LiteRT linear operators, bias scales use the input scale times the corresponding weight scale. A dynamically changing input scale therefore cannot simply reuse an unchanged integer bias representation.

### Resolution and a derived error bound

For rows [0.01, 0.002, -0.005, 0.001] and [3, -2, 5, 0.1], a shared absmax scale is 5/127. Every first-row weight lies below half this step and rounds to zero. Per-row scales are 0.01/127 and 5/127, preserving much finer first-row resolution. This example concerns representation error, not a guarantee of better task accuracy after a complete multilayer conversion. Activations, distributions, operator support, clipping and requantization also matter.

Without clipping, nearest reconstruction errors satisfy $`|\delta x_i|\le s_x/2`$ and $`|\delta w_{ji}|\le s_{w,j}/2`$. Expanding the perturbed product gives $`w\delta x+x\delta w+\delta w\delta x`$. Applying the triangle inequality and summing yields the bound above. It may be loose because it discards cancellation. Saturation does not obey the half-step assumption, and floating-point residuals are handled separately by a small test tolerance.

### Executed calculation and deployment limits

For input [0.3,-0.8,1,0.01], the first two floating-point outputs are -0.00359 and 7.501. Executed integer accumulators reconstruct approximately -0.00362019 and 7.50883502; a third zero row remains zero. Tests compute an independent float dot-product reference, check the analytic bound, and cover zero rows/inputs, scales and integer ranges. This is numerical validation of a small layer, not measured task accuracy or a device kernel benchmark.

Each signed symmetric integer product has magnitude at most $`127^2`$, so a length-n accumulator is bounded by $`n127^2`$. An int32 implementation must fit the accumulator and any bias within its supported range; Python's arbitrary-precision integers do not reproduce int32 overflow. Intermediate width, saturation and accumulation order remain backend contracts.

For C outputs and n input features, computation is O(Cn) and weight storage is O(Cn). The runtime of these Python loops does not measure integer-accelerator performance.

## 출처 / Sources

- [Google LiteRT: 8-bit quantization specification](https://developers.google.com/edge/litert/conversion/tensorflow/quantization/quantization_spec): affine representation, per-axis weights, int8 ranges and bias-scale contracts.
- [ONNX QuantizeLinear operator](https://onnx.ai/onnx/operators/onnx__QuantizeLinear.html): per-axis scale shape and nearest ties-to-even rounding. 확인 / checked: 2026-10-19.
