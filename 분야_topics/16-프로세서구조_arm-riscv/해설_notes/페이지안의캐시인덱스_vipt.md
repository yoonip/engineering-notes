# 페이지 안에서 캐시를 찾기: VIPT와 alias 조건

[프로세서 구조 목차](../README.md) · [주소 모델](../../../예제_examples/심화_advanced/hardware/models.py) · [검산](../../../예제_examples/심화_advanced/hardware/test_models.py)

## 한국어

### 주소 번역을 기다리지 않고 먼저 찾을 수 있을까

가상주소를 물리주소로 바꾸는 동안 cache의 모든 작업을 멈추면 access가 느려진다. VIPT는 virtual address로 set을 먼저 고르고, 번역된 physical tag로 맞는 line인지 확인한다. 도서관에서 책장의 위치를 먼저 찾아가면서 정확한 책 번호를 확인하는 것과 비슷하다. 문제는 서로 다른 가상주소가 같은 물리 메모리를 가리킬 수 있다는 점이다. 이런 synonym이 다른 cache set으로 가면 같은 데이터의 복사본이 생길 수 있다.

[Arm의 page-colouring 설명](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/page-colouring-on-armv6-and-a-bit-on-armv7)은 이런 문제와 특정 ARM 세대의 대응을 다룬다. [CMU의 cache 강의](https://www.cs.cmu.edu/~15346-s21/lectures/lec5_6-cache.pdf)는 virtual/physical indexing 구분을 제공한다. 여기서는 특정 제품의 cache 구현을 단정하지 않고, 단순 VIPT 구조의 충분조건을 비트 배치로 유도한다.

### 번역해도 달라지지 않는 비트

페이지 크기를 P byte, line 크기를 B byte, set 수를 S, way 수를 A로 두고 모두 2의 거듭제곱이라고 하자. cache capacity는 $`C=ABS`$다. 주소의 가장 낮은 $`\log_2B`$비트는 line 내부 위치, 그다음 $`\log_2S`$비트는 set index다. 가상·물리주소 번역은 page offset $`\log_2P`$비트를 그대로 둔다.

따라서 set index와 block offset이 모두 page offset에 들어가면 두 synonym의 index는 항상 같다.

```math
\log_2 B+\log_2 S\le\log_2 P
\iff BS\le P
\iff C\le AP.
```

등호도 허용된다. 예를 들어 4 KiB page, 64 B line이면 page offset은 12비트, block offset은 6비트이므로 set index에 6비트를 쓸 수 있다. 64 sets×8 ways×64 B=32 KiB가 이 기하 조건을 만족한다. associativity는 같은 index에 들어갈 수 있는 line 수이며 set index bit 수를 늘리는 것과 다르다.

### 조건을 넘었을 때의 반례

set이 128개면 index에 7비트가 필요해 가상 page number의 1비트를 쓰게 된다. 가상주소 0x0000과 0x1000이 같은 physical page의 같은 offset에 매핑된다고 하자. 64 B line에서 두 index는 0과 64다. physical tag가 같더라도 다른 set에 들어갈 수 있어 단순한 set-local tag lookup만으로 synonym을 정리할 수 없다.

| 구조 | line×sets | 4 KiB offset 안에 index 포함? |
|---|---:|---|
| 64 B, 64 sets | 4096 B | 포함 |
| 64 B, 128 sets | 8192 B | 벗어남 |

위반이 곧 구현 불가능이라는 뜻은 아니다. page colouring, alias 탐지, 추가 lookup, 다른 indexing, 큰 page 같은 설계 선택이 있다. 반대로 위 조건만 만족한다고 coherence, 권한 검사, speculative access, cache maintenance까지 모두 해결되는 것도 아니다. 이 조건은 page offset에 기반한 set synonym 문제를 피하는 충분조건이다.

### 작은 주소 모델 실행

```bash
python demo.py --case vipt
python -m unittest -v test_models.HardwareModels.test_vipt_safe_synonyms test_models.HardwareModels.test_vipt_unsafe_counterexample
```

`cache_index()`는 $`\lfloor address/B\rfloor\bmod S`$를 계산한다. 검산은 서로 다른 virtual page의 같은 offset들을 안전한 geometry에서 비교하고, 128 sets에서는 위 두 주소가 서로 다른 index를 갖는지 확인한다. 주소 번역기나 CPU cache를 실행하는 코드가 아니라, 번역에서 보존되는 offset과 index의 관계를 검산하는 모델이다.

실제 CPU 문서에서는 최소 page size, cache의 indexing 함수, tag 비교 시점, alias 처리와 OS의 memory attribute 규약을 함께 확인한다. 큰 page를 사용할 때만 성립하는 구조를 작은 page에도 안전하다고 옮기면 안 된다. DMA와 instruction/data cache 일관성은 별도 문제이며, 이 계산이 invalidate·clean·barrier 필요 여부를 대신 판단하지 않는다.

## English

### Looking up a set while translation proceeds

A virtually indexed, physically tagged cache can select a set using the virtual address while address translation produces the physical tag. This overlap can reduce lookup latency. The complication is that different virtual addresses can refer to the same physical memory. If such synonyms select different sets, duplicate cached copies may appear.

[Arm's page-colouring discussion](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/page-colouring-on-armv6-and-a-bit-on-armv7) describes the issue and generation-specific responses. [CMU's cache lecture](https://www.cs.cmu.edu/~15346-s21/lectures/lec5_6-cache.pdf) supplies the virtual/physical indexing distinction. The derivation here concerns a simple VIPT organization and does not assert how every Arm or RISC-V processor is built.

### Deriving an offset-only indexing condition

Let page size P, line size B, set count S and associativity A all be powers of two. Capacity is C=ABS. The lowest log2(B) bits select a byte within a line; the following log2(S) bits select a set. Translation preserves the log2(P) page-offset bits.

If block-offset plus set-index bits fit entirely inside the page offset, synonyms necessarily select the same set. This yields $`BS\le P`$, equivalently $`C\le AP`$. Equality is allowed. A 4 KiB page has twelve offset bits; a 64 B line uses six, leaving six for 64 sets. Eight ways therefore permit a 32 KiB cache under this sufficient geometric condition. Ways add candidate lines within a set rather than index bits.

### A counterexample beyond the bound

With 128 sets, the index needs seven bits and includes one virtual page-number bit. Suppose virtual addresses 0x0000 and 0x1000 map to the same physical page and offset. With 64 B lines their set indices are zero and 64. A set-local physical-tag comparison alone cannot reconcile the possible duplicate copies across those sets.

Breaking this bound does not make a cache impossible. Page colouring, alias detection, additional lookups, other indexing schemes or larger pages can address the problem. Satisfying it does not solve all coherence, permissions, speculation or maintenance issues either. It is a sufficient condition specifically for offset-based set synonym avoidance.

### Executable check and application limits

The commands above run the geometry demo and independent safe/unsafe alias cases. `cache_index()` calculates floor(address/B) modulo S. Tests compare equal offsets in different virtual pages under the safe geometry and confirm differing indices in the 128-set counterexample. This is an address-bit model, not a CPU or translation emulator.

For a physical processor, inspect minimum page size, actual indexing, tag timing, alias handling and the operating system's memory attributes together. A geometry valid only with large pages may not be safe with small pages. DMA coherence and instruction/data cache maintenance remain separate questions; this calculation does not determine required clean, invalidate or barrier operations.

## 출처 / Sources

- Arm, *Page colouring on ARMv6 (and a bit on ARMv7)*: synonym handling and generation-specific context.
- Carnegie Mellon University, *Caches*, 15-346 Spring 2021: cache organization and virtual/physical addressing. Both links appear above.
