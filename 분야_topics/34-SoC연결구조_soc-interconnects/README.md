# SoC와 연결 구조 | SoC & Interconnects

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

SoC는 CPU·메모리·가속기·주변장치와 연결망을 하나의 시스템으로 통합한다. 개별 블록이 빨라도 공유 자원을 기다리는 시간이 길면 전체 처리량이 줄어든다.

## 버스와 네트워크

AMBA의 AXI·AHB·APB는 대상과 복잡도가 다른 연결 프로토콜이다. AXI는 독립적인 채널과 transaction을, APB는 비교적 단순한 주변장치 접근을 다룬다. TileLink·Wishbone은 공개 하드웨어에서 접하는 프로토콜이다. NoC는 칩 내부 통신을 라우터와 링크의 네트워크로 구성한다.

## 주소와 데이터 일관성

주소 맵은 메모리와 주변장치의 접근 위치를 정한다. DMA와 CPU가 같은 buffer를 다룰 때는 소유권·cache 관리·순서 보장이 중요하다. Cache coherence는 여러 cache가 같은 메모리 위치의 일관된 값을 관찰하도록 하는 문제이고, memory consistency는 메모리 연산 순서의 관찰 규칙과 관련된다.

Arbitration은 경쟁 요청의 순서를, QoS는 서비스 조건을 다룬다. 평균 대역폭과 최악 지연은 별개다. CHI·PCIe·CXL·chiplet 연결에서는 데이터 일관성, 장치 연결, die 간 통신까지 함께 다룬다.

## 관련 기술

AXI, AMBA, TileLink, Wishbone, NoC, PCIe, CXL, Chiplet, CHI

## 참고 자료

- [Arm documentation](https://developer.arm.com/documentation)
- [RISC-V specifications](https://docs.riscv.org/)

## 기초 해설

- [준비된 순간에만 옮기기: ready/valid와 backpressure](해설_notes/준비된순간에만옮기기_ready-valid-backpressure.md)

## English

### SoCs and interconnects

An SoC integrates processors, memory, accelerators, peripherals, and their interconnects into one system. Fast individual blocks do not guarantee high system throughput when requests spend time waiting for shared resources.

### Buses and networks

AMBA's AXI, AHB, and APB protocols serve different targets and levels of complexity. AXI uses independent channels and transactions, while APB supports relatively simple peripheral access. TileLink and Wishbone are also used in open hardware. A network-on-chip organizes on-chip communication as routers and links.

### Addresses and data consistency

An address map specifies where memory and peripherals are accessed. When DMA and a CPU share a buffer, ownership, cache management, and ordering affect correctness. Cache coherence concerns consistent views of the same memory location across caches. Memory consistency defines how the ordering of memory operations can be observed.

Arbitration decides the order of competing requests; QoS controls service requirements. Average bandwidth and worst-case latency are different metrics. CHI, PCIe, CXL, and chiplet interconnects extend these ideas to coherence, device connectivity, and communication between dies.

### Foundation article

- [준비된 순간에만 옮기기: ready/valid와 backpressure](해설_notes/준비된순간에만옮기기_ready-valid-backpressure.md#english)
