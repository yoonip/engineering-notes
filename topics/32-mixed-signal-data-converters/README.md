# Mixed-Signal · ADC · DAC · Clock

[전체 목차](../../CATALOG.md) · [처음으로](../../README.md)

Mixed-signal 회로는 연속적인 아날로그 신호와 이산적인 디지털 표현을 연결한다. ADC는 아날로그 값을 코드로, DAC는 디지털 코드를 전압·전류 같은 물리량으로 변환한다.

## 샘플링과 양자화

샘플링은 시간 축을, 양자화는 크기 축을 이산화한다. 이상적인 N비트 ADC의 step 크기는 입력 범위를 `2^N`개 수준으로 나눈 값이다. 이상적인 양자화 모델과 full-scale 정현파 조건에서 SNR은 약 `6.02N + 1.76 dB`로 표현되지만 실제 잡음과 왜곡은 별도로 존재한다.

SAR는 비교와 이진 탐색을 이용한 변환, pipeline은 여러 단계를 통한 높은 처리율, delta-sigma는 oversampling과 noise shaping에 기반한다. 시간 인터리빙은 여러 변환기를 나누어 사용하며 채널 간 offset·gain·timing 차이가 오차를 만든다.

## 정적·동적 지표와 클록

INL·DNL은 정적 전달 특성의 비선형성을, SNDR·SFDR은 잡음·왜곡과 주파수 성분을 다룬다. ENOB는 SNDR을 이상적인 비트 수와 연결한 지표다. PLL·DLL·CDR은 클록의 주파수·위상·데이터 타이밍에 관여한다. Jitter는 시간 변동, phase noise는 위상 변동의 주파수 영역 표현과 관련된다.

## 관련 기술

SAR ADC, Delta-Sigma, DAC, PLL, DLL, CDR, Spectre, Verilog-AMS

## 참고 자료

- [Analog Devices technical resources](https://www.analog.com/en/resources.html)
