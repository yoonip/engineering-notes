# Embedded Linux의 readiness: 바이트를 끝까지 읽는 상태

[분야 안내](../README.md) · [실행 예제](../../../예제_examples/심화_advanced/systems/advanced_models.py) · [독립 테스트](../../../예제_examples/심화_advanced/systems/test_advanced_models.py) · [실행 안내](../../../예제_examples/심화_advanced/systems/README.md)

## 한국어

### 데이터가 준비됐다는 신호와 완성된 메시지는 다르다

센서·socket·pipe를 한 event loop에서 읽을 때 매번 잠깐 자는 반복문을 만들면 반응 시간이 늦거나 CPU를 불필요하게 쓴다. readiness API는 어느 descriptor에서 I/O를 진행할 수 있는지 기다린다. 그러나 한 번 준비됐다고 해서 한 개의 메시지가 정확히 도착했다는 뜻은 아니다. 한 레코드가 여러 read로 나뉘거나 여러 레코드가 한 read에 들어올 수 있다.

Linux `poll()`은 descriptor별 event mask를 반환한다. `POLLIN`과 `POLLHUP`가 동시에 나올 수 있으며, peer가 닫았어도 버퍼에 남은 데이터를 모두 읽은 뒤에야 read가 0이 된다. `select()`는 descriptor 집합을 입력·출력으로 사용하고 호출 뒤 집합을 갱신하므로 반복 호출 전에 다시 준비해야 한다. 일반적인 `fd_set` 크기 제한도 있다. [Linux poll(2)](https://man7.org/linux/man-pages/man2/poll.2.html), [Linux select(2)](https://man7.org/linux/man-pages/man2/select.2.html)

### stream 상태와 parser 상태를 나눈다

예제 프로토콜은 newline으로 끝나는 byte record다. UTF-8 decoding보다 먼저 byte 경계를 찾으므로 다중 byte 문자가 read 경계에서 갈라져도 transport 단계에서 손상시키지 않는다. newline을 레코드 내용으로 넣는 escaping 규칙은 이 형식에 없다. 빈 줄은 빈 레코드로 허용한다.

`LineReceiver`는 완성되지 않은 한 줄만 `pending`에 유지한다. chunk를 읽으면 각 byte를 보고 newline 전까지 저장하고 newline에서 한 레코드를 방출한다. 저장 상한 80바이트를 넘으면 실패한다. 수신이 끝날 때 pending이 비어 있지 않으면 이 계약에서는 잘린 마지막 record이므로 오류다. 끝에 newline 없는 마지막 줄을 허용하는 형식도 있지만 그 규칙을 여기와 혼동하면 안 된다.

상태 불변식은 $`0\le\mathrm{len}(pending)\le80`$이고, 이미 내보낸 레코드는 다음 chunk에서 다시 나오지 않는다는 것이다. 전체 N바이트를 한 번씩 처리하므로 시간은 $`O(N)`$다. parser 자체의 대기 저장 공간은 상한으로 제한되지만, 반환된 레코드 전체를 list에 모으는 demo의 공간은 출력 크기에 비례한다. 스트리밍 소비자는 처리한 레코드를 즉시 넘길 수 있다.

### 실제 실행 예제의 경계

`socket_records()`는 표준 라이브러리의 실제 local `socketpair`에 작은 fixture를 보내고 writer의 쓰기 방향을 닫는다. reader를 nonblocking으로 두고 `DefaultSelector`에서 이벤트를 기다린 뒤 3바이트씩 읽는다. 매번 반환된 길이를 보고 parser를 진행시키며 EOF에서 pending을 검사한다. 예제 fixture 크기는 1,024바이트로 제한한다. 일반적인 양방향 송수신 서버를 구현한 것은 아니다.

Python `selectors`는 플랫폼에 맞는 backend를 고르는 상위 API다. Windows에서 실행된 결과는 local socket의 readiness·EOF 검증이며 Linux `poll` syscall 자체를 실행했다는 의미가 아니다. Linux 장치 파일은 해당 driver가 readiness를 제대로 구현했는지도 별도로 확인해야 한다. [Python selectors](https://docs.python.org/3/library/selectors.html)

### 종료와 경계가 검증 기준이다

테스트는 `alpha`, 빈 레코드, `beta`를 포함한 bytes를 가능한 모든 두 조각 분할 위치에서 먹이고 항상 같은 세 레코드가 나오는지 비교한다. 길이 상한 초과와 EOF에서 잘린 줄을 거부하며 실제 socketpair 경로도 같은 결과를 내는지 확인한다. 시간에 기대어 “충분히 기다렸으니 왔을 것”이라고 판단하는 대신 EOF와 parser 상태를 검사한다.

실제 장치에서는 read 오류, `EINTR`, 재연결, 여러 client의 공정성, 쓰기 버퍼 상한이 추가된다. 하나의 event에서 무제한으로 계속 읽으면 바쁜 장치가 다른 descriptor를 굶길 수 있다. per-event 처리량을 제한할 때에는 level-triggered·edge-triggered 방식의 drain 규약까지 맞춰야 한다. 이 예제는 selector의 일반적인 반복 구조와 bounded record 조합에 한정한다.

저장소 루트에서 실행한다. 첫 명령은 입력과 계산 결과를 출력하고, 두 번째 명령은 이 디렉터리의 전체 테스트를 실행한다.

```sh
python "예제_examples/심화_advanced/systems/demo.py" poll
python "예제_examples/심화_advanced/systems/test_advanced_models.py" -v
```

## English

### Readiness and message completeness differ

Sleeping repeatedly while checking sensors, sockets, and pipes can waste CPU or delay responses. Readiness APIs wait for descriptors on which I/O can progress. A readiness notification does not identify a complete application message: one record may span reads, and one read may contain several records.

Linux `poll()` returns per-descriptor event masks. `POLLIN` can coexist with `POLLHUP`; buffered data must be consumed before read returns zero after peer closure. `select()` modifies its descriptor sets, requiring reinitialization before reuse, and conventional `fd_set` implementations have size limits. [Linux poll(2)](https://man7.org/linux/man-pages/man2/poll.2.html), [Linux select(2)](https://man7.org/linux/man-pages/man2/select.2.html)

### Separate transport state from parser state

The example protocol uses newline-terminated byte records. It identifies byte boundaries before UTF-8 decoding, avoiding premature decoding when a multibyte character spans reads. This format provides no escaping for embedded newlines, and an empty line is a valid empty record.

`LineReceiver` retains one incomplete line in `pending`. It appends ordinary bytes and emits a record at newline. More than 80 pending bytes is an error. At EOF, nonempty pending data means truncation under this contract. A format that permits an unterminated final line would have a different rule.

The invariant is $`0\le\mathrm{len}(pending)\le80`$, and previously emitted records never reappear on a later chunk. Processing N bytes costs $`O(N)`$ time. Pending parser storage is bounded, while the demo's list of all returned records additionally scales with total output. A streaming consumer can process records immediately.

### What actually runs

`socket_records()` sends a small fixture through a real standard-library local `socketpair`, shuts down the writer's sending direction, and uses a nonblocking reader with `DefaultSelector`. It reads three bytes at a time, feeds actual returned bytes, and validates pending state at EOF. Fixture size is capped at 1,024 bytes; this is not a general bidirectional server.

Python `selectors` chooses a platform backend. A run on Windows verifies local socket readiness and EOF, not the Linux `poll` syscall. Linux device files additionally depend on their driver implementing meaningful readiness behavior. [Python selectors](https://docs.python.org/3/library/selectors.html)

### Verify boundaries and termination

Tests feed `alpha`, an empty record, and `beta` using every possible two-chunk split and require the same three outputs. They reject overlength records and truncated EOF and execute the real socketpair path. Completion follows EOF and parser state rather than a timing assumption that enough sleeping must have delivered the bytes.

Real devices add read errors, `EINTR`, reconnection, client fairness, and bounded outgoing buffers. Draining one busy device indefinitely can starve others. Limiting work per event must still respect the selected level-triggered or edge-triggered contract. This example covers the selector loop combined with bounded record parsing.

Run the following commands from the repository root. The first prints the input and computed observations; the second runs the complete test suite in this example directory.

```sh
python "예제_examples/심화_advanced/systems/demo.py" poll
python "예제_examples/심화_advanced/systems/test_advanced_models.py" -v
```

## 출처 / Sources

- [Linux poll(2)](https://man7.org/linux/man-pages/man2/poll.2.html): POLLIN·HUP·readiness
- [Linux select(2)](https://man7.org/linux/man-pages/man2/select.2.html): 집합 갱신·fd 제한 / set updates and descriptor limits
- [Python selectors](https://docs.python.org/3/library/selectors.html): 플랫폼별 backend / platform backend
