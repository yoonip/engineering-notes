# die와 package가 다른 속도로 뜨거워질 때: 두 노드 열망

[패키징·열 목차](../README.md) · [열망 모델](../../../예제_examples/심화_advanced/hardware/models.py) · [검산](../../../예제_examples/심화_advanced/hardware/test_models.py)

## 한국어

### 표면 온도가 같아도 내부 온도는 다를 수 있습니다

작은 die는 빨리 뜨거워지고 큰 package·board는 더 천천히 온도가 변할 수 있습니다. 한 개의 thermal RC는 한 가지 완화 시간만 표현하므로 이런 차이를 놓칩니다. 두 노드 모델은 열을 저장하는 곳을 두 개로 나누고 그 사이의 열 흐름을 따로 계산합니다. 전기 RC처럼 식을 쓰지만, 전압은 온도 차, 전류는 열유속에 대응합니다.

[ADI의 transient thermal analysis](https://www.analog.com/en/resources/technical-articles/use-thermal-analysis-to-predict-an-ics-transient-behavior-and-avoid-overheating.html)는 내부 층을 나눈 열망을 설명합니다. [TI thermal dynamics](https://www.ti.com/video/6243719539001)는 thermal capacitance와 RC 모델의 역할을 설명합니다. 이 글의 R·C는 교육용 가정이며 어떤 package의 데이터시트에서 추출한 값이 아닙니다.

### 에너지 보존에서 두 식을 만듭니다

ambient는 일정한 Ta, die와 case의 상승 온도는 $`\theta_j=T_j-T_a`$, $`\theta_c=T_c-T_a`$입니다. P는 die에서 발생하는 W, Rjc·Rca는 K/W, Cj·Cc는 J/K입니다. 열이 die→case→ambient 한 경로로만 이동하고 매개변수가 일정하다고 가정합니다.

```math
C_j\dot\theta_j=P-\frac{\theta_j-\theta_c}{R_{jc}},
\qquad
C_c\dot\theta_c=\frac{\theta_j-\theta_c}{R_{jc}}-\frac{\theta_c}{R_{ca}}.
```

첫 식은 die에 발생한 열에서 case로 나간 열을 뺀 것입니다. 둘째는 case로 들어온 열에서 ambient로 나간 열을 뺀 것입니다. 온도 상승 1 K와 1 °C의 간격은 같지만 절대 온도 변환은 별개입니다. 열저항의 기준 온도와 경로도 명시해야 합니다.

### 정상상태와 최초 기울기

미분을 0으로 두면 모든 경로에서 같은 열 P가 흐릅니다.

```math
\theta_{c,\infty}=PR_{ca},\qquad
\theta_{j,\infty}=P(R_{jc}+R_{ca}).
```

처음 두 노드가 ambient와 같으면 $`\dot\theta_j(0)=P/C_j`$, $`\dot\theta_c(0)=0`$입니다. die는 즉시 가열되지만 case는 die와 온도 차가 생긴 뒤 따라갑니다. P=2 W, Rjc=2 K/W, Rca=8 K/W, Cj=0.1 J/K, Cc=1 J/K이면 최종 상승은 die 20 K, case 16 K입니다. 단순히 두 time constant를 각각 Rjc Cj, Rca Cc라고 붙이는 것은 결합을 무시합니다. 실제 두 decay rate는 결합 상태행렬의 고유값에서 나옵니다.

### 계산이 에너지를 만들어 내지 않는지

기준 ambient 대비 저장된 열의 변화량은 $`E=C_j\theta_j+C_c\theta_c`$입니다. 두 상태식을 더하면 내부 전달 항이 상쇄됩니다.

```math
\dot E=P-\frac{\theta_c}{R_{ca}},\qquad
E(t)+\int_0^t\frac{\theta_c(u)}{R_{ca}}du=Pt
```

초기 상승 온도가 0일 때의 식입니다. 코드에서는 바깥으로 나간 누적 열도 세 번째 상태로 적분합니다. 입력한 열=저장된 열+방출한 열인지 독립적으로 확인할 수 있습니다. 전기 커패시터 식을 흉내 내 $`C\theta^2/2`$를 물리적인 저장 열이라고 부르면 단위부터 틀립니다. 그런 이차식은 안정성의 수학적 함수로는 쓸 수 있지만 J 단위 열량과 구별해야 합니다.

### 실행과 현실 적용

```bash
python demo.py --case thermal
python -m unittest -v test_models.HardwareModels.test_thermal_energy_balance test_models.HardwareModels.test_thermal_steady_and_timestep
```

RK4로 두 온도와 방출 열을 계산합니다. 2 s의 에너지 보존, 충분히 긴 시간의 20·16 K 정상값, 10 ms와 5 ms step의 수렴을 검사합니다. 초기 온도·power를 바꿀 때 에너지 식의 초기항도 맞춰야 합니다. explicit 적분의 step은 가장 빠른 고유시간보다 충분히 작게 선택합니다.

실제 열망은 board copper, airflow, heatsink, 여러 heat source, 온도 의존성·복사에 따라 달라집니다. 데이터시트 θJA를 임의 환경의 Rjc+Rca로 그대로 쓰지 않습니다. Foster fitting의 내부 노드는 물리적인 case와 같지 않을 수 있어 Cauer 모델과도 구분합니다. fitting에 쓴 power step 외의 파형으로 holdout 검증하고 측정 위치·sensor 지연을 확인합니다. 이 결과는 가정한 두 노드 모델 계산이며 실제 die 온도 측정이 아닙니다.

### 전원을 껐을 때도 내부 온도는 곧바로 같아지지 않습니다

열용량은 물체 온도를 1 K 바꾸는 데 필요한 열량 J입니다. 열저항은 같은 열전달률 W를 흘릴 때 필요한 온도 차 K를 나타냅니다. 열유속이라는 말은 문맥에 따라 면적당 W/m²를 뜻하므로, 위 회로의 가지에서 흐르는 양은 열전달률 W라고 읽는 편이 단위를 분명히 합니다. 도함수는 온도가 지금 얼마나 빨리 변하는지를 나타냅니다.

위의 P=2 W 모델이 정상상태에 도달한 뒤 전원을 끈다고 합시다. 처음 상승 온도는 die 20 K, case 16 K입니다. die에서 case로 전달되는 열은 (20−16)/2=2 W이고, case가 주변으로 내보내는 열도 16/8=2 W입니다. 전원을 끈 직후 die는 −2/0.1=−20 K/s로 식지만 case의 최초 기울기는 0입니다. 전력 공급이 멈춘 순간에도 die에 저장된 열이 case로 들어오기 때문입니다.

이것이 표면 온도만 보고 내부가 충분히 식었다고 판단하기 어려운 이유입니다. 반대로 표면이 한동안 뜨겁게 남는다고 전력이 계속 들어오는 것으로 단정할 수도 없습니다. 저장된 열이 이동하는 시간이 필요합니다. 실제 측정에서는 센서 자신의 응답 시간까지 더해지므로 노드의 지연과 센서 지연을 분리해야 합니다.

### 두 시간척도를 작은 행렬로 확인합니다

위 가정값을 상태식에 대입하면 주변 온도 대비 상승 상태의 선형 부분은 다음과 같습니다. 전력은 첫 노드에 P/Cj로 들어갑니다.

```math
\frac{d}{dt}
\begin{bmatrix}\theta_j\\\theta_c\end{bmatrix}
=
\begin{bmatrix}-5&5\\0.5&-0.625\end{bmatrix}
\begin{bmatrix}\theta_j\\\theta_c\end{bmatrix}
+\begin{bmatrix}P/0.1\\0\end{bmatrix}.
```

고유값은 상태가 자체적으로 줄어드는 두 비율입니다. 이 행렬의 특성식은 `λ²+5.625λ+0.625=0`이며, 근은 약 −5.512와 −0.1134 s⁻¹입니다. 대응 시간척도는 약 0.181 s와 8.82 s입니다. `Rjc×Cj=0.2 s`, `Rca×Cc=8 s`와 비슷한 크기이지만 같지 않습니다. 두 노드가 서로 영향을 주어 생긴 모드이기 때문입니다. 위 수치는 상용 패키지의 측정값이 아니라 기존 모델을 검산한 결과입니다.

빠른 모드는 짧은 die 변화를, 느린 모드는 더 큰 열 저장과 외부 방출을 이해하는 데 도움을 줍니다. 그러나 각 모드가 die 또는 case 하나만의 온도라는 뜻은 아닙니다. 일반적으로 두 모드가 두 상태에 함께 섞입니다. 따라서 온도 곡선에서 지수 성분을 두 개 맞췄다고 각 성분을 특정 물리층으로 바로 지목할 수 없습니다.

### 펄스의 평균 전력만으로 최고 온도를 정할 수 없습니다

4 W를 0.1초 켜고 0.9초 끄는 주기 입력의 평균 전력은 0.4 W입니다. 정상적인 주기 상태에서 에너지 저장의 한 주기 순변화는 0이므로 평균 case 상승은 0.4×8=3.2 K, 평균 die 상승은 0.4×10=4 K입니다. 이는 이 선형 모델의 평균 관계입니다. 최고 온도가 4 K라는 뜻은 아닙니다.

펄스가 빠른 열 시간척도보다 충분히 짧으면 내부에 열이 집중된 뒤 외부로 전달됩니다. 반대로 긴 펄스는 높은 전력의 정상상태 쪽으로 접근합니다. 평균 0.4 W가 같은 두 파형도 펄스 길이와 반복 간격에 따라 최고 온도가 다를 수 있습니다. 수명·보호 판단에 최고 온도가 필요하다면 실제 파형을 입력해 시간응답을 계산하고 측정해야 합니다.

### 에너지 경계와 초기조건의 검산

전원을 끄는 예에서 초기 저장 열은 0.1×20+1×16=18 J입니다. 이후 입력 전력이 0이고 최종적으로 주변 온도까지 식는다면 이 18 J가 주변으로 나가야 합니다. 초기 에너지를 빼먹고 방출 열이 0이어야 한다고 검사하면 올바른 냉각도 오류로 판정하게 됩니다.

일반적인 입력과 초기조건에서는 다음 식을 사용합니다.

```math
E(t)-E(0)+\int_0^t\frac{\theta_c(u)}{R_{ca}}du
=\int_0^t P(u)du.
```

예를 들어 초기 저장 열 18 J인 상태에 1 W를 2초 더 넣고, 그동안 3 J가 주변으로 나갔다고 가정하면 마지막 저장 열은 17 J입니다. 온도 한 점만 맞추는 것과 달리 이 수지는 모델 전체가 에너지를 만들어 내거나 지우지 않는지 확인합니다. 다만 에너지수지가 맞는다고 열저항·열용량의 식별이 유일하거나 실측과 맞는다는 뜻은 아닙니다.

### 센서와 모델을 비교하는 실제 순서

먼저 입력 전력을 어디서 잰 것인지 정합니다. 전원장치의 입력 W에는 변환기 손실이 포함될 수 있으므로 die에서 발생한 열 P와 같다고 놓기 어렵습니다. 그다음 주변 온도, 방열판 장착·공기 흐름과 표면 센서 위치를 고정합니다. 서로 다른 환경의 온도 곡선을 같은 R·C로 맞추면 환경 차이가 부품 차이처럼 보일 수 있습니다.

단계 입력 한 번으로 적합한 값은 다른 크기와 펄스 길이에서 점검합니다. 적합에 쓰지 않은 파형에서 오차가 커진다면 온도 의존성·여러 열경로·센서 지연을 빠뜨렸을 수 있습니다. 이를 확인하지 않고 노드를 더 늘리면 데이터에는 잘 맞아도 물리적 의미가 불분명한 모델이 될 수 있습니다. 위 계산은 가정한 열망의 검산이며 실제 칩의 온도 측정값은 아닙니다.

### 확인 문제

1. 정상상태에서 전원을 끈 직후 case의 기울기가 0이어도 냉각이 없는 것은 아닌 이유는 무엇인가요?
2. 평균 전력이 같은 펄스들의 최고 온도가 다를 수 있는 이유는 무엇인가요?
3. 초기 저장 열 18 J, 추가 입력 2 J, 주변 방출 3 J이면 남는 열은 얼마인가요?

<details><summary>해설 보기</summary>

1. 그 순간 die에서 들어오는 열과 주변으로 나가는 열이 같기 때문입니다. die는 이미 식기 시작합니다.
2. 내부에 열이 쌓이고 전달되는 시간이 있어 펄스 길이·간격이 영향을 주기 때문입니다.
3. 18+2−3=17 J입니다. 냉각 검산에는 초기 에너지가 포함되어야 합니다.

</details>

## English

### Internal and surface temperatures evolve differently

A small die may heat quickly while its package and board respond more slowly. A single thermal RC has only one relaxation mode. A two-node network assigns separate heat storage to the die and case and computes their coupling. Temperature differences correspond to voltages and heat flow to current.

[ADI's transient thermal analysis](https://www.analog.com/en/resources/technical-articles/use-thermal-analysis-to-predict-an-ics-transient-behavior-and-avoid-overheating.html) develops layered thermal networks. [TI's thermal dynamics lecture](https://www.ti.com/video/6243719539001) independently explains thermal capacitance and RC modeling. The component values here are educational assumptions, not an identified commercial package.

### Deriving the coupled equations

Ambient Ta is constant; theta_j and theta_c are die and case rises above it. Power is in W, thermal resistance in K/W and capacitance in J/K. Assume a single die-to-case-to-ambient heat path and constant parameters. Energy conservation gives the two displayed state equations: generated heat minus outgoing heat at the die, incoming minus outgoing heat at the case.

Setting derivatives to zero gives theta_c=P Rca and theta_j=P(Rjc+Rca). Starting from ambient, the initial slopes are P/Cj at the die and zero at the case. For 2 W, resistances 2 and 8 K/W and capacitances 0.1 and 1 J/K, final rises are 20 K and 16 K. Coupled decay rates come from the state-matrix eigenvalues; assigning separate Rjc Cj and Rca Cc time constants ignores coupling.

### Independent heat-balance check

Physical stored-heat change relative to ambient is $`E=C_j\theta_j+C_c\theta_c`$. Adding the state equations cancels internal transfer and gives $`\dot E=P-\theta_c/R_{ca}`$. From zero initial rise, stored heat plus integrated heat rejected to ambient must equal Pt. The code integrates rejected heat as a third state to check that balance.

The expression C theta²/2 is not physical thermal energy; its units differ from joules. A quadratic function can be useful for mathematical stability analysis, but must not be confused with the linear sensible-heat expression here.

### Execution and model boundaries

Run the commands above. Tests check heat balance at two seconds, the long-time 20/16 K limits and step refinement from 10 to 5 ms. Other initial temperatures require the corresponding initial-energy term. An explicit integrator must resolve the fastest coupled thermal mode.

Real networks depend on copper, airflow, heatsinks, multiple heat sources, temperature dependence and radiation. A datasheet theta_JA is not automatically the sum of these two resistances in another environment. Foster-fit internal nodes need not be physical case temperatures and must be distinguished from a Cauer ladder. Validate fitted parameters on waveforms not used for fitting and account for sensor position and lag. These are assumed-network computations, not measured die temperatures.

## 출처 / Sources

- Analog Devices, *Use Thermal Analysis to Predict an IC's Transient Behavior*: coupled layered heat models and calibration conditions.
- Texas Instruments, *Thermal dynamics*, 2026-07-29: thermal storage and RC representation. Links appear above.
