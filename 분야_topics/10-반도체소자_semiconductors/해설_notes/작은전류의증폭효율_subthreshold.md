# 작은 전류의 증폭 효율: subthreshold와 gm/Id

[반도체 소자 목차](../README.md) · [참조모델](../../../예제_examples/심화_advanced/hardware/models.py) · [검산](../../../예제_examples/심화_advanced/hardware/test_models.py)

## 한국어

### 문턱 아래에서도 전류는 흐릅니다

MOSFET을 스위치로 배울 때는 문턱전압 아래를 꺼짐이라고 부릅니다. 실제로는 전류가 갑자기 0이 되지 않습니다. 물이 넘치는 높은 둑을 생각하면, 물 높이가 조금만 달라져도 둑을 넘어갈 수 있는 입자의 비율이 크게 달라지는 모습과 비슷합니다. 약한 반전에서는 이 변화가 대략 지수함수로 나타납니다. 작은 전류로 큰 상대적 전류 변화를 만들 수 있어 저전력 아날로그 설계에서 중요합니다. [MIT 6.012 Lecture 12](https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-fall-2009/282ca336565ffdd1aeda1c212c3b0696_MIT6_012F09_lec12.pdf)의 weak-inversion 모델이 출발점입니다.

여기서 $`V_{th}`$는 문턱전압이고, $`U_T=kT/q`$는 열전압입니다. 둘은 전혀 다른 양입니다. 300 K에서 열전압은 약 25.85 mV입니다. n은 slope factor, $`I_0`$는 이 단순 모델의 전류 스케일입니다. 소스·몸체 조건과 온도를 고정하고, drain 전압은 비음수로 둡니다.

### 지수함수에서 gm/Id와 subthreshold slope까지

```math
I_D=I_0\exp\left(\frac{V_{GS}-V_{th}}{nU_T}\right)
\left[1-\exp\left(-\frac{V_{DS}}{U_T}\right)\right].
```

drain 항은 $`V_{DS}=0`$에서 전류를 0으로 만들고, $`V_{DS}\gg U_T`$에서는 1에 가까워집니다. 이 포화는 강한 반전의 square-law 포화 조건과 같은 식을 뜻하지 않습니다. $`V_{DS}`$, 온도와 모델 매개변수를 고정한 채 gate 전압으로 미분하면 다음을 얻습니다. gm/Id 비는 $`I_D>0`$인 동작점에서 정의합니다.

```math
g_m=\frac{\partial I_D}{\partial V_{GS}}=\frac{I_D}{nU_T},
\qquad \frac{g_m}{I_D}=\frac{1}{nU_T}.
```

$`g_m`$은 A/V, $`g_m/I_D`$는 1/V입니다. 전류 한 단위당 gate가 전류를 얼마나 잘 조절하는지 나타냅니다. $`\log_{10}`$를 취한 뒤 전압으로 미분하면 한 decade, 즉 전류 10배에 필요한 gate 전압을 얻습니다.

```math
S=\frac{dV_{GS}}{d\log_{10}I_D}=nU_T\ln 10.
```

