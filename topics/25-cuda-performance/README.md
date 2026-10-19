# CUDA & GPU Optimization

[전체 목차](../../CATALOG.md) · [처음으로](../../README.md)

CUDA는 NVIDIA GPU에서 병렬 연산을 작성하고 실행하는 플랫폼이다. CUDA C++의 kernel은 GPU에서 여러 thread로 실행되며, thread는 block에, block은 grid에 묶인다. 모든 GPU가 CUDA를 실행하는 것은 아니다.

## 실행 단위와 데이터 이동

Block 안의 thread는 shared memory와 동기화를 사용할 수 있다. Global memory는 큰 데이터를 저장하지만 접근 패턴이 성능에 영향을 준다. 인접 thread가 인접 메모리에 접근하는 coalescing은 메모리 요청 효율과 관련된다. Stream은 작업의 순서를 구성하며, 서로 다른 작업이 실제로 겹치는지는 의존성과 하드웨어 조건에 달려 있다.

## 라이브러리와 직접 작성한 kernel

cuBLAS는 선형대수, cuDNN은 신경망 연산, CUTLASS는 고성능 행렬 연산 구성요소를 제공한다. Triton은 GPU kernel을 작성하는 별도 언어·컴파일러 생태계다. 직접 kernel을 작성하는 경우에는 산술 결과뿐 아니라 경계 인덱스와 동기화 조건도 정확해야 한다.

Nsight Systems는 시스템 수준의 실행 타임라인, Nsight Compute는 kernel 내부 성능 분석에 쓰인다. GPU 작업은 비동기로 실행되므로 CPU에서 호출 시간만 재면 실제 계산 시간을 놓칠 수 있다. CUDA event나 적절한 동기화를 포함한 측정이 필요하다.

드라이버·CUDA Toolkit·프레임워크에 포함된 runtime은 구분된다. TensorRT는 추론 최적화에, ROCm·HIP은 AMD GPU 생태계에, SYCL·oneAPI·OpenCL·Metal은 다른 이기종 연산 환경에 쓰인다. OpenMP·OpenACC도 가속기 연산을 표현하는 방법이다.

## 관련 기술

CUDA, cuBLAS, cuDNN, CUTLASS, Triton, Nsight, ROCm/HIP, SYCL/oneAPI, OpenCL, Metal, OpenMP/OpenACC, TensorRT, OpenVINO

## 참고 자료

- [CUDA Programming Guide](https://docs.nvidia.com/cuda/cuda-programming-guide/index.html)
