# 메모리와 저장장치 | Memory & Storage Systems

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

메모리와 저장장치는 데이터를 유지하는 방식·속도·용량·내구성·접근 단위가 다릅니다. 프로세서 가까이의 캐시부터 주메모리, SSD, 파일시스템까지 계층을 이루며 전체 성능은 계층 사이에서 데이터를 옮기는 데 드는 시간과 비용에 영향을 받습니다.

## 소자와 인터페이스

SRAM은 latch 회로에 상태를 저장합니다. DRAM은 커패시터의 전하로 정보를 저장하며 주기적인 refresh가 필요합니다. NAND flash는 비휘발성 저장에 쓰이고 페이지·블록 단위의 동작과 쓰기 수명 특성을 가집니다. DDR·LPDDR·GDDR·HBM은 서로 다른 전력·대역폭·연결 조건을 가진 메모리 규격 계열입니다.

## SSD와 신뢰성

NVMe는 비휘발성 저장장치를 위한 프로토콜입니다. SSD의 FTL은 논리 주소를 물리 flash 위치에 연결하고 garbage collection·wear leveling 같은 작업을 수행합니다. ECC는 오류를 검출·수정하는 부호입니다. 장치의 대역폭이 높아도 작은 무작위 요청에서는 지연과 queue depth가 병목이 될 수 있습니다.

fio는 저장장치 I/O 부하를 생성·측정하는 도구입니다. 읽기·쓰기, 순차·무작위, block size, cache 조건을 구분해야 측정값을 해석할 수 있습니다. CXL은 장치와 메모리를 연결하고 데이터 일관성 기능을 제공하는 인터커넥트입니다.

## 캐시의 값과 DMA가 보는 RAM

같은 주소라도 CPU가 캐시에서 읽는 값과 DMA가 RAM에서 읽는 값이 다를 수 있습니다. 자동 캐시 일관성이 없는 write-back 구성을 가정하면 CPU가 바꾼 값이 캐시에만 dirty 상태로 남을 수 있습니다. dirty는 RAM에 아직 반영하지 않은 변경이 있다는 뜻입니다. clean은 그 변경을 메모리 쪽에 반영하고, invalidate는 캐시 복사본을 버립니다. Cortex-M7의 구체적인 유지 연산은 [CMSIS-Core D-cache 함수](https://arm-software.github.io/CMSIS_6/latest/Core/group__Dcache__functions__m7.html)와 사용하는 MCU의 메모리 경로를 함께 확인합니다.

직접 구성한 TX 예에서 RAM의 순번은 16인데 CPU가 캐시의 순번만 17로 바꿨다면 DMA는 여전히 16을 읽을 수 있습니다. DMA 시작 전에 올바른 범위를 clean하면 RAM에도 17이 반영됩니다. 반대로 새 dirty 값을 invalidate만 하면 17을 버릴 수 있습니다. 함수 이름만 바꾸는 대신 데이터가 어느 방향으로 이동하고 지금 누가 버퍼를 소유하는지부터 정해야 합니다.

캐시 유지의 단위는 요청한 payload 길이와 같지 않을 수 있습니다. 이 Cortex-M7 예제는 32바이트 line을 사용합니다. 아래 주소는 계산용이며 특정 보드에서 DMA가 접근 가능한 주소라고 가정하지 않습니다.

```python
start, size, line = 0x2000101C, 12, 32  # 0x는 16진수이며 세 정수를 한 번에 대입합니다.
low = start // line * line  # //는 정수 나눗셈으로 시작을 line 경계까지 내립니다.
high = (start + size + line - 1) // line * line  # 끝 미포함 주소를 다음 경계로 올립니다.
print(hex(low), hex(high), high - low)  # hex는 16진수 문자열이며 영향 범위는 64바이트입니다.
print(start - low, high - (start + size))  # payload 밖의 앞 28·뒤 24바이트도 같은 line에 있습니다.
```

12바이트 payload 때문에 총 64바이트에 유지 연산이 영향을 줍니다. 그중 52바이트는 payload 밖입니다. 시작을 32바이트 경계로 옮기면 이 12바이트는 한 line에 들어가지만, 배열 시작 정렬만으로 뒤의 다른 변수가 같은 line에 배치되지 않는다고 보장할 수는 없습니다. 전용 line을 예약하려면 이 예에서는 32바이트 공간과 그 소유권을 함께 관리합니다.

RX의 공유 line에서 CPU가 이웃 flag를 dirty로 만들면 사후 invalidate가 그 변경을 버릴 수 있습니다. 반대로 사후 clean은 캐시에 남은 낡은 RX를 새 RAM 데이터 위에 쓸 수 있습니다. 버퍼·padding·이웃 객체의 배치와 DMA 소유 중 CPU 접근을 함께 살펴보는 이유입니다. [캐시·DMA 오류 재현](../../설계와검증사례_engineering-cases/캐시와RAM의데이터불일치_dma-cache-lines.md)에서 메모리 복사본의 변화를 코드로 비교합니다.

이 계산은 cache miss 지연이나 DMA 성능 측정이 아닙니다. line 크기·자동 일관성·메모리 접근 경로는 실제 CPU와 시스템마다 확인하며, 메모리 barrier 하나가 clean이나 외부 DMA 완료 확인을 모두 대신한다고 해석하지 않습니다.

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


### Cache-line ownership and DMA

In the constructed non-coherent write-back example, CPU sequence 17 can remain in cache while RAM still holds 16. Cache maintenance affects entire lines. A twelve-byte payload at 0x2000101C spans two 32-byte lines: 64 bytes including 28 before and 24 after the payload. Alignment alone does not reserve the remainder of a line. These are address and ownership examples, not timing or physical DMA measurements.

### Concepts, derivations, models, and verification

[Foundations reading guide](../../공학기초_foundations/README.md#english)

- [Locality, cache and average memory access time](해설_notes/메모리지역성과캐시_locality-cache-amat.md#english)


## 심화 해설 | Advanced article

- [SRAM을 읽을 때 저장 노드가 올라가는 이유](해설_notes/SRAM읽기교란_read-disturb.md) · [English](해설_notes/SRAM읽기교란_read-disturb.md#english)
