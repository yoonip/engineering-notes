# C의 고정 크기 ring buffer: 경계와 소유권부터

[분야 안내](../README.md) · [실행 예제](../../../예제_examples/심화_advanced/systems/advanced_models.py) · [독립 테스트](../../../예제_examples/심화_advanced/systems/test_advanced_models.py) · [실행 안내](../../../예제_examples/심화_advanced/systems/README.md)

## 한국어

### 매번 원소를 앞으로 옮길 필요가 없다

UART 수신 bytes를 배열 앞에 쌓고 하나 꺼낼 때마다 나머지를 전부 이동시키면 pop 한 번에 데이터 길이만큼 복사가 발생한다. ring buffer는 배열을 원처럼 사용한다. 쓰기 위치와 읽기 위치가 끝에 닿으면 처음으로 돌아가므로 앞의 빈 공간을 재사용한다. 데이터 자체를 회전시키는 대신 index만 이동한다.

이 글은 단일 실행 흐름에서 호출하는 bounded FIFO를 다룬다. main과 interrupt, 두 thread, DMA가 동시에 같은 큐에 접근하는 규약은 포함하지 않는다. 같은 알고리즘 모양이라도 동시성 조건을 추가하면 원자성·메모리 순서·수명 규칙을 다시 설계해야 한다. `volatile`을 붙이는 것만으로 이 큐가 concurrent queue가 되지는 않는다.

### head, tail, used로 모호함을 없애기

양의 용량 $`C`$, 다음 쓰기 index $`h`$, 다음 읽기 index $`t`$, 저장 개수 $`u`$를 둔다.

```math
0\le h,t\lt C,\qquad0\le u\le C.
```

head와 tail이 같다는 사실만으로 empty와 full을 구분할 수는 없다. 예제는 `used`를 따로 두어 empty는 $`u=0`$, full은 $`u=C`$로 구분한다. 성공한 push는 `storage[h]=value` 후 $`h\leftarrow(h+1)\bmod C`$, $`u\leftarrow u+1`$로 간다. 성공한 pop은 `storage[t]`를 읽고 tail을 같은 방식으로 옮긴 다음 used를 줄인다. full push와 empty pop은 상태를 바꾸지 않는다.

