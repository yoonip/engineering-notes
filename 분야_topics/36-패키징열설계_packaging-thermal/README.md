# 패키징·Chiplet·열 설계 | Packaging, Chiplets, Thermal & Reliability

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

패키지는 die를 기판·전원·외부 신호·냉각 구조와 연결합니다. 반도체 시스템의 성능과 신뢰성은 칩 내부 회로뿐 아니라 패키지의 전기적·기계적·열적 조건에도 영향을 받습니다.

## 연결 구조

Wire bonding·flip-chip은 die의 연결 방식이고, interposer는 die 사이의 고밀도 연결을 제공합니다. 2.5D·3D integration은 배치·적층 구조를 확장합니다. Chiplet은 기능을 여러 die로 나누어 연결하는 방식입니다. UCIe는 die 간 연결에 쓰이는 인터커넥트 생태계입니다.

## 전원과 열

PDN은 부하에 전원을 전달하는 경로입니다. IR drop은 저항에 의한 전압 강하, electromigration은 전류와 관련된 배선 신뢰성 문제입니다. 열저항 모델의 단순 정상상태에서는 `온도 상승 = 손실 전력 × 열저항`으로 관계를 볼 수 있지만 실제 구조는 여러 열 경로와 시간 응답을 가집니다.

Ansys·COMSOL 같은 해석 도구는 열·구조·전자기 문제를 모델링합니다. 냉각·열팽창·재료 계면·반복 온도 변화는 장기 신뢰성과 연결됩니다. 높은 연산 성능도 전력 공급과 열 제거가 받쳐 주어야 유지할 수 있습니다.

## 관련 기술

Chiplets, UCIe, 2.5D/3D IC, Interposer, COMSOL, Ansys, Thermal RC, EM/IR

## 참고 자료

- [COMSOL Multiphysics](https://www.comsol.com/comsol-multiphysics)

## 기초 해설

- [시간에 따라 달라지는 방열: thermal RC와 과도 온도](해설_notes/열은바로빠져나가지않는다_thermal-rc-steady-transient.md)

## 제조 공정과 연결

제조·조립 순서와 연결 방식의 비교는 [패키징과 첨단 집적](../../반도체제조공정_semiconductor-fabrication/08-패키징과첨단집적_packaging.md)에서 wire bond·flip-chip·RDL·TSV·hybrid bonding을 따라 읽으실 수 있습니다.

## English

### Packaging, chiplets, and thermal behavior

A package connects a die to its substrate, power supply, external signals, and cooling structure. Semiconductor performance and reliability depend on the package's electrical, mechanical, and thermal conditions as well as on the circuits inside the die.

### Interconnect structures

Wire bonding and flip-chip provide different die connection methods. An interposer provides dense connections between dies, while 2.5D and 3D integration extend placement and stacking options. Chiplet designs distribute functions across multiple dies. UCIe is one interconnect ecosystem for communication between dies.

### Power delivery and heat

A power delivery network carries power to the load. IR drop is voltage loss caused by resistance, and electromigration is a current-related interconnect reliability issue. In a simple steady-state thermal-resistance model, `temperature rise = power loss × thermal resistance`. Real structures have multiple heat paths and transient responses.

Tools such as Ansys and COMSOL model thermal, structural, and electromagnetic behavior. Cooling, thermal expansion, material interfaces, and repeated temperature cycling affect long-term reliability. Sustained computing performance also needs adequate power delivery and heat removal.

### Foundation article

- [시간에 따라 달라지는 방열: thermal RC와 과도 온도](해설_notes/열은바로빠져나가지않는다_thermal-rc-steady-transient.md#english)


## 심화 해설 | Advanced article

- [die와 package가 다른 속도로 뜨거워질 때: 두 노드 열망](해설_notes/두노드의열흐름_thermal-network.md) · [English](해설_notes/두노드의열흐름_thermal-network.md#english)
