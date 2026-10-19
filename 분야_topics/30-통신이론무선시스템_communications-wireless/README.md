# 통신이론과 무선 시스템 | Communication Systems & Information Theory

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

통신 시스템은 정보를 신호에 실어 채널을 거쳐 전달한다. 변조는 정보를 파형의 진폭·위상·주파수 등에 대응시키고, 수신기는 채널과 잡음의 영향을 받은 신호에서 정보를 복원한다.

## 변조, 부호화, 채널

QAM은 진폭과 위상을 함께 이용하는 변조 방식이다. 높은 차수의 변조는 심볼당 정보를 늘리지만 같은 오류율을 얻는 데 더 좋은 신호 품질이 필요할 수 있다. 오류정정부호는 데이터에 구조를 더해 전송 오류를 복구한다. LDPC·Polar code는 대표적인 부호 계열이다.

Shannon 용량의 대표적인 AWGN 모델은 `C = B*log2(1+SNR)`이다. 여기서 SNR은 선형 비율이며, 이 식은 주어진 모델에서 신뢰할 수 있는 통신의 이론적 한계를 나타낸다. 실제 데이터율에는 변조·부호화·오버헤드·규격 조건이 추가된다.

## 다중 반송파와 다중 안테나

OFDM은 여러 직교 부반송파를 사용하고, MIMO는 여러 송수신 안테나의 공간 채널을 이용한다. 시간·주파수 동기와 채널 추정은 수신 성능을 결정하는 요소다. BER은 비트 오류 비율이며 SNR에 따른 BER 곡선은 통신 방식 비교에 쓰인다. GNU Radio·USRP 같은 SDR 생태계는 신호처리 블록을 실제 무선 입출력과 연결한다.

## 관련 기술

GNU Radio, SDR, USRP, RTL-SDR, OFDM, QAM, MIMO, LDPC, Polar Codes

## 참고 자료

- [GNU Radio documentation](https://www.gnuradio.org/doc/)

## 기초 해설

- [잡음 속에서 bit를 고르기: BPSK, Eb/N0와 BER](해설_notes/잡음속에서bit를고르기_bpsk-awgn-ber.md)

## English

### Communication theory and wireless systems

A communication system carries information in a signal through a channel. Modulation maps information to properties such as amplitude, phase, or frequency. The receiver recovers that information after the channel and noise have affected the signal.

### Modulation, coding, and channels

QAM uses amplitude and phase together. Higher-order modulation carries more information per symbol, but can require better signal quality to reach the same error rate. Error-correcting codes add structure that allows a receiver to recover from transmission errors. LDPC and polar codes are two major code families.

For a common AWGN channel model, Shannon capacity is `C = B*log2(1+SNR)`. SNR is a linear ratio in this expression. The equation gives the theoretical limit of reliable communication under that model; practical data rates also depend on modulation, coding, overhead, and the relevant standard.

### Multicarrier and multiple-antenna systems

OFDM uses orthogonal subcarriers, while MIMO uses spatial channels between multiple transmit and receive antennas. Timing and frequency synchronization, together with channel estimation, shape receiver performance. BER is the fraction of erroneous bits, and BER-versus-SNR curves help compare communication schemes. SDR tools such as GNU Radio and USRP connect signal-processing blocks to real radio input and output.

### Foundation article

- [잡음 속에서 bit를 고르기: BPSK, Eb/N0와 BER](해설_notes/잡음속에서bit를고르기_bpsk-awgn-ber.md#english)
