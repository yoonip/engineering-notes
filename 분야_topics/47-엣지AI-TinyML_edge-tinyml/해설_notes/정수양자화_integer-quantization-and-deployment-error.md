# 정수 양자화: scale, zero-point, 배포 오차

## 적은 bit로 값을 표현한다는 것

실수 tensor를 8 bit 정수로 표현하면 저장 공간과 전송량을 줄일 수 있다. 적절한 연산 지원이 있는 장치에서는 실행 비용도 줄일 가능성이 있다. 하지만 파일 크기가 작다는 사실만으로 추론 시간이 줄었다고 결론내릴 수는 없다. 변환·메모리 이동·지원되지 않는 연산의 fallback 비용이 있기 때문이다. 먼저 수치 표현이 무엇을 보존하고 무엇을 버리는지 살펴본다.

Affine quantization은 실수 $x$와 정수 $q$의 관계를 양의 scale $s$와 정수 zero-point $z$로 정의한다.

$$\hat x=s(q-z),\qquad
q=\operatorname{clip}\bigl(\operatorname{round}(x/s)+z,q_{min},q_{max}\bigr).$$

Scale의 단위는 원래 값/정수 단계이며, zero-point는 실수 0을 표현하는 정수다. $q=z$이면 $\hat x=0$이 정확하다. Google LiteRT의 int8 사양은 이 재구성식을 사용하고, activation과 weight의 범위·zero-point 조건을 구분한다. 모든 tensor가 같은 양자화 조건을 쓰는 것은 아니다. [LiteRT specification](https://developers.google.com/edge/litert/conversion/tensorflow/quantization/quantization_spec)

## 격자 간격과 clipping을 나누어 생각하기

정수 $q$는 실수축의 등간격 눈금 하나에 해당한다. 범위를 벗어나지 않는 값의 최근접 반올림에서는 $x/s$와 선택한 정수의 차이가 최대 $1/2$이므로

$$|x-\hat x|\le s/2.$$

이 경계는 clipping이 일어나지 않는다는 조건 아래의 단일 값 오차다. 표현 범위 $[s(q_{min}-z),s(q_{max}-z)]$ 밖의 값은 끝으로 잘려 오차가 훨씬 커질 수 있다. 예를 들어 $s=0.5,z=0$인 int8에서 100은 127로 포화되고 복원값은 63.5다. 이 경우 오차 36.5에 $s/2=0.25$ 경계를 적용할 수 없다.

반올림의 동점 처리도 계약의 일부다. 예제는 Python `round`의 ties-to-even을 사용한다. $0.25/0.5=0.5$는 0으로, $0.75/0.5=1.5$는 2로 간다. ONNX `QuantizeLinear`도 최근접 짝수 반올림과 saturation을 명시한다. 실제 kernel의 연산 순서·수치 형식은 대상 연산자 사양과 맞춰야 한다. [ONNX QuantizeLinear](https://onnx.ai/onnx/operators/onnx__QuantizeLinear.html)

## 정수 내적은 왜 누산 범위가 중요한가

벡터 $x,w$에 서로 다른 $s_x,z_x,s_w,z_w$를 사용하면

$$\hat x\cdot\hat w=s_xs_w\sum_{i=1}^n(q_{x,i}-z_x)(q_{w,i}-z_w).$$

괄호를 전개하면 정수 곱의 합과 zero-point 보정 항이 나온다. Weight의 $z_w=0$인 대칭 양자화는 일부 보정 비용을 없앤다. LiteRT는 여러 weight 연산에 이런 조건을 둔다. [LiteRT의 대칭 weight 설명](https://developers.google.com/edge/litert/conversion/tensorflow/quantization/quantization_spec)

입력 범위에서 $|q_x-z_x|\le A$, $|q_w-z_w|\le B$라면 누산 절댓값은 최악의 경우 (nAB) 이하다. 이 값에 bias와 추가 연산을 포함해 누산 dtype의 범위와 비교해야 한다. Python 정수는 큰 값으로 확장되므로 Python 계산이 overflow하지 않았다는 사실은 int32 하드웨어의 안전성을 검증하지 못한다.

## Tensor별·channel별 scale과 배포 평가

Per-tensor는 tensor 전체에 하나의 scale, per-axis는 지정 축의 각 slice에 다른 scale을 둔다. 채널 간 크기가 크게 다르면 하나의 큰 scale이 작은 값의 해상도를 거칠게 만들 수 있다. 반대로 finer granularity는 metadata와 연산 지원 조건을 바꾼다. Calibration은 대표 입력을 통해 activation 범위를 정하는 과정이며, 배포 데이터와 전혀 다른 표본이면 clipping과 오차 추정이 빗나갈 수 있다.

| 검증 층 | 비교할 값 |
|---|---|
| 숫자 표현 | 0, 최소·최대, 동점, clipping, scale |
| 연산자 | 입력·출력 scale, 축, bias, 누산 범위 |
| 모델 | float 기준과 task 지표·조건별 오차 |
| 장치 | 실제 latency, 메모리, 에너지, fallback |

단일 값의 반올림 경계는 최종 모델 정확도의 경계가 아니다. 여러 층의 비선형 연산, clipping, requantization이 오차를 바꾼다. 실제 배포 비교는 동일 입력과 전처리, float 기준 출력, 정답 label 및 대상 장치 측정을 함께 사용한다.

## 구현과 검증

[`quantize`, `dequantize`](../../../예제_examples/확장기초_extended/ai_data/models.py)는 scalar affine 모델이다. [테스트](../../../예제_examples/확장기초_extended/ai_data/test_models.py)는 256개 int8 격자점을 왕복 변환하고, ties-to-even과 양 끝 clipping을 확인한다. 표현 범위 안의 1,001개 값에서 $s/2$ 오차 경계를 검사한다. Scale $1/8$을 사용해 이진 부동소수점으로도 격자를 정확히 표현한다. 실제 신경망의 quantization-aware training, 연산자 변환이나 장치 가속 검증 결과는 아니다.

## English

### Representing values with fewer bits

Eight-bit tensors reduce storage and transfer volume. Hardware with suitable operators may also reduce computation cost, but a smaller file alone does not establish faster inference: conversion, data movement and fallback operations matter.

Affine quantization uses positive scale $s$ and integer zero-point $z$. The equations above reconstruct $\hat x=s(q-z)$ and quantize with rounding and clipping. Scale has units of the original quantity per integer step; $q=z$ represents real zero exactly. LiteRT distinguishes activation and weight ranges and zero-point requirements rather than applying one rule to every tensor. [LiteRT specification](https://developers.google.com/edge/litert/conversion/tensorflow/quantization/quantization_spec)

### Rounding error and saturation

Integer codes form an evenly spaced real-valued grid. Without clipping, nearest rounding changes $x/s$ by at most $1/2$, giving $|x-\hat x|\le s/2$. Outside the representable interval, saturation invalidates that bound. With int8, $s=0.5,z=0$, quantizing 100 produces 127 and reconstructs 63.5, an error of 36.5 rather than at most 0.25.

Tie handling is part of the contract. This model uses ties-to-even: $0.25/0.5=0.5$ rounds to zero and $0.75/0.5=1.5$ rounds to two. ONNX `QuantizeLinear` specifies nearest-even rounding and saturation. Actual kernels must match their operator's numerical format and ordering rules. [ONNX operator](https://onnx.ai/onnx/operators/onnx__QuantizeLinear.html)

### Dot products and accumulator range

Different input and weight scales give $s_xs_w\sum(q_x-z_x)(q_w-z_w)$. Expanding the product exposes zero-point correction terms. Symmetric weights with $z_w=0$ remove some runtime correction work, as required by several LiteRT weight operators. [Symmetric weights](https://developers.google.com/edge/litert/conversion/tensorflow/quantization/quantization_spec)

If centered code magnitudes are bounded by $A,B$, then the accumulator magnitude is at most (nAB). Bias and later arithmetic also need range analysis. Python's arbitrary-size integers do not demonstrate that a fixed-width int32 device accumulator is safe.

### Granularity and deployment

Per-tensor quantization shares parameters across the tensor; per-axis assigns parameters to slices of a specified axis. Large channel-to-channel scale differences can make a shared scale coarse for small values. Finer granularity changes metadata and operator support requirements. Calibration estimates activation ranges from representative data; mismatched calibration data can misrepresent clipping and error.

The table separates representation checks, operator agreement, task-level comparison and measured device cost. A scalar rounding bound is not a bound on final model accuracy: nonlinear layers, clipping and requantization alter propagation. Deployment evaluation needs identical inputs and preprocessing, a floating-point reference, labels and measurements on the target device.

### Implementation and checks

The scalar functions are linked above. Tests round-trip every int8 grid point, verify tie behavior and saturation, and check the $s/2$ bound on 1,001 in-range values. A scale of $1/8$ makes the test grid exactly representable in binary floating point. These are numerical checks, not results from quantization-aware training, model conversion or device acceleration.

## Sources

- [Google LiteRT, 8-bit quantization specification](https://developers.google.com/edge/litert/conversion/tensorflow/quantization/quantization_spec): affine reconstruction, per-axis granularity, activation/weight restrictions and integer products.
- [ONNX, QuantizeLinear](https://onnx.ai/onnx/operators/onnx__QuantizeLinear.html): nearest-even rounding and saturation semantics. Reference date: 2026-10-19.
