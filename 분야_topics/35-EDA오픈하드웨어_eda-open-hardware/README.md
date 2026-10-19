# EDA와 오픈 하드웨어 | EDA & Open Hardware Ecosystems

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

EDA는 회로의 설계·검증·구현·제조 데이터 생성을 자동화하는 도구 체계입니다. 각 도구가 데이터와 제약 조건을 주고받으며 하나의 설계 흐름을 이룹니다.

## 흐름을 잇는 데이터

RTL·회로도는 기능과 연결을, timing constraint는 시간 조건을, library는 셀 특성을, LEF/DEF는 물리 구현 정보를, GDS는 레이아웃 형상을 전달하는 데 쓰입니다. Signoff는 제조 전에 타이밍·물리 규칙·전력·신뢰성 등을 최종 확인하는 단계입니다.

## PDK와 도구

PDK는 공정의 layer·rule·device model·설계 지원 데이터를 묶습니다. 표준 셀 라이브러리는 기본 논리 기능의 회로·특성·물리 정보를 제공합니다. 공개 PDK가 있어도 모든 제조 옵션이나 상용 공정 조건이 동일하게 열려 있는 것은 아닙니다.

Cadence·Synopsys·Siemens는 설계 단계별 상용 도구를 제공합니다. Yosys는 합성, OpenROAD·OpenLane은 디지털 물리 설계 흐름, KLayout·Magic은 레이아웃 작업, Netgen은 회로 비교에 쓰입니다. SKY130·GF180MCU·IHP SG13G2는 공개 공정 자료를 제공합니다. 입력 버전과 도구 로그를 함께 남기면 결과가 나온 과정을 추적할 수 있습니다.

## 관련 기술

Cadence, Synopsys, Siemens EDA, Yosys, OpenROAD, OpenLane, KLayout, Magic, Netgen, SKY130, GF180, IHP SG13G2

## 참고 자료

- [OpenROAD documentation](https://openroad.readthedocs.io/en/latest/)

## 기초 해설

- [RTL에서 layout까지: 서로 다른 검증을 연결하는 EDA 흐름](해설_notes/RTL에서layout까지_rtl-netlist-timing-physical-checks.md)

## English

### EDA and open hardware

Electronic design automation covers tools for circuit design, verification, implementation, and manufacturing-data generation. A design flow connects tools through data and constraints rather than relying on one tool to handle every stage.

### Data between design stages

RTL and schematics describe function and connectivity. Timing constraints specify timing requirements, libraries describe cell characteristics, LEF/DEF convey physical-design information, and GDS carries layout geometry. Before manufacturing, signoff checks timing, physical rules, power, reliability, and other requirements.

### PDKs and tools

A process design kit contains process layers, rules, device models, and supporting design data. A standard-cell library supplies circuits, characterized behavior, and physical views of basic logic functions. An open PDK does not imply that every manufacturing option or commercial process condition is publicly available.

Cadence, Synopsys, and Siemens provide commercial tools across the design flow. Yosys handles synthesis; OpenROAD and OpenLane support digital physical-design flows. KLayout and Magic support layout work, and Netgen compares circuits. SKY130, GF180MCU, and IHP SG13G2 provide access to open process resources. Input versions and tool logs make design results traceable.

### Foundation article

- [RTL에서 layout까지: 서로 다른 검증을 연결하는 EDA 흐름](해설_notes/RTL에서layout까지_rtl-netlist-timing-physical-checks.md#english)


## 심화 해설 | Advanced article

- [다른 회로, 같은 상태 전이: equivalence를 확인하는 기준](해설_notes/같은상태전이_equivalence.md) · [English](해설_notes/같은상태전이_equivalence.md#english)