이 불변식에서 배열 접근의 유효성을 직접 읽을 수 있다. 실제로 dereference하는 index는 항상 $`C`$보다 작고, modulo는 양수로만 수행된다. C의 배열 밖 pointer를 만들거나 dereference하는 것은 별개의 언어 규칙 위반이 될 수 있다. 배열 끝 한 칸 뒤 pointer를 반복 종료 비교에 쓰는 경우와 그 pointer를 역참조하는 경우도 다르다. [WG14 N1570 §6.5.6](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [CMU SEI ARR30-C](https://cmu-sei.github.io/secure-coding-standards/sei-cert-c-coding-standard/rules/arrays-arr/arr30-c/)

### C 구현이 선택한 범위

[ring_buffer.c](../../../예제_examples/심화_advanced/systems/ring_buffer.c)는 용량 7을 compile-time 상수로 둔다. index는 `size_t`, 데이터는 `unsigned char`다. C의 byte는 반드시 8비트라는 뜻이 아니므로 이 소스는 C byte 값을 저장한다. Python의 `ByteRing`은 명시적으로 0~255를 받는 octet 모델이다. 일반 MCU나 PC의 8-bit byte 환경에서는 두 데이터 범위가 대응한다.

고정된 작은 용량이므로 `head+1`이 `size_t` 최대값을 넘지 않는다. 크기를 runtime으로 일반화할 때에는 할당 크기와 덧셈의 범위를 다시 확인해야 한다. 용량이 2의 거듭제곱일 때만 modulo를 bit mask로 바꿀 수 있다. 7의 용량에 `index & (C-1)`을 적용하면 잘못된 큐가 된다. 무조건 비트 연산을 쓰는 것보다 계약과 입력 크기에 맞는 구현이 먼저다.

### 경계를 많이 넘겨서 검증하기

각 push/pop은 $`O(1)`$ 시간, 저장 공간은 $`O(C)`$다. Python 테스트는 용량 1·2·7·64에서 각 4,000회, 총 16,000회의 선택된 push/pop을 독립 `deque`와 비교한다. 모든 단계에서 index 범위와 used를 검사하므로 wrap 직전·직후, empty/full 전이가 함께 확인된다. capacity 1도 유효하며 “한 칸 비워 두기” 방식과 실제 저장 용량이 다르다.

C 파일에는 초기 empty, 반복 wrap, full에서의 push 거부와 FIFO 순서 assert가 있다. C 컴파일러 실행 결과는 이 검증에 포함하지 않았다. C11 도구가 있는 환경에서는 `cc -std=c11 -Wall -Wextra -Werror ring_buffer.c -o ring_buffer` 후 실행할 수 있다. 이 명령은 예제 디렉터리 기준이다. Python 모델 통과가 C compiler 진단이나 target ISR 안전성을 대신하지 않는다.

저장소 루트에서 실행한다. 첫 명령은 입력과 계산 결과를 출력하고, 두 번째 명령은 이 디렉터리의 전체 테스트를 실행한다.

```sh
python "예제_examples/심화_advanced/systems/demo.py" ring
python "예제_examples/심화_advanced/systems/test_advanced_models.py" -v
```

## English

### Reuse array space without moving every element

A queue that shifts all remaining UART bytes after each removal costs time proportional to queue length per pop. A ring buffer treats a fixed array cyclically. Read and write indices wrap at the end, reusing earlier space without rotating stored data.

This bounded FIFO assumes calls from one execution flow. It provides no shared-access contract for interrupts, threads, or DMA. Adding concurrency requires atomicity, memory ordering, and lifetime rules. Applying `volatile` does not turn it into a concurrent queue.

### Use head, tail, and occupancy

Let positive capacity be $`C`$, next write index $`h`$, next read index $`t`$, and occupancy $`u`$:

```math
0\le h,t\lt C,\qquad0\le u\le C.
```

Equal head and tail alone cannot distinguish empty from full. This implementation stores occupancy: empty means $`u=0`$ and full means $`u=C`$. Successful push writes `storage[h]`, advances $`h\leftarrow(h+1)\bmod C`$, and increments occupancy. Pop reads `storage[t]`, advances tail, and decrements occupancy. Rejected operations leave state unchanged.

These invariants directly justify array bounds: every dereferenced index is below $`C`$, and the divisor is positive. C separately constrains forming and dereferencing pointers outside arrays. A pointer one past the array can serve as an end marker but cannot be dereferenced. [WG14 N1570 §6.5.6](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [CMU SEI ARR30-C](https://cmu-sei.github.io/secure-coding-standards/sei-cert-c-coding-standard/rules/arrays-arr/arr30-c/)

### Scope chosen by the C implementation

[ring_buffer.c](../../../예제_examples/심화_advanced/systems/ring_buffer.c) fixes capacity at seven, uses `size_t` indices and `unsigned char` elements. A C byte is not universally eight bits: this source stores C byte values. Python's `ByteRing` explicitly accepts octets from 0 through 255. The ranges correspond on ordinary eight-bit-byte MCU and PC targets.

The small fixed capacity makes `head+1` representable in `size_t`. A runtime-sized generalization must reconsider allocation and arithmetic limits. Replacing modulo with a bit mask is valid only for a power-of-two capacity. Applying `index & (C-1)` at capacity seven breaks the queue. The implementation must follow its contract rather than use bit operations indiscriminately.

### Verify repeated boundary crossings

Each push/pop takes $`O(1)`$ time and storage is $`O(C)`$. Python tests compare 4,000 selected operations at each capacity 1, 2, 7, and 64 against an independent deque: 16,000 operations in total. Every step checks occupancy and index bounds, covering wraparound and empty/full transitions. Capacity one remains usable; it differs from designs that reserve an empty slot.

The C file contains assertions for initial emptiness, repeated wraparound, full-buffer rejection, and FIFO order. C compiler execution is not part of the reported verification. With a C11 toolchain, run `cc -std=c11 -Wall -Wextra -Werror ring_buffer.c -o ring_buffer` and execute the result from the example directory. Passing the Python model does not establish compiler diagnostics or ISR safety on a target.

Run the following commands from the repository root. The first prints the input and computed observations; the second runs the complete test suite in this example directory.

```sh
python "예제_examples/심화_advanced/systems/demo.py" ring
python "예제_examples/심화_advanced/systems/test_advanced_models.py" -v
```

## 출처 / Sources

- [WG14 N1570 §6.5.6](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf): 배열과 pointer 산술 규칙 / array and pointer arithmetic
- [CMU SEI CERT ARR30-C](https://cmu-sei.github.io/secure-coding-standards/sei-cert-c-coding-standard/rules/arrays-arr/arr30-c/): 배열 경계 밖 접근 / out-of-bounds access
