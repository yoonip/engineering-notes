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
