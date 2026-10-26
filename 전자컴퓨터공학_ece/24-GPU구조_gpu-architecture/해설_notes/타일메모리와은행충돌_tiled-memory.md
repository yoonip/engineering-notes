# 타일 재사용과 shared-memory bank conflict

[계산 코드](../../../예제_examples/심화_advanced/ai_data/advanced_ai_models.py) · [실행 CLI](../../../예제_examples/심화_advanced/ai_data/demo.py) · [검증](../../../예제_examples/심화_advanced/ai_data/test_advanced_ai.py)

## 함께 쓰는 데이터는 한 번 가져옵니다

Warp의 주소가 잘 모여 있어도 같은 데이터를 반복해서 global memory에서 가져오면 불필요한 요청이 남습니다. Tiling은 함께 쓸 작은 영역을 먼저 가져온 뒤 여러 계산에서 재사용하는 방식입니다. 식탁마다 소금을 매번 창고에서 가져오는 대신 작은 통을 놓는 것과 비슷합니다. 다만 통을 채우는 시간, 크기, 여러 사람이 동시에 접근하는 방식까지 고려해야 합니다.

행렬 $`A:M\times K`$, $`B:K\times N`$의 곱에서 출력 하나는 $`K`$개의 곱을 더합니다. 출력 tile을 $`T\times T`$로 나누고, 각 inner 구간에서 A와 B tile을 shared memory에 저장하면 입력 하나를 같은 block의 여러 출력에 재사용할 수 있습니다. Shared memory는 block 내부 협력을 위한 공간이며 다른 block에 자동으로 공유되는 cache가 아닙니다. [NVIDIA CUDA의 memory spaces와 동기화](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/writing-cuda-kernels.html)

## 입력 원소 요청 수를 직접 세기

출력마다 A와 B 값을 각각 읽는 단순한 코드의 입력 원소 요청은 $`2MNK`$개입니다. 이것은 source-level load 요청 수이며 실제 DRAM transaction 수는 아닙니다. Cache, broadcast와 compiler가 실제 traffic을 바꿉니다.

각 block이 필요한 A·B 영역을 한 번씩 가져오고 경계 밖 값을 0으로 채운다고 하겠습니다. A 전체의 유효 원소는 출력의 열 tile마다 한 번, B 전체는 행 tile마다 한 번 필요합니다.

```math
L_A=MK\left\lceil N/T\right\rceil,\qquad
L_B=KN\left\lceil M/T\right\rceil,\qquad
L=L_A+L_B.
```

