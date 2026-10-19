# EDA & Open Hardware

[전체 목차](../../CATALOG.md) · [처음으로](../../README.md)

EDA는 회로의 설계·검증·구현·제조 데이터 생성을 자동화하는 도구 체계다. 도구 하나가 모든 단계를 담당하기보다 서로 다른 데이터와 제약을 주고받으며 설계 흐름을 이룬다.

## 흐름을 잇는 데이터

RTL·회로도는 기능과 연결을, timing constraint는 시간 조건을, library는 셀 특성을, LEF/DEF는 물리 구현 정보를, GDS는 레이아웃 형상을 전달하는 데 쓰인다. Signoff는 제조 전 최종 검증의 맥락에서 타이밍·물리 규칙·전력·신뢰성 등을 확인하는 단계다.

## PDK와 도구

PDK는 공정의 layer·rule·device model·설계 지원 데이터를 묶는다. 표준 셀 라이브러리는 기본 논리 기능의 회로·특성·물리 정보를 제공한다. 공개 PDK가 있어도 모든 제조 옵션이나 상용 공정 조건이 동일하게 열려 있는 것은 아니다.

Cadence·Synopsys·Siemens는 설계 단계별 상용 도구를 제공한다. Yosys는 합성, OpenROAD·OpenLane은 디지털 물리 설계 흐름, KLayout·Magic은 레이아웃 작업, Netgen은 회로 비교에 쓰인다. SKY130·GF180MCU·IHP SG13G2는 공개 공정 자료를 접할 수 있는 생태계다. 도구 로그와 입력 버전은 결과를 다시 추적하는 연결점이다.

## 관련 기술

Cadence, Synopsys, Siemens EDA, Yosys, OpenROAD, OpenLane, KLayout, Magic, Netgen, SKY130, GF180, IHP SG13G2

## 참고 자료

- [OpenROAD documentation](https://openroad.readthedocs.io/en/latest/)
