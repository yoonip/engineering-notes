# 경계 tile까지 계산하는 행렬곱: CPU 기준선과 CUDA kernel

[CPU 계산](../../../예제_examples/심화_advanced/ai_data/advanced_ai_models.py) · [CUDA 전체 소스](../../../예제_examples/심화_advanced/ai_data/tiled_matmul.cu) · [검증 코드](../../../예제_examples/심화_advanced/ai_data/test_advanced_ai.py)

## 성능 식에서 실행 코드로

Roofline은 가능한 처리량의 상한을 설명한다. 실제 kernel을 만들 때는 각 출력의 담당 thread, 입력의 수명, 경계 조건과 검증 기준이 필요하다. 이 글은 $`C=AB`$, $`A:M\times K`$, $`B:K\times N`$의 순수 행렬곱을 다룬다. 기존 C를 더하거나 bias·activation을 적용하는 GEMM 변형은 아니다.

출력 정의는 $`C_{ij}=\sum_{p=0}^{K-1}A_{ip}B_{pj}`$다. Row-major 배열에서 주소 index는 A가 $`iK+p`$, B가 $`pN+j`$, C가 $`iN+j`$다. 이 세 stride를 섞으면 정방 행렬 일부에서만 우연히 맞는 구현이 생길 수 있다. 그래서 실행 예는 서로 다른 $`M=37,N=45,K=29`$를 사용한다. T=16의 배수도 아니므로 마지막 tile의 처리까지 확인한다.

## Tile의 부분합을 합치기

각 block은 출력의 16×16 영역을 맡는다. 내부 축을 16개씩 나누면

```math
C_{ij}=\sum_{q=0}^{\lceil K/T\rceil-1}
\sum_{r=0}^{T-1}\widetilde A_{i,qT+r}\widetilde B_{qT+r,j}.
```

물결표는 유효 범위 밖 원소를 0으로 확장했다는 뜻이다. 확장된 항은 합에 기여하지 않아 원래 식과 같다. 각 thread가 A·B shared tile의 한 원소를 채운 뒤 barrier를 지나고, 내부 r을 돌며 자신의 출력 하나에 누산한다. 다음 q가 같은 shared 저장소를 재사용하기 전에 다시 barrier를 둔다. 이 block 간에 공유하는 출력은 없어서 출력 누산에 atomic은 필요하지 않다.

