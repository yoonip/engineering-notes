# 전력전자와 에너지

[전체 목차](../../CATALOG.md) · [처음으로](../../README.md)

전력전자는 반도체 스위칭과 수동소자를 이용해 전기 에너지를 원하는 전압·전류·주파수로 바꾸는 분야다. DC/DC·AC/DC 변환기, 인버터, 충전기, 모터 구동기, PMIC와 연결된다.

## 변환기와 스위칭

Buck은 강압, boost는 승압의 기본 구조다. 이상적인 연속전도 buck의 정상상태에서는 `Vout = D*Vin`으로 듀티비와 출력이 연결된다. 실제 회로에는 도통 손실·스위칭 손실·리플·제어 지연이 있다. LLC는 공진을 이용하는 변환기 구조다.

## 소자와 구동

MOSFET·IGBT·SiC·GaN 소자는 전압·전류·스위칭 주파수·손실 특성에 따라 사용 영역이 달라진다. 게이트 드라이버는 게이트 전하를 충·방전하고, dead time은 상하 스위치의 동시 도통을 방지하는 데 관여한다. 배선의 기생 인덕턴스는 ringing과 과전압을 만들 수 있다.

배터리 시스템의 BMS는 전압·전류·온도 관측과 상태 추정·보호를 담당한다. 효율은 출력 전력/입력 전력이며 부하 조건과 함께 읽는다. PLECS·PSIM·LTspice·Simulink는 전력단과 제어 동작을 모델링하는 도구다. 열과 보호 동작도 전기적 성능의 일부다.

## 관련 기술

PLECS, PSIM, LTspice, Simulink, Buck/Boost, LLC, BMS, PMIC

## 참고 자료

- [LTspice](https://www.analog.com/en/resources/design-tools-and-calculators/ltspice-simulator.html)
