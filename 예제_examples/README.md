# 코드 예제 | Code examples

개념 설명에 사용한 짧은 예제를 모았습니다. [기초 모델과 자동 검증](공학기초_foundations/README.md)은 수학·물리, 회로·하드웨어, 펌웨어·시스템, 신호·제어·AI의 참조 구현을 연결합니다.

| 파일 | 내용 | 실행 환경 |
|---|---|---|
| [mean.c](mean.c) | 배열과 길이를 전달해 평균 계산 | C17, GCC·Clang |
| [mean.cpp](mean.cpp) | vector와 accumulate | C++17 이상 |
| [lower_bound.py](lower_bound.py) | 정렬 배열의 첫 경계 탐색 함수 | Python 3 |
| [rc_euler.py](rc_euler.py) | RC 미분방정식의 Euler 근사와 해석해 | Python 3 표준 라이브러리 |
| [rc_plot.py](rc_plot.py) | RC 충전 파형 | NumPy·Matplotlib |
| [rc_response.m](rc_response.m) | MATLAB RC 응답 계산 | MATLAB·호환 환경 |
| [rc_response.ipynb](rc_response.ipynb) | 수식·계산·그래프를 묶은 노트북 | Jupyter·NumPy·Matplotlib |
| [counter.sv](counter.sv) | 동기식 리셋 8비트 카운터 | SystemVerilog 도구 |
| [pytorch_autograd.py](pytorch_autograd.py) | x²의 자동미분 | PyTorch |
| [tensorflow_autograd.py](tensorflow_autograd.py) | 같은 미분의 GradientTape 표현 | TensorFlow |
| [files.sh](files.sh) | 디렉터리·CSV·파일 검색 | Bash |

아래 명령은 Bash에서 `예제_examples` 디렉터리를 작업 위치로 하여 실행합니다.

```bash
python3 rc_euler.py
gcc -std=c17 -Wall -Wextra -Wpedantic mean.c -o mean
./mean
g++ -std=c++17 -Wall -Wextra -Wpedantic mean.cpp -o mean_cpp
./mean_cpp
```

