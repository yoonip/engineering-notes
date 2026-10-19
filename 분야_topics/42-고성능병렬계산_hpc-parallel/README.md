# 고성능·병렬 계산 | HPC, Parallel & Distributed Computing

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

병렬 계산은 작업을 여러 실행 자원에 나누는 방법이다. 작업을 얼마나 나눌 수 있는지와 데이터 이동·동기화 비용이 전체 성능을 제한한다. Amdahl 법칙은 병렬화되지 않는 부분이 속도 향상의 한계를 만든다는 점을 보여준다.

## 공유 메모리와 분산 메모리

OpenMP는 thread 기반 공유 메모리 병렬화, MPI는 프로세스 간 메시지 전달에 쓰인다. SIMD는 하나의 명령으로 여러 데이터 원소를 처리한다. AVX·NEON은 아키텍처별 벡터 명령이다. NUMA에서는 어느 CPU에 연결된 메모리에 접근하는지가 지연과 대역폭에 영향을 준다.

## GPU와 분산 작업

NCCL은 GPU 간 집단 통신에, Slurm은 계산 자원의 작업 관리에, Ray·Dask는 분산 실행·데이터 처리에 쓰인다. 다중 GPU 학습에서는 gradient·parameter·activation을 어떤 방식으로 나누는지에 따라 계산과 통신 비용이 달라진다.

속도 향상은 `기준 실행 시간 / 병렬 실행 시간`으로 계산한다. 작업 크기 고정과 자원당 작업 크기 고정은 서로 다른 scaling 분석이다. Roofline·perf·profiler는 산술량보다 실제 메모리·통신·대기 병목을 드러내는 데 사용된다.

## 관련 기술

OpenMP, MPI, OpenACC, SIMD, AVX/NEON, NCCL, Slurm, Ray, Dask, perf

## 참고 자료

- [MPI Forum](https://www.mpi-forum.org/docs/)
- [OpenMP specifications](https://www.openmp.org/specifications/)

## 기초 해설

- [병렬 계산의 분할, reduction, 통신 비용](해설_notes/병렬계산의분할reduction통신비용_partition-reduction-and-communication.md)

## English

### HPC and parallel computing

Parallel computing divides work among execution resources. The portion that can be parallelized, together with data movement and synchronization, limits performance. Amdahl's law describes how the serial portion limits overall speedup.

### Shared and distributed memory

OpenMP supports thread-based shared-memory parallelism, and MPI supports message passing between processes. SIMD applies one instruction to several data elements. AVX and NEON provide architecture-specific vector instructions. On a NUMA system, the location of memory relative to a CPU affects latency and bandwidth.

### GPUs and distributed workloads

NCCL provides collective communication between GPUs. Slurm schedules computing jobs, while Ray and Dask support distributed execution and data processing. Multi-GPU training has different computation and communication costs depending on how gradients, parameters, and activations are partitioned.

Speedup is `baseline execution time / parallel execution time`. Holding total problem size fixed and holding work per resource fixed are different scaling studies. Roofline analysis, perf, and profilers help reveal memory, communication, and waiting bottlenecks beyond the arithmetic workload.

### Foundation article

- [병렬 계산의 분할, reduction, 통신 비용](해설_notes/병렬계산의분할reduction통신비용_partition-reduction-and-communication.md#english)
