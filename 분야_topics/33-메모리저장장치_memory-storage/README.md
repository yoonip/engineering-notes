# 메모리와 저장장치 | Memory & Storage Systems

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

메모리와 저장장치는 데이터를 유지하는 방식·속도·용량·내구성·접근 단위가 다릅니다. 프로세서 가까이의 캐시부터 주메모리, SSD, 파일시스템까지 계층을 이루며 전체 성능은 계층 사이에서 데이터를 옮기는 데 드는 시간과 비용에 영향을 받습니다.

## 소자와 인터페이스

SRAM은 latch 회로에 상태를 저장합니다. DRAM은 커패시터의 전하로 정보를 저장하며 주기적인 refresh가 필요합니다. NAND flash는 비휘발성 저장에 쓰이고 페이지·블록 단위의 동작과 쓰기 수명 특성을 가집니다. DDR·LPDDR·GDDR·HBM은 서로 다른 전력·대역폭·연결 조건을 가진 메모리 규격 계열입니다.

## SSD와 신뢰성

NVMe는 비휘발성 저장장치를 위한 프로토콜입니다. SSD의 FTL은 논리 주소를 물리 flash 위치에 연결하고 garbage collection·wear leveling 같은 작업을 수행합니다. ECC는 오류를 검출·수정하는 부호입니다. 장치의 대역폭이 높아도 작은 무작위 요청에서는 지연과 queue depth가 병목이 될 수 있습니다.

fio는 저장장치 I/O 부하를 생성·측정하는 도구입니다. 읽기·쓰기, 순차·무작위, block size, cache 조건을 구분해야 측정값을 해석할 수 있습니다. CXL은 장치와 메모리를 연결하고 데이터 일관성 기능을 제공하는 인터커넥트입니다.

## 관련 기술

SRAM, DRAM, NAND, DDR, LPDDR, GDDR, HBM, NVMe, fio, CXL

## 참고 자료

- [fio documentation](https://fio.readthedocs.io/en/latest/)


## 개념·유도·모델·검증

[기초부터 읽기](../../공학기초_foundations/README.md)

- [메모리 지역성과 캐시: 평균 지연과 대역폭을 나눠 보기](해설_notes/메모리지역성과캐시_locality-cache-amat.md)

## English

### Memory and storage

Memory and storage technologies differ in how they retain data, their speed, capacity, endurance, and access granularity. Caches, main memory, SSDs, and filesystems form a hierarchy. Moving data between these levels can determine overall performance.

### Devices and interfaces

SRAM stores state in latch-based circuits. DRAM stores charge in capacitors and requires periodic refresh. NAND flash provides nonvolatile storage, with page- and block-level operations and finite write endurance. DDR, LPDDR, GDDR, and HBM are memory-standard families with different power, bandwidth, and interconnect requirements.

### SSDs and reliability

NVMe is a protocol for nonvolatile storage devices. An SSD's flash translation layer maps logical addresses to physical flash locations and manages work such as garbage collection and wear leveling. ECC detects and corrects errors. Even a high-bandwidth device can be limited by latency and queue depth when handling small random requests.

fio generates and measures storage I/O workloads. Read versus write, sequential versus random access, block size, and cache conditions all affect the meaning of a result. CXL extends this topic to device and memory interconnects with coherency features.


### Concepts, derivations, models, and verification

[Foundations reading guide](../../공학기초_foundations/README.md#english)

- [Locality, cache and average memory access time](해설_notes/메모리지역성과캐시_locality-cache-amat.md#english)


## 심화 해설 | Advanced article

- [SRAM을 읽을 때 저장 노드가 올라가는 이유](해설_notes/SRAM읽기교란_read-disturb.md) · [English](해설_notes/SRAM읽기교란_read-disturb.md#english)