n=1.5, 300 K에서는 $`g_m/I_D\approx25.79\ \mathrm{V}^{-1}`$, $`S\approx89.3\ \mathrm{mV/dec}`$입니다. 같은 조건에서 gate 전압을 89.3 mV 높이면 전류가 10배가 됩니다. n=1의 약 59.5 mV/dec는 이 열적 모델의 300 K 기준값이며 모든 소자 기술의 보편적 한계라는 뜻은 아닙니다. [CERN Indico에 공개된 Valerio Re의 INFIERI 강의](https://indico.cern.ch/event/850479/contributions/3718283/attachments/2297665/3907771/Re_INFIERI_2021.pdf) 24쪽의 전류 효율 식과 의미를 교차 확인합니다.

### 전류 효율이 높으면 항상 좋습니까

| 양 | 이 단순 모델이 보여 주는 것 | 별도로 확인할 것 |
|---|---|---|
| gm/Id | 약한 반전의 높은 상대 민감도 | 입력 용량과 실제 대역폭 |
| S | gate 전압당 전류 비율 | DIBL, trap, body bias |
| 온도 | 열전압 증가와 비례 관계 | I0·Vth·n의 온도 변화 |
| drain 전압 | 작은 VDS의 전류 감소 | 출력 저항·단채널 효과 |

같은 전류에서 gm이 커도 대역폭, 잡음, 면적, mismatch까지 자동으로 좋아지지는 않습니다. 실제 gm/Id 설계는 PDK의 동작점 데이터를 전류 밀도와 길이에 따라 훑고, gm/gds·fT·용량을 함께 비교합니다. 본 모델에서 온도만 바꾸고 I0와 Vth를 고정한 실험은 식의 민감도를 보는 것이며 실제 소자의 온도별 drain current 예측이 아닙니다.

### 구현과 검증

`weak_inversion()`은 drain 항에 `expm1`을 사용합니다. 매우 작은 x에서 `1-exp(-x)`를 직접 계산할 때 생기는 상쇄 오차를 줄이기 위해서입니다. 다음 명령은 전류 비율과 미분을 확인합니다.

```bash
python demo.py --case subthreshold
python -m unittest -v test_models.HardwareModels.test_weak_inversion_gm_derivative test_models.HardwareModels.test_subthreshold_decade_and_drain_zero
```

중앙 차분으로 구한 gm/Id를 해석식과 비교하고, S만큼 전압을 올렸을 때 10배가 되는지, VDS=0이면 0인지 확인합니다. 차분 간격을 너무 작게 하면 부동소수점 소거 오차가, 너무 크게 하면 미분 근사 오차가 늘어납니다. 실제 소자 검증에는 충분히 낮은 누설 측정 한계, SMU compliance, 안정된 온도, body 연결과 VDS 조건 기록이 필요합니다. 이 저장소의 결과는 수식·수치 모델 검산이며 소자 측정치는 아닙니다.

## English

### Current below the nominal threshold

The switch abstraction calls a MOSFET off below threshold, but current does not abruptly become zero. In weak inversion, a modest change in the barrier changes the fraction of carriers crossing it exponentially. This yields high relative current sensitivity at low current and matters in low-power analog circuits. The starting model is the weak-inversion treatment in [MIT 6.012 Lecture 12](https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-fall-2009/282ca336565ffdd1aeda1c212c3b0696_MIT6_012F09_lec12.pdf).

Distinguish threshold voltage $`V_{th}`$ from thermal voltage $`U_T=kT/q`$: the latter is about 25.85 mV at 300 K. n is the slope factor and I0 is the current scale of this simplified model. Source/body conditions, temperature and other parameters are fixed; drain voltage is nonnegative.

### Deriving current efficiency and slope

The displayed current equation contains an exponential gate factor and the drain factor $`1-\exp(-V_{DS}/U_T)`$. The drain factor gives zero current at zero drain voltage and approaches one for drain voltages much larger than thermal voltage. This saturation statement is not the strong-inversion square-law saturation condition.

Differentiating with respect to gate voltage at fixed drain voltage and parameters gives $`g_m=I_D/(nU_T)`$, hence $`g_m/I_D=1/(nU_T)`$ at operating points with $`I_D>0`$. The units are A/V and 1/V respectively. Taking a base-10 logarithm gives the voltage required per current decade: $`S=nU_T\ln10`$.

At n=1.5 and 300 K, gm/Id is approximately 25.79 per volt and S is 89.3 mV/decade. Raising gate voltage by S multiplies current by ten within the model. The approximately 59.5 mV/decade value at n=1 is a reference for this thermal model at 300 K, not a statement covering every device technology. Page 24 of [Valerio Re's INFIERI lecture hosted by CERN Indico](https://indico.cern.ch/event/850479/contributions/3718283/attachments/2297665/3907771/Re_INFIERI_2021.pdf) independently checks the current-efficiency expression.

### What efficiency does and does not imply

High gm/Id alone does not guarantee better bandwidth, noise, area or mismatch. Input capacitance, output conductance, DIBL, traps and body bias require additional characterization. Practical gm/Id design uses PDK operating-point sweeps across current density and channel length, with gm/gds, fT and capacitance examined together. Varying temperature while keeping I0, Vth and n fixed explores the formula's sensitivity; it is not a prediction of a real device's temperature-dependent current.

### Implementation and independent checks

Run the two tests above or `python demo.py --case subthreshold` in the linked example directory. The implementation uses `expm1` to avoid subtractive cancellation in the small-drain-voltage factor. Central differences independently check the analytic gm/Id, a gate increment of S must yield a tenfold current ratio, and zero drain voltage must give zero current. Excessively small difference steps suffer roundoff; large steps introduce derivative approximation error.

Physical characterization additionally needs adequate current resolution, SMU compliance, controlled temperature and recorded body and drain conditions. The provided results verify equations and numerical behavior; they are not device measurements.

## 출처 / Sources

- MIT, *6.012 Lecture 12*: weak-inversion exponential current and thermal voltage.
- Valerio Re, *INFIERI 2021*, p.24, CERN Indico: weak-inversion gm/Id and current efficiency. Source links are attached to the relevant sections.
