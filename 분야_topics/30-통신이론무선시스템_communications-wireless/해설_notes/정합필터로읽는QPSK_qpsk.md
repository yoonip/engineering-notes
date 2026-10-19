# 정합필터로 읽는 QPSK: 에너지와 잡음의 눈금 맞추기

[통신 이론 목차](../README.md) · [시뮬레이션](../../../예제_examples/심화_advanced/hardware/models.py) · [검산](../../../예제_examples/심화_advanced/hardware/test_models.py)

## 한국어

### 두 방향에서 각각 한 비트를 고른다

QPSK는 한 심벌에 두 비트를 싣는다. 직교하는 I와 Q 방향에서 각각 + 또는 −를 고르면 네 점을 만들 수 있다. 같은 총 심벌 에너지를 네 점에 나눈다는 말과, 비트 에너지를 고정한다는 말은 다르다. BER을 비교할 때 이 눈금을 맞추지 않으면 3 dB 차이 같은 잘못된 결과를 얻는다.

여기서는 coherent detection, 완전한 carrier·symbol timing, AWGN, Gray mapping, 부호화 없는 전송을 가정한다. 두 비트가 I와 Q의 부호에 하나씩 대응하므로 인접 점은 한 비트만 다르다. [MIT 통신 강의의 signal-space·Gaussian 판정](https://ocw.mit.edu/courses/16-36-communication-systems-engineering-spring-2009/ecba60e6759f2eb6683f340cc5fed6b2_MIT16_36s09_lec11.pdf)과 [MathWorks berawgn 수식](https://www.mathworks.com/help/comm/ug/analytical-expressions-used-in-berawgn-function-and-bit-error-rate-analysis-app.html)을 대조한다.

### 단위 에너지 pulse와 matched filter

L개의 실수 표본으로 pulse를 $`p_k=1/\sqrt L`$로 정하면 $`\sum p_k^2=1`$이다. 각 축에서 amplitude a=±1을 보내면 축 에너지가 1, 두 축을 합친 심벌 에너지는 Es=2, 비트 에너지는 Eb=1이다. 각 표본의 독립 잡음 분산은 N0/2로 둔다. 이 discrete orthonormal 모델의 표본을 실제 전압·sample rate에 바로 대응시키는 것은 별도 정규화가 필요하다.

```math
r_k=a p_k+n_k,\qquad z=\sum_kp_kr_k
=a+\sum_kp_kn_k.
```

정합필터 출력의 신호는 a다. 잡음은 독립이므로 분산이 더해진다.

```math
\mathrm{Var}(z)=\sum_kp_k^2\frac{N_0}{2}=\frac{N_0}{2}.
```

표본 수가 늘어도 pulse 에너지를 1로 고정했으므로 decision SNR이 저절로 좋아지지 않는다. L개 평균이 잡음을 줄인다고만 생각하면서 송신 에너지 증가를 빠뜨리는 것이 흔한 정규화 오류다.

### 판정 확률에서 BER·SER까지

0을 기준으로 부호를 판정한다. $`\gamma_b=E_b/N_0`$이고 Eb=1이면 noise 표준편차는 $`\sigma=\sqrt{1/(2\gamma_b)}`$다. 한 축의 판정 오류는 Gaussian tail에서 얻는다.

```math
P_b=Q\left(\sqrt{2\gamma_b}\right)
=\frac12\mathrm{erfc}(\sqrt{\gamma_b}),
\qquad P_s=1-(1-P_b)^2=2P_b-P_b^2.
```

마지막 식은 I·Q 잡음과 판정 오류가 독립일 때 성립한다. 이 Gray QPSK의 BER은 같은 Eb/N0의 coherent BPSK와 같다. 같은 Es/N0를 놓고 비교하면 QPSK의 비트당 에너지는 Es/2이므로 조건이 달라진다. 0 dB에서 이론 BER은 약 0.07865, SER은 약 0.1511이다. BER과 SER을 서로 같은 지표로 쓰지 않는다.

### 구현과 통계 검산

```bash
python demo.py --case qpsk
python -m unittest -v test_models.HardwareModels.test_qpsk_energy_and_symbol_relation test_models.HardwareModels.test_qpsk_monte_carlo
```

`qpsk_simulate()`는 각 I/Q pulse 표본에 Gaussian 잡음을 더하고 내적 후 부호를 판정한다. 난수 seed를 고정해 실행을 재현한다. 0·4 dB에서 각각 20000심벌을 보내 이론 BER·SER과 비교한다. 표본 비율의 표준오차 $`\sqrt{p(1-p)/N}`$보다 넓은 6배 경계로 검사하며, BER은 N=40000비트, SER은 N=20000심벌이다. 통계 경계의 통과는 모든 난수 실행의 보장이 아니다.

오류가 한 번도 안 나와도 BER이 0임을 증명한 것은 아니다. 높은 SNR에서 작은 BER을 정밀하게 추정하려면 충분한 오류 수나 신뢰구간·importance sampling 같은 추가 방법이 필요하다. 실제 무선에서는 pulse shaping, timing error, carrier offset, phase noise, IQ imbalance, multipath와 channel estimation을 모델에 추가한다. 여기서 확인한 것은 baseband AWGN Monte Carlo와 이론식의 일치이며 RF 장비 측정이 아니다.

## English

### Two binary decisions in orthogonal directions

QPSK carries two bits per symbol by choosing the signs of orthogonal I and Q components. Fixing symbol energy and fixing bit energy are different comparisons; inconsistent normalization can introduce an erroneous 3 dB shift. Each bit selects one axis sign, giving Gray mapping between neighboring constellation points.

Assume coherent detection, perfect carrier and timing recovery, uncoded transmission and AWGN. Signal-space detection is checked against [MIT's communication lecture](https://ocw.mit.edu/courses/16-36-communication-systems-engineering-spring-2009/ecba60e6759f2eb6683f340cc5fed6b2_MIT16_36s09_lec11.pdf), with QPSK error expressions independently checked against [MathWorks berawgn documentation](https://www.mathworks.com/help/comm/ug/analytical-expressions-used-in-berawgn-function-and-bit-error-rate-analysis-app.html).

### Matched-filter energy and noise

Choose an L-sample real pulse pk=1/sqrt(L), so its squared samples sum to one. Sending amplitude ±1 on each axis gives axis energy one, symbol energy two and bit energy one. Independent real sample noise has variance N0/2. These are normalized discrete orthonormal coordinates; mapping them to voltage and sampling rate requires an additional physical normalization.

The matched-filter statistic is the pulse inner product with received samples: $`z=\sum p_kr_k=a+\sum p_kn_k`$. Independent noise gives variance $`\sum p_k^2N_0/2=N_0/2`$. Increasing L therefore does not improve decision SNR when pulse energy remains fixed. Averaging arguments that ignore an accompanying change in transmit energy give the wrong comparison.

### Deriving BER and SER

With Eb=1 and gamma_b=Eb/N0, the per-axis noise deviation is sqrt(1/(2 gamma_b)). A zero-threshold sign decision gives $`P_b=Q(\sqrt{2\gamma_b})=\mathrm{erfc}(\sqrt{\gamma_b})/2`$. Independent I/Q errors yield $`P_s=1-(1-P_b)^2`$.

Gray coherent QPSK therefore has the same BER as coherent BPSK at the same Eb/N0. A comparison at equal Es/N0 uses different per-bit energies because QPSK has Eb=Es/2. At 0 dB the BER is about 0.07865 and SER about 0.1511; they are distinct measures.

### Executable statistical validation and limits

The commands above run seeded pulse-sample Monte Carlo and theory checks. At 0 and 4 dB, each test transmits 20000 symbols and compares measured error proportions with theory using six standard errors. BER uses 40000 bits; SER uses 20000 symbols. Fixed seeds make the run reproducible, but the statistical tolerance does not guarantee every random run passes.

Observing zero errors does not prove a zero underlying BER. Very small error rates require adequate error counts, confidence bounds or suitable advanced estimation. A physical wireless model also needs pulse shaping, timing and carrier errors, phase noise, IQ imbalance, multipath and channel estimation. This execution verifies normalized baseband AWGN simulation against theory, not RF hardware measurements.

## 출처 / Sources

- MIT, *16.36 Lecture 11*: signal-space detection and Gaussian error tails.
- MathWorks, *Analytical Expressions Used in berawgn*: coherent QPSK BER and SER. Both sources are linked above.