Shared-memory 재사용 원리와 협력 thread의 동기화는 [NVIDIA Best Practices](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#shared-memory-in-matrix-multiplication-c-ab)와 [CUDA Programming Guide](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/writing-cuda-kernels.html)에서 대조했다. 문서의 성능 수치를 이 코드의 실측 결과로 옮기지 않는다.

## 경계를 검사하는 위치

Kernel 초반에 `if (row>=M || col>=N) return;`을 두면 출력이 없는 thread가 block barrier에 참여하지 않을 수 있다. 대신 load마다 유효성을 검사해 0을 넣고, 모든 thread가 같은 반복·barrier에 참여한다. C 저장에서만 유효한 row·column을 확인한다.

이 kernel은 정해진 tile16, 256 thread, FP32 입력과 누산을 사용한다. Tensor Core·비동기 복사·double buffering·register tiling을 쓰지 않는다. 설명이 단순한 비교 기준이며 최고 성능 GEMM의 설계라고 부르지 않는다. Block당 shared 배열은 두 개로 2,048 byte지만 실제 occupancy에는 register와 장치 제한도 들어간다.

## CPU 실행과 독립 기준해

```bash
python "예제_examples/심화_advanced/ai_data/demo.py" matrix
python -m unittest discover -s "예제_examples/심화_advanced/ai_data" -p "test_*.py" -v
```

CPU CLI는 Python의 blocked loop로 행렬곱을 실제 계산하고, 별도로 각 출력의 내적을 계산한 기준과 비교한다. 정수로 만든 작은 입력에서 최대 절대 차이 0, checksum -31이 나왔다. `cpu_seconds`는 해당 실행의 Python CPU 시간이며 CUDA 시간과 섞지 않는다.

테스트에서는 1×1뿐 아니라 3×5와 5×2, 17×9와 9×19처럼 서로 다른 크기를 사용한다. Fraction 기반 내적 기준과 tile 1·2·8·32의 결과를 비교한다. 출력 shape만 맞는지 보는 검사보다 stride·경계·누산 초기화 오류를 더 잘 드러낸다.

## CUDA 프로그램 실행 계약

CUDA Toolkit, 지원 GPU, 호환 driver와 host C++ compiler가 준비된 환경에서 아래 소스를 별도로 빌드한다. 생성한 실행 파일에서 직접 출력한 JSON이 GPU 실행의 근거다. Python CLI의 `cuda_executed:false`는 그 CPU 명령이 CUDA를 실행하지 않는다는 표시다.

```bash
nvcc -O2 -std=c++17 "예제_examples/심화_advanced/ai_data/tiled_matmul.cu" -o tiled_matmul
./tiled_matmul 37 45 29
```

Windows에서는 실행 파일 이름을 `tiled_matmul.exe`로 지정하고 `.\tiled_matmul.exe 37 45 29`로 실행할 수 있다. 인자 순서는 M N K이며 각각 1~2048을 받는다. 소스는 allocation·copy·launch·synchronize 오류를 확인하고, warm-up 한 번 뒤 CUDA event로 kernel 5회의 평균을 잰다. 이 시간에는 host-device 복사를 포함하지 않는다. 새 크기에서 정확도 확인 없이 시간 숫자만 비교하지 않는다.

GPU 결과 기준은 원래 FP32 입력을 CPU double로 곱해 누산한 값이다. 허용 오차는 $`2\times10^{-4}+2\times10^{-4}\lvert C_{\mathrm{ref}}\rvert`$이며 모든 원소를 검사한다. `failed_elements=0`일 때 정상 종료한다. 수치 합산 순서와 FMA 때문에 float 결과가 기준과 bit 단위로 같을 필요는 없다. 이 허용 오차가 모든 크기·입력 분포에 충분한 일반 정리라는 뜻도 아니다.

## 결과를 해석하는 범위

행렬이 작으면 launch와 고정 비용이 지배할 수 있다. Python CPU와 CUDA kernel의 비율은 같은 언어·최적화 수준의 CPU BLAS 대비 가속비가 아니다. 실제 비교는 같은 dtype·shape·정확도 조건, warm-up·반복 분포, transfer 포함 범위와 library 기준을 맞춘다. 여기서 구현한 것은 실행 가능한 행렬곱과 독립 정확도 검사이며, 작은 benchmark 하나로 장치 전체의 성능을 대표하지 않는다.

## English

### From a bound to an implementation

Roofline bounds throughput; a kernel additionally needs output ownership, data lifetime, boundaries and a correctness reference. This program computes only $`C=AB`$ for shapes $`M\times K`$ and $`K\times N`$, without an existing-C term, bias or activation. Row-major indices are $`iK+p`$, $`pN+j`$ and $`iN+j`$. Distinct nonmultiple dimensions 37, 45 and 29 expose indexing errors hidden by square or aligned tests.

Each 16×16-thread block owns one output tile. Splitting the inner sum into tile-sized chunks yields the equation above. Extending invalid input coordinates with zero preserves the original product. Threads stage shared A and B entries, synchronize, accumulate one output each and synchronize again before overwriting shared storage. Disjoint output ownership avoids the need for atomics.

The memory and synchronization design was cross-checked against [NVIDIA Best Practices](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#shared-memory-in-matrix-multiplication-c-ab) and [CUDA SIMT programming](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/writing-cuda-kernels.html). Published vendor timings are not results for this source.

### Boundary participation

Returning invalid output threads before a block barrier can violate required participation. The kernel instead guards each load, writes zero outside the input and keeps every thread in the same loop/barriers. Only the final output store is conditional.

This is an FP32 scalar-accumulation reference with tile 16 and 256 threads. It does not implement Tensor Cores, asynchronous copies, double buffering or register tiling and is not claimed as a peak-performance GEMM. Two shared arrays require 2,048 bytes, while registers and architecture constraints also affect residency.

### Executed CPU path and CUDA contract

The Python commands above execute a blocked CPU product and compare separately computed output dot products. Small integer-valued inputs gave maximum absolute error zero and checksum -31. The reported CPU duration is a Python measurement, not a CUDA duration. Unit tests compare rectangular products against Fraction dot products for tile widths 1, 2, 8 and 32.

Build the CUDA program with the shown command in an environment with a compatible GPU, driver, Toolkit and host compiler. The executable's own JSON provides GPU-run evidence. The CPU CLI's `cuda_executed:false` describes only that Python command. On Windows, name the executable `tiled_matmul.exe` and invoke `.\tiled_matmul.exe 37 45 29`. Argument order is M N K, each 1–2048.

The host checks CUDA allocation, copy, launch and synchronization errors. After one warm-up it times five kernels using CUDA events, excluding transfers. Every output is compared against a CPU double-precision accumulation of the original FP32 inputs. The threshold is $`2\times10^{-4}+2\times10^{-4}\lvert C_{\mathrm{ref}}\rvert`$. Zero failed elements returns success. Different summation orders and FMA need not give bit-identical float outputs; the threshold is an explicit example policy, not a universal error theorem.

### Interpretation

Small problems can be dominated by launch overhead. Comparing Python loops with a CUDA kernel does not establish speedup over optimized CPU BLAS. Useful comparisons align dtype, shape, tolerance, warm-up, repetition distribution and transfer scope, and include an appropriate library baseline. The program supplies executable arithmetic and an independent accuracy check; one small timing does not characterize an entire device.

## 출처 / Sources

- [NVIDIA CUDA Best Practices, shared-memory matrix multiplication](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#shared-memory-in-matrix-multiplication-c-ab): block reuse and synchronization.
- [NVIDIA CUDA Programming Guide, Writing SIMT Kernels](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/writing-cuda-kernels.html): thread indices, memory scope and block barriers. 확인 / checked: 2026-10-19.
