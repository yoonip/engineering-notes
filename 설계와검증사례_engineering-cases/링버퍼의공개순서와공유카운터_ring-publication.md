# 링 버퍼의 공개 순서와 공유 카운터 / Ring-buffer publication and shared counters

링 버퍼는 배열의 끝에 도달하면 처음으로 돌아와 저장 공간을 재사용하는 큐입니다. 배열 인덱스를 순환시키는 것과 여러 실행 문맥에서 올바르게 공유하는 것은 서로 다른 과제입니다. 이 사례에서는 잘못된 사건 순서를 직접 열거해 오래된 값 읽기를 재현하고, 생산자와 소비자의 소유 필드를 나눈 C11 SPSC 코드를 함께 실행합니다. SPSC는 single producer, single consumer의 줄임말로 생산자와 소비자가 각각 하나라는 뜻입니다.

[실행 코드](../예제_examples/실무검증_practical-validation/native_firmware/ring_publish_model.c), [재현 방법](../예제_examples/실무검증_practical-validation/native_firmware/README.md), [실행 기록](검증기록_evidence/C펌웨어경계검사_20261021.md)을 연결했습니다. 기존 [단일 실행 흐름용 ring_buffer.c](../예제_examples/심화_advanced/systems/ring_buffer.c)는 그대로 유지합니다. 기존 코드에 새로 발견된 동시성 버그가 있다는 주장이 아니라, 적용 범위가 다른 새 교육 예제입니다.

## 1. 데이터와 인덱스 중 무엇을 먼저 보입니까?

값 42를 빈 슬롯에 넣는 작업을 두 사건으로 나눕니다. 하나는 슬롯에 42를 기록하는 일이고 다른 하나는 `head`를 움직여 새 데이터가 있다고 공개하는 일입니다. 소비자는 `head != tail`로 데이터 존재를 확인한 뒤 슬롯을 읽습니다.

잘못된 생산자 순서는 `head 공개 → 슬롯 쓰기`입니다. 소비자가 그 사이에 실행되면 데이터가 있다고 믿지만 아직 이전 값 0을 읽습니다. 올바른 의도는 `슬롯 쓰기 → head 공개`입니다. 물건을 상자에 넣기 전에 배송 완료 표식을 붙이면 상자를 연 사람이 빈 상자를 만나는 것과 같습니다.

| 사건 | 잘못된 생산자 | 순서를 바꾼 생산자 |
| --- | --- | --- |
| 첫 번째 P | head를 1로 공개합니다. | 슬롯에 42를 기록합니다. |
| 두 번째 P | 슬롯에 42를 기록합니다. | head를 1로 공개합니다. |
| 첫 번째 C | head와 tail로 데이터 존재를 확인합니다. | 같은 확인을 합니다. |
| 두 번째 C | 데이터가 있다고 봤으면 슬롯을 읽습니다. | 같은 읽기를 합니다. |

모델의 `PCCP` 순서를 따라가면 잘못된 경로에서는 `head=1 → 존재 확인 → 0 읽기 → 42 기록`이 됩니다. 순서를 수정하면 `42 기록 → 비어 있음 확인 → 읽기 생략 → head=1`이므로 오래된 값을 소비하지 않습니다. 이때 소비자가 당장 읽지 않는 것은 허용한 동작입니다. 나중에 재시도하면 됩니다.

이 모델은 실제 CPU가 명령을 재배치하는 현상을 측정하지 않습니다. 하나의 호스트 스레드가 정해진 사건을 차례로 실행해 그 순서가 허용되면 어떤 상태가 되는지 확인합니다. 실제 인터럽트와 연결할 때에도 우선순위를 따져야 합니다. 전경 생산자를 ISR 소비자가 중단하는 경우에는 `PCCP`가 직접 대응할 수 있지만, ISR 생산자를 전경 소비자가 그 ISR 도중 중단한다고 가정할 수는 없습니다.

## 2. 여섯 순서를 모두 열거합니다

각 문맥 내부의 두 사건 순서를 유지하면서 두 P와 두 C를 배치하면 가능한 문자열은 여섯 개입니다. 모델은 `PPCC`, `PCPC`, `PCCP`, `CPPC`, `CPCP`, `CCPP`를 실행합니다. 잘못된 순서에서 값 0을 실제로 소비한 경우만 실패로 셉니다. 소비자가 빈 큐를 보고 이번 시도에서 읽지 않은 것은 실패로 세지 않습니다.

2026-10-21의 호스트 실행 출력은 다음과 같습니다.

