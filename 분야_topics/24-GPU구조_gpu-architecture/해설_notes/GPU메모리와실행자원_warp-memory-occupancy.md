# GPU의 warp, 메모리 접근, occupancy

## 계산이 많다고 GPU가 항상 빠른 것은 아니다

GPU는 많은 작업을 겹쳐 처리해 전체 처리량을 높인다. 한 사람이 물건을 가져오는 동안 다른 사람이 계산하는 작업장을 떠올리면 이해하기 쉽다. 작업자가 많아도 모두 멀리 떨어진 창고를 제각각 방문하거나 서로의 결과를 기다리면 처리량이 떨어진다. GPU에서도 연산 수뿐 아니라 스레드가 읽는 주소, 분기, 레지스터와 shared memory 사용량을 함께 살펴야 한다.

CUDA의 thread는 프로그램의 실행 단위이고, block은 협력하고 동기화할 수 있는 thread 묶음이다. NVIDIA GPU에서 warp는 32개 thread로 구성된다. 같은 warp의 thread가 다른 분기 경로를 선택하면 필요한 경로를 나누어 실행하면서 일부 lane이 비활성화될 수 있다. 최근 장치의 독립적인 thread scheduling도 프로그램에 필요한 동기화를 대신하지 않는다. 이 글은 NVIDIA CUDA의 실행 모델을 다루며 다른 GPU의 실행 단위 크기까지 일반화하지 않는다. [CUDA SIMT kernels](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/writing-cuda-kernels.html)

## 같은 데이터를 읽어도 주소 배치에 따라 비용이 달라진다

