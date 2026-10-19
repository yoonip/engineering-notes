# FPGA·ASIC 설계 | FPGA & ASIC Design

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

FPGA는 이미 제작된 소자의 논리·연결 자원을 설정해 회로를 구성한다. ASIC은 특정 회로를 반도체 공정으로 제작한다. 같은 RTL을 사용해도 메모리·클록·입출력·배치배선 조건에 따라 구현 결과가 달라진다.

## 구현 흐름

합성은 RTL을 게이트나 FPGA 자원으로 매핑한다. 이후 배치와 배선이 위치·연결을 결정한다. ASIC에서는 floorplan·전원망·clock tree·물리 검증을 거쳐 제조용 데이터를 만든다. FPGA의 bitstream은 대상 장치의 구성을 담는다.

## 타이밍과 PPA

STA는 제약과 지연 모델을 이용해 경로의 setup·hold 조건 등을 분석한다. 클록 주기뿐 아니라 입출력 지연, 생성 클록, 예외 경로의 정의도 중요하다. PPA는 power·performance·area를 함께 살펴보는 기준이다. 파이프라인을 늘려 속도를 올리면 레지스터와 지연 단계가 늘 수 있다.

Vivado·Vitis는 AMD FPGA 생태계, Quartus는 Altera FPGA 생태계, Radiant는 Lattice FPGA 설계에 쓰인다. Genus·Innovus, Design Compiler·Fusion Compiler·PrimeTime은 ASIC 구현·타이밍 흐름의 도구다. Yosys·nextpnr·OpenROAD·OpenLane은 공개 합성·배치배선 흐름을 구성한다.

## 관련 기술

AMD/Xilinx Vivado/Vitis, Intel/Altera Quartus, Lattice Radiant, Yosys, nextpnr, OpenROAD/OpenLane, Genus/Innovus, Design Compiler/Fusion Compiler, PrimeTime

## 참고 자료

- [OpenROAD documentation](https://openroad.readthedocs.io/en/latest/)

## 기초 해설

- [너무 늦어도, 너무 빨라도 문제다: setup·hold와 STA](해설_notes/너무늦어도너무빨라도문제다_setup-hold-static-timing.md)

## English

An FPGA configures logic and routing resources in an already manufactured device. An ASIC implements a particular circuit through a semiconductor fabrication process. A shared RTL design can produce different implementations because memory, clocks, I/O, and placement and routing constraints differ.

### Implementation flow

Synthesis maps RTL into gates or FPGA resources. Placement and routing determine physical locations and connections. An ASIC flow also includes floorplanning, power distribution, clock-tree construction, and physical verification before generating manufacturing data. An FPGA bitstream contains the configuration for its target device.

### Timing and PPA

Static timing analysis uses constraints and delay models to check path requirements such as setup and hold. I/O delays, generated clocks, and timing exceptions matter alongside the clock period. Power, performance, and area are linked: adding pipeline stages can improve frequency while increasing register count and latency.

Vivado and Vitis belong to the AMD FPGA ecosystem, Quartus to Altera, and Radiant to Lattice. Genus, Innovus, Design Compiler, Fusion Compiler, and PrimeTime support ASIC implementation and timing workflows. Yosys, nextpnr, OpenROAD, and OpenLane provide components for open synthesis and physical-design flows.

### Foundation article

- [너무 늦어도, 너무 빨라도 문제다: setup·hold와 STA](해설_notes/너무늦어도너무빨라도문제다_setup-hold-static-timing.md#english)
