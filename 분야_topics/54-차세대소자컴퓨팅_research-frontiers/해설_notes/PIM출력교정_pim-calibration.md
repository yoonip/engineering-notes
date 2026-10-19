# PIM 출력 교정: gain·offset을 고칠 수 있는 범위

[차세대 소자·컴퓨팅 목차](../README.md) · [모델](../../../예제_examples/심화_advanced/hardware/models.py) · [검산](../../../예제_examples/심화_advanced/hardware/test_models.py)

## 한국어

### 계산이 조금 크게 나오는 경우와 휘어지는 경우

analog PIM의 column 출력이 이상적인 dot product의 0.9배에 offset을 더한 값이라면 직선 교정으로 보정할 수 있다. 반면 작은 입력과 큰 입력에서 오차 비율이 다르면 직선 하나로 고칠 수 없다. 교정이 효과적인지 보려면 맞추는 데 쓴 데이터와 다른 입력에서 결과를 확인해야 한다. calibration data를 잘 맞춘다는 사실은 일반 입력의 정확도와 다르다.

[IBM의 analog AI 하드웨어 설명](https://research.ibm.com/blog/the-hardware-behind-analog-ai)은 conductance 기반 계산과 주변 회로를 설명한다. [NIST hardware accelerator 연구](https://www.nist.gov/programs-projects/hardware-accelerators-neural-networks)는 소자 variability와 hardware-aware 평가의 필요성을 다룬다. 이 글은 그런 장치의 실제 측정 데이터를 사용하지 않고, 무엇이 교정 가능한 오차인지 분리한 수치 모델을 쓴다.

### 이상적인 전류와 column별 오차

한 column의 이상적인 전류는 $`I_j^*=\sum_iG_{ji}V_i`$다. G를 S, V를 V로 쓰면 I는 A다. signed weight의 차분 구현을 이미 유효 G로 묶었거나 수학적으로 signed 행렬을 다룬다고 가정한다. 실제 음의 conductance 소자가 있다는 뜻은 아니다.

```math
I_j^{meas}=g_j I_j^*+o_j+\eta_j,\qquad
I_j^{corr}=\frac{I_j^{meas}-\hat o_j}{\hat g_j}.
```

gj는 무차원 gain, oj는 A 단위 offset, ηj는 noise다. 선형·시간 불변이고 gain이 0이 아니며 calibration과 실제 입력 범위가 맞는다고 가정한다. 알려진 전류 수준 x를 여러 개 넣고 측정 y에 직선을 맞추면 slope가 gain, intercept가 offset이다. 참조모델은 [직선 교정 글](../../37-센서계측_sensors-instrumentation/해설_notes/직선교정의불확도_linear-calibration.md)의 OLS를 공유한다.

### holdout에서 확인하는 affine 보정

예제는 이상 전류 수준 −2,−1,0,1,2의 normalized 값을 사용해 두 column의 gain 0.8·1.2와 offset 0.1·−0.2를 추정한다. 그 후 calibration에 없던 voltage vector [0.2,−0.4]와 행렬 [[1,−2],[0.5,3]]을 계산한다. 이상 출력은 [1,−1.1]이다. noise 없는 정확한 affine 모델에서는 보정 출력이 이 값과 일치해야 한다. 수치 예의 normalized 단위를 실제 A 단위 측정값으로 오해하지 않는다.

### 비선형 오차를 숨기지 않는 반례

측정값이 다음처럼 cubic 성분을 가진다고 하자.

```math
y=2x+0.4x^3.
```

calibration 입력 [−1,0,1]에서는 slope 2.4, offset 0인 직선이 세 점을 정확하게 지난다. 그런데 holdout x=0.5에서는 y=1.05이고, 직선 역교정값은 1.05/2.4=0.4375다. 실제 0.5와 −0.0625만큼 다르다. calibration residual이 0이라는 결과만 보면 이 실패를 놓친다.

| 오차 | column affine 교정의 범위 |
|---|---|
| 일정 gain·offset | 모델 가정 안에서 보정 가능 |
| 독립 noise | 평균 편향을 줄여도 분산은 남음 |
| 입력 크기에 따른 비선형성 | 직선 하나로 일반 보정 불가 |
| 입력 패턴별 IR drop | 같은 이상 내적이어도 오차가 달라질 수 있음 |
| ADC·DAC clipping | 잃어버린 정보는 역변환으로 복원 불가 |
| 시간·온도 drift | 교정 상태의 유효기간·범위 필요 |

### 구현, 검산과 장치 적용

```bash
python demo.py --case pim
python -m unittest -v test_models.HardwareModels.test_pim_heldout_affine_recovery test_models.HardwareModels.test_pim_nonlinearity_not_repaired
```

첫 테스트는 따로 추정한 column별 직선으로 새로운 vector의 dot product를 복원한다. 두 번째는 위 cubic 모델에서 정확히 0.4375가 나오는 실패 사례를 확인한다. “교정했으니 정확하다”가 아니라 성립하는 오차 모델과 실패하는 모델을 함께 실행한다.

실제 장치는 conductance programming·read bias·온도·시간을 기록하고, calibration 전후의 holdout 분포와 최대 오차·RMS 오차를 비교해야 한다. 서로 다른 input sparsity와 부호 패턴도 필요하다. 보정 연산의 디지털 비용, ADC 범위와 양자화, gain 추정 불확도까지 포함해야 시스템 효율을 판단할 수 있다. 여기서는 Python 모델만 실행했으며 RRAM·PCM array, ADC 또는 accelerator에서 교정 실험을 했다는 의미는 아니다.

## English

### Gain error differs from a curved response

A column output equal to a constant gain times the ideal dot product plus an offset can be corrected by a line. If the error ratio changes with input level, one line cannot generally fix it. Evaluation must therefore include inputs separate from those used for calibration. A perfect training fit is not evidence of accuracy for every input.

[IBM's analog AI hardware article](https://research.ibm.com/blog/the-hardware-behind-analog-ai) explains conductance-based computation and surrounding circuitry. [NIST's accelerator research](https://www.nist.gov/programs-projects/hardware-accelerators-neural-networks) independently addresses device variability and hardware-aware assessment. The example below uses constructed numerical data rather than device measurements.

### Deriving column-wise correction

Ideal current is $`I_j^*=\sum_iG_{ji}V_i`$, in amperes when conductance and voltage use siemens and volts. Signed entries stand for effective differential encoding or an abstract signed matrix, not physically negative conductances. Model measured current as $`g_jI_j^*+o_j+\eta_j`$, with dimensionless gain, current offset and noise. Estimate gain and offset from known reference levels, then correct by subtracting offset and dividing by gain.

Assume linear, time-invariant behavior, nonzero gain and a representative calibration range. The implementation shares OLS with the linked linear-calibration article, whose uncertainty assumptions still apply.

### Affine recovery on held-out data

Fit two columns using normalized ideal levels [−2,−1,0,1,2], gains 0.8 and 1.2 and offsets 0.1 and −0.2. Then evaluate a new voltage vector [0.2,−0.4] with matrix rows [1,−2] and [0.5,3]. Ideal outputs are [1,−1.1]. In a noiseless exact affine model, correction must recover these values. The normalized example numbers are not reported physical current measurements.

### A nonlinear counterexample

For $`y=2x+0.4x^3`$, reference levels −1,0,1 lie exactly on a line of slope 2.4 and zero intercept. At the new level x=0.5, however, y=1.05 and inverse-line correction gives 0.4375 instead of 0.5. Zero calibration residual therefore hides a −0.0625 holdout error.

Constant gain and offset are correctable under the model. Noise variance remains, input-dependent nonlinearity is not generally removed, and pattern-dependent IR drop may produce different errors for identical ideal dot products. Clipping loses information that an affine inverse cannot recover. Drift limits a calibration's valid time and temperature range.

### Executable and physical evaluation

The commands above verify exact affine recovery on a held-out vector and the explicitly calculated nonlinear failure. They test both a successful error model and a model outside the correction's scope.

Physical experiments must record programming, read bias, temperature and elapsed time, then compare pre/post-correction holdout distributions, worst-case and RMS error across input sparsity and signs. Digital correction cost, converter range, quantization and fitted-parameter uncertainty belong in system efficiency accounting. Only Python reference models were executed here; no RRAM/PCM array or accelerator calibration is reported.

## 출처 / Sources

- IBM Research, *The hardware behind analog AI*: conductance computation and peripheral implementation.
- NIST, *Hardware Accelerators for Neural Networks*: variability and hardware-aware validation. Source links appear above.
