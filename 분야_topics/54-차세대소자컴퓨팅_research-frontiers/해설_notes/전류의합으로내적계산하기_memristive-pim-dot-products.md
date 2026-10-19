# 전류의 합으로 내적 계산하기: memristive PIM과 비이상성

[연구 주제](../README.md) · [참조 모델](../../../예제_examples/확장기초_extended/hardware/models.py) · [검산](../../../예제_examples/확장기초_extended/hardware/test_models.py)

## 한국어

### 저장한 자리에서 계산한다는 뜻

행렬 원소를 메모리에서 계산기로 반복해서 옮기는 대신, 저장 소자의 전도도를 계산에 직접 쓰는 방법이 있다. Analog in-memory computing의 crossbar가 그 예다. PIM이라는 큰 범주에는 digital·near-memory 방식도 포함되므로 모든 PIM을 memristor와 같은 것으로 부르지는 않는다. 여기서는 읽기 중 conductance가 거의 일정한 programmable resistive array의 내적 모델을 다룬다. PCM과 resistive-switching 소자의 실제 물리적 프로그래밍 과정은 서로 다를 수 있다. [IBM의 PCM 계산 구조](https://research.ibm.com/blog/the-hardware-behind-analog-ai)

### Ohm과 Kirchhoff 법칙에서 행렬 곱 유도

n개의 row 전압 $V_i$와 m개의 column이 있다고 하자. Cell conductance는 $G_{ij}\ge0$ S이고, column은 이상적인 readout에 의해 virtual ground를 유지한다. 배선저항·기생·소자 비선형성을 무시하면 각 cell 전류는 $I_{ij}=G_{ij}V_i$, column의 KCL은

$$I_j=\sum_{i=1}^{n}G_{ij}V_i,\qquad \mathbf I=G^T\mathbf V.$$

이 글은 row가 입력 index이므로 transpose가 붙는다. 논문마다 행렬을 반대로 정의할 수 있어 이름보다 index를 먼저 확인한다. V·S=A이므로 출력 단위는 전류다. 이를 무차원 신경망 값으로 쓰려면 입력 voltage scale과 conductance scale, readout gain을 되돌리는 과정이 필요하다.

### 음수 weight와 scale

물리적인 양의 conductance 하나로 음수 weight를 바로 만들 수는 없다. 예를 들어

$$G^+_{ij}=G_{min}+g_s\max(w_{ij},0),\quad
G^-_{ij}=G_{min}+g_s\max(-w_{ij},0)$$

의 differential pair를 두면 $G^+-G^-=g_sW$다. $V_i=v_sx_i$일 때

$$y_j=\frac{I^+_j-I^-_j}{v_sg_s}=\sum_iw_{ij}x_i.$$

$g_s$는 weight당 S, $v_s$는 V이다. $G_{max}$가 있다면 $g_s|w_{ij}|\le G_{max}-G_{min}$을 만족해야 한다. 이 차감은 이상적인 공통 baseline을 제거하지만, 서로 다른 소자 오차·drift까지 자동으로 지우지는 않는다. IBM은 실제 구조에서 양·음 weight를 차분 conductance로 표현한다. [IBM의 differential array 설명](https://research.ibm.com/blog/the-hardware-behind-analog-ai)

음의 입력을 음의 voltage로 표현하는 것도 수학적 모델에서는 간단하지만, 실제 device의 극성 의존 I–V가 다르면 오차가 생긴다. 분리된 read phase나 calibration이 필요한 이유다. [IBM 2024의 polarity·4-quadrant 연구](https://research.ibm.com/publications/demonstration-of-4-quadrant-analog-in-memory-matrix-multiplication-in-a-single-modulation)

### 작은 오차가 어디서 들어오는가

독립적인 작은 변화의 1차항은

$$\delta I_j\approx\sum_iV_i\delta G_{ij}+\sum_iG_{ij}\delta V_i+\delta I_{read,j}.$$

$\delta G\delta V$의 2차항은 생략했다. Programming 오차·시간 drift·read noise, DAC의 입력 오차, ADC의 quantization·clipping은 다른 항목이다. Fault나 소자 간 편차가 inference에 미치는 영향은 NIST의 실제 array 연구에서도 중요한 검증 대상으로 다룬다. [NIST Hardware Accelerators](https://www.nist.gov/programs-projects/hardware-accelerators-neural-networks)

행 앞의 공통 직렬저항 r만 넣고 column을 여전히 0 V로 두면 row 전류 합은 $V_{row}\sum_jG_{ij}$다. 전압 강하를 대입해

$$V_{row,i}=\frac{V_{source,i}}{1+r\sum_jG_{ij}}$$

를 얻는다. Row의 전체 conductance에 따라 입력 전압이 달라져 원하는 선형 mapping이 흔들린다. 이는 한 개의 공통 저항 모델이다. 셀 위치마다 다른 분포 배선저항·sneak path·selector는 전체 nodal network를 풀어야 한다.

### 구현과 독립 검증

`crossbar_currents`는 이상적인 column KCL과 선택적인 공통 row 저항을 계산한다. Differential mapping의 W와 x를 사용해 직접 정수·실수 내적 결과와 복원한 값을 비교한다. 예제 $W=[(1,-0.5),(-0.25,0.75),(0.5,0)]$, $x=(0.5,-1,0.25)$의 출력은 $(0.875,-1)$이다. Row 저항이 있는 경우는 별도로 공급 전압에서 $r\sum I$를 뺀 전압과 각 cell의 Ohm 법칙이 맞는지 확인한다.

`quantize_symmetric`는 ±bound의 끝점을 포함하는 $2^b$개 균일 level을 가진 수치 양자화 예다. 범위 안에서는 간격 $\Delta=2bound/(2^b-1)$의 절반 이내 오차, 범위 밖에서는 clipping을 검사한다. 실제 ADC code 체계나 offset을 복제한 모델은 아니며 이 짝수 level 집합에는 정확한 0이 없을 수 있다.

실물 검증은 read voltage·온도·program/verify 절차·drift 시간을 고정하고 독립적인 측정 I–V와 array 출력으로 모델을 대조한다. 오차의 평균뿐 아니라 위치·시간·입력별 분포를 남기며, 쓰지 않은 입력으로 calibration을 평가한다. Array의 병렬 전류 합이 곧 시스템 전체의 O(1) 실행·무한 정밀도·무조건적인 에너지 우위를 뜻하지 않는다. DAC/ADC, settling, tiling, digital accumulation, weight write와 데이터 이동까지 같은 precision·workload 기준으로 비교해야 한다. Python 결과는 실제 memristor 제작·chip 측정이나 AIHWKit 실행 결과가 아니다.

## English

### Compute where values are stored

Analog crossbars use stored conductance directly instead of repeatedly moving matrix entries into a separate arithmetic unit. PIM also includes digital and near-memory approaches; it is not synonymous with memristors. The model here concerns programmable resistive arrays with approximately fixed conductance during reading. PCM and resistive-switching devices can have different programming physics. [IBM PCM architecture](https://research.ibm.com/blog/the-hardware-behind-analog-ai)

### Matrix multiplication from Ohm's law and KCL

For n row voltages $V_i$ and m columns, let $G_{ij}\ge0$ S. Assume ideal virtual-ground columns, negligible wiring resistance/parasitics and linear reads. Then $I_{ij}=G_{ij}V_i$ and

$$I_j=\sum_iG_{ij}V_i,\qquad\mathbf I=G^T\mathbf V.$$

Rows are input indices here, hence the transpose. Other conventions may differ; inspect indices. Outputs are amperes since V·S=A. Dimensionless neural values require input/conductance scaling and readout-gain conversion.

### Signed weights and scaling

One positive conductance cannot directly encode a negative weight. A differential mapping can use $G^+=G_{min}+g_s\max(W,0)$ and $G^-=G_{min}+g_s\max(-W,0)$. With $V_i=v_sx_i$,

$$y_j=(I^+_j-I^-_j)/(v_sg_s)=\sum_iw_{ij}x_i.$$

Here $g_s$ is S per weight unit and $v_s$ is V. Finite range requires $g_s|w_{ij}|\le G_{max}-G_{min}$. Differencing removes an ideal common baseline, not arbitrary device mismatch or drift. IBM describes differential conductance encoding in its physical arrays. [IBM explanation](https://research.ibm.com/blog/the-hardware-behind-analog-ai)

Negative inputs can use negative voltages mathematically, but real polarity-dependent I–V behavior can introduce error, requiring multiple read phases or calibration. [IBM's 2024 four-quadrant study](https://research.ibm.com/publications/demonstration-of-4-quadrant-analog-in-memory-matrix-multiplication-in-a-single-modulation)

### Sources of nonideality

To first order,

$$\delta I_j\approx\sum_iV_i\delta G_{ij}+\sum_iG_{ij}\delta V_i+\delta I_{read,j},$$

omitting the second-order $\delta G\delta V$ product. Programming error, drift, read noise, DAC error, ADC quantization and clipping are distinct mechanisms. NIST's array research independently emphasizes device variability and fault-aware evaluation. [NIST accelerators](https://www.nist.gov/programs-projects/hardware-accelerators-neural-networks)

With just one common series row resistor r and ideal grounded columns, KCL and the resistor drop give $V_{row,i}=V_{source,i}/(1+r\sum_jG_{ij})$. Total row conductance now changes the applied voltage. This lumped approximation does not solve position-dependent wiring, sneak paths or selectors; those require a full nodal network.

### Implementation and verification

`crossbar_currents` calculates column KCL with optional common row resistance. Differential decoded results are compared against direct dot products. For $W=[(1,-0.5),(-0.25,0.75),(0.5,0)]$ and $x=(0.5,-1,0.25)$, output is $(0.875,-1)$. Row-resistance tests independently subtract $r\sum I$ from supply voltage and verify each cell's Ohm law.

`quantize_symmetric` is an illustrative numerical quantizer with $2^b$ equally spaced levels including ±bound. Tests check at most half a step, $\Delta/2=bound/(2^b-1)$, error inside range and clipping outside. It does not replicate a particular ADC code format or offset, and this even-sized level set may not represent exact zero.

Physical validation fixes read voltage, temperature, program/verify procedure and drift duration, then compares independent I–V/array measurements against predictions. Preserve spatial, temporal and input-dependent error distributions, using held-out inputs for calibration evaluation. Parallel analog summation does not imply system-wide O(1) runtime, infinite precision or automatic energy superiority. Include DAC/ADC, settling, tiling, digital accumulation, writes and movement at comparable workload and precision. Python results are not fabricated-device, chip-measurement or AIHWKit execution results.

## 출처 대조 / Source cross-check

IBM의 PCM·차분 내적 구조 및 극성 연구와 NIST의 독립적인 소자 편차·array 측정 연구를 대조했다. / IBM's architecture and polarity study were cross-checked against NIST's independent variability and array research. 확인 / checked: 2026-10-19.
