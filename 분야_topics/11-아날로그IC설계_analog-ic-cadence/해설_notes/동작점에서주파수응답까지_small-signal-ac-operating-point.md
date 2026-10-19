# 동작점에서 주파수 응답까지: 소신호와 AC 해석

[Analog IC](../README.md) · [참조 모델](../../../예제_examples/확장기초_extended/hardware/models.py) · [검산](../../../예제_examples/확장기초_extended/hardware/test_models.py)

## 한국어

### 작은 변화부터 보는 이유

트랜지스터의 입력을 두 배로 키운다고 출력도 항상 두 배가 되지는 않는다. 하지만 한 동작점 주변을 충분히 좁게 보면 곡선을 직선으로 근사할 수 있다. 소신호 해석은 이 국소적인 기울기로 증폭기의 이득과 주파수 응답을 구한다. 큰 신호에서의 clipping이나 왜곡을 없애 주는 방법은 아니다. [MIT 6.012 Lecture 19](https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-fall-2005/7a51249eb734152c5ce95df393cf4f1f_lec19.pdf)

먼저 DC 해석으로 전압·전류가 균형을 이루는 동작점 Q를 찾는다. 회로의 정적 방정식을 $F(v_Q)=0$이라 쓰고 작은 변화 $\delta v$를 더하면 Taylor 전개의 1차항은 $F(v_Q+\delta v)\approx F(v_Q)+J_Q\delta v$다. 동작점을 바꾸면 Jacobian $J_Q$도 달라진다. 같은 회로도라도 bias가 다르면 같은 AC 응답을 기대할 수 없는 이유다.

MOSFET에서는

$$\delta i_D=g_m\delta v_{GS}+g_{ds}\delta v_{DS}+g_{mb}\delta v_{BS},\qquad
g_m=\left.\frac{\partial I_D}{\partial V_{GS}}\right|_Q,\quad r_o=1/g_{ds}.$$

$g_m,g_{ds},g_{mb}$의 단위는 S=A/V, $r_o$는 Ω다. 독립적인 이상적 DC 전압원은 두 단자의 소신호 전압 차이가 0인 단락으로 치환한다. 한 단자가 기준 접지일 때 다른 단자도 AC ground가 되며, 떠 있는 전압원의 두 단자를 각각 접지하는 것은 아니다. 독립적인 이상적 DC 전류원은 소신호 개방으로 치환한다. 종속 전원은 소자 기울기를 나타내므로 남겨 둔다.

### 공통 소스의 한 pole 모델 유도

source와 bulk가 AC ground인 common-source 단계에서 drain에 $R_D$, 소자 출력저항 $r_o$, 부하 $R_L$와 합성 출력 커패시턴스 $C_o$가 있다고 하자. 입력은 이상적인 gate 전압원이며 $C_{gd}$에 의한 입력 귀환 등은 생략한다. 출력 노드의 KCL은

$$g_mv_i+\left(\frac1{R_D}+\frac1{r_o}+\frac1{R_L}+sC_o\right)v_o=0.$$

$R=R_D\parallel r_o\parallel R_L$로 두면

$$A_v(s)=\frac{v_o}{v_i}=\frac{-g_mR}{1+sRC_o},\qquad f_p=\frac1{2\pi RC_o}.$$

음수 이득은 입력이 올라갈 때 출력이 내려감을 뜻한다. pole에서는 저주파 이득에 비해 크기가 $1/\sqrt2$, 추가 위상 지연이 45°다. 이 출력 한 pole 모델은 실제 MOSFET의 여러 capacitance를 모두 포함한 결과가 아니다. 입력 구동원의 저항과 $C_{gd}$를 넣으면 Miller 효과와 추가 pole·zero를 살펴야 한다. [MIT Lecture 23](https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-fall-2005/44ed13d9b5e46dd459d9bca431fc547a_lec23.pdf)

$g_m=1$ mS, $R_D=10$ kΩ, $r_o=R_L=100$ kΩ, $C_o=20$ pF이면 $R=8.333$ kΩ, $A_v(0)=-8.333$, $f_p\approx0.955$ MHz다. 이는 가정한 수치의 계산 예이며 특정 공정의 성능 수치가 아니다.

### AC 자극의 1은 큰 신호의 1 V와 다르다

