# 같은 계산, 다른 메모리 배치: AoS·SoA와 캐시

[분야 안내](../README.md) · [실행 예제](../../../예제_examples/심화_advanced/systems/advanced_models.py) · [독립 테스트](../../../예제_examples/심화_advanced/systems/test_advanced_models.py) · [실행 안내](../../../예제_examples/심화_advanced/systems/README.md)

## 한국어

### 연산 수가 같아도 읽어 오는 양은 다릅니다

64개 입자의 위치 x만 합산한다고 하겠습니다. 각 입자가 x·y·z·mass라는 네 개의 4바이트 필드로 구성되면, x의 주소는 16바이트 간격입니다. x만 별도 배열에 두면 주소 간격은 4바이트가 됩니다. 덧셈 횟수는 같지만 캐시가 가져오는 메모리 블록의 수는 달라질 수 있습니다. 알고리즘의 점근 복잡도와 실제 메모리 접근 비용을 함께 봐야 하는 이유입니다.

구조체 배열은 AoS, 필드별 배열은 SoA라고 부릅니다. AoS는 한 개체의 여러 필드를 함께 다루기에 편리하고, SoA는 같은 필드를 연속 처리할 때 인접 데이터를 모을 수 있습니다. 어느 쪽이 항상 빠른 것은 아닙니다. 접근 패턴, SIMD, 필드 크기, 정렬, cache line과 compiler의 변환이 결과에 영향을 줍니다. Cornell의 cache 설명은 시간·공간 지역성과 cache line을 구분합니다. [Cornell CS3410 caches](https://www.cs.cornell.edu/courses/cs3410/2025fa/notes/caches.html)

### 주소에서 cache line까지

byte 주소를 $`a`$, line 크기를 $`B`$라 하면 line 번호와 내부 offset은

```math
\ell=\left\lfloor\frac{a}{B}\right\rfloor,\qquad o=a\bmod B.
```

예제는 64바이트 line, 시작 주소 0, 각 x의 크기 4바이트를 가정합니다. AoS의 64개 x 주소는 $`16i`$, SoA는 $`4i`$입니다. AoS는 16개 line, SoA는 4개 line에 걸칩니다. 모든 접근이 한 line 안의 4바이트 load이고 재방문이 없는 이 순차 패턴에서는 cold miss 수가 각각 16과 4입니다. “SoA가 4배 빠르다”는 결론은 여기서 나오지 않습니다. miss 수와 프로그램 시간 사이에는 다른 비용이 있습니다.

### 작은 LRU 모델이 설명하는 것

`cache_trace()`는 완전 연관 cache와 LRU 교체를 모델링합니다. 최근 쓴 line을 `OrderedDict` 끝으로 옮기고, 가득 차면 가장 오래 쓰지 않은 line을 지웁니다. 주소 접근 수가 $`N`$이면 평균 $`O(N)`$ 시간, line 수 $`L`$에 대해 $`O(L)`$ 공간입니다. 공간 지역성을 보는 데 적합하지만 실제 CPU의 set mapping, prefetch, multi-level cache, coherence, miss 병렬성은 없습니다.

특히 Python list의 원소는 수치 값이 연속한 C 배열과 같지 않습니다. 포인터 배열과 별도 객체가 관여할 수 있으므로 `list`를 순회한 시간을 이 주소 모델의 물리 측정으로 간주하면 안 됩니다. Python `array`는 타입별 연속 수치 저장을 제공하지만 `itemsize`는 typecode와 플랫폼에 따라 확인해야 합니다. 이 예제는 Python 객체 주소를 추측하지 않고 명시적인 합성 주소를 넣습니다. [Python array](https://docs.python.org/3/library/array.html)

### 독립 검사와 측정 설계

테스트는 작은 list로 구현한 별도 LRU 참조와 100개의 무작위 trace를 비교합니다. 두 자료구조가 같은 miss count를 내는지 확인하고, 위의 16 대 4라는 분석값도 별도로 고정합니다. `demo.py cache`는 이 두 수와 모델 이름을 출력합니다. 측정한 CPU cache miss counter나 실행 시간은 아닙니다.

실제 AoS·SoA 비교에서는 같은 수치 결과, 같은 입력 크기와 정렬, compiler 옵션을 유지하고 준비 시간과 kernel 시간을 나누어야 합니다. 모든 필드를 읽는 버전도 함께 보면 x 하나만 읽는 편향을 확인할 수 있습니다. 큰 stride가 cache set 충돌을 만드는 경우에는 완전 연관 LRU와 결과가 달라질 수 있습니다. 자료구조의 논리적 기능이 같다는 사실과 layout이 실행 환경에 맞는다는 사실은 서로 다른 검증 대상입니다.

저장소 루트에서 실행합니다. 첫 명령은 입력과 계산 결과를 출력하고, 두 번째 명령은 이 디렉터리의 전체 테스트를 실행합니다.

```sh
python "예제_examples/심화_advanced/systems/demo.py" cache
python "예제_examples/심화_advanced/systems/test_advanced_models.py" -v
```

## English

### Equal arithmetic can move different amounts of data

Consider summing x for 64 particles with four four-byte fields: x, y, z, and mass. In an array of structures, consecutive x addresses are 16 bytes apart. In a separate x array, they are four bytes apart. Addition counts are identical, but memory blocks fetched can differ. Asymptotic complexity and memory access cost answer different questions.

AoS means array of structures; SoA means structure of arrays. AoS conveniently groups fields belonging to one object. SoA groups one field across objects, favoring some streaming accesses. Neither universally wins: access patterns, SIMD, sizes, alignment, cache geometry, and compiler transformations matter. Cornell distinguishes temporal and spatial locality and explains cache lines. [Cornell CS3410 caches](https://www.cs.cornell.edu/courses/cs3410/2025fa/notes/caches.html)

### Map an address to a cache line

For byte address $`a`$ and line size $`B`$,

```math
\ell=\left\lfloor\frac{a}{B}\right\rfloor,\qquad o=a\bmod B.
```

Assume 64-byte lines, base address zero, and four-byte x loads wholly within a line. The 64 AoS addresses are $`16i`$; the SoA addresses are $`4i`$. They touch 16 and four lines respectively. With no revisits, this sequential pattern incurs 16 versus four cold misses. It does not establish a fourfold speedup: elapsed time includes other costs.

### What the LRU model captures

`cache_trace()` models a fully associative cache with LRU replacement. An `OrderedDict` moves recently used lines to its end and evicts the least recent line when full. Average time is $`O(N)`$ for $`N`$ accesses and storage is $`O(L)`$ for $`L`$ resident lines. It illustrates locality while omitting set mapping, prefetch, multiple cache levels, coherence, and parallel misses.

A Python list is not a packed C array of numeric values; pointers and separately stored objects may be involved. Timing list iteration is therefore not a physical measurement of this address model. Python `array` provides typed numeric storage, with `itemsize` that must be checked for the selected typecode and platform. The example supplies explicit synthetic addresses instead of guessing Python object layout. [Python array](https://docs.python.org/3/library/array.html)

### Independent checks and measurement design

Tests compare 100 random traces with an independent list-based LRU reference and separately assert the analytically expected 16-versus-four result. `demo.py cache` prints both counts and identifies the model. These are neither hardware performance counters nor measured execution times.

A real layout comparison keeps numerical results, input sizes, alignment, and compiler options comparable, and separates preparation from kernel time. A workload reading every field exposes bias introduced by reading x alone. Set conflicts at particular strides can produce behavior absent from fully associative LRU. Functional equivalence of a data structure and suitability of its layout are separate verification targets.

Run the following commands from the repository root. The first prints the input and computed observations; the second runs the complete test suite in this example directory.

```sh
python "예제_examples/심화_advanced/systems/demo.py" cache
python "예제_examples/심화_advanced/systems/test_advanced_models.py" -v
```

## 출처 / Sources

- [Cornell CS3410: Caches](https://www.cs.cornell.edu/courses/cs3410/2025fa/notes/caches.html): 캐시·지역성 / caches and locality
- [Python: array](https://docs.python.org/3/library/array.html): 수치 배열의 저장·itemsize / numeric storage and itemsize
