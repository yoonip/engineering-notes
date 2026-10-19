# PCB와 하드웨어 설계 | PCB & Hardware Design

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

PCB는 부품을 고정하고 전기적으로 연결하는 기판이다. 회로도에는 논리적인 연결을, 레이아웃에는 실제 부품 위치와 배선, 층 구조, 전류 경로를 담는다. 같은 회로도라도 배치·배선에 따라 잡음과 신호 품질이 달라진다.

## 부품과 제조 데이터

부품 선정에는 정격, 오차, 주파수 특성, 패키지, 공급 조건이 함께 들어간다. BOM은 부품 명세, netlist는 연결 정보, Gerber와 drill 데이터는 제조에 사용하는 파일이다. KiCad·Altium Designer·OrCAD/Allegro·PADS/Xpedition·EasyEDA는 회로도와 PCB 작업에 쓰인다.

## 신호와 전원의 경로

디커플링 커패시터는 부하 가까이에서 빠른 전류 변화를 공급한다. 고속 신호의 귀환 전류는 배선만큼 중요하며, 기준면 단절은 루프와 방사를 키울 수 있다. SI는 신호 파형과 타이밍, PI는 전원망의 임피던스와 전압 변동, EMI/EMC는 전자파 방출과 내성을 다룬다. IBIS 모델은 디지털 입출력 버퍼의 신호 특성 해석에 쓰인다.

제작 후 bring-up에서는 전원·클록·리셋·통신을 차례로 확인하며 보드를 구동한다. DFM은 제조 가능성과 조립 조건을 설계에 반영한다.

## 관련 기술

KiCad, Altium Designer, OrCAD, Allegro, PADS, Xpedition, EasyEDA, IBIS, SI/PI, EMC/EMI, DFM

## 참고 자료

- [About KiCad](https://www.kicad.org/about/kicad/)

## 기초 해설

- [전원은 배선까지 포함한다: PDN, decoupling과 귀환 전류](해설_notes/전원은배선까지포함한다_pdn-decoupling-return-current.md)

## English

A PCB mechanically supports components and connects them electrically. The schematic describes logical connections; the layout determines physical placement, routing, layer structure, and current paths. Different layouts of the same schematic can have different noise and signal quality.

### Components and manufacturing files

Component selection includes ratings, tolerances, frequency behavior, package, and availability. A BOM lists components, a netlist describes connections, and Gerber and drill files provide manufacturing data. KiCad, Altium Designer, OrCAD/Allegro, PADS/Xpedition, and EasyEDA are used for schematic and PCB work.

### Signal and power paths

Decoupling capacitors supply rapidly changing current close to a load. A high-speed signal's return path matters alongside its outgoing trace; a break in its reference plane can enlarge the current loop and increase radiation. Signal integrity concerns waveforms and timing, power integrity concerns supply-network impedance and voltage variation, and EMI/EMC concerns electromagnetic emissions and immunity. IBIS models support analysis of digital I/O buffer behavior.

Board bring-up works through power, clocks, reset, and communication to establish operation. Design for manufacturing incorporates fabrication and assembly constraints into the design.

### Foundation article

- [전원은 배선까지 포함한다: PDN, decoupling과 귀환 전류](해설_notes/전원은배선까지포함한다_pdn-decoupling-return-current.md#english)


## 심화 해설 | Advanced article

- [커패시터를 더 달았는데 왜 전원 임피던스가 커질까](해설_notes/커패시터사이의공진_pdn-antiresonance.md) · [English](해설_notes/커패시터사이의공진_pdn-antiresonance.md#english)
