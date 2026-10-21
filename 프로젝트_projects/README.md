# 구현 프로젝트

회로와 펌웨어, 정수 연산 모델과 학습 코드를 구현하고 실행 결과를 비교한 프로젝트를 모았습니다. 각 폴더에 소스와 실행 방법, 검증 조건을 함께 정리했습니다.

| 프로젝트 | 구현 내용 | 확인한 결과 |
| --- | --- | --- |
| [제조 trace 이상 탐지](st-awfd-anomaly-triage/README.md) | Strict-causal Transformer·CNN 비교, 저장 모델 추론, CSV·Excel 결과 저장 | CPU 모델·causal mask·결과 저장 회귀 9개 |
| [점자 → 한국어 Transformer](braille-transformer/README.md) | 문자 단위 encoder–decoder, 전처리·학습·생성 평가, CPU 앱 | 16 epoch 실험 기록, 합성 자료 회귀 6개 |
| [M2M100 · LoRA 영한 번역](en-ko-m2m100-lora/README.md) | 그룹 분할, LoRA 학습·평가, CPU·GPU 추론 앱 | 3 epoch 실험 기록, 합성 자료 회귀 6개 |
| [Transformer · DRAM-PIM](transformer-dram-pim/README.md) | 2-layer GPT RTL, Q8.8 기준 모델, K/V cache, E8M7 연산, DRAM 이벤트 분석 | Python 회귀·경계 검사, RTL 수치 비교, 저장된 Vivado 구현 결과 |
| [부분곱 제거 · CNN](cnn-partial-product-reproduction/README.md) | Signed 부분곱 열 제거, CMOS MAC netlist, CIFAR ResNet 양자화 | 산술 전수 비교 548,864건, 회귀 23개, 정수 출력 비교 |
| [MNIST 회로 추론](mnist-circuit-inference/README.md) | 학습 가중치의 저항 행렬 매핑, 2-layer 아날로그 추론 netlist | ngspice 두 표본 재실행, Python 기준 출력과 수치 비교 |
| [Embedded validation lab](embedded-validation-lab/README.md) | RV32I CPU, Arm·STM32·ESP32 펌웨어, UART 자동화 | RTL 14회, QEMU 실행, STM32 빌드, UART 검사 10개 |
| [FPGA validation harness](fpga-validation-harness/README.md) | FPGA 입력·출력 프레임, ADC 오류 시나리오, 검증 자동화 | RTL 64개 패턴, Python 오류·프레임 검사 |
| [Practical Silicon Lab](practical-silicon-lab/README.md) | Arm64 시작 코드, JTAG TAP, Linux driver, 가상 bench | 오프라인·mock 검사 19개 |
| [신경망 에너지 모델](neural-network-energy-models/README.md) | 연산 정밀도·메모리 이동·에너지 수식의 수치 모델 | 단위 검사 8개와 수치 비교 108조건 |
| [Tiny Transformer RTL](tiny-transformer-rtl/README.md) | NumPy 학습과 Q8.8 가중치 export, SystemVerilog token 생성 | 네 입력 조건의 token·causal mask·EOS, RTL·JSON 가중치 일치 |

## 설계 선택과 새 실행 기록

[설계와 검증 사례](../설계와검증사례_engineering-cases/README.md)에서 C/C++·펌웨어·RTOS·인터럽트·DMA·SPI·I2C·CAN·UART·이더넷·워치독·리셋·USB·PCIe·펌웨어 업데이트·DDR·RTL·CDC·칩 시험 자동화·AI·FPGA·SQLite의 요구사항과 대안, 재현 코드와 2026-10-21의 실행 결과를 읽으실 수 있습니다. [현장 계측과 검증](../현장계측과검증_measurement-validation/README.md)은 장비 사용·펌웨어 오류·칩 시험·자동화 절차를 관련 구현으로 연결합니다. 프로젝트별 이전 결과와 새 검사의 범위는 각 기록에서 구별합니다.

## 알고리즘과 개발 도구

| 프로젝트 | 내용 | 확인한 결과 |
| --- | --- | --- |
| [Coding practice toolkit](coding-practice-toolkit/README.md) | C·C++·Python 주석 예제, 입력 fixture, VS Code 실행·디버깅 도구 | 주석 코드 66개, fixture 실행 255회, 한글 경로 실행 |
| [기초 알고리즘 · 세 언어 비교](coding-practice-basics/README.md) | 센서 요약·빈도·정렬·BFS·DP·이분 탐색의 독립 실행 예제 | C/C++ 빌드 12개, Python 문법 검사 6개, 실행 18회 |
| [Python 연습문제 풀이](python-practice-solutions/README.md) | 공개 연습문제 39개의 풀이와 알고리즘별 학습 기록 | 로컬 테스트 65개, 함수 호출 4,190회 |
| [Python 기초 실습](python-foundations-practice/README.md) | 콘솔 예제와 독립 실행 HTML 50문항 | 허용 정답 68건 실행, 콘솔·화면 상태 전환 검사 |

## 코드와 검증

