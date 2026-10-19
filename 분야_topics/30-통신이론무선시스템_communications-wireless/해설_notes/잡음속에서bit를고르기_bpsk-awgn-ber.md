# 잡음 속에서 bit를 고르기: BPSK, Eb/N0와 BER

[통신과 무선](../README.md) · [참조 모델](../../../예제_examples/확장기초_extended/hardware/models.py) · [검산](../../../예제_examples/확장기초_extended/hardware/test_models.py)

## 한국어

### 두 점 중 어느 쪽에 가까운가

BPSK는 두 bit를 서로 반대 위상의 신호로 보낸다. 수신기가 carrier 위상과 symbol timing을 정확히 알고 matched filter로 신호를 모았다면, 한 bit의 판단을 실수축의 두 점 중 하나를 고르는 문제로 줄일 수 있다. AWGN은 신호에 더해지는 white Gaussian noise다. 여기서는 uncoded bit가 독립·동일 확률이며 동기 오차, fading, 간섭이 없는 coherent 검출만 다룬다. [MIT 16.36 Lecture 11](https://ocw.mit.edu/courses/16-36-communication-systems-engineering-spring-2009/ecba60e6759f2eb6683f340cc5fed6b2_MIT16_36s09_lec11.pdf)

정규직교 basis에 투영한 송신값을 $`x\in\{-\sqrt{E_b},+\sqrt{E_b}\}`$라 두면 수신 통계량은

$$y=x+n,\qquad n\sim\mathcal N(0,N_0/2).$$

$`E_b`$는 bit 에너지(J), $`N_0`$는 잡음 전력 스펙트럼 밀도 계수(W/Hz=J)다. 실수 passband noise의 two-sided PSD를 $`N_0/2`$로 정의했을 때 unit-energy basis에 투영한 분산이 $`N_0/2`$가 된다. 따라서 $`\gamma_b=E_b/N_0`$는 무차원 비율이다.

### Gaussian 꼬리에서 오류 확률 유도

두 bit의 사전확률과 비용이 같으면 threshold는 0이다. $`+\sqrt{E_b}`$를 보냈는데 $`y<0`$이면 오류이므로

$$P_b=P\{n<-\sqrt{E_b}\}=Q\left(\sqrt{2E_b/N_0}\right)
=\frac12\mathrm{erfc}(\sqrt{\gamma_b}),$$

$$Q(z)=\frac1{\sqrt{2\pi}}\int_z^\infty e^{-u^2/2}\,du.$$

반대 bit에도 같은 확률이 적용된다. BPSK는 symbol당 bit가 하나여서 이 조건의 BER와 SER가 같다. 이 식은 differential encoding이나 fading 채널에 그대로 적용하지 않는다. [MathWorks의 BPSK 이론식](https://www.mathworks.com/help/comm/ug/analytical-expressions-used-in-berawgn-function-and-bit-error-rate-analysis-app.html)

| $`E_b/N_0`$ (dB) | 선형 비율 | 이론 BER(근삿값) |
|---|---|---|
| 0 | 1 | 0.07865 |
| 4 | 2.5119 | 0.01250 |
| 8 | 6.3096 | 0.0001909 |

dB 입력은 $`\gamma_b=10^{dB/10}`$로 바꾼 뒤 제곱근을 취한다. $`E_b=1`$로 정규화했다면 simulation noise의 표준편차는 $`\sigma=1/\sqrt{2\gamma_b}`$다. 분산과 표준편차를 혼동하거나 complex noise의 각 성분과 총 전력을 혼동하면 BER 곡선이 이동한다. Sample SNR와 $`E_b/N_0`$도 sampling rate·bits/symbol·pulse 정규화·code rate를 정하지 않으면 같은 수치가 아니다.

### 오류를 몇 개 보아야 하는가

N bit 중 오류 K개라면 추정량은 $`\hat p=K/N`$이다. 독립 Bernoulli 모델에서 $`K\sim Binomial(N,p)`$이고 $`Var(\hat p)=p(1-p)/N`$다. 이론 p가 작을수록 같은 상대 오차를 얻으려면 더 긴 실행이 필요하다. 기대 오류 수가 작을 때 정규근사의 신뢰구간을 무조건 사용하지 않는다.

오류 0개가 BER 0의 증거는 아니다. 독립성 가정에서 $`P(K=0)=(1-p)^N`$이므로 95% 단측 상한은 $`p_{upper}=1-0.05^{1/N}\approx3/N`$이다. Fading이나 burst error처럼 오류가 상관되어 있다면 이 단순 binomial 해석부터 재검토해야 한다.

### 구현과 독립 검증

`bpsk_ber`는 `erfc`로 이론값을 계산하고, `bpsk_errors`는 임의의 ±1 symbol에 실수 Gaussian noise를 더해 threshold 0으로 판정한다. 후자는 bit 단위 matched-filter 출력 모델이지 oversampled RF 파형이나 실제 송수신기 모델은 아니다. 시간은 O(N), 누적 오류 수만 보관하면 추가 공간은 O(1)이다.

검산은 Gaussian tail을 별도 Simpson 적분으로 계산해 이론 함수와 대조한다. 이어 0·4·8 dB에서 각 200,000 bit를 정해진 seed로 실행하고 오류 수가 binomial의 이론 평균에서 6표준편차+1 이내인지 확인한다. 넓은 허용 폭은 난수 검사의 불필요한 실패를 줄이기 위한 수치 기준이며 매 실행이 특정 신뢰수준을 보증한다는 선언은 아니다.

실제 통신 검증에서는 pulse shaping·matched filter의 에너지, 위상·주파수·timing 복구, coding 전후의 bit 기준, error counter의 정렬을 먼저 맞춘다. 채널과 RF impairment를 추가할 때마다 이 이상적 AWGN 기준과 차이를 분리한다. 위 결과는 수치 simulation이며 무선 장비 측정 수치가 아니다.

## English

### Selecting one of two points

BPSK assigns bits to opposite phases. With correct carrier phase, symbol timing and matched filtering, detection reduces to choosing between two points on a real axis. AWGN is additive white Gaussian noise. This article assumes independent equiprobable uncoded bits, coherent detection, and no fading, interference or synchronization error. [MIT 16.36 Lecture 11](https://ocw.mit.edu/courses/16-36-communication-systems-engineering-spring-2009/ecba60e6759f2eb6683f340cc5fed6b2_MIT16_36s09_lec11.pdf)

Projection onto a unit-energy basis gives $`y=x+n`$, where $`x=\pm\sqrt{E_b}`$ and $`n\sim\mathcal N(0,N_0/2)`$. Bit energy $`E_b`$ is in J, and $`N_0`$ has units W/Hz=J. With real passband two-sided noise PSD $`N_0/2`$, that projection has variance $`N_0/2`$. Consequently $`\gamma_b=E_b/N_0`$ is dimensionless.

### Deriving BER from a Gaussian tail

Equal priors and costs place the threshold at zero. Sending $`+\sqrt{E_b}`$ causes an error when $`n<-\sqrt{E_b}`$:

$$P_b=Q(\sqrt{2\gamma_b})=\tfrac12\mathrm{erfc}(\sqrt{\gamma_b}),\qquad
Q(z)=\frac1{\sqrt{2\pi}}\int_z^\infty e^{-u^2/2}du.$$

The other bit has the same error probability. BPSK carries one bit per symbol, so BER equals SER under these assumptions. Differential encoding and fading need different expressions. [MathWorks BPSK expression](https://www.mathworks.com/help/comm/ug/analytical-expressions-used-in-berawgn-function-and-bit-error-rate-analysis-app.html)

At 0/4/8 dB, linear ratios are 1/2.5119/6.3096 and theoretical BERs are about 0.07865/0.01250/0.0001909. Convert dB by $`10^{dB/10}`$ before taking square roots. For normalized $`E_b=1`$, noise standard deviation is $`1/\sqrt{2\gamma_b}`$. Confusing variance with standard deviation, or a complex component's power with total noise power, shifts the BER curve. Sample SNR and $`E_b/N_0`$ also require sampling rate, bits per symbol, pulse normalization and code rate before comparison.

### How many errors establish precision?

For K errors in N bits, $`\hat p=K/N`$. Under independent Bernoulli trials, $`K\sim Binomial(N,p)`$ and $`Var(\hat p)=p(1-p)/N`$. Smaller p requires more bits for the same relative precision. Normal-approximation intervals are inappropriate when expected errors are too few.

Zero observed errors do not establish zero BER. Since $`P(K=0)=(1-p)^N`$, the 95% one-sided upper bound is $`1-0.05^{1/N}\approx3/N`$. Correlated fading or burst errors invalidate the simple independent-trial interpretation.

### Implementation and independent validation

`bpsk_ber` evaluates the analytic expression through `erfc`. `bpsk_errors` generates ±1 symbols, adds real Gaussian noise and thresholds at zero. It models matched-filter samples, not oversampled RF waveforms or a complete receiver. Runtime is O(N), with O(1) extra space when only counting errors.

Tests independently integrate the Gaussian tail by Simpson's method. They then simulate 200,000 bits at each of 0, 4 and 8 dB with fixed seeds and compare counts against the binomial mean using a six-standard-deviation-plus-one tolerance. This broad numerical check reduces random test fragility; it is not a promise of a specified confidence level for every run.

Real-system validation must align pulse/filter energy, phase/frequency/timing recovery, pre-/post-coding bit definitions and counters. Add channel and RF impairments separately and compare against the ideal AWGN baseline. These results are numerical simulations, not radio measurements.

## 출처 대조 / Source cross-check

MIT의 matched-filter 검출·Gaussian tail 유도와 MathWorks의 uncoded BPSK 식을 대조했다. / MIT's detection derivation was cross-checked against MathWorks's uncoded BPSK formula. 확인 / checked: 2026-10-19.
