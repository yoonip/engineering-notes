# 회로와 전자공학 | Circuits & Electronics

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

회로 모델은 소자와 연결 구조를 통해 전압·전류·전하의 관계를 나타냅니다. Kirchhoff 전류 법칙은 노드의 전하 보존, 전압 법칙은 회로 모델에서 폐경로의 전압 관계를 나타냅니다. 고주파·분포 회로에서는 배선의 전파 지연과 전자기장도 고려합니다.

## RLC와 시간·주파수 응답

저항은 전력을 소모하고, 커패시터는 전기장에, 인덕터는 자기장에 에너지를 저장합니다. RC 회로의 시정수는 `RC`, 이상적인 LC 공진의 각주파수는 `1/sqrt(LC)`입니다. 과도응답은 입력 변화 직후의 시간 동작, 주파수응답은 주파수에 따른 크기와 위상 변화를 보여줍니다.

## 능동 소자와 증폭

다이오드는 비선형 전류·전압 특성을 갖습니다. BJT·MOSFET은 바이어스에 따라 전류를 제어하고 신호를 증폭하거나 스위칭합니다. 연산증폭기 회로의 폐루프 동작은 피드백과 소자의 이득·대역폭·출력 범위에 영향을 받습니다. 이상적인 모델로 동작 원리를 이해하고, 실제 소자의 동작 범위와 제약을 함께 살펴봅니다.

필터는 신호의 주파수 성분을 선택하고, 발진기는 에너지를 공급받아 주기 신호를 만듭니다. 레귤레이터는 부하와 입력 변화에 대응해 전원을 유지합니다. 부품 오차·잡음·기생 성분·접지 경로는 회로도에서 생략되기 쉽지만 실제 성능을 좌우합니다.

## 관련 기술

RLC, Op-Amp, BJT, MOSFET, CMOS, Filters, Oscillators, Regulators, SPICE, Breadboard Measurements

## 참고 자료

- [MIT OCW — Circuits and Electronics](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/)


## 개념·유도·모델·검증

[기초부터 읽기](../../공학기초_foundations/README.md)

- [RC·RLC: 회로 법칙에서 시간·주파수 응답까지](해설_notes/rc-rlc-response.md)

## English

A circuit models the relationships between voltage, current, and charge through devices and their connections. Kirchhoff's current law expresses charge conservation at a node, and the voltage law describes the voltage relationship around a closed path in a circuit model. High-frequency and distributed circuits also involve propagation delay and electromagnetic fields.

### RLC circuits in time and frequency

Resistors dissipate power, capacitors store energy in electric fields, and inductors store energy in magnetic fields. An RC circuit has a time constant of `RC`; an ideal LC circuit has a resonant angular frequency of `1/sqrt(LC)`. A transient response describes behavior after an input change, while a frequency response shows gain and phase across frequency.

### Active devices and amplification

A diode has a nonlinear current-voltage characteristic. BJT and MOSFET operation depends on bias, allowing current control, amplification, and switching. An op-amp circuit's closed-loop behavior depends on feedback and the device's gain, bandwidth, and output range. Idealized models help explain operation, while device limits determine the available operating range.

Filters select frequency components. Oscillators use supplied energy to sustain periodic signals, and regulators maintain a supply as input and load conditions change. Component tolerances, noise, parasitics, and ground paths can strongly affect performance even when they are absent from the schematic.


### Concepts, derivations, models, and verification

[Foundations reading guide](../../공학기초_foundations/README.md#english)

- [RC/RLC laws and response](해설_notes/rc-rlc-response.md#english)


## 심화 해설 | Advanced article

- [회로를 행렬로 풀기: Modified Nodal Analysis](해설_notes/회로를행렬로풀기_mna.md) · [English](해설_notes/회로를행렬로풀기_mna.md#english)