세부 실습은 아래 본문으로 바로 들어가실 수 있습니다.

- Practical Silicon Lab: [Arm64 시작과 UART](practical-silicon-lab/arm64/README.md), [JTAG TAP와 디버깅](practical-silicon-lab/jtag/README.md), [Linux 장치 I/O](practical-silicon-lab/linux/README.md), [검증 결과 판정](practical-silicon-lab/validation/README.md)
- Embedded validation lab: [MNIST의 학습·검증·추론](embedded-validation-lab/mnist/README.md)

RTL의 출력은 Python 정수 기준 모델과 대조하고, 펌웨어는 컴파일·시뮬레이션·통신 검사로 확인했습니다. 합성·배치배선 결과와 소프트웨어 시뮬레이션 결과는 해당 프로젝트의 검증 기록에서 구분합니다.

짧은 계산·언어 예제는 [examples](../예제_examples/README.md), Arm·RISC-V의 명령 단위 실행과 OpenOCD·GDB 실습은 [embedded-debug-labs](../예제_examples/임베디드디버깅_embedded-debug-labs/README.md)에 있습니다. [Programmers](../programmers/README.md)에는 문제 풀이와 학습 기록을 정리했습니다.

## English

These projects connect circuits, firmware, integer reference models and machine-learning experiments. Each directory contains the source, execution steps and verification conditions.

### Hardware, models and machine learning

| Project | Implementation | Recorded checks |
| --- | --- | --- |
| [Manufacturing-trace anomaly detection](st-awfd-anomaly-triage/README.md) | Strict-causal Transformer/CNN comparison, saved-model inference, CSV/Excel export | Nine CPU model, causal-mask and export regression checks |
| [Braille-to-Korean Transformer](braille-transformer/README.md) | Character-level encoder–decoder, preprocessing, training, generation evaluation and CPU app | Recorded 16-epoch experiment and six synthetic-data checks |
| [M2M100/LoRA English-to-Korean translation](en-ko-m2m100-lora/README.md) | Grouped data split, LoRA training/evaluation and CPU/GPU apps | Recorded three-epoch experiment and six synthetic-data checks |
| [Transformer/DRAM-PIM](transformer-dram-pim/README.md) | Two-layer GPT RTL, Q8.8 reference, K/V cache, E8M7 arithmetic and DRAM event analysis | Python regressions/boundaries, RTL numerical comparisons and recorded Vivado implementation |
| [Partial-product removal/CNN](cnn-partial-product-reproduction/README.md) | Signed partial-product removal, CMOS MAC netlists and quantized CIFAR ResNets | 548,864 exhaustive arithmetic cases, 23 regressions and integer-output comparisons |
| [MNIST circuit inference](mnist-circuit-inference/README.md) | Trained-weight resistor mapping and two-layer analog inference netlists | Two ngspice samples replayed against a Python reference |
| [Embedded validation lab](embedded-validation-lab/README.md) | RV32I CPU, Arm/STM32/ESP32 firmware and UART automation | Fourteen RTL runs, QEMU execution, STM32 build and ten UART tests |
| [FPGA validation harness](fpga-validation-harness/README.md) | Input/output frames, ADC fault scenarios and automated validation | Sixty-four RTL patterns and Python fault/frame checks |
| [Practical Silicon Lab](practical-silicon-lab/README.md) | Arm64 startup, JTAG TAP, Linux driver and virtual bench | Nineteen offline/mock checks |
| [Neural-network energy models](neural-network-energy-models/README.md) | Precision, data movement and analytical energy models | Eight unit tests and 108 numerical conditions |
| [Tiny Transformer RTL](tiny-transformer-rtl/README.md) | NumPy training, Q8.8 weight export and SystemVerilog token generation | Four input cases, causal masking, EOS and matching RTL/JSON weights |

### Algorithms and development tools

| Project | Content | Recorded checks |
| --- | --- | --- |
| [Coding practice toolkit](coding-practice-toolkit/README.md) | Annotated C/C++/Python examples, fixtures and VS Code execution/debugging tools | Sixty-six annotated programs, 255 fixture executions and Korean-path execution |
| [Basic algorithms across three languages](coding-practice-basics/README.md) | Aggregation, counting, sorting, BFS, DP and binary search | Twelve C/C++ builds, six Python syntax checks and eighteen executions |
| [Python practice solutions](python-practice-solutions/README.md) | Thirty-nine public exercises with an algorithm index | Sixty-five local tests and 4,190 solution calls |
| [Python foundations](python-foundations-practice/README.md) | Console examples and a standalone 50-question HTML exercise | Sixty-eight accepted answers, console checks and UI-state checks |

RTL outputs are compared with Python integer references. Firmware checks cover compilation, simulation and communication behavior; synthesis/place-and-route results are identified separately in each project. Short examples are in [examples](../예제_examples/README.md), instruction-level Arm/RISC-V and OpenOCD/GDB exercises are in [embedded-debug-labs](../예제_examples/임베디드디버깅_embedded-debug-labs/README.md), and [Programmers](../programmers/README.md) contains problem solutions and study records.
