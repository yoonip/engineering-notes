# 반도체 소자 | Semiconductor Devices

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

반도체의 전기적 특성은 에너지 밴드와 전자·정공의 농도, 이동도, 전기장에 따라 달라집니다. 도핑은 캐리어 농도를 조절하고, PN 접합은 공핍층과 전위 장벽을 형성합니다.

## MOSFET에서 CMOS로

MOSFET은 게이트 전압으로 채널의 전도성을 조절합니다. 문턱전압·트랜스컨덕턴스·출력저항·기생 커패시턴스는 회로의 이득과 속도, 전력에 연결됩니다. CMOS는 NMOS와 PMOS를 조합해 논리 게이트와 아날로그 회로를 구성합니다. 이상적인 장채널 식은 동작을 이해하는 모델이고 실제 공정 소자는 더 복잡한 모델을 사용합니다.

## 구조와 재료

FinFET과 GAA는 채널에 대한 게이트 제어를 개선하는 소자 구조입니다. SOI는 절연층 위에 소자를 형성합니다. SiC·GaN은 전력·고주파 응용에서 사용되는 재료 계열입니다. SRAM·DRAM·NAND는 전하나 회로 상태를 저장하는 방식이 다릅니다.

## 소자 모델과 공정 변동

PVT는 공정·전압·온도에 따른 변화를 뜻합니다. BSIM 같은 compact model은 회로 시뮬레이터에서 소자 특성을 계산합니다. TCAD는 공정과 소자의 물리 현상을 더 직접적으로 해석합니다. 모델 파라미터와 레이아웃의 기생 성분은 같은 회로 구조의 성능을 바꿉니다.

## 관련 기술

PN, MOS, BJT, CMOS, FinFET, GAA, SOI, SiC/GaN, BSIM, SRAM/DRAM/NAND, TCAD

## 참고 자료

- [MIT OCW — Microelectronic Devices and Circuits](https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-fall-2009/)


## 개념·유도·모델·검증

[기초부터 읽기](../../공학기초_foundations/README.md)

- [MOSFET: 전기장으로 전류를 조절하는 원리와 모델의 한계](해설_notes/MOSFET의동작원리_mos-electrostatics-switching.md)

## 제조 공정과 연결

소자를 실제로 형성하는 과정은 [반도체 제조 공정](../../반도체제조공정_semiconductor-fabrication/README.md)의 [게이트 절연막](../../반도체제조공정_semiconductor-fabrication/02-산화와게이트절연막_oxidation-gate-dielectrics.md)과 [로직·메모리 공정 비교](../../반도체제조공정_semiconductor-fabrication/10-로직과메모리의공정차이_logic-memory-integration.md)로 이어집니다.

## English

Semiconductor behavior depends on energy bands, electron and hole concentrations, mobility, and electric fields. Doping controls carrier concentration, and a PN junction forms a depletion region and a potential barrier.

### From MOSFETs to CMOS

A MOSFET uses gate voltage to control channel conduction. Threshold voltage, transconductance, output resistance, and parasitic capacitance affect circuit gain, speed, and power. CMOS combines NMOS and PMOS devices in logic and analog circuits. Long-channel equations provide an accessible operating model; practical process devices use more detailed models.

### Structures and materials

FinFET and GAA structures improve gate control over the channel. SOI forms devices above an insulating layer. SiC and GaN are material families used in power and high-frequency applications. SRAM, DRAM, and NAND store information through different circuit states or charge-storage mechanisms.

### Device models and process variation

PVT describes process, voltage, and temperature variation. Compact models such as BSIM calculate device behavior in circuit simulators. TCAD analyzes process and device physics more directly. Model parameters and extracted layout parasitics can change the performance of the same circuit topology.


### Concepts, derivations, models, and verification

[Foundations reading guide](../../공학기초_foundations/README.md#english)

- [MOS electrostatics and switching](해설_notes/MOSFET의동작원리_mos-electrostatics-switching.md#english)


## 심화 해설 | Advanced article

- [작은 전류의 증폭 효율: subthreshold와 gm/Id](해설_notes/작은전류의증폭효율_subthreshold.md) · [English](해설_notes/작은전류의증폭효율_subthreshold.md#english)
