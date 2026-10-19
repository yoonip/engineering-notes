# 전력전자와 에너지 | Power Electronics & Energy

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

전력전자는 반도체 스위칭과 수동소자를 이용해 전기 에너지를 필요한 전압·전류·주파수로 바꿉니다. DC/DC·AC/DC 변환기, 인버터, 충전기, 모터 구동기, PMIC와 연결됩니다.

## 변환기와 스위칭

Buck은 강압, boost는 승압의 기본 구조입니다. 이상적인 연속전도 buck의 정상상태에서는 `Vout = D*Vin`으로 듀티비에 따른 출력 전압을 구할 수 있습니다. 실제 회로에는 도통 손실·스위칭 손실·리플·제어 지연이 있습니다. LLC는 공진을 이용하는 변환기 구조입니다.

## 소자와 구동

MOSFET·IGBT·SiC·GaN 소자는 전압·전류·스위칭 주파수·손실 특성에 따라 사용 영역이 달라집니다. 게이트 드라이버는 게이트 전하를 충·방전하고, dead time은 상하 스위치의 동시 도통을 방지하는 데 관여합니다. 배선의 기생 인덕턴스는 ringing과 과전압을 만들 수 있습니다.

배터리 시스템의 BMS는 전압·전류·온도 관측과 상태 추정·보호를 담당합니다. 효율은 출력 전력을 입력 전력으로 나눈 값입니다. 같은 회로에서도 부하 조건에 따라 달라집니다. PLECS·PSIM·LTspice·Simulink는 전력단과 제어 동작을 모델링하는 도구입니다. 열과 보호 동작도 전기적 성능의 일부입니다.

## 관련 기술

PLECS, PSIM, LTspice, Simulink, Buck/Boost, LLC, BMS, PMIC

## 참고 자료

- [LTspice](https://www.analog.com/en/resources/design-tools-and-calculators/ltspice-simulator.html)

## 기초 해설

- [스위칭으로 낮은 전압 만들기: buck의 CCM과 ripple](해설_notes/스위칭으로낮은전압만들기_buck-ccm-ripple.md)

## English

### Power electronics and energy

Power electronics uses semiconductor switching and passive components to convert electrical energy to the required voltage, current, and frequency. Applications include DC/DC and AC/DC converters, inverters, chargers, motor drives, and PMICs.

### Converters and switching

Buck and boost converters provide basic step-down and step-up structures. For an ideal buck converter in steady-state continuous conduction, `Vout = D*Vin` relates duty cycle to output voltage. Real circuits also have conduction and switching losses, ripple, and control delay. LLC converters use resonance in their conversion stage.

### Devices and gate driving

MOSFET, IGBT, SiC, and GaN devices suit different voltage, current, switching-frequency, and loss requirements. A gate driver charges and discharges the gate. Dead time helps prevent the upper and lower switches from conducting together, while parasitic wiring inductance can cause ringing and overvoltage.

A battery management system monitors voltage, current, and temperature, estimates battery state, and provides protection. Efficiency is output power divided by input power and needs to be read alongside the load conditions. PLECS, PSIM, LTspice, and Simulink model power stages and their controls. Thermal behavior and protection are also part of the circuit's electrical performance.

### Foundation article

- [스위칭으로 낮은 전압 만들기: buck의 CCM과 ripple](해설_notes/스위칭으로낮은전압만들기_buck-ccm-ripple.md#english)


## 심화 해설 | Advanced article

- [부하가 갑자기 바뀔 때: buck의 평균 과도모델](해설_notes/부하변화의과도응답_buck-transient.md) · [English](해설_notes/부하변화의과도응답_buck-transient.md#english)
