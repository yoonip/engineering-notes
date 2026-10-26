# 파이프가 꽉 찼을 때: backpressure와 종료 조건

[분야 안내](../README.md) · [실행 예제](../../../예제_examples/심화_advanced/systems/advanced_models.py) · [독립 테스트](../../../예제_examples/심화_advanced/systems/test_advanced_models.py) · [실행 안내](../../../예제_examples/심화_advanced/systems/README.md)

## 한국어

### 느린 소비자가 전체 속도를 정합니다

센서 로그를 만드는 프로그램이 초당 2 MB를 내보내고 저장 프로그램은 1 MB만 처리한다면, 둘을 파이프로 연결하는 것만으로 차이가 사라지지 않습니다. 중간 버퍼가 채워진 뒤에는 생산자가 기다리거나 일부 데이터를 버려야 합니다. 소비 속도에 맞춰 생산을 늦추는 흐름을 backpressure라고 부릅니다. 큰 버퍼는 순간적인 속도 차이를 흡수하지만 지속적인 처리율 부족을 해결하지는 않습니다.

Linux 파이프는 유한한 바이트 스트림입니다. 읽을 데이터가 없고 쓰기 끝이 열려 있으면 blocking read는 기다립니다. 가득 찬 파이프에 대한 write도 기다릴 수 있습니다. `O_NONBLOCK`에서는 조건에 따라 `EAGAIN` 또는 부분 쓰기가 발생합니다. 파이프의 전체 용량과 여러 writer의 작은 write를 섞이지 않게 하는 `PIPE_BUF`는 다른 값입니다. [Linux pipe(7)](https://man7.org/linux/man-pages/man7/pipe.7.html)

### 버퍼의 보존식을 먼저 세우기

시간 단계 $`k`$에서 버퍼에 있는 바이트 수를 $`q_k`$, 실제로 받아들인 바이트를 $`a_k`$, 실제로 읽은 바이트를 $`d_k`$, 용량을 $`C`$라고 하면

```math
q_{k+1}=q_k+a_k-d_k,\qquad 0\le q_k\le C.
```

여기서 전송을 시도한 양과 받아들여진 양을 구분해야 합니다. `write()` 반환값이 4라면 6바이트를 요청했어도 다음 시도는 나머지 2바이트부터 시작합니다. 처음부터 다시 보내면 중복이 생기고, 전부 보냈다고 처리하면 누락이 생깁니다. 예제는 4바이트 큐에 `abcdef`를 넣어 첫 시도 4, 두 번째 시도 2가 받아들여지는 과정을 보여 줍니다. 반환값을 이용해 offset을 옮기므로 읽은 결과는 정확히 `abcdef`입니다.

writer가 살아 있는 빈 큐와 종료된 빈 큐도 구분합니다. 앞의 경우에는 앞으로 데이터가 올 수 있습니다. 뒤의 경우에만 EOF입니다. 실제 Linux에서는 쓰기 끝을 가리키는 모든 descriptor가 닫혀야 EOF를 볼 수 있으므로, 자식 프로세스에 남은 불필요한 복제 descriptor도 종료를 지연시킬 수 있습니다.

### readiness는 전체 작업 완료와 다릅니다

`poll()`의 `POLLOUT`은 쓸 수 있는 상태를 알려 주지만, 임의로 큰 write 전체가 기다림 없이 끝난다는 뜻은 아닙니다. `POLLHUP` 뒤에도 아직 읽지 않은 데이터가 남아 있을 수 있습니다. 준비 이벤트를 받은 뒤에도 실제 read/write 반환값을 기준으로 상태를 옮겨야 합니다. 여러 thread가 같은 descriptor를 소비하면 관찰 이후 조건이 바뀔 수 있으므로 nonblocking 처리와 `EAGAIN` 경로가 필요합니다. [Linux poll(2)](https://man7.org/linux/man-pages/man2/poll.2.html)

### 실행 결과를 어떻게 판정할까요

`BoundedStream`은 deque에 바이트를 보관하며 받아들인 길이를 반환합니다. push/pop은 바이트당 상수 시간이고 저장 공간은 $`O(C)`$입니다. 빈 상태의 대기를 실제로 block하지 않고 `BlockingIOError`로 나타냅니다. 이 모델은 작은 write의 원자성, 여러 writer 사이의 interleaving, 신호와 kernel의 실제 스케줄링을 구현하지 않습니다.

테스트는 생산 단위 11바이트, 소비 단위 3바이트, 큐 용량 7바이트를 사용해 250바이트 전체가 순서대로 한 번씩 나오는지 확인합니다. 매 단계에서 용량 상한을 검사하고 writer 종료 후 잔여 데이터와 EOF를 따로 읽습니다. 대기 시간 자체보다 보존식, 순서, 종료 조건을 확인하는 검사입니다. 실제 Linux 측정에서는 완료 바이트 수와 CPU 시간, blocking 시간, 최대 queue 길이를 구분해서 남겨야 버퍼 증가가 어떤 효과를 냈는지 판단할 수 있습니다.

저장소 루트에서 실행합니다. 첫 명령은 입력과 계산 결과를 출력하고, 두 번째 명령은 이 디렉터리의 전체 테스트를 실행합니다.

```sh
python "예제_examples/심화_advanced/systems/demo.py" pipe
python "예제_examples/심화_advanced/systems/test_advanced_models.py" -v
```

## English

### The slower consumer determines sustained throughput

Suppose a sensor logger produces 2 MB/s while its storage process consumes only 1 MB/s. Connecting them with a pipe does not remove that gap. Once the intermediate buffer fills, production must wait or data must be dropped. Backpressure propagates the consumer's limited capacity upstream. A larger buffer absorbs a temporary burst; it cannot fix a persistent throughput deficit.

A Linux pipe is a bounded byte stream. A blocking read on an empty pipe waits while a writer remains open, and a write to a full pipe can wait too. With `O_NONBLOCK`, the applicable conditions determine whether an operation reports `EAGAIN` or a partial write. Total pipe capacity differs from `PIPE_BUF`, which governs noninterleaving of sufficiently small writes by multiple writers. [Linux pipe(7)](https://man7.org/linux/man-pages/man7/pipe.7.html)

### Start with conservation of bytes

Let $`q_k`$ denote queued bytes, $`a_k`$ bytes actually accepted, $`d_k`$ bytes actually consumed, and $`C`$ capacity:

```math
q_{k+1}=q_k+a_k-d_k,\qquad 0\le q_k\le C.
```

Attempted transfer size is not accepted transfer size. If a write returns 4 after requesting 6 bytes, the next attempt begins at the remaining 2 bytes. Repeating the original buffer duplicates data; assuming all bytes were accepted loses data. The demo places `abcdef` in a four-byte queue, accepting 4 bytes first and 2 later. Advancing the offset by the returned count reconstructs exactly `abcdef`.

An empty queue with a live writer differs from an empty queue after writing ends. Only the latter represents EOF. On Linux, every descriptor referring to the write end must close before the reader observes EOF. An unnecessary duplicate inherited by a child can therefore delay termination.

### Readiness is not completion

`POLLOUT` from `poll()` indicates an opportunity to write, not that an arbitrarily large write will complete without waiting. `POLLHUP` can coexist with unread buffered data. Transfer state must follow actual read/write return values. Another thread can consume readiness between observation and use, which is another reason to handle nonblocking operations and `EAGAIN`. [Linux poll(2)](https://man7.org/linux/man-pages/man2/poll.2.html)

### Decide what the executable check establishes

`BoundedStream` stores bytes in a deque and returns the accepted length. Push/pop cost constant time per byte and storage is $`O(C)`$. Rather than actually blocking, an empty live stream raises `BlockingIOError`. The model omits small-write atomicity, multiple-writer interleaving, signals, and kernel scheduling.

Tests transfer 250 bytes using 11-byte producer requests, three-byte consumer reads, and seven bytes of capacity. They compare the complete output with the original sequence, check the capacity bound after every step, and distinguish remaining data from EOF after writer closure. These are checks of conservation, ordering, and termination rather than elapsed waiting time. A Linux performance measurement needs separate counts for completed bytes, CPU use, blocked time, and maximum queue occupancy to explain the effect of changing buffer capacity.

Run the following commands from the repository root. The first prints the input and computed observations; the second runs the complete test suite in this example directory.

```sh
python "예제_examples/심화_advanced/systems/demo.py" pipe
python "예제_examples/심화_advanced/systems/test_advanced_models.py" -v
```

## 출처 / Sources

- [Linux man-pages: pipe(7)](https://man7.org/linux/man-pages/man7/pipe.7.html): 유한 바이트 스트림·EOF·부분 쓰기 / bounded streams, EOF, partial writes
- [Linux man-pages: poll(2)](https://man7.org/linux/man-pages/man2/poll.2.html): readiness와 HUP의 의미 / readiness and HUP semantics
