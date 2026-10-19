# 혼성신호·ADC·DAC·클록 | Mixed-Signal, Data Converters & Clocks

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

Mixed-signal 회로는 연속적인 아날로그 신호와 이산적인 디지털 표현을 연결한다. ADC는 아날로그 값을 코드로, DAC는 디지털 코드를 전압·전류 같은 물리량으로 변환한다.

## 샘플링과 양자화

샘플링은 시간을 일정한 간격으로 나누고, 양자화는 신호의 크기를 정해진 단계로 표현한다. 이상적인 N비트 ADC의 step 크기는 입력 범위를 `2^N`개 수준으로 나눈 값이다. 이상적인 양자화 모델과 full-scale 정현파 조건에서 SNR은 약 `6.02N + 1.76 dB`로 표현된다. 실제 회로에서는 다른 잡음과 왜곡도 더해진다.

SAR는 비교와 이진 탐색을 이용한 변환, pipeline은 여러 단계를 통한 높은 처리율, delta-sigma는 oversampling과 noise shaping에 기반한다. 시간 인터리빙은 변환 작업을 여러 변환기에 나누어 맡기며 채널 간 offset·gain·timing 차이가 오차를 만든다.

## 정적·동적 지표와 클록

INL·DNL은 정적 전달 특성의 비선형성을, SNDR·SFDR은 잡음·왜곡과 주파수 성분을 다룬다. ENOB는 SNDR을 이상적인 비트 수와 연결한 지표다. PLL·DLL·CDR은 클록의 주파수·위상·데이터 타이밍에 관여한다. Jitter는 시간 변동, phase noise는 위상 변동의 주파수 영역 표현과 관련된다.

## 관련 기술

SAR ADC, Delta-Sigma, DAC, PLL, DLL, CDR, Spectre, Verilog-AMS

## 참고 자료

- [Analog Devices technical resources](https://www.analog.com/en/resources.html)


## 개념·유도·모델·검증

[기초부터 읽기](../../문서_docs/공학기초_FOUNDATIONS.md)

- [ADC 양자화: 비트 수와 정확도를 구분하기](해설_notes/ADC양자화_adc-quantization.md)

## English

### Mixed-signal circuits, ADCs, DACs, and clocks

Mixed-signal circuits connect continuous analog signals with discrete digital representations. An ADC converts an analog value to a code. A DAC converts a digital code to a physical quantity such as voltage or current.

### Sampling and quantization

Sampling discretizes time; quantization discretizes amplitude. The step size of an ideal N-bit ADC is its input range divided into `2^N` levels. Under the ideal quantization model and a full-scale sinusoidal input, SNR is approximately `6.02N + 1.76 dB`. Real converters have additional noise and distortion.

SAR conversion uses comparisons and binary search. Pipeline ADCs use multiple stages for high throughput, while delta-sigma ADCs use oversampling and noise shaping. Time-interleaved converters divide the work among channels, where offset, gain, and timing mismatches introduce errors.

### Static and dynamic metrics, and clocking

INL and DNL describe static transfer nonlinearity. SNDR and SFDR describe noise, distortion, and spectral components. ENOB expresses SNDR as an equivalent ideal bit count. PLLs, DLLs, and CDR circuits control clock frequency, phase, and data timing. Jitter describes timing variation, while phase noise describes phase fluctuations in the frequency domain.

Related technologies include SAR and delta-sigma ADCs, DACs, PLLs, DLLs, CDR, Spectre, and Verilog-AMS.


### Concepts, derivations, models, and verification

[Foundations reading guide](../../문서_docs/공학기초_FOUNDATIONS.md#english)

- [ADC quantization and resolution](해설_notes/ADC양자화_adc-quantization.md#english)
