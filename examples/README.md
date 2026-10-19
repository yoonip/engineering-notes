# 코드 예제

개념 설명에 사용한 짧은 예제를 모았다. [기초 모델과 자동 검증](foundations/README.md)은 수학·물리, 회로·하드웨어, 펌웨어·시스템, 신호·제어·AI의 참조 구현을 연결한다.

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

```bash
python3 rc_euler.py
gcc -std=c17 -Wall -Wextra -Wpedantic mean.c -o mean
./mean
g++ -std=c++17 -Wall -Wextra -Wpedantic mean.cpp -o mean_cpp
./mean_cpp
```

Jupyter·그래프 예제의 패키지는 [requirements.txt](requirements.txt)에 묶었다. 자동미분 파일은 각각 PyTorch 또는 TensorFlow가 필요하다. Scalar 미분 예제에는 GPU가 필요하지 않다. Framework 설치는 [Python & Jupyter](../topics/03-python-jupyter/README.md)의 참고 자료와 [PyTorch](https://pytorch.org/get-started/locally/)·[TensorFlow](https://www.tensorflow.org/install) 설치 문서에서 환경별로 다룬다.

## MCU 펌웨어와 디버깅

[Arm·RISC-V·STM32·ESP32 실습](embedded-debug-labs/README.md)은 시작 코드, 메모리 배치, OpenOCD·GDB 연결, GPIO와 FreeRTOS 명령 처리를 다룬다.

[Embedded validation lab](../projects/embedded-validation-lab/README.md)은 RV32I CPU와 Python 참조 모델, Cortex-M7·STM32·ESP32 펌웨어, UART 호스트 검증을 하나의 프로젝트로 연결한다.

## English

Short executable examples accompany the concept notes. [Foundation models and automated checks](foundations/README.md#english) connect mathematics, physics, circuits, hardware, firmware, systems, signals, control and AI.

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

The commands above run the RC calculation and build/run the C/C++ examples. [requirements.txt](requirements.txt) lists notebook/plot dependencies. Autograd files additionally require their respective framework; these scalar examples need no GPU. See [Python & Jupyter](../topics/03-python-jupyter/README.md), [PyTorch](https://pytorch.org/get-started/locally/) and [TensorFlow](https://www.tensorflow.org/install) for installation references.

[Embedded debug labs](embedded-debug-labs/README.md) cover Arm/RISC-V startup, memory layout, OpenOCD/GDB, GPIO and FreeRTOS command processing. The [embedded validation lab](../projects/embedded-validation-lab/README.md) connects an RV32I CPU/Python reference with Cortex-M7/STM32/ESP32 firmware and UART validation.
