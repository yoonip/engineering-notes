# SoC & Interconnects

[전체 목차](../../CATALOG.md) · [처음으로](../../README.md)

SoC는 CPU·메모리·가속기·주변장치와 연결망을 하나의 시스템으로 통합한다. 개별 블록이 빠르더라도 공유 자원에서 대기가 길어지면 전체 처리량은 제한된다.

## 버스와 네트워크

AMBA의 AXI·AHB·APB는 대상과 복잡도가 다른 연결 프로토콜이다. AXI는 독립적인 채널과 transaction을, APB는 비교적 단순한 주변장치 접근을 다룬다. TileLink·Wishbone은 공개 하드웨어에서 접하는 프로토콜이다. NoC는 칩 내부 통신을 라우터와 링크의 네트워크로 구성한다.

## 주소와 데이터 일관성

주소 맵은 메모리와 주변장치의 접근 위치를 정한다. DMA와 CPU가 같은 buffer를 다룰 때는 소유권·cache 관리·순서 보장이 중요하다. Cache coherence는 여러 cache가 같은 메모리 위치의 일관된 값을 관찰하도록 하는 문제이고, memory consistency는 메모리 연산 순서의 관찰 규칙과 관련된다.

Arbitration은 경쟁 요청의 순서를, QoS는 서비스 조건을 다룬다. 평균 대역폭과 최악 지연은 별개다. CHI·PCIe·CXL·chiplet 연결은 일관성·장치 연결·패키지 간 통신으로 범위를 넓힌다.

## 관련 기술

AXI, AMBA, TileLink, Wishbone, NoC, PCIe, CXL, Chiplet, CHI

## 참고 자료

- [Arm documentation](https://developer.arm.com/documentation)
- [RISC-V specifications](https://docs.riscv.org/)