AC 해석은 선형화한 회로에서 복소 전압·전류를 계산한다. 입력의 AC magnitude를 1로 두면 출력과 전달함수의 수치가 같아져 편리하지만, 트랜지스터가 실제로 1 V 진폭까지 선형이라는 뜻은 아니다. $20\log_{10}|v_o/v_i|$와 위상을 함께 읽고 Hz와 rad/s를 구분한다. [ADI의 AC sweep 설명](https://www.analog.com/en/resources/technical-articles/ltspice-ac-analysis-using-the-step-command.html)

Spectre/ADE에서 재현할 때는 공정 모델·corner·온도·전원·부하를 고정하고 DC 동작점과 소자 영역을 먼저 저장한다. 이어 입력 AC magnitude를 설정하고 예상 pole을 충분히 포함하는 logarithmic sweep에서 $V(out)/V(in)$을 측정한다. 입력이 여러 개라면 다른 입력의 AC 자극을 0으로 설정한다. 수렴을 위해 강제한 초기조건이 실제 동작점을 대신하지 않는지도 확인한다. Cadence의 동작점 설명 역시 소신호 해석 전에 올바른 동작점을 얻어야 한다는 점을 강조한다. [Cadence 기술 답변](https://community.cadence.com/cadence_technology_forums/f/custom-ic-design/49506/dc-operating-point-for-different-analyses/1379372)

### 구현과 독립 검증

`cs_gain`은 위 KCL의 복소수 해를 직접 계산한다. 검산은 DC 병렬저항, pole의 −3 dB 조건, 여러 주파수의 KCL 잔차를 따로 확인한다. 비선형 제곱 법칙을 별도로 전개하여 선형 근사의 잔차가 입력 변화의 제곱에 비례하는지도 검사한다. 따라서 단순히 같은 식을 두 번 호출하는 비교가 아니다.

실제 회로에서는 작은 sine transient의 기본파 이득을 AC 결과와 비교하고 진폭을 절반으로 줄이며 차이가 줄어드는지 확인할 수 있다. 최대 시간 간격과 안정화 시간을 바꿔 수치 오차도 분리한다. Python 검산은 이 참조 모델의 확인이며 Spectre 실행, PDK 검증, noise·stability·공정 편차 분석을 대신하지 않는다.

## English

### Why begin with a small change?

A transistor does not generally double its output when its input doubles. A sufficiently narrow neighborhood of an operating point can nevertheless be approximated by a line. Small-signal analysis uses that local slope to calculate gain and frequency response; it does not remove large-signal clipping or distortion. [MIT 6.012 Lecture 19](https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-fall-2005/7a51249eb734152c5ce95df393cf4f1f_lec19.pdf)

DC analysis first finds Q, where the static circuit equations satisfy $F(v_Q)=0$. Taylor expansion gives $F(v_Q+\delta v)\approx F(v_Q)+J_Q\delta v$. Changing bias changes the Jacobian and therefore the AC response. For a MOSFET,

$$\delta i_D=g_m\delta v_{GS}+g_{ds}\delta v_{DS}+g_{mb}\delta v_{BS},\quad
g_m=\left.\partial I_D/\partial V_{GS}\right|_Q,\quad r_o=1/g_{ds}.$$

Conductances have units S=A/V; $r_o$ is in Ω. An independent ideal constant DC voltage source becomes a small-signal short: the incremental voltage difference between its terminals is zero. The other terminal becomes AC ground only if one terminal is grounded; a floating voltage source does not ground both terminals. An independent ideal constant DC current source becomes a small-signal open circuit, and dependent sources remain.

### Deriving a one-pole common-source model

Assume an AC-grounded source and bulk, an ideal gate-voltage drive, drain resistance $R_D$, device resistance $r_o$, load $R_L$, and lumped output capacitance $C_o$. Input feedback through $C_{gd}$ is omitted. Output KCL is

$$g_mv_i+(1/R_D+1/r_o+1/R_L+sC_o)v_o=0.$$

With $R=R_D\parallel r_o\parallel R_L$,

$$A_v(s)=-g_mR/(1+sRC_o),\qquad f_p=1/(2\pi RC_o).$$

The negative sign represents inversion. At the pole, magnitude is $1/\sqrt2$ of its low-frequency value, with an additional 45° phase lag. This simplified output model does not include every transistor capacitance. Adding input driving-source resistance and $C_{gd}$ introduces Miller feedback and potentially additional poles and zeros. [MIT Lecture 23](https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-fall-2005/44ed13d9b5e46dd459d9bca431fc547a_lec23.pdf)

For $g_m=1$ mS, $R_D=10$ kΩ, $r_o=R_L=100$ kΩ and $C_o=20$ pF, $R=8.333$ kΩ, DC gain is −8.333 and the pole is about 0.955 MHz. These are illustrative model parameters, not measured process performance.

### AC magnitude 1 does not establish a 1 V linear range

AC analysis solves a linearized circuit for complex voltages and currents. Setting the input AC magnitude to 1 makes the output numerically equal to the transfer function, but says nothing about linear behavior at a physical 1 V amplitude. Read $20\log_{10}|v_o/v_i|$ together with phase, and distinguish Hz from rad/s. [ADI AC sweeps](https://www.analog.com/en/resources/technical-articles/ltspice-ac-analysis-using-the-step-command.html)

To reproduce the analysis in Spectre/ADE, fix the process model, corner, temperature, supplies and load; save the DC operating point and device regions. Configure the input AC magnitude and a logarithmic sweep spanning the expected pole, measuring $V(out)/V(in)$. Set unrelated AC inputs to zero. Forced initial conditions must not substitute for a physically valid operating point. Cadence's technical explanation makes the same operating-point distinction. [Cadence response](https://community.cadence.com/cadence_technology_forums/f/custom-ic-design/49506/dc-operating-point-for-different-analyses/1379372)

### Implementation and independent checks

`cs_gain` solves the stated KCL in complex arithmetic. Tests independently check parallel-resistance DC gain, the −3 dB pole condition, and KCL residuals at several frequencies. A separate expansion of a nonlinear square law checks that the linearization residual scales with the square of input amplitude.

For a real circuit, compare the fundamental gain from a small-sine transient against AC analysis, then halve the amplitude. Vary timestep and settling duration to separate numerical error. The Python checks validate this reference model; they do not constitute a Spectre run, PDK validation, or noise, stability and process-variation analysis.

## 출처 대조 / Source cross-check

MIT의 소신호 KCL·주파수 모델을 ADI의 AC sweep 정의, Cadence의 동작점 설명과 대조했다. / MIT's small-signal equations were cross-checked against ADI's AC-sweep definition and Cadence's operating-point explanation. 확인 / checked: 2026-10-19.
