# 코드 예제

개념 설명에 사용한 짧은 예제를 모았다.

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
