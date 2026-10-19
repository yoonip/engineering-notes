# GPU Architecture

[전체 목차](../../CATALOG.md) · [처음으로](../../README.md)

GPU는 많은 연산을 병렬로 처리하도록 구성된 프로세서다. CPU는 분기와 다양한 제어 흐름을 빠르게 처리하고, GPU는 병렬성이 충분하고 메모리 접근이 규칙적인 작업에서 높은 처리량을 얻는다. 그래픽카드는 GPU와 메모리·전원·냉각·입출력 회로를 포함한 제품이다.

## 실행과 메모리

NVIDIA GPU의 SM·warp, AMD GPU의 compute unit·wavefront는 각 생태계의 실행 구조와 용어다. SIMT는 여러 스레드가 명령 실행을 공유하는 모델이다. 같은 그룹 안에서 분기 경로가 갈라지면 활성 스레드가 나뉘어 처리량이 줄 수 있다. Tensor Core 같은 행렬 연산기는 지원 자료형과 연산 조건에서 높은 처리량을 제공한다.

GDDR·HBM은 고대역폭 메모리에 사용되며 용량과 대역폭은 다른 특성이다. PCIe는 호스트와 장치 사이의 전송, NVLink는 지원 시스템에서 GPU 연결에 사용된다. NVIDIA·AMD·Intel·Apple GPU는 하드웨어와 소프트웨어 지원 조건이 서로 다르다.

## 처리량과 병목 읽기

Roofline 모델은 연산 집약도와 메모리 대역폭을 이용해 계산 병목을 본다. 연산량이 많아도 데이터를 공급하지 못하면 메모리 제한을 받는다. 그래픽 작업은 vertex·rasterization·fragment 처리 등으로 이어지고, OpenGL·Vulkan·DirectX는 그래픽·컴퓨팅 기능에 접근하는 API 계열이다. 처리량·지연·전력·온도는 서로 다른 측정 항목이다.

## 관련 기술

NVIDIA, AMD, Intel, Apple GPU, SIMT/SIMD, Cache/VRAM, HBM/GDDR, PCIe/NVLink, Roofline, Vulkan, OpenGL, DirectX

## 참고 자료

- [CUDA Programming Guide](https://docs.nvidia.com/cuda/cuda-programming-guide/index.html)

## English

A GPU is designed to process many operations in parallel. CPUs handle diverse control flow and branching well, while GPUs achieve high throughput when work offers enough parallelism and regular memory access. A graphics card contains the GPU together with memory, power delivery, cooling, and I/O circuitry.

### Execution and memory

SM and warp are NVIDIA execution terms; compute unit and wavefront are terms used in the AMD ecosystem. SIMT allows groups of threads to share instruction execution. Divergent branches within a group can reduce useful throughput. Matrix units such as Tensor Cores provide high throughput for supported operations and data types.

GDDR and HBM provide high-bandwidth device memory. Capacity and bandwidth describe different properties. PCIe transfers data between host and device, while NVLink connects GPUs in supported systems. NVIDIA, AMD, Intel, and Apple GPUs have different hardware and software support.

### Reading performance results

The Roofline model relates arithmetic intensity to memory bandwidth and compute limits. Even a compute-heavy algorithm becomes memory-bound if data cannot be supplied fast enough. Graphics workloads include stages such as vertex processing, rasterization, and fragment processing. OpenGL, Vulkan, and DirectX expose graphics and computing capabilities through APIs. Throughput, latency, power, and temperature are separate measurements.
