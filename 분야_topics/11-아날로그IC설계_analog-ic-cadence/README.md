# 아날로그 IC 설계·Cadence·Spectre | Analog IC Design: Cadence & Spectre

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

아날로그 IC는 소자의 전기적 특성을 이용해 신호를 증폭·비교·변환하고 기준 전압과 클록을 만든다. 회로도에서 정한 소자 크기와 바이어스가 레이아웃·기생 성분·공정 변동을 거쳐 어떤 성능을 내는지 연결해 본다.

## 도구의 역할

Cadence의 Virtuoso는 custom IC의 회로도·레이아웃 설계 환경, Spectre는 회로 시뮬레이터, ADE는 테스트 조건과 해석·결과를 관리하는 환경이다. SKILL은 Virtuoso 환경의 확장과 자동화에, OCEAN은 시뮬레이션과 결과 처리 자동화에 쓰인다. Synopsys Custom Compiler·PrimeSim·HSPICE, Siemens Eldo도 관련 설계·해석 생태계다. LTspice·ngspice·Xschem은 회로 해석과 회로도 작업에서 만나는 도구다.

## 해석이 알려주는 것

DC 해석은 바이어스와 동작점을, AC 해석은 동작점 주변의 소신호 주파수응답을, transient 해석은 시간에 따른 비선형 동작을 구한다. Noise 해석은 모델에 포함된 잡음의 기여를 본다. Corner는 대표적인 모델·환경 조건을, Monte Carlo는 통계적 변동을 다루며 두 분석의 목적은 다르다.

## 회로도에서 레이아웃으로

증폭기는 이득·대역폭·안정도·잡음·소비전력을 함께 고려한다. 비교기·기준 회로·ADC·DAC·PLL은 응용에 따라 속도·정확도·전력의 우선순위가 달라진다. Verilog-A는 아날로그 동작 모델, Verilog-AMS는 아날로그와 디지털을 함께 다루는 모델링에 사용된다.

DRC는 제조 규칙, LVS는 회로도와 레이아웃의 연결·소자 일치, PEX는 기생 성분 추출을 다룬다. 추출 후 시뮬레이션은 배선과 소자 주변 구조의 영향을 포함한다. 회로 데이터와 PDK는 서로 다른 배포·사용 조건을 가질 수 있다.

## 관련 기술

Cadence Virtuoso, Spectre, ADE, SKILL, OCEAN, Synopsys Custom Compiler, HSPICE, PrimeSim, Siemens Eldo, LTspice, ngspice, Xschem

## 참고 자료

- [Cadence Circuit Simulation](https://www.cadence.com/en_US/home/tools/custom-ic-analog-rf-design/circuit-simulation.html)

## 기초 해설

- [동작점에서 주파수 응답까지: 소신호와 AC 해석](해설_notes/동작점에서주파수응답까지_small-signal-ac-operating-point.md)

## English

Analog IC design uses device behavior to amplify, compare, and convert signals, and to generate reference voltages and clocks. It connects schematic choices such as device sizing and bias with the effects of layout, parasitics, and process variation.

### Tool roles

Cadence is the vendor. Virtuoso is a custom IC schematic and layout environment, Spectre is a circuit simulator, and ADE manages test conditions, analyses, and results. SKILL extends and automates the Virtuoso environment; OCEAN automates simulation and result processing. Synopsys Custom Compiler, PrimeSim, HSPICE, and Siemens Eldo belong to related design and simulation ecosystems. LTspice, ngspice, and Xschem are other tools used for circuit simulation and schematic work.

### What the analyses show

DC analysis finds bias and operating points. AC analysis calculates small-signal frequency response around an operating point, and transient analysis computes nonlinear time-domain behavior. Noise analysis evaluates noise sources included in device models. Corner analysis examines representative model and environmental conditions, while Monte Carlo analysis samples statistical variation.

### From schematic to layout

Amplifier design brings together gain, bandwidth, stability, noise, and power. Comparators, references, ADCs, DACs, and PLLs balance speed, precision, and power differently depending on the application. Verilog-A describes analog behavior, while Verilog-AMS supports mixed analog and digital modeling.

DRC checks manufacturing rules, LVS compares schematic and layout devices and connectivity, and PEX extracts parasitics. Post-layout simulation includes wiring and surrounding-structure effects. Circuit data and the process design kit can have separate usage and distribution terms.

### Foundation article

- [동작점에서 주파수 응답까지: 소신호와 AC 해석](해설_notes/동작점에서주파수응답까지_small-signal-ac-operating-point.md#english)


## 심화 해설 | Advanced article

- [피드백을 걸면 이득과 대역폭은 어떻게 바뀌는가](해설_notes/피드백과대역폭_feedback.md) · [English](해설_notes/피드백과대역폭_feedback.md#english)
