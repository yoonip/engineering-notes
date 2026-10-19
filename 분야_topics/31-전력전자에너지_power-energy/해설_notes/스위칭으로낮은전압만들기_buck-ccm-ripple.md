# 스위칭으로 낮은 전압 만들기: buck의 CCM과 ripple

[전력과 에너지](../README.md) · [참조 모델](../../../예제_examples/확장기초_extended/hardware/models.py) · [검산](../../../예제_examples/확장기초_extended/hardware/test_models.py)

## 한국어

### 스위치를 꺼도 전류가 계속 흐르는 이유

Buck converter는 입력 전압을 스위칭하고 인덕터·커패시터로 평활해 낮은 DC 전압을 만든다. 인덕터 전류는 순간적으로 바뀔 수 없으므로 switch가 꺼진 구간에도 diode 또는 동기식 하단 MOSFET을 통한 전류 경로가 필요하다. 여기서는 주기 정상상태, 이상적인 switch·diode, 일정한 입력, 작은 출력 ripple, 양의 inductor current가 한 주기 내내 유지되는 CCM을 가정한다. [TI SLVA057의 CCM 해석](https://www.ti.com/lit/an/slva057/slva057.pdf)

기호는 입력 $V_{in}$, 평균 출력 $V_o$, 인덕턴스 L(H), 출력 C(F), 주파수 $f_s$(Hz), 주기 $T_s=1/f_s$, duty $D=t_{on}/T_s$, 평균 부하전류 $I_o$다. 출력 capacitor의 한 주기 평균 전류가 0이므로 평균 inductor current도 $I_o$다.

### Volt-second balance에서 변환비 유도

On 구간의 인덕터 전압은 $V_{in}-V_o$, off 구간은 $-V_o$다. $v_L=L\,di_L/dt$를 한 주기 적분하고 정상상태의 $i_L(T_s)=i_L(0)$를 사용하면

$$0=(V_{in}-V_o)DT_s-V_o(1-D)T_s,\qquad V_o=DV_{in}.$$

따라서 peak-to-peak 전류 ripple은

$$\Delta I_L=\frac{(V_{in}-V_o)D}{Lf_s}
=\frac{V_o(1-D)}{Lf_s},\quad
I_{min}=I_o-\Delta I_L/2,\quad I_{max}=I_o+\Delta I_L/2.$$

이 양의 CCM 모델은 $I_o>\Delta I_L/2$에서 적용한다. Diode 방식에서 전류가 0에 닿아 머무르면 DCM이고 단순 $V_o=DV_{in}$ 관계를 그대로 유지할 수 없다. 강제 PWM 동기식 구조는 음의 전류도 허용할 수 있어 diode의 DCM과 동작을 구분한다.

실제 손실은 switch 저항·diode 전압·인덕터 DCR 등으로 전압 균형에 들어간다. 효율 하나를 duty의 정확한 보정식으로 일반화하지 않는다. TI의 power-stage 계산 자료도 부품의 제한과 권장 L/C 범위를 함께 보도록 한다. 열람한 URL의 실제 본문은 2026-09 개정 SLVA477C다. [TI SLVA477](https://www.ti.com/lit/an/slva477b/slva477b.pdf)

### 전류 삼각형이 출력 전압에 남기는 흔적

부하가 주기 내 거의 일정하면 $i_C=i_L-I_o$는 평균 0인 삼각파다. 양의 전류 부분은 밑변 $T_s/2$, 높이 $\Delta I_L/2$인 삼각형이므로 전하 변화가 $\Delta Q=\Delta I_LT_s/8$이다. 따라서 ideal capacitor의 전압 ripple은

$$\Delta V_{C,pp}\approx\frac{\Delta I_L}{8f_sC},\qquad
\Delta V_{ESR,pp}=ESR\,\Delta I_L.$$

두 성분의 최대·최소 시점은 다를 수 있다. 합은 보수적인 간단 추정에 쓸 수 있지만 정확한 파형의 peak-to-peak 합이라고 단정하지 않는다. ESL, switching spike, control-loop transient는 이 두 식 밖이다. [ADI MAXREFDES1269, Step 6의 출력 ripple 식](https://www.analog.com/media/en/reference-design-documentation/reference-designs/maxrefdes1269.pdf)

$V_{in}=12$ V, $V_o=3.3$ V, L=10 µH, $f_s=500$ kHz, C=22 µF, $I_o=2$ A이면 D=0.275, $\Delta I_L=0.4785$ A, $I_{min}=1.76075$ A, $I_{max}=2.23925$ A다. C만의 ripple은 약 5.44 mV다. C의 유효값과 부품 정격을 이상값과 구분한다.

### 구현과 독립 검증

`buck_ccm`은 이 이상적 정상상태 식을 계산하고 양의 CCM이 아니면 결과를 거부한다. 테스트는 on/off 전압의 시간 적분이 0인지 확인한다. 이어 전류 삼각파를 별도로 촘촘히 적분해 capacitor 전압의 최대·최소 차이를 구하고 $\Delta I_L/(8f_sC)$와 비교한다. 따라서 ripple 식을 그대로 다시 평가하는 검사가 아니다.

실제 설계의 다음 단계는 부품 모델·동작 모드·보상 조건을 고정한 switching simulation이다. 입력·부하·온도 범위를 sweep하고 $i_L$, switch-node 전압과 출력 ripple, startup·load step, 안정성을 각각 확인한다. 인덕터 saturation current와 peak current limit, RMS 발열, capacitor DC bias도 검토한다. 측정에서는 probe loop와 대역폭 조건을 명시해 switching spike와 저주파 ripple을 분리한다. Python의 전하 균형 검사는 controller 안정성이나 실제 power-stage 효율의 검증 결과가 아니다.

## English

### Current continues when the switch turns off

A buck converter switches its input and smooths the result through an inductor and capacitor. Inductor current cannot change instantaneously, so the off interval needs a diode or synchronous low-side MOSFET path. Assume periodic steady state, ideal switches/diode, constant input, small output ripple and positive inductor current throughout the cycle. [TI SLVA057 CCM analysis](https://www.ti.com/lit/an/slva057/slva057.pdf)

Define $V_{in}$, mean output $V_o$, inductance L in H, capacitance C in F, switching frequency $f_s$ in Hz, $T_s=1/f_s$, duty $D=t_{on}/T_s$ and mean load $I_o$. Zero average capacitor current requires mean inductor current $I_o$.

### Volt-second balance

Inductor voltage is $V_{in}-V_o$ while on and $-V_o$ while off. Integrating $v_L=L\,di_L/dt$ over a periodic cycle gives

$$0=(V_{in}-V_o)DT_s-V_o(1-D)T_s,\quad V_o=DV_{in}.$$

Consequently

$$\Delta I_L=(V_{in}-V_o)D/(Lf_s)=V_o(1-D)/(Lf_s),\quad
I_{min,max}=I_o\mp\Delta I_L/2.$$

Positive CCM requires $I_o>\Delta I_L/2$. A diode converter entering a zero-current interval operates in DCM and no longer generally follows the same conversion ratio. Forced-PWM synchronous designs may allow negative current, which differs from diode DCM.

Real switch resistance, diode drop and inductor DCR modify voltage balance. A single efficiency factor is not a universally exact duty correction. TI's sizing guidance also requires component limits and recommended L/C ranges. The inspected file at the linked URL is the September 2026 SLVA477C revision. [TI SLVA477](https://www.ti.com/lit/an/slva477b/slva477b.pdf)

### From triangular current to output ripple

For nearly constant load within a cycle, $i_C=i_L-I_o$ is a zero-mean triangle. Its positive area has base $T_s/2$ and height $\Delta I_L/2$, giving $\Delta Q=\Delta I_LT_s/8$. Thus

$$\Delta V_{C,pp}\approx\Delta I_L/(8f_sC),\quad
\Delta V_{ESR,pp}=ESR\,\Delta I_L.$$

These components need not reach extrema simultaneously. Their sum is a conservative simple estimate rather than an exact general peak-to-peak waveform identity. ESL, switching spikes and feedback transients require additional models. [ADI MAXREFDES1269, Step 6](https://www.analog.com/media/en/reference-design-documentation/reference-designs/maxrefdes1269.pdf)

For 12 V to 3.3 V, L=10 µH, $f_s=500$ kHz, C=22 µF and $I_o=2$ A, duty is 0.275, current ripple 0.4785 A, minimum 1.76075 A and maximum 2.23925 A. Ideal capacitive voltage ripple is about 5.44 mV. Effective capacitance and real ratings must be checked separately.

### Implementation and verification

`buck_ccm` evaluates this ideal steady-state model and rejects cases outside positive CCM. Tests independently check zero net inductor volt-seconds, then numerically integrate a separately constructed triangular capacitor current and compare its voltage range with the ripple formula.

Actual design verification additionally fixes device models, control mode and compensation, then sweeps input/load/temperature in switching simulation. Inspect inductor current, switch-node voltage, ripple, startup, load steps and stability separately; check saturation/peak limits, RMS heating and capacitor bias. Measurement bandwidth and probe-loop geometry must distinguish switching spikes from ripple. Python charge-balance checks do not establish controller stability or physical efficiency.

## 출처 대조 / Source cross-check

TI의 CCM·부품 산정 자료와 ADI의 실제 buck 설계 절차를 대조하고 이상 모델의 전하·전압 균형을 독립 계산했다. / TI's CCM analysis and ADI's design procedure were cross-checked; the ideal model was independently checked by charge and voltage balance. 확인 / checked: 2026-10-19.
