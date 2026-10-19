# 고정소수점 곱셈: 비트 폭, 반올림, 포화를 따로 결정하기

[RTL 설계 목차](../README.md) · [Python 모델](../../../예제_examples/심화_advanced/hardware/models.py) · [RTL](../../../예제_examples/심화_advanced/hardware/qmul16.sv) · [실행기](../../../예제_examples/심화_advanced/hardware/run_rtl.py)

## 한국어

### 정수에 소수점의 위치를 약속한다

고정소수점은 정수 저장 공간에 눈금을 붙이는 방법이다. 소수 8비트를 약속하면 raw 정수 256은 실제 값 1을 뜻한다. 같은 비트열도 눈금이 다르면 다른 수가 된다. 따라서 “16비트 곱셈”만으로는 결과를 정의할 수 없다. 부호, 소수 비트 수, 중간 비트 폭, 반올림 방향, 범위를 넘었을 때의 처리를 함께 정해야 한다.

여기서는 두 입력 모두 signed 16비트, 소수 8비트이며 $`x=a/2^8`$, $`z=b/2^8`$다. 표현 범위는 −128에서 127.99609375, 눈금은 1/256이다. Q 표기에서 sign bit를 정수 비트에 포함하는 관례가 다를 수 있어 비트 수와 해석식을 직접 적는다. [AMD UG1399의 quantization 정의](https://docs.amd.com/r/2021.1-English/ug1399-vitis-hls/Quantization-Modes)와 [MathWorks rounding 정의](https://www.mathworks.com/help/fixedpoint/ug/rounding.html)를 대조해 ties-to-even을 사용한다.

### 곱의 소수점은 두 배로 늘어난다

```math
xz=\frac{ab}{2^{16}},\qquad
y_{raw}=\mathrm{sat}_{16}\left(\mathrm{roundEven}\left(\frac{ab}{2^8}\right)\right).
```

출력도 소수 8비트이므로 전체 정수 곱을 256으로 나눈 뒤 반올림한다. signed 16×16 곱은 signed 32비트에 담긴다. 먼저 잘라 버린 뒤 넓히면 이미 잃은 상위 비트가 돌아오지 않는다. RTL은 `product`를 32비트로 명시하고, 반올림한 값은 포화 판정 전까지 더 넓은 부호형에 둔다.

짝수 반올림은 정확히 중간이면 가까운 두 정수 중 짝수를 고른다. 양수의 버림 몫을 q, 나머지를 r이라 하면 r>128이면 q+1, r=128이고 q가 홀수여도 q+1, 그 외에는 q다. 음수는 크기에 같은 연산을 한 뒤 부호를 복원한다. 단순한 arithmetic right shift는 음수에서 floor에 가깝고, 여기의 round-to-nearest 정책과 다르다.

| a×b의 raw 곱 /256 | 반올림 결과 | 이유 |
|---|---:|---|
| 128/256 = 0.5 | 0 | 중간의 짝수 |
| 384/256 = 1.5 | 2 | 중간의 짝수 |
| −128/256 = −0.5 | 0 | 부호와 무관한 짝수 규칙 |
| −384/256 = −1.5 | −2 | 같은 규칙 |
| 표현 가능한 최대보다 큼 | 32767 | 상단 포화 |

포화는 raw 범위를 [−32768,32767]로 제한한다. wrap-around와 달리 큰 양수가 갑자기 음수가 되지 않지만, 파형 왜곡은 생긴다. 정확한 값이 출력 범위 안에 있고 포화되지 않는다면 반올림 오차 절댓값은 출력 한 눈금의 절반 이하, 즉 1/512다. 포화가 발생한 경우 이 경계는 적용되지 않는다.

### Python과 RTL을 다르게 구현해 비교하기

```bash
python demo.py --case fixedpoint
python -m unittest -v test_models.HardwareModels.test_qmul_fraction_oracle test_models.HardwareModels.test_qmul_ties_and_saturation
python run_rtl.py
```

Python `qmul16()`은 정수 몫과 나머지로 구현했다. 독립 oracle은 `Fraction(a*b,256)`에 Python의 정확한 유리수 짝수 반올림을 적용한다. 무작위 10000쌍과 경계·동률·포화 사례를 비교한다. 별도 RTL 실행기는 경계값 11×11쌍과 무작위 10000쌍, 총 10121개 기대값을 `vectors.hex`에 임시 생성한다. Icarus로 SystemVerilog를 컴파일하고 vvp에서 모든 출력을 비교한다.

이 예제는 Icarus 12.0에서 10121개 벡터를 통과했다. `always_comb`의 constant-select 관련 진단은 sensitivity에 모든 비트를 포함한다는 구현 안내이며, 관찰된 결과 불일치는 없었다. 이 기록은 유한한 벡터 RTL 시뮬레이션이다. 합성 후 timing·자원·모든 입력의 formal proof를 완료했다는 뜻은 아니다.

실제 DSP에서는 누산기의 최악 범위, 각 단계의 스케일, overflow flag와 입력 분포를 함께 정해야 한다. 파이프라인을 추가하면 valid와 데이터 latency도 맞춰야 한다. 단순히 출력 폭을 넓히는 것과 정수 범위·정밀도를 어떻게 나누는지는 별개다.

## English

### A stored integer with an agreed scale

With eight fractional bits, raw integer 256 represents one. The same bit pattern means a different number under another scale. A fixed-point multiplication is therefore specified by signedness, fractional bits, intermediate width, rounding and overflow handling together.

Both inputs here are signed 16-bit integers interpreted as a/256 and b/256. Their represented range is −128 through 127.99609375 with spacing 1/256. Q-format conventions differ on whether the sign counts among integer bits, so the width and interpretation are stated explicitly. Ties-to-even is checked against [AMD UG1399](https://docs.amd.com/r/2021.1-English/ug1399-vitis-hls/Quantization-Modes) and [MathWorks rounding documentation](https://www.mathworks.com/help/fixedpoint/ug/rounding.html).

### Derivation and edge cases

The exact product is ab/65536. To return eight fractional bits, the raw product must be divided by 256, rounded to nearest with ties to even, then saturated to the signed 16-bit range. A full signed 16×16 product fits in signed 32 bits. Widening a value after prematurely truncating it cannot recover lost bits. The RTL keeps the complete product and uses a wider signed value until saturation is decided.

For the nonnegative magnitude, divide by 256 into quotient q and remainder r. Increment q when r exceeds 128, or when r equals 128 and q is odd. Restore the original sign afterward. Thus 0.5 and −0.5 round to zero, while 1.5 and −1.5 round to 2 and −2. An arithmetic right shift of a negative product instead behaves like downward rounding and is not this policy.

Saturation clamps raw output to −32768…32767. It prevents wrap-around sign reversals but still distorts the signal. If the exact result is within range and no saturation occurs, rounding error is at most half an output step, or 1/512 in represented units. This bound does not apply to saturated results.

### Independent model and real RTL execution

The commands above run the demo, Python tests and RTL comparisons. The implementation uses integer division and remainders; its independent oracle rounds the exact rational `Fraction(a*b,256)`. Tests compare 10000 random pairs and explicit tie, sign and overflow cases. The RTL runner separately generates 121 boundary pairs plus 10000 random pairs, writes temporary hexadecimal vectors and checks all 10121 outputs after Icarus compilation and vvp execution.

Icarus 12.0 passed those 10121 vectors. Its constant-select diagnostic for `always_comb` reports that all bits are included in sensitivity; no output mismatch was observed. This is finite-vector RTL simulation, not synthesis, timing closure, resource characterization or an all-input formal proof.

For a DSP pipeline, also derive accumulator bounds, stage scales, overflow flags and data distributions. Added pipeline stages require matching valid latency to the data. Increasing total width and deciding how much of that width represents range versus precision remain separate decisions.

## 출처 / Sources

- AMD, *UG1399 Quantization Modes*: convergent rounding and explicit tie examples.
- MathWorks, *Rounding Modes*: round-to-nearest policies and fixed-point interpretation. Links are attached above.