```text
schedule=PPCC faulty_stale_read=0 corrected_stale_read=0
schedule=PCPC faulty_stale_read=0 corrected_stale_read=0
schedule=PCCP faulty_stale_read=1 corrected_stale_read=0
schedule=CPPC faulty_stale_read=0 corrected_stale_read=0
schedule=CPCP faulty_stale_read=0 corrected_stale_read=0
schedule=CCPP faulty_stale_read=0 corrected_stale_read=0
```

따라서 이 작은 상태 모델에서 조기 공개는 1건의 오래된 값 읽기를 만들고, 기록 후 공개는 0건입니다. 이 수치를 인터럽트 오류율 1/6로 해석하면 안 됩니다. 여섯 문자열은 확률 분포가 아니며 장치에서 발생할 빈도를 측정하지 않았습니다. 또한 많은 원소·여러 생산자·카운터 순환이 있는 전체 동시성 상태 공간을 검증한 것도 아닙니다.

## 3. 공유 `used`의 증가와 감소도 따로 봅니다

값의 공개 순서를 고쳐도 생산자와 소비자가 같은 일반 정수 `used`를 각각 수정하면 문제가 남습니다. `++used` 한 줄이 실제로 읽기·더하기·쓰기의 한 묶음이라는 보장은 없습니다.

자체 재현은 `used=1`에서 시작합니다. 전경 소비자가 1을 읽고 잠시 멈춥니다. 인터럽트 생산자가 1을 읽어 2를 기록하고 돌아옵니다. 소비자는 먼저 읽은 1에서 1을 빼 0을 기록합니다. 추가 1회와 소비 1회이므로 순차적인 기대값은 1인데 관측값은 0이 됩니다. 이 기록은 실제 ISR을 띄우지 않고 지역 변수 두 개로 그 읽기·쓰기 순서를 표현합니다.

```c
int consumer_local = used; // 소비자가 옛값 1을 보관합니다.
int producer_local = used; // 생산자도 옛값 1을 보관합니다.
used = producer_local + 1; // 생산자가 2를 기록합니다.
used = consumer_local - 1; // 소비자의 나중 쓰기가 0으로 덮습니다.
```

