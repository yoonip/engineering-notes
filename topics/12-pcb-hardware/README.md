# PCB & Hardware Design

[전체 목차](../../CATALOG.md) · [처음으로](../../README.md)

PCB는 부품을 고정하고 전기적으로 연결하는 기판이다. 회로도가 논리적인 연결을 표현한다면 레이아웃은 실제 부품 위치, 배선, 층 구조, 전류 경로를 결정한다. 같은 회로도라도 배치·배선에 따라 잡음과 신호 품질이 달라진다.

## 부품과 제조 데이터

부품 선정에는 정격, 오차, 주파수 특성, 패키지, 공급 조건이 함께 들어간다. BOM은 부품 명세, netlist는 연결 정보, Gerber와 drill 데이터는 제조에 사용하는 파일이다. KiCad·Altium Designer·OrCAD/Allegro·PADS/Xpedition·EasyEDA는 회로도와 PCB 작업에 쓰인다.

## 신호와 전원의 경로

디커플링 커패시터는 부하 가까이에서 빠른 전류 변화를 공급한다. 고속 신호의 귀환 전류는 배선만큼 중요하며, 기준면 단절은 루프와 방사를 키울 수 있다. SI는 신호 파형과 타이밍, PI는 전원망의 임피던스와 전압 변동, EMI/EMC는 전자파 방출과 내성을 다룬다. IBIS 모델은 디지털 입출력 버퍼의 신호 특성 해석에 쓰인다.

제작 후 bring-up은 전원·클록·리셋·통신을 확인하며 보드 동작을 연결해 가는 과정이다. DFM은 제조 가능성과 조립 조건을 설계에 반영한다.

## 관련 기술

KiCad, Altium Designer, OrCAD, Allegro, PADS, Xpedition, EasyEDA, IBIS, SI/PI, EMC/EMI, DFM

## 참고 자료

- [About KiCad](https://www.kicad.org/about/kicad/)