정방 크기 $`M=N=K=n`$이 T의 배수면 단순 요청 $`2n^3`$에서 $`2n^3/T`$로 줄어 T배 재사용이 생깁니다. 같은 크기의 두 FP32 shared tile은 $`2T^2\times4`$ byte를 차지합니다. T를 키우면 재사용은 늘지만 shared memory와 thread·register 자원이 늘어 동시에 상주할 block 수가 줄 수 있습니다. 재사용 식만 최대화하는 문제가 아닙니다. [NVIDIA Best Practices의 shared-memory 행렬곱](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#shared-memory-in-matrix-multiplication-c-ab)

CLI의 $`M=37,N=45,K=29,T=16`$은 경계 tile이 생기는 사례입니다. 단순 요청 96,570개, tiled 유효 입력 요청 7,134개, 출력 1,665개, shared 공간 2,048 byte가 계산됩니다. 이 숫자를 DRAM 측정 byte나 실측 속도 향상률로 바꾸어 부르지 않습니다.

## Global coalescing과 bank conflict는 다른 문제입니다

Global memory의 coalescing은 warp의 주소 요청을 적은 메모리 구간으로 묶는 성질입니다. Shared memory의 bank conflict는 같은 명령에서 여러 주소가 같은 bank에 몰리는 문제입니다. 한쪽이 좋아도 다른 쪽이 나쁠 수 있습니다.

32개 bank, 연속된 32 bit word가 다음 bank로 가는 단순 모델에서는 word 주소 $`a`$의 bank가 $`a\bmod32`$입니다. 32×32 tile의 같은 열을 32개 lane이 읽으면 주소 간격이 32 word여서 모두 같은 bank에 갑니다. 행 stride를 33으로 늘리면 $`33i\bmod32=i`$가 되어 서로 다른 bank로 흩어집니다. 이 padding은 별도 열을 저장한다기보다 다음 행의 시작 위치를 바꿉니다. 동일한 주소를 함께 읽는 broadcast는 서로 다른 주소의 충돌과 구분합니다. [NVIDIA bank 설명과 transpose padding](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#shared-memory)

```math
\mathrm{bank}(32i)=0,\qquad
\mathrm{bank}(33i)=i\pmod{32}.
```

이 수식은 32 bit word 단위의 단일 명령 모델입니다. 더 넓은 접근, compiler의 명령 분할, architecture의 세부 동작에는 별도 분석이 필요합니다. Padding을 모든 배열에 기계적으로 넣으면 공간만 늘 수도 있습니다.

## 데이터 수명과 동기화

Shared tile을 채운 직후 다른 warp가 읽을 수 있다면 block barrier가 필요합니다. 현재 tile의 계산을 모두 마치기 전에 다음 tile이 덮어써도 오류가 생기므로 재사용 직전에도 읽기 종료를 보장해야 합니다. 경계 밖 thread만 barrier 전에 return하면 block 전체가 같은 barrier에 도달한다는 조건을 깨뜨릴 수 있습니다. 경계 값은 0으로 채우고 thread는 동기화에 참여하는 방식으로 처리합니다. 관련 CUDA 소스는 다음 성능 문서와 연결되는 [tiled_matmul.cu](../../../예제_examples/심화_advanced/ai_data/tiled_matmul.cu)에 있습니다.

## 실행과 독립 검증

```bash
python "예제_examples/심화_advanced/ai_data/demo.py" tile
python -m unittest discover -s "예제_examples/심화_advanced/ai_data" -p "test_*.py" -v
```

`tiled_loads`는 닫힌식을 계산하고, 테스트는 block·inner tile을 실제로 열거해 각 block이 요청하는 유효 A·B 좌표 수를 따로 합산합니다. 배수가 아닌 여러 크기를 비교합니다. `shared_bank_conflict`는 같은 bank의 서로 다른 주소 개수를 세어 32 word stride의 32-way, 33 stride의 1-way, 같은 주소 broadcast의 1-way를 검사합니다.

이 실행은 CPU의 주소·수량 모델입니다. 실제 GPU에서는 결과 정확성을 먼저 비교하고, kernel의 global/shared 요청·bank conflict·상주 자원과 실행 시간을 같은 장치에서 확인합니다. 요청 수 감소만으로 실제 병목이 해결됐다고 결론 내리지 않습니다.

## English

### Reuse within a block

Coalesced accesses can still reread the same values. Tiling first stages a neighborhood and reuses it across several outputs. For $`A:M\times K`$ and $`B:K\times N`$, one output tile combines shared A and B tiles along the inner dimension. Shared memory enables block-local cooperation; it is not automatically shared between blocks. [CUDA memory and synchronization](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/writing-cuda-kernels.html)

A naive source-level implementation requests $`2MNK`$ input elements. This is not measured DRAM traffic: caching, broadcasts and compilation affect physical transfers. Under the stated staging model, every valid A element is loaded once per output-column tile and every B element once per output-row tile, giving $`L_A=MK\lceil N/T\rceil`$ and $`L_B=KN\lceil M/T\rceil`$.

For square dimensions divisible by T, the request count changes from $`2n^3`$ to $`2n^3/T`$. Two FP32 shared tiles require $`8T^2`$ bytes. Larger tiles improve reuse while increasing shared, thread and register demands, potentially reducing resident blocks. [NVIDIA tiled matrix multiplication](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#shared-memory-in-matrix-multiplication-c-ab)

For the nonmultiple shape $`37,45,29`$ and tile 16, the CLI computes 96,570 naive input requests, 7,134 staged valid requests, 1,665 output elements and 2,048 shared bytes. These are model counts, not measured bytes or a speedup.

### Bank mapping is a separate issue

Global coalescing combines nearby global requests. Shared-bank conflicts concern different addresses mapping to one bank within an instruction. In the 32-bank model for successive 32-bit words, the bank is word address modulo 32. Column reads with stride 32 all reach one bank; stride 33 maps lane i to bank i. The extra column changes row starts. Multiple reads of the same address are a broadcast, not a conflict among different addresses. [Shared banks and padding](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#shared-memory)

The formulas assume word-width accesses in one instruction. Wider accesses, instruction splitting and architecture details require their own analysis. Padding every array can waste storage without benefit.

### Ownership, barriers and checks

When another warp reads staged values, a block barrier is needed after loading. Reads must also finish before the next tile overwrites storage. Boundary threads must not return before barriers; fill invalid entries with zero while preserving participation. The linked CUDA matrix source implements that pattern.

Run the two commands above. Tests independently enumerate coordinates loaded by output blocks and inner tiles, then compare those counts with the closed form, including nonmultiple shapes. Bank checks compare stride-32, stride-33 and same-address requests.

These runs execute CPU address and resource arithmetic. Real GPU evaluation first needs numerical correctness, then global/shared requests, bank conflicts, residency and timing on the same device. Fewer modeled requests alone do not establish that the actual bottleneck disappeared.

## 출처 / Sources

- [NVIDIA, Writing SIMT Kernels](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/writing-cuda-kernels.html): memory scope, block cooperation and barriers.
- [NVIDIA, CUDA Best Practices `10.2.3](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#shared-memory): tile reuse, 32-bit bank mapping and transpose padding. 확인 / checked: 2026-10-19.