`volatile`은 이 복합 갱신을 원자적으로 만들지 않습니다. 또한 일반 메모리 접근의 순서를 모두 보장하는 장치도 아닙니다. [GCC의 volatile 설명](https://gcc.gnu.org/onlinedocs/gcc/Volatiles.html)도 일반 객체와 volatile 객체 사이의 순서 보장을 구분합니다. 짧은 임계 구역으로 보호하거나, 필요한 원자 연산을 쓰거나, 공유 카운터 자체를 없애는 설계를 선택해야 합니다.

## 4. 생산자는 head, 소비자는 tail을 소유합니다

동봉한 SPSC 구현은 크기 8 배열에 한 칸을 비워 실제로 7개를 담습니다. `head == tail`은 비어 있음, 다음 head가 tail과 같으면 가득 참입니다. 생산자만 head를 쓰고 소비자만 tail을 씁니다. 공통 `used`를 둘이 동시에 갱신하지 않습니다.

```c
unsigned head = atomic_load_explicit(&q->head, memory_order_relaxed);
// &는 객체의 주소, ->는 포인터가 가리키는 구조체 멤버 접근입니다.
unsigned tail = atomic_load_explicit(&q->tail, memory_order_acquire);
// 상대가 사용을 마친 위치를 acquire로 관측합니다.
if (next == tail) return false; // 가득 차면 새 바이트를 거부합니다.
q->bytes[head] = value; // 실제 데이터 기록을 먼저 수행합니다.
atomic_store_explicit(&q->head, next, memory_order_release);
// release 공개를 소비자의 acquire 관측과 연결합니다.
```

소비자는 head를 acquire로 읽은 뒤 데이터를 읽고, 사용을 마친 tail을 release로 공개합니다. tail 쪽의 공개도 중요합니다. 생산자가 슬롯을 다시 덮어쓰기 전에 소비자의 읽기가 끝났다는 관계가 필요하기 때문입니다. `_Atomic unsigned`는 그 인덱스를 C11 원자 객체로 선언하는 문법입니다. [N1570의 7.17.3](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)에서 원자 접근의 메모리 순서를 확인했습니다.

이 코드는 ISR에 그대로 붙이면 된다는 장치 드라이버가 아닙니다. 대상에서 원자 연산이 잠금 없는지, 그 구현이 ISR에서 호출 가능한지, 접근 폭과 정렬이 맞는지 확인해야 합니다. ISR 안에서 사용할 수 없는 내부 잠금 구현이라면 다른 방식을 선택해야 합니다. 인터럽트 마스크를 사용한다면 기존 마스크 상태를 저장·복원해야 하며, 종료 시 무조건 인터럽트를 켜면 상위 호출자의 상태를 깨뜨릴 수 있습니다.

Arm의 `__DMB()`는 메모리 접근 순서와 관련되지만 그 하나가 원자성·소유권·DMA 캐시 일관성을 모두 해결하지는 않습니다. [CMSIS의 DMB·DSB 정의](https://arm-software.github.io/CMSIS_6/main/Core/group__intrinsic__CPU__gr.html)를 구분하고, 실제 MCU의 메모리 유형과 DMA 규칙을 별도로 봐야 합니다.

## 5. 실행 결과와 버퍼 용량의 의미

```text
shared_counter_observed=0 expected=1
spsc_capacity=7 wrap_pairs=10000 head_lock_free=1
schedules=6 faulty_stale_reads=1 corrected_stale_reads=0
ring publication model checks passed
```

Windows x86-64, Zig 0.17.0 C 드라이버, C11, `-O2 -UNDEBUG -Wall -Wextra -Werror`에서 실행했습니다. 빈 큐의 pop 거부, 7개 채운 후 추가 push 거부, FIFO 순서, 10,000회의 push/pop 쌍을 검사했습니다. `head_lock_free=1`은 이 호스트의 이 원자 객체에서 확인한 값입니다. MCU의 지원 여부로 옮겨 적을 수 없습니다. SPSC 구현을 실제 두 스레드로 경쟁 실행하지 않았으므로 이 순차 검사를 동시성 스트레스 시험으로 부르지 않습니다.

자체 계산으로 UART 115,200 baud, 8N1, 간격 없는 수신을 가정하면 바이트당 시작·데이터·정지 비트가 합쳐 10비트입니다. 초당 11,520바이트이고, 소비자가 50ms 멈추면 약 576바이트가 쌓입니다. 7바이트 큐의 흡수 시간은 약 0.608ms뿐입니다. 이는 장치 실측이 아닌 이상적인 처리량 계산입니다. 7칸 큐의 알고리즘이 맞는 것과 업무의 최악 지연을 견디는 것은 다른 판정입니다.

가득 찼을 때 새 바이트를 거부하는 정책도 호출자가 처리해야 합니다. 반환값을 무시하면 조용한 손실이 됩니다. 프레임 조립기는 손실 카운터와 시퀀스 번호를 보고 다음 정상 경계에서 재동기화할 수 있어야 합니다. 여러 ISR이 생산한다면 더 이상 단일 생산자가 아니므로 같은 SPSC 규약을 그대로 적용하지 않습니다.

## 확인 문제

1. 여섯 순서 중 한 번 실패했으므로 장치 오류율이 약 16.7%입니까?
2. `volatile used`로 바꾸면 증가·감소 유실이 해결됩니까?
3. 크기 8 배열을 사용하지만 왜 실제 용량은 7입니까?

답: 1. 아닙니다. 사건 순서의 가능성을 열거한 것이며 실제 시간과 발생 확률을 측정하지 않았습니다. 2. 아닙니다. 복합 갱신의 원자성이나 상호 배제를 제공하지 않습니다. 3. head와 tail이 같을 때 비어 있음을 나타내기 위해 한 칸을 비워 둡니다.

## English

A single-threaded event model enumerates six interleavings. Publishing head before storing the byte allows one stale read; storing first prevents stale consumption in that model. A separate read/modify/write trace loses a shared used-counter update. The accompanying C11 SPSC queue uses producer-owned head, consumer-owned tail, and release/acquire publication in both directions. Host checks cover full/empty behavior, FIFO, and 10,000 sequential wrap pairs. They are not MCU interrupt, weak-memory, or concurrent stress measurements.

## 출처와 읽은 범위

- [C11 공개 초안 N1570](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf): 5.1.2.4와 7.17.3의 동기화·원자 순서를 확인했습니다.
- [GCC Volatiles](https://gcc.gnu.org/onlinedocs/gcc/Volatiles.html): 일반 메모리와 volatile의 순서에 관한 설명을 확인했습니다.
- [Arm CMSIS-Core의 CPU intrinsics](https://arm-software.github.io/CMSIS_6/main/Core/group__intrinsic__CPU__gr.html): DMB와 DSB의 정의를 확인했습니다. 해당 명령을 이 호스트 실행에서 호출하지 않았습니다.
- 입력 값 42, 여섯 스케줄, 용량 7, UART 용량 예제는 직접 구성한 교육 자료입니다.
