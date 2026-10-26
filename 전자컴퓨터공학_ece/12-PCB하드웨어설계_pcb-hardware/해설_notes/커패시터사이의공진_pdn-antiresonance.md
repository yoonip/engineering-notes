# 커패시터를 더 달았는데 왜 전원 임피던스가 커질까요

[PCB·하드웨어 목차](../README.md) · [실행 코드](../../../예제_examples/심화_advanced/hardware/models.py) · [검산](../../../예제_examples/심화_advanced/hardware/test_models.py)

## 한국어

### 큰 용량 하나와 작은 용량 하나

이상적인 커패시터는 주파수가 높을수록 임피던스가 작아집니다. 실제 부품과 배선에는 저항과 인덕턴스가 있어서, 충분히 높은 주파수에서는 오히려 인덕터처럼 동작합니다. 서로 다른 커패시터를 병렬로 놓으면 한쪽은 인덕터, 다른 쪽은 커패시터처럼 보이는 구간이 생깁니다. 두 가지의 전류가 서로 상쇄되면 외부에서 보이는 전체 전류는 작아지고 임피던스는 커집니다. 이것이 antiresonance를 이해하는 출발점입니다.

[ADI MT-101](https://www.analog.com/media/en/training-seminars/tutorials/MT-101.pdf)은 ESR·ESL을 포함한 decoupling 모델을 설명합니다. [AVX의 *Introduction to Choosing MLC Capacitors for Bypass/Decoupling Applications*](https://www.kyocera-avx.com/docs/techinfo/DecouplingLowInductance/mlcbypas.pdf)은 서로 다른 커패시터와 연결 인덕턴스가 만드는 주파수 응답을 다룹니다. 후자는 KYOCERA AVX에서 공개한 Yun Chase의 기술 문서입니다. pp. 7–8의 antiresonance와 연결 인덕턴스 설명을 참고합니다.

### 두 가지 RLC를 병렬로 놓은 모델

각 가지가 같은 전원 노드와 같은 이상 접지 사이에 연결되고 서로의 상호 인덕턴스가 없다고 가정합니다. C는 F, L은 H, R은 Ω, ω는 rad/s입니다. R에는 해당 가지의 ESR과 등가 직렬 손실, L에는 부품·비아·연결의 등가 인덕턴스를 묶습니다.

```math
Z_k=R_k+j\left(\omega L_k-\frac{1}{\omega C_k}\right),
\qquad Z_{PDN}=\left(\frac{1}{Z_1}+\frac{1}{Z_2}\right)^{-1}.
```

가지 하나의 self-resonance에서는 $`\omega L=1/(\omega C)`$라서 Z가 R까지 내려갑니다. 반대로 두 가지 병렬 연결의 무손실 antiresonance는 전체 admittance가 0인 점입니다. R=0을 두고 $`X_k=\omega L_k-1/(\omega C_k)`$라 쓰면 다음 순서로 나옵니다.

```math
Y=\frac{1}{jX_1}+\frac{1}{jX_2}=0
\Rightarrow X_1+X_2=0
\Rightarrow \omega_{ar}^2=\frac{1/C_1+1/C_2}{L_1+L_2}.
```

이 유도는 각 X가 0이 아닌 구간에서 성립합니다. 두 self-resonance가 겹치는 퇴화 사례에는 이 식을 임피던스 발산점으로 적용하지 않습니다. 유한한 ESR이 있으면 peak는 유한해지고 최대점 위치도 달라질 수 있습니다. 따라서 위 식을 손실이 있는 PDN의 정확한 최대점 주파수로 부르지 않습니다.

### 수치 예와 해석

C1=1 μF, C2=0.1 μF, L1=L2=1 nH이면 self-resonance는 약 5.03 MHz와 15.92 MHz, 무손실 antiresonance 기준은 약 11.80 MHz입니다. 그 사이에서 첫 가지의 reactance는 양수, 두 번째는 음수입니다. 저항이 작을수록 가지 사이의 순환 전류에 비해 외부 공급 전류가 작아지는 peak가 뚜렷해질 수 있습니다.

| 변경 | 모델에서 확인할 것 | 실제 해석에 필요한 추가 조건 |
|---|---|---|
| C 추가 | admittance 합과 peak 이동 | DC bias에 따른 실효 용량 |
| ESR 증가 | peak 완화와 저주파 손실 | 발열·전압 강하·소자 허용값 |
| 비아·배선 변경 | 등가 L 변화 | 공통 인덕턴스·return 경로 |
| regulator 추가 | 저주파 출력 임피던스 | 제어 루프와 부하 안정성 |

“용량은 많을수록 좋다”는 규칙 대신, 필요한 주파수 범위에서 목표 임피던스를 만족하는지 확인합니다. $`Z_{target}=\Delta V/\Delta I`$는 부하 변화와 허용 전압 오차에서 얻는 설계 기준이며, 비선형 시간 응답까지 완전히 규정하지 않습니다.

### 구현과 독립 검증

```bash
python demo.py --case pdn
python -m unittest -v test_models.HardwareModels.test_pdn_antiresonance_and_loss test_models.HardwareModels.test_pdn_branch_kcl
```

코드는 복소수로 가지별 Z를 만든 뒤 admittance를 합합니다. 검산에서는 손으로 구한 무손실 주파수에서 susceptance 합이 0인지 확인합니다. ESR=0.01 Ω을 넣은 모델은 유한하고 실수부가 양수여야 합니다. 또 전체 1 A 입력을 가정하고 각 가지 전류를 별도로 구해 그 합이 1 A인지 확인합니다.

실제 PCB에서는 공통 via·plane의 결합, package·die 임피던스, regulator, 여러 부하 위치 때문에 이 두 가지 모델만으로 충분하지 않습니다. 부품의 DC-bias·온도 특성, S-parameter 모델, 추출된 interconnect를 사용하고, VNA 측정에서는 fixture와 포트 기준면을 보정해야 합니다. 여기에 실린 수치는 두 RLC 참조모델의 계산이며 PCB 임피던스 측정 결과는 아닙니다.

## English

### Why two capacitors can create a peak

An ideal capacitor becomes less impedant as frequency rises. A physical capacitor and its connection also contain resistance and inductance, eventually producing inductive behavior. With unlike capacitors in parallel, one branch may be inductive while the other remains capacitive. Their currents can cancel at the input, reducing total admittance and increasing the impedance seen by the load.

[ADI MT-101](https://www.analog.com/media/en/training-seminars/tutorials/MT-101.pdf) establishes the ESR/ESL decoupling model. [AVX's *Introduction to Choosing MLC Capacitors for Bypass/Decoupling Applications*](https://www.kyocera-avx.com/docs/techinfo/DecouplingLowInductance/mlcbypas.pdf), by Yun Chase, discusses interactions among capacitors and connection inductance. The latter is available from KYOCERA AVX; pp. 7–8 discuss antiresonance and connection inductance.

### Deriving the two-branch model

Each series RLC branch connects the same ideal power and ground nodes, with mutual inductance excluded. R combines series losses; L combines component and connection inductance. Units are Ω, H, F and rad/s. The branch impedances and parallel combination are displayed above.

An individual branch reaches series resonance when its inductive and capacitive reactances cancel, leaving R. To derive a parallel antiresonance reference, set both resistances to zero and define branch reactances X1 and X2. Zero total admittance requires $`1/(jX_1)+1/(jX_2)=0`$, hence $`X_1+X_2=0`$. Rearrangement gives $`\omega_{ar}^2=(1/C_1+1/C_2)/(L_1+L_2)`$.

This derivation requires nonzero individual reactances and does not identify an impedance pole when both self-resonances coincide. Finite ESR limits the peak and can shift its maximum; the lossless formula is not an exact peak-frequency formula for a lossy network.

### Numerical interpretation

For 1 μF and 0.1 μF with 1 nH in each branch, self-resonances are approximately 5.03 and 15.92 MHz; the lossless antiresonance reference is about 11.80 MHz. Between the self-resonances, one branch has positive reactance and the other negative reactance. Smaller losses can make their circulating-current effect more pronounced.

Adding capacitance changes the admittance sum and peak positions; DC bias also changes physical capacitance. Increasing ESR can damp a peak but adds loss and possible voltage drop. Via and routing changes alter inductance and the return path. Including a regulator adds its control-loop-dependent output impedance. Instead of assuming that more capacitance is always better, compare impedance over the relevant band with a target derived from $`\Delta V/\Delta I`$. That target alone does not specify the complete nonlinear transient response.

### Implementation, checks and application limits

The commands above run the complex-impedance model and two independent checks. The lossless analytic reference must give zero summed susceptance. Adding 0.01 Ω ESR must produce a finite impedance with positive real part. Computing individual branch currents under a unit input current must satisfy KCL independently of the impedance-combination expression.

A PCB also contains common via and plane inductance, package and die impedances, regulator dynamics and spatially separated loads. Use bias- and temperature-dependent component models, S-parameters and extracted interconnect where needed. VNA measurements require fixture and reference-plane correction. These numerical examples describe a two-RLC reference model, not measured PCB impedance.

## 출처 / Sources

- Analog Devices, *MT-101*, Rev. 0 (March 2009), pp. 2–4: ESR/ESL and decoupling behavior.
- AVX, Yun Chase, *Introduction to Choosing MLC Capacitors for Bypass/Decoupling Applications*, manufacturer-hosted original, pp. 7–8: capacitor interactions and connection parasitics. Links are given above.
