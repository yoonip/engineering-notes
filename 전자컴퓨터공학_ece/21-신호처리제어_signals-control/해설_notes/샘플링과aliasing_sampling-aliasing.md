# 샘플링과 aliasing: 숫자로 바꾼 뒤에는 되돌릴 수 없는 정보

[신호·제어](../README.md) · [기초부터 읽기](../../../공학기초_foundations/README.md) · [English](#english)

![sampling_aliasing](../../../예제_examples/공학기초_foundations/figures/sampling_aliasing.png)

서로 다른 두 코사인이 같은 표본을 만듭니다. 점은 1 kS/s 표본입니다. / Two different cosines share the same 1 kS/s samples.

직접 계산해 그린 원본 도표 · [생성 코드](../../../예제_examples/공학기초_foundations/make_figures.py). / Original plot calculated for these notes; [generation code](../../../예제_examples/공학기초_foundations/make_figures.py).

## 먼저 그림으로 생각하기

동영상을 찍을 때 빠르게 도는 바퀴가 느리게 돌거나 거꾸로 도는 것처럼 보이기도 합니다. 카메라는 움직임 전체가 아니라 일정한 순간의 장면만 기록하기 때문입니다. 센서와 ADC도 마찬가지입니다. 표본 사이에 어떤 일이 있었는지 알려면 신호의 변화 속도에 대한 조건이 필요합니다.

샘플링은 시간을 골라 값을 읽는 일이고, 양자화는 읽은 크기를 유한한 코드와 복원값에 대응시키는 일입니다. 그 대응 규칙이 항상 가장 가까운 정수로의 반올림인 것은 아닙니다. 표본율을 높이는 것과 ADC 비트 수를 늘리는 것은 서로 다른 문제를 해결합니다. [MIT의 sampling 강의 노트 pp.16-1–16-2](https://ocw.mit.edu/courses/res-6-007-signals-and-systems-spring-2011/8708ec068ebdea2c4ee2f38fad39fb83_MITRES_6_007S11_lec16.pdf)는 시간 표본과 연속 신호의 관계를, [TI TIPL 4304 발표 자료 pp.2–7](https://www.ti.com/content/dam/videos/external-videos/en-us/2/3816841626001/5831231183001.mp4/subassets/adcs-aliasing-and-anti-aliasing-filters-presentation-quiz.pdf)는 alias 주파수와 ADC 앞단 필터를 다룹니다.

![샘플링과 aliasing: 숫자로 바꾼 뒤에는 되돌릴 수 없는 정보 — 개념도 / Concept diagram](../../../그림자료_assets/도식_diagrams/sampling-aliasing.png)

[SVG](../../../그림자료_assets/도식_diagrams/sampling-aliasing.svg) · [그림 원본 / Diagram source](../../../그림자료_assets/도식_diagrams/sampling-aliasing.mmd)

이 문서의 그림은 설명을 위해 직접 구성했습니다.

## 정의와 수식

표본 간격을 $`T_s`$ [s], 표본율을 $`f_s=1/T_s`$ [Hz]라 두면 $`x[n]=x(nT_s)`$입니다. $`n`$은 정수이고 $`x[n]`$의 단위는 원래 신호와 같습니다. Hz와 rad/s를 혼동하지 않도록 각주파수는 $`\omega=2\pi f`$로 따로 씁니다.

코사인 $`x(t)=A\cos(2\pi ft+\phi)`$를 읽으면

$$
x[n]=A\cos(2\pi fn/f_s+\phi).
$$

$`f`$를 $`f+kf_s`$로 바꿔도 정수 $`k,n`$에 대해 위상이 $`2\pi kn`$만큼 달라질 뿐이므로 표본은 같습니다. 실수 코사인의 주파수 크기를 첫 Nyquist 구간으로 접으면

$$
f_a=\left\vert ((f+f_s/2)\bmod f_s)-f_s/2\right\vert ,\qquad 0\le f_a\le f_s/2.
$$

이는 주파수 크기입니다. 일반적인 사인·위상 표현까지 동일하게 쓰려면 부호와 위상 변화를 함께 추적해야 합니다. 예를 들어 위상 0인 900 Hz와 100 Hz 코사인은 1 kS/s에서 같은 숫자 열을 만듭니다. 표본만 보고 어느 쪽이 원래 신호였는지 구별할 수 없습니다.

대역이 $`\vert f\vert \le B`$로 제한된 이상적인 기저대역 신호는 $`f_s>2B`$일 때 이상적인 재구성이 가능합니다. 경계의 주파수 성분이나 위상까지 고려하면 단순히 등호를 넣는 것은 안전하지 않습니다. $`\sin(2\pi(f_s/2)n/f_s)=0`$이라는 반례가 있습니다. 이는 [MIT 강의 노트 §16](https://ocw.mit.edu/courses/res-6-007-signals-and-systems-spring-2011/8708ec068ebdea2c4ee2f38fad39fb83_MITRES_6_007S11_lec16.pdf)의 대역 제한 가정과 함께 읽어야 합니다.

## 모델과 구현

위상 0인 코사인을 생성하고 두 표본 열을 직접 비교합니다. [참조 구현](../../../예제_examples/공학기초_foundations/signals_ai/models.py)의 `sample_cosine`은 $`O(N)`$ 시간·출력 공간, `alias_frequency`는 고정 개수의 산술 연산을 사용합니다.

```python
from signals_ai.models import sample_cosine, alias_frequency  # from/import는 표본·alias 계산 함수를 가져옵니다.

high = sample_cosine(900.0, 1000.0, 100)  # 900 Hz를 1 kS/s로 읽은 표본 100개를 만듭니다.
low = sample_cosine(100.0, 1000.0, 100)  # 같은 표본율에서 100 Hz의 표본을 만듭니다.
print(max(abs(a - b) for a, b in zip(high, low)))  # zip으로 표본을 짝짓고 절댓값 차이의 최댓값을 출력합니다.
print(alias_frequency(900.0, 1000.0))  # 접힌 주파수 크기 100 Hz를 계산합니다.
```

`예제_examples/공학기초_foundations`를 작업 폴더로 사용하거나 그 폴더를 `PYTHONPATH`에 추가한 환경에서 실행합니다. 위 `from signals_ai.models ...`가 그 폴더 안의 패키지를 가리켜야 합니다. 운영체제별 실행 명령은 [예제 안내](../../../예제_examples/공학기초_foundations/README.md)에 있습니다.

## 검증과 현실의 차이

| 확인할 것 | 기준 |
| --- | --- |
| 900 Hz와 100 Hz 코사인의 동일 표본 | 100개 표본 최대 차이 $`<10^{-12}`$ |
| Nyquist 경계에서 정보 손실 | 위상 $`\pi/2`$인 코사인의 표본이 수치 오차 범위에서 0 |
| 주파수 접기 | 음수·여러 Nyquist 구간·DC를 포함해 범위와 예상값 검사 |

이 검사는 표본 계산을 확인합니다. 실제 ADC에서는 입력 대역, 아날로그 필터의 유한한 감쇠, aperture jitter, 샘플 유지 회로와 구동기의 settling도 확인해야 합니다. 디지털 필터는 이미 같은 숫자로 겹쳐 버린 두 성분을 일반적으로 분리하지 못합니다. 기저대역 설계에서는 원하는 대역 뒤에 필터 전이 대역을 두고, 접혀 들어올 대역 밖 성분이 요구 수준까지 감쇠되는지 확인합니다. `f_c<f_s/2`라는 조건 하나만으로 충분한 감쇠가 보장되지는 않습니다. [TI SBAA282B, 2024-09, pp.1–2](https://www.ti.com/lit/sbaa282)는 cutoff 외에 alias 입력 크기·허용 출력·ADC settling을 따로 정합니다. 대역통과 샘플링에는 별도 조건이 있으므로 기저대역의 $`2B`$ 규칙을 그대로 적용하지 않습니다.

## English

### Intuition and definitions

A filmed wheel can appear to turn slowly or backward because the camera records selected instants. An ADC also needs a condition on what can happen between observations. Sampling selects times; quantization maps amplitudes to a finite set. More samples and more bits solve different problems. The original diagram above separates analog band limiting, time sampling, quantization, and digital processing.

Let $`T_s`$ [s] be the interval and $`f_s=1/T_s`$ [Hz] the sample rate. Then $`x[n]=x(nT_s)`$, with integer $`n`$ and the original amplitude unit. Angular frequency is $`\omega=2\pi f`$ [rad/s]. For a cosine,

$$
x[n]=A\cos(2\pi fn/f_s+\phi).
$$

Adding an integer multiple of $`f_s`$ changes phase by $`2\pi kn`$, so it leaves the samples unchanged. Folding the frequency magnitude of a real cosine into the first Nyquist interval gives

$$
f_a=\left\vert ((f+f_s/2)\bmod f_s)-f_s/2\right\vert .
$$

This gives a magnitude; signed frequency and phase must also be tracked for a general sinusoid. At 1 kS/s, zero-phase 900 Hz and 100 Hz cosines give identical samples. The samples alone cannot identify the original frequency.

An ideally band-limited baseband signal with support $`\vert f\vert \le B`$ can be reconstructed ideally if $`f_s>2B`$. Equality is insufficient when a component lies exactly at the boundary: $`\sin(2\pi(f_s/2)n/f_s)=0`$ loses its amplitude information. The [MIT notes](https://ocw.mit.edu/courses/res-6-007-signals-and-systems-spring-2011/8708ec068ebdea2c4ee2f38fad39fb83_MITRES_6_007S11_lec16.pdf) support these assumptions and reconstruction conditions.

### Implementation and verification

The code above compares two generated sample sequences. `sample_cosine` takes $`O(N)`$ time and output storage; `alias_frequency` uses a fixed number of arithmetic operations. The [implementation](../../../예제_examples/공학기초_foundations/signals_ai/models.py) is checked by a maximum sequence difference below $`10^{-12}`$, a zero-valued boundary-frequency counterexample, and signed/multiple-zone frequency cases. See the [run instructions](../../../예제_examples/공학기초_foundations/README.md).

These tests verify sample calculations. A physical ADC also requires checks of input bandwidth, finite analog-filter attenuation, aperture jitter, sample-and-hold behavior and driver settling. A digital filter generally cannot separate components that already produced the same samples. A baseband design needs a transition band and adequate attenuation of out-of-band components that fold into the useful band; `f_c<f_s/2` alone is insufficient. [TI SBAA282B, September 2024, pp.1–2](https://www.ti.com/lit/sbaa282) specifies alias amplitude, allowable output and settling separately. Bandpass sampling requires its own conditions. Use `예제_examples/공학기초_foundations` as the working directory or Python import path for the existing example.

## 출처 / Sources

- [MIT OCW, Lecture 16: Sampling](https://ocw.mit.edu/courses/res-6-007-signals-and-systems-spring-2011/resources/lecture-16-sampling/) — 표본의 비유일성, 대역 제한, 재구성 / non-unique samples, band limitation, reconstruction.
- [TI Precision Labs TIPL 4304 발표 자료, pp.2–7](https://www.ti.com/content/dam/videos/external-videos/en-us/2/3816841626001/5831231183001.mp4/subassets/adcs-aliasing-and-anti-aliasing-filters-presentation-quiz.pdf) — alias 주파수·필터 감쇠·charge-bucket 회로 / alias frequency, attenuation and charge-bucket circuitry. 발표 자료를 읽었으며 동영상 전체 시청 기록은 아닙니다 / the slides were read; this is not a claim of viewing the full video.
- [TI SBAA282B, 2024-09, pp.1–2](https://www.ti.com/lit/sbaa282) — alias 크기·허용 오차·settling을 지정하는 SAR 입력 필터 설계 / SAR input filtering with explicit alias, tolerance and settling targets.

두 자료의 샘플링 조건을 대조하고, 위상 경계 반례와 동일 표본 계산으로 확인했습니다. / Sampling conditions were cross-checked against both sources and tested using a boundary-phase counterexample and identical sample sequences.