32개 thread가 각각 4 byte를 읽으면 유효 요청량은 128 byte다. Compute capability 6.0 이상 장치의 일반적인 global memory coalescing 설명에서는 필요한 32 byte 구간 수를 센다. 시작 주소가 32 byte 경계에 있고 각 thread가 연속된 4 byte를 읽으면 네 구간이면 충분하다. 시작을 4 byte 옮기면 다섯 구간, thread 간 주소 간격이 32 byte이면 32개 구간이 필요하다. 캐시 재사용이나 실제 DRAM 거래까지 이 숫자만으로 결정되지는 않는다. [NVIDIA Best Practices §10.2.1](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#coalesced-access-to-global-memory)

주소 $`a_i`$, 단어 크기 $`w`$, 구간 크기 $`S`$일 때 요청한 구간의 집합은 다음과 같다.

```math
\mathcal S=\bigcup_i\left\{\left\lfloor\frac{a_i}{S}\right\rfloor,\ldots,
\left\lfloor\frac{a_i+w-1}{S}\right\rfloor\right\}.
```

따라서 단순 모델의 전송량은 $`S\vert \mathcal S\vert `$다. 모든 주소가 서로 다른 단어라면 유효 byte 비율을 $`32w/(S\vert \mathcal S\vert )`$로 계산할 수 있다. 여러 thread가 같은 주소를 읽는 broadcast에서는 이 분자가 중복 요청량이므로, 고유하게 사용한 byte 수와 구분한다. Coalescing은 thread 번호순 정렬 자체가 아니라 같은 명령의 주소들이 적은 구간에 모이는 성질이다. 네 구간 안에서 주소 순서를 바꾸어도 구간 수는 같다.

| 32개 lane, 각 4 byte | 32 byte 구간 수 | 서로 다른 데이터의 유효 비율 |
|---|---:|---:|
| `a[i]=4*i` | 4 | 100% |
| `a[i]=4+4*i` | 5 | 80% |
| `a[i]=32*i` | 32 | 12.5% |

## Occupancy는 속도계가 아니라 자원 수용률이다

Occupancy는 SM에 상주하는 warp 수를 해당 SM의 최대 상주 warp 수로 나눈 값이다. 실행 중인 lane의 비율이나 GPU 사용률과 같은 뜻이 아니다. Block당 thread $`T`$, thread당 레지스터 $`r`$, block당 shared memory $`s`$를 사용한다고 하자. 총량만 고려한 block 수의 상한은

```math
B\le\min\left(B_{\max},\left\lfloor\frac{T_{SM}}T\right\rfloor,
\left\lfloor\frac{R_{SM}}{rT}\right\rfloor,
\left\lfloor\frac{S_{SM}}s\right\rfloor,
\left\lfloor\frac{W_{SM}}{\lceil T/32\rceil}\right\rfloor\right).
```

사용량이 0인 자원 항은 제외한다. 예를 들어 가정한 SM의 레지스터가 65,536개이고 block이 256 thread라면 thread당 32개 사용 시 레지스터로는 8개 block, 64개 사용 시 4개 block까지 들어간다. 실제 장치는 레지스터 할당 단위, SM 내부 분할, block당 제한도 있으므로 이 식은 정확한 occupancy 계산기를 대체하지 않는다. 레지스터를 과도하게 줄여 spill이 생기면 occupancy가 높아져도 느려질 수 있다. [NVIDIA occupancy 설명](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#occupancy)

## 구현과 검증

[계산 모델](../../../예제_examples/확장기초_extended/ai_data/models.py)의 `memory_sectors`는 경계에 걸친 단어까지 포함해 집합을 계산한다. `occupancy_bound`는 위 자원 상한을 구현하며 기본 용량은 설명용 가정이다. 특정 GPU 사양으로 표시하지 않는다.

```python
from models import memory_sectors, occupancy_bound

# 연속 접근과 큰 간격 접근이 요구하는 구간 수를 비교한다.
print(memory_sectors([4 * i for i in range(32)]))   # 4
print(memory_sectors([32 * i for i in range(32)]))  # 32
print(occupancy_bound(256, 64, 0))                  # (4, 0.5)
```

[독립 검증](../../../예제_examples/확장기초_extended/ai_data/test_models.py)은 표의 세 패턴, 구간 경계를 넘는 단어, broadcast, 레지스터·shared memory 한계를 확인한다. 이는 CPU에서 실행하는 주소·자원 계산 검증이다. 실제 커널은 대상 GPU에서 결과 정확성, 전송 포함 실행 시간, profiler의 메모리 지표를 함께 측정해야 성능을 판단할 수 있다. Roofline의 연산량/전송량 분석에 이 글의 주소 배치와 자원 제한을 더하면 병목의 원인을 더 구체적으로 설명할 수 있다.

## English

### Throughput depends on how work is arranged

A GPU overlaps many tasks to increase throughput. A workshop with many workers can still stall when everyone visits distant storage or waits for another worker. Similarly, arithmetic count alone does not determine GPU performance: addresses, branches, registers and shared memory matter.

A CUDA thread is an execution unit and a block groups threads that can cooperate and synchronize. An NVIDIA warp contains 32 threads. Divergent branches can require different paths to run with some lanes inactive. Independent thread scheduling on newer devices does not remove required synchronization. These statements describe NVIDIA CUDA, not every GPU architecture. [CUDA execution and SIMT](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/writing-cuda-kernels.html)

### Count the memory regions touched

For the usual global-memory coalescing model on compute capability 6.0 or newer, count the required 32-byte regions. Thirty-two distinct aligned consecutive 4-byte loads touch four regions. Moving the first address by four bytes touches five; a 32-byte stride touches 32. The table above gives the corresponding useful-byte fractions. Cache reuse and actual DRAM traffic are additional effects. [NVIDIA coalescing](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#coalesced-access-to-global-memory)

For addresses $`a_i`$, word width $`w`$ and region width $`S`$, the union in the equation above includes every region crossed by each word, including words spanning a boundary. The model transfers $`S\vert \mathcal S\vert `$ bytes. The fraction $`32w/(S\vert \mathcal S\vert )`$ assumes distinct requested words. Broadcast requests require distinguishing duplicate lane requests from unique useful bytes. Permuting addresses within the same four regions does not change the count: coalescing concerns locality within one warp instruction, not thread ordering by itself.

### Occupancy measures residency

Occupancy is resident warps divided by the SM's maximum resident warps, not active-lane fraction or general GPU utilization. The resource equation bounds resident blocks using block count, threads, registers, shared memory and warps. Omit a resource term when its usage is zero. With the illustrative 65,536-register SM and 256-thread blocks, 32 registers per thread permit at most eight blocks from register capacity; 64 permit four.

Real allocation granularity, SM partitions and per-block limits can reduce residency further. The model is therefore a resource upper bound, not an architecture-accurate occupancy calculator. Forcing fewer registers may cause spills, so a higher occupancy need not improve performance. [NVIDIA occupancy](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#occupancy)

### Implementation and checks

The linked `memory_sectors` computes the set of touched regions, and `occupancy_bound` implements the simplified bound. Its default capacities are illustrative assumptions, not specifications of a named GPU. The tests check aligned, misaligned, strided, boundary-spanning and broadcast accesses, plus register and shared-memory limits. They validate CPU calculations without running CUDA. Actual kernel performance requires correctness checks, timing including relevant transfers and profiler evidence on the target device. These address and residency models complement the operation/traffic analysis used by roofline.

## Sources

- [NVIDIA CUDA Programming Guide, Writing SIMT Kernels](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/writing-cuda-kernels.html): warp execution, divergence and global-memory transactions.
- [NVIDIA CUDA Best Practices Guide](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html): coalescing examples, residency limits and the distinction between occupancy and performance. Reference date: 2026-10-19.
