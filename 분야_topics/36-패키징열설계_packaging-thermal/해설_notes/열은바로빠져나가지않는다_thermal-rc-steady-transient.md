# 열은 바로 빠져나가지 않는다: thermal RC와 과도 온도

[Packaging과 열](../README.md) · [참조 모델](../../../예제_examples/확장기초_extended/hardware/models.py) · [검산](../../../예제_examples/확장기초_extended/hardware/test_models.py)

## 한국어

### 같은 평균 전력인데 peak 온도가 다른 이유

발열 5 W를 계속 내는 것과 짧게 켰다가 끄는 것은 온도 파형이 다르다. 열이 외부로 이동하는 데 저항이 있고 물체가 열을 저장하기 때문이다. 전기 회로에서 voltage·current·capacitance를 쓰듯 thermal 모델에서는 온도·열유량·열용량을 쓸 수 있다. TI의 thermal dynamics 설명도 정상 열저항만으로는 즉각적인 가열·냉각을 표현할 수 없어 thermal capacitance가 필요하다고 구분한다. [TI Thermal dynamics](https://www.ti.com/video/6243719539001)

| 열 모델 | 단위 | 전기적 대응 |
|---|---|---|
| 온도 차이 $`\theta=T-T_a`$ | K | 전압 |
| 발열 P·열유량 | W=J/s | 전류 |
| 열저항 $`R_{th}`$ | K/W | 저항 |
| 열용량 $`C_{th}`$ | J/K | capacitance |

온도 차이 1 K와 1 °C의 크기는 같다. 온도 자체를 Kelvin과 Celsius 사이에서 바꾸는 데는 offset이 필요하다. 순수한 1차원 정상 전도라면 $`R=l/(kA)`$, 균일한 물체라면 $`C=mc_p`$로 출발할 수 있지만 실제 package의 여러 경로를 하나의 막대로 취급하지는 않는다.

### 에너지 보존에서 한 pole 모델 유도

물체 내부 온도가 하나의 T로 표현되고 주변 $`T_a`$가 일정하다고 하자. 열저항을 통해 나가는 열은 $`\theta/R_{th}`$다. 들어온 에너지 중 빠져나가지 않은 부분이 저장되므로

$$C_{th}\frac{d\theta}{dt}=P(t)-\frac{\theta}{R_{th}},\qquad
\tau=R_{th}C_{th}.$$

상수 P를 가했을 때 초기 상승분 $`\theta_0`$에서의 해는

$$\theta(t)=PR_{th}+(\theta_0-PR_{th})e^{-t/\tau}.$$

정상상태는 $`\theta_\infty=PR_{th}`$, 초기 기울기는 $`(P-\theta_0/R_{th})/C_{th}`$다. 처음 주변 온도와 같았다면 한 시정수에서 최종 상승분의 약 63.2%가 된다. $`R=10`$ K/W, $`C=2`$ J/K, P=5 W, $`T_a=25`$ °C라면 시정수 20 s, 20 s 뒤 약 56.6 °C, 충분히 뒤에는 75 °C인 모델이다. 실제 부품을 측정한 값이 아니다.

ADI의 열 과도 모델도 energy balance를 RC network로 연결한다. 실제 die·접착층·package는 여러 시간상수를 가질 수 있어 한 pole로 모든 초기·장시간 응답을 동시에 맞추기는 어렵다. [ADI transient thermal modeling](https://www.analog.com/en/resources/technical-articles/use-thermal-analysis-to-predict-an-ics-transient-behavior-and-avoid-overheating.html)

### 주기 발열의 최고 온도

P를 $`t_{on}`$ 동안 가하고 $`t_{off}`$ 동안 0으로 두는 주기 정상상태를 생각하자. $`a=e^{-t_{on}/\tau}`$, $`b=e^{-t_{off}/\tau}`$이면

$$\theta_{max}=PR_{th}(1-a)+a\theta_{min},\quad \theta_{min}=b\theta_{max}.$$

두 식을 풀면

$$\theta_{max}=\frac{PR_{th}(1-a)}{1-ab},\qquad \theta_{min}=b\theta_{max}.$$

평균 온도 상승은 이 선형 모델의 주기 에너지 균형에서 $`R_{th}P_{avg}`$지만 최고 온도는 일반적으로 더 크다. $`P_{avg}`$만 넣은 정상 식으로 pulse의 peak를 대신하면 안 된다. Datasheet의 transient thermal impedance $`Z_{th}(t)`$는 지정한 경계 조건과 pulse 조건에 맞춰 사용한다.

### Datasheet 열 수치의 적용 범위

$`\theta_{JA}`$는 package만의 고유 상수가 아니다. PCB 구리·via·공기 흐름·장착 조건의 영향을 받는다. Junction-to-case 값과도 경계 조건이 다르며, characterization parameter인 $`\psi_{JT}`$ 등을 무조건 같은 열저항으로 직렬 연결할 수 없다. [TI의 열 경로·데이터시트 해설](https://www.ti.com/document-viewer/lit/html/SSZTB80/GUID-D4E3F3F5-260D-45A1-862A-6E9A3052DC5A), [TI SPRA953D, §1·3](https://www.ti.com/lit/an/spra953d/spra953d.pdf)

전력이나 열전도도가 온도에 따라 변하고 열원이 공간적으로 퍼져 있으면 비선형·다중 노드 모델이나 thermal solver가 필요하다. 단일 RC 식으로 hot spot, 열응력, package 수명을 직접 예측하지 않는다.

### 구현과 독립 검증

`thermal_step`은 구간별 일정 전력의 정확한 1차 해를 이어 붙인다. `thermal_pulse_steady`는 위 고정점 식으로 주기 최저·최고 온도를 계산한다. 테스트는 0시간·한 시정수·장시간 한계, 별도의 Euler ODE 적분의 수렴, 주기 해의 on/off 재적용과 100주기 반복 결과를 비교한다.

실제 검증에서는 전력·주변 온도·fixture·PCB·airflow와 온도 센서의 위치·응답을 고정한다. 서로 다른 전력과 ambient에서 가열·냉각 trace를 얻어 모델을 맞추고, fitting에 쓰지 않은 조건으로 예측을 검증한다. 표면 온도와 junction 추정의 차이도 남긴다. Python의 해석해 일치는 이 수치 모델의 확인이며 실물의 최대 junction 온도 측정이나 열안전 인증 결과가 아니다.

## English

### Equal average power can produce different peaks

Continuous and pulsed 5 W dissipation produce different temperature trajectories because heat encounters resistance and matter stores thermal energy. Temperature rise corresponds to voltage, heat flow in W to current, thermal resistance in K/W to resistance, and thermal capacitance in J/K to capacitance. Thermal capacitance is required to represent finite heating/cooling time. [TI Thermal dynamics](https://www.ti.com/video/6243719539001)

Temperature differences of 1 K and 1 °C have the same magnitude, although absolute temperature conversion requires an offset. A one-dimensional conduction path gives $`R=l/(kA)`$ and a uniform body gives $`C=mc_p`$, but a package's multiple paths cannot generally be replaced by one physical rod.

### A one-pole model from energy conservation

Assume one uniform body temperature and constant ambient $`T_a`$. With $`\theta=T-T_a`$, outgoing heat is $`\theta/R_{th}`$. Energy balance gives

$$C_{th}\,d\theta/dt=P(t)-\theta/R_{th},\qquad \tau=R_{th}C_{th}.$$

For constant P and initial rise $`\theta_0`$,

$$\theta(t)=PR_{th}+(\theta_0-PR_{th})e^{-t/\tau}.$$

Steady rise is $`PR_{th}`$; initial slope is $`(P-\theta_0/R_{th})/C_{th}`$. From ambient, one time constant reaches about 63.2% of the final rise. R=10 K/W, C=2 J/K, P=5 W and ambient 25 °C give τ=20 s, about 56.6 °C after 20 s and 75 °C asymptotically. This is an illustrative model, not a component measurement.

ADI likewise derives RC networks from thermal energy balance. Dies, interfaces and packages can have several time constants, so one pole may not fit both early and late behavior. [ADI transient modeling](https://www.analog.com/en/resources/technical-articles/use-thermal-analysis-to-predict-an-ics-transient-behavior-and-avoid-overheating.html)

### Periodic power and peak temperature

Apply P for $`t_{on}`$ and zero for $`t_{off}`$. For $`a=e^{-t_{on}/\tau}`$ and $`b=e^{-t_{off}/\tau}`$, periodic steady state satisfies $`\theta_{max}=PR_{th}(1-a)+a\theta_{min}`$ and $`\theta_{min}=b\theta_{max}`$, hence

$$\theta_{max}=PR_{th}(1-a)/(1-ab),\qquad\theta_{min}=b\theta_{max}.$$

Periodic energy balance gives mean rise $`R_{th}P_{avg}`$ for this linear model, but peak rise is generally higher. Average-power steady-state calculations cannot replace pulse-peak analysis. Datasheet transient thermal impedance applies under its specified boundary and pulse conditions.

### Limits of datasheet metrics

$`\theta_{JA}`$ depends on board copper/vias, airflow and mounting; it is not solely an intrinsic package constant. Junction-to-case resistance uses different boundary conditions, and characterization parameters such as $`\psi_{JT}`$ cannot simply be chained as ordinary thermal resistances. [TI thermal-path explanation](https://www.ti.com/document-viewer/lit/html/SSZTB80/GUID-D4E3F3F5-260D-45A1-862A-6E9A3052DC5A), [TI SPRA953D, §§1/3](https://www.ti.com/lit/an/spra953d/spra953d.pdf)

Temperature-dependent power/material properties and distributed heat sources may require nonlinear or multi-node models and thermal solvers. One RC equation does not directly predict hot spots, mechanical stress or package lifetime.

### Implementation and independent validation

`thermal_step` composes exact constant-power interval solutions; `thermal_pulse_steady` solves the periodic fixed point. Tests check zero-time, one-time-constant and long-time limits, convergence of an independent Euler ODE calculation, on/off consistency of the periodic solution and agreement after 100 repeated cycles.

Physical validation fixes power, ambient, fixture, board, airflow and sensor location/response. Fit heating/cooling traces at several powers and ambients, then predict conditions excluded from fitting. Distinguish surface temperature from junction estimates. Python agreement establishes numerical-model consistency, not physical maximum-junction measurement or thermal certification.

## 출처 대조 / Source cross-check

ADI의 다중 RC 열 모델을 TI의 thermal capacitance·transient impedance 및 경계 조건 설명과 대조했다. / ADI's RC modeling was cross-checked against TI's dynamics and boundary-condition explanations. 확인 / checked: 2026-10-19.
