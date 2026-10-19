# 차세대 소자와 컴퓨팅 | Research Frontiers

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

새로운 컴퓨팅 구조는 기존 시스템의 데이터 이동·전력·연결·물리 구현 한계를 새로운 방식으로 해결하려는 연구에서 출발한다. 서로 다른 분야의 성능 수치를 비교할 때는 무엇을 계산했고 비용을 어디까지 포함했는지 함께 본다.

## Neuromorphic와 메모리 연산

Spiking neural network는 event와 시간에 따른 상태 변화를 사용한다. Event camera는 밝기 변화 사건을 비동기적으로 출력한다. Compute-in-memory는 저장 위치 가까이에서 연산해 이동 비용을 줄이려는 접근이며 memristive 소자·디지털 회로 등 여러 구현이 있다. 소자 편차·정밀도·변환 회로의 비용이 전체 시스템의 결과에 영향을 준다.

## 빛, 양자, 생체 인터페이스

Photonic computing은 빛의 전파·간섭 등을 연산과 통신에 이용한다. Quantum computing은 qubit의 상태와 연산·측정에 기반하며 특정 알고리즘과 오류 조건에서 계산적 이점을 논의한다. Bioelectronics·웨어러블·유연 전자소자는 생체 신호와 재료, 구동 조건, 장시간 안정성을 함께 다룬다.

소자의 동작 원리, 회로의 기능, 시스템의 유효 성능은 서로 다른 수준에서 확인할 내용이다. 논문의 비교 조건과 실제 입출력·보정·주변 회로까지 연결하면 기술의 위치를 구체적으로 이해할 수 있다.

## 관련 기술

SNN, Neuromorphic, Event Camera, Quantum, Photonics, Compute-in-Memory, Memristor, Wearables

## 참고 자료

- [snnTorch documentation](https://snntorch.readthedocs.io/en/latest/)

## 기초 해설

- [전류의 합으로 내적 계산하기: memristive PIM과 비이상성](해설_notes/전류의합으로내적계산하기_memristive-pim-dot-products.md)

## English

### Emerging devices and computing

New computing architectures explore different approaches to the limits of data movement, power, connectivity, and physical implementation. Comparing results across fields requires knowing what was computed and which costs were included.

### Neuromorphic and in-memory computing

Spiking neural networks use events and state changes over time. Event cameras asynchronously report brightness changes. Compute-in-memory moves computation closer to stored data to reduce transfer costs, with implementations ranging from memristive devices to digital circuits. Device variation, numerical precision, and conversion-circuit costs affect system-level results.

### Photonics, quantum computing, and biointerfaces

Photonic computing uses light propagation and interference for computation and communication. Quantum computing uses qubit states, operations, and measurements; computational advantages depend on the algorithm and error conditions. Bioelectronics, wearables, and flexible electronics combine biological signals, materials, operating conditions, and long-term stability.

A device's operating principle, a circuit's function, and a system's effective performance are different levels of evidence. A paper's comparison conditions, inputs and outputs, calibration, and peripheral circuits help place its results in context.

### Foundation article

- [전류의 합으로 내적 계산하기: memristive PIM과 비이상성](해설_notes/전류의합으로내적계산하기_memristive-pim-dot-products.md#english)


## 심화 해설 | Advanced article

- [PIM 출력 교정: gain·offset을 고칠 수 있는 범위](해설_notes/PIM출력교정_pim-calibration.md) · [English](해설_notes/PIM출력교정_pim-calibration.md#english)