Jupyter·그래프 예제의 패키지는 [requirements.txt](requirements.txt)에 묶었습니다. 자동미분 파일은 각각 PyTorch 또는 TensorFlow가 필요합니다. Scalar 미분 예제에는 GPU가 필요하지 않습니다. Framework 설치는 [Python & Jupyter](../분야_topics/03-python-jupyter/README.md)의 참고 자료와 [PyTorch](https://pytorch.org/get-started/locally/)·[TensorFlow](https://www.tensorflow.org/install) 설치 문서에서 환경별로 다룹니다.

## 실무 오류 재현

[C/C++·펌웨어·칩·AI 검증 코드](실무검증_practical-validation/README.md)는 프레임 길이, 소유권·공개 순서, RTOS 동시성, 인터럽트·DMA·캐시, CAN·SPI·I2C·UART·이더넷, 워치독·리셋, USB·PCIe, 부트로더·업데이트, NVMe·eMMC·SD, 저널 복구, NAND 관리, FTL 매핑, 파일시스템 복구, 백업 복원, RAID, I/O 재시도, ECC, DDR, RTL·CDC와 기준 모델, 산술 폭·시험 ID·자식프로그램 판정, 배포 전처리·group 평가의 잘못된 조건과 해결한 조건을 실행합니다. [설계 사례](../설계와검증사례_engineering-cases/README.md)에서 원인·입력·검증 결과를 함께 읽으실 수 있습니다.

## 분야별 참조 모델과 통합 검사

[분야별 계산 예제](확장기초_extended/README.md)에서는 타이밍·전력·통신·테스트를 포함한 하드웨어, OS·도구·디버깅·로봇 제어를 포함한 시스템, GPU·데이터베이스·분산 시스템·AI·수치해석을 계산하고 검증합니다. 기초·추론·확장·심화 참조 모델의 통합 검사는 저장소 루트에서 실행합니다. 실무 검증과 임베디드 실습은 각 디렉터리의 별도 명령을 사용합니다.

```bash
python 예제_examples/run_checks.py
```

2026-10-19 기록에서는 Python 표준 라이브러리를 사용하는 298개 검사가 통과했습니다. 검사에는 독립 계산과의 비교, 경계 조건, 상태 불변식, 수렴률, 무작위 입력, 오류 주입이 포함됩니다. 실행 환경과 검사별 결과는 [검증 기록](VALIDATION.json)에 남겼습니다.

## 심화 구현과 검증

[심화 예제](심화_advanced/README.md)는 회로·RTL, 펌웨어·시스템, AI·데이터, 수학·제어·추론의 구현과 독립 검사를 연결합니다. [심화 해설](../공학기초_foundations/심화학습_ADVANCED.md)에서 단계별 유도와 실행 결과를 읽을 수 있습니다.

## 하드웨어 코딩 문제와 회로 예제

[하드웨어 코딩 문제와 예제](../하드웨어코딩_hardware-coding/README.md)는 HDLBits의 Verilog 풀이와 사이트 채점 기록, SystemVerilog 전송 버퍼·UART·순서 검출기, VHDL·Amaranth 카운터를 연결합니다. 각 회로의 소스·시간 흐름·자체 검사와 실행 도구를 함께 읽으실 수 있습니다.

## MCU 펌웨어와 디버깅

[Arm·RISC-V·STM32·ESP32 실습](임베디드디버깅_embedded-debug-labs/README.md)은 시작 코드, 메모리 배치, OpenOCD·GDB 연결, GPIO와 FreeRTOS 명령 처리를 다룹니다.

[Embedded validation lab](../프로젝트_projects/embedded-validation-lab/README.md)은 RV32I CPU와 Python 참조 모델, Cortex-M7·STM32·ESP32 펌웨어, UART 호스트 검증을 하나의 프로젝트로 연결합니다.

## English

[Advanced examples](심화_advanced/README.md) connect circuit/RTL, firmware/systems, AI/data and mathematical implementations with independent checks. [The advanced articles](../공학기초_foundations/심화학습_ADVANCED.md#english) provide step-by-step derivations and execution results.

Short executable examples accompany the concept notes. [Foundation models and automated checks](공학기초_foundations/README.md#english) connect mathematics, physics, circuits, hardware, firmware, systems, signals, control and AI.

| File | Content | Runtime |
| --- | --- | --- |
| [mean.c](mean.c) | Mean from an array and length | C17, GCC/Clang |
| [mean.cpp](mean.cpp) | vector and accumulate | C++17+ |
| [lower_bound.py](lower_bound.py) | First-boundary search in a sorted array | Python 3 |
| [rc_euler.py](rc_euler.py) | Euler approximation and analytic RC solution | Python standard library |
| [rc_plot.py](rc_plot.py) | RC charging waveform | NumPy/Matplotlib |
| [rc_response.m](rc_response.m) | RC response | MATLAB or compatible runtime |
| [rc_response.ipynb](rc_response.ipynb) | Equations, calculation and plots | Jupyter/NumPy/Matplotlib |
| [counter.sv](counter.sv) | Synchronous-reset eight-bit counter | SystemVerilog tools |
| [pytorch_autograd.py](pytorch_autograd.py) | Automatic derivative of x² | PyTorch |
| [tensorflow_autograd.py](tensorflow_autograd.py) | The same derivative with GradientTape | TensorFlow |
| [files.sh](files.sh) | Directory, CSV and file search | Bash |

The first command block runs the RC calculation and builds/runs the C/C++ examples from the `예제_examples` directory in Bash. [requirements.txt](requirements.txt) lists notebook/plot dependencies. Autograd files additionally require their respective framework; these scalar examples need no GPU. See [Python & Jupyter](../분야_topics/03-python-jupyter/README.md), [PyTorch](https://pytorch.org/get-started/locally/) and [TensorFlow](https://www.tensorflow.org/install) for installation references.

### Reference models by topic and integrated checks

The [extended foundation models](확장기초_extended/README.md) cover hardware timing, power, communications and test; systems tools, debugging and robot control; and GPU, database, distributed-system, AI and numerical models. The repository-root command runs the foundation, reasoning, extended and advanced reference suites. Practical-validation and embedded labs use their own commands.

The 2026-10-19 record reports 298 passing checks using the Python standard library. They include independent calculations, boundary conditions, state invariants, convergence rates, randomized inputs and fault injection. The [validation record](VALIDATION.json) contains the execution environment and per-suite results.

[Embedded debug labs](임베디드디버깅_embedded-debug-labs/README.md) cover Arm/RISC-V startup, memory layout, OpenOCD/GDB, GPIO and FreeRTOS command processing. The [embedded validation lab](../프로젝트_projects/embedded-validation-lab/README.md) connects an RV32I CPU/Python reference with Cortex-M7/STM32/ESP32 firmware and UART validation.
