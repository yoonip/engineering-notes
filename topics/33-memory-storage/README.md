# Memory & Storage

[전체 목차](../../CATALOG.md) · [처음으로](../../README.md)

메모리와 저장장치는 데이터를 유지하는 방식·속도·용량·내구성·접근 단위가 다르다. 프로세서 가까이의 캐시부터 주메모리, SSD, 파일시스템까지 계층을 이루며 전체 성능은 계층 간 이동의 영향을 받는다.

## 소자와 인터페이스

SRAM은 latch 기반 상태를, DRAM은 커패시터 전하를 사용하며 주기적인 refresh가 필요하다. NAND flash는 비휘발성 저장에 쓰이고 페이지·블록 단위의 동작과 쓰기 수명 특성을 가진다. DDR·LPDDR·GDDR·HBM은 서로 다른 전력·대역폭·연결 조건을 가진 메모리 규격 계열이다.

## SSD와 신뢰성

NVMe는 비휘발성 저장장치를 위한 프로토콜이다. SSD의 FTL은 논리 주소를 물리 flash 위치에 연결하고 garbage collection·wear leveling 같은 작업을 수행한다. ECC는 오류를 검출·수정하는 부호다. 장치의 대역폭이 높아도 작은 무작위 요청에서는 지연과 queue depth가 병목이 될 수 있다.

fio는 저장장치 I/O 부하를 생성·측정하는 도구다. 읽기·쓰기, 순차·무작위, block size, cache 조건을 구분해야 측정값을 해석할 수 있다. CXL은 장치와 메모리의 연결·일관성 기능을 포함한 인터커넥트 생태계로 이어진다.

## 관련 기술

SRAM, DRAM, NAND, DDR, LPDDR, GDDR, HBM, NVMe, fio, CXL

## 참고 자료

- [fio documentation](https://fio.readthedocs.io/en/latest/)
