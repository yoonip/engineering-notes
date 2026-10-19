# 전이 전압으로 읽는 ADC 선형성: DNL과 INL

[ADC·DAC 목차](../README.md) · [전이값 모델](../../../예제_examples/심화_advanced/hardware/models.py) · [검산](../../../예제_examples/심화_advanced/hardware/test_models.py)

## 한국어

### 눈금의 폭과 눈금의 위치는 다른 문제입니다

자를 만들었는데 어떤 1 mm 구간은 넓고 다음 구간은 좁다고 하겠습니다. 구간 폭이 얼마나 다른지는 DNL, 눈금 전체가 기준 직선에서 얼마나 벗어났는지는 INL과 비슷합니다. ADC에서도 코드가 바뀌는 입력 전압, 즉 transition voltage를 알면 두 양을 구할 수 있습니다. 비트 수가 같아도 전이 간격이 다르면 측정 결과는 달라집니다.

[TI의 *Selecting an A/D Converter*](https://www.ti.com/lit/an/sbaa004a/sbaa004a.pdf)와 [ADI의 INL/DNL 측정 설명](https://www.analog.com/en/resources/technical-articles/inldnl-measurements-for-types-of-highspeed-adcs.html)을 비교했습니다. 기준 직선을 어떻게 정하는지에 따라 INL이 달라지므로, 이 글의 계산 정의를 먼저 고정합니다. 제조사별 보고값에 바로 숫자를 대입해 비교하지 않습니다.

### 끝점 전이 기준의 정의

N비트 ADC는 M=2^N개 코드와 M−1개 내부 전이 $`T_1,\ldots,T_{M-1}`$를 가집니다. 전이값은 V 단위이며 감소하지 않는다고 가정합니다. 첫 코드와 마지막 코드는 입력 한계 밖까지 이어질 수 있으므로 폭 계산에서 제외합니다. 여기서는 첫·마지막 내부 전이를 잇는 직선으로 offset과 gain을 제거합니다.

```math
\Delta_{fit}=\frac{T_{M-1}-T_1}{M-2},\qquad
T_{k,ideal}=T_1+(k-1)\Delta_{fit}.
```

내부 코드 k의 폭은 $`W_k=T_{k+1}-T_k`$입니다. 따라서 signed DNL과 transition INL을 다음처럼 정합니다.

```math
DNL_k=\frac{W_k}{\Delta_{fit}}-1\quad (1\le k\le M-2),
\qquad INL_k=\frac{T_k-T_{k,ideal}}{\Delta_{fit}}.
```

두 값의 단위는 여기서 정의한 fitted LSB입니다. DNL 절댓값 최대치만 보고하는 표와 달리 코드별 부호를 보존합니다. 이 끝점 정의는 best-fit 직선을 최소제곱으로 구하는 INL과 다릅니다. Δfit 자체가 데이터에서 구해졌으므로 absolute gain error가 별도로 남지 않습니다.

### 한 전이를 밀면 두 코드 폭이 바뀝니다

3비트의 이상 전이값이 [1,2,3,4,5,6,7] V라고 하겠습니다. T4만 4.25 V로 바꾸면 첫·마지막 전이는 같아서 Δfit=1 V입니다.

| 내부 코드 | 실제 폭 | DNL |
|---|---:|---:|
| 3 | 4.25−3=1.25 V | +0.25 LSB |
| 4 | 5−4.25=0.75 V | −0.25 LSB |

다른 내부 폭은 그대로이고 T4의 INL은 +0.25 LSB입니다. 전이 하나의 이동이 인접한 두 DNL에 반대 부호로 나타나는 것이 좋은 검산입니다. 내부 DNL 합은 이 normalization에서 정확히 0입니다. fitted 첫·마지막 INL도 0입니다. 이 결과는 ADC가 완벽하다는 뜻이 아니라 기준선을 그렇게 정했기 때문입니다.

폭이 0이면 DNL=−1이고 해당 코드가 차지하는 입력 구간이 사라집니다. 감소하는 전이 목록은 이 단조 threshold 모델과 맞지 않으므로 코드가 거부합니다. 노이즈가 있는 실제 전이는 확률적으로 관찰되며 경계에서 두 인접 코드가 같은 확률로 나오는 지점을 정의할 수 있습니다. noise·hysteresis·고속 동작의 memory effect는 이상적 정적 threshold 목록보다 복잡합니다.

### 구현과 계측의 차이

```bash
python demo.py --case adc
python -m unittest -v test_models.HardwareModels.test_adc_transition_error_pair test_models.HardwareModels.test_adc_missing_code_and_endpoint_sum
```

`adc_linearity()`는 2비트 이상 2^N 코드에 맞는 내부 전이 목록을 받습니다. 위 ±0.25 쌍, missing-code −1, DNL 합과 끝점 INL, 전이 역전 입력을 독립 기준으로 검사합니다. 결과는 합성한 전이값의 수학적 계산이며 ADC 보드의 선형성 측정이 아닙니다.

균일 ramp를 일정한 속도로 충분히 촘촘히 관찰하면 내부 코드 발생 빈도가 폭에 비례하지만, ramp 비선형성과 finite-count 불확도가 같이 들어옵니다. sine histogram은 입력 분포가 균일하지 않으므로 같은 정규화식을 쓰면 안 됩니다. 실물은 source 정확도·settling·noise·Vref·입력 driver를 기록하고 전이 추정과 confidence interval을 확인합니다. 서로 다른 endpoint·best-fit·ideal-LSB 관례를 섞지 않는 것이 수치 정밀도보다 먼저입니다.

## English

### Width errors and position errors

A ruler can have intervals of unequal width and marks that deviate from a straight reference scale. ADC DNL describes the first effect; INL describes the second. Transition voltages locate the input values at which codes change. Identical bit counts do not guarantee identical transfer accuracy.

Definitions and measurement interpretation are cross-checked against [TI's converter selection report](https://www.ti.com/lit/an/sbaa004a/sbaa004a.pdf) and [ADI's INL/DNL article](https://www.analog.com/en/resources/technical-articles/inldnl-measurements-for-types-of-highspeed-adcs.html). Because reference-line conventions differ, the example explicitly defines its own transition-endpoint normalization before calculating errors.

### Defining the fitted transition scale

An N-bit converter has M=2^N codes and M−1 internal transitions. Transitions are nondecreasing voltages. First and last code widths are excluded because their bins may extend beyond the specified input range. The reference line joins the first and last internal transitions, giving $`\Delta_{fit}=(T_{M-1}-T_1)/(M-2)`$ and ideal transition $`T_1+(k-1)\Delta_{fit}`$.

For an interior code, width is $`W_k=T_{k+1}-T_k`$. Signed DNL is width/Delta_fit−1. INL is transition deviation from the fitted line divided by Delta_fit. The unit is the fitted LSB used here. These signed code errors differ from a specification reporting only a maximum absolute error. Endpoint fitting also differs from a least-squares best-fit INL, and removes absolute offset and gain from this representation.

### Independent example and invariants

For a three-bit example with transitions [1,2,3,4,5,6,7] V, move only T4 to 4.25 V. Delta_fit remains 1 V. The neighboring code widths become 1.25 and 0.75 V, giving +0.25 and −0.25 LSB DNL. T4 has +0.25 LSB INL; other transitions remain on the reference line. One displaced threshold must therefore affect two adjacent widths with opposite signs.

Interior DNL values sum to zero under this fitted normalization, and endpoint INLs are zero by construction. Neither fact establishes a perfect converter. A zero-width bin gives DNL=−1 and no finite input interval for that code. Decreasing thresholds are rejected by this monotonic-threshold model. Real noisy transitions are probabilistic; a 50/50 boundary definition is possible, but hysteresis and dynamic memory effects require richer models.

### Running and measuring

The commands above run the synthetic-transition demo and checks for the ±0.25 pair, missing-code case, DNL sum, endpoint INLs and reversed input thresholds. They calculate properties of supplied thresholds; they are not board measurements.

With a sufficiently sampled constant-speed uniform ramp, interior code counts are proportional to bin widths, subject to ramp nonlinearity and finite-count uncertainty. A sine histogram has a nonuniform input distribution and needs different normalization. Physical testing must record source accuracy, settling, noise, reference and input-driver conditions, and examine transition-estimation uncertainty. Keep endpoint, best-fit and ideal-LSB conventions distinct before comparing reported numbers.

## 출처 / Sources

- Texas Instruments, *SBAA004A Selecting an A/D Converter*: static linearity definitions and test context.
- Analog Devices, *INL/DNL Measurements for High-Speed ADCs*: reference-line choices and probabilistic transitions. Links are provided above.
