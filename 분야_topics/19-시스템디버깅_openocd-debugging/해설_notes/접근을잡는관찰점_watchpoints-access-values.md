# Watchpoint: 값이 바뀐 순간과 메모리 접근은 다르다

[분야 안내](../README.md) · [실행 예제](../../../예제_examples/심화_advanced/systems/advanced_models.py) · [독립 테스트](../../../예제_examples/심화_advanced/systems/test_advanced_models.py) · [실행 안내](../../../예제_examples/심화_advanced/systems/README.md)

## 한국어

### 값이 망가진 뒤가 아니라 쓴 위치를 찾는다

배열 옆의 변수가 가끔 바뀌는 오류를 찾을 때, 함수 시작마다 breakpoint를 놓으면 관찰 위치가 너무 많아진다. watchpoint는 특정 메모리나 표현식을 관찰해 관련 접근 때 실행을 멈추는 도구다. “이 값이 언제 달라졌는가”를 질문하는 출발점이지만, 접근과 값 변화는 같은 사건이 아니다. 같은 값을 다시 쓰면 write는 일어났어도 값은 그대로다.

GDB의 `watch expr`는 표현식 값 변화를, `rwatch`는 읽기를, `awatch`는 읽기·쓰기를 관찰한다. 가능한 경우 hardware watchpoint를 사용하고, 지원되지 않는 값 변화 관찰은 software single-step 방식으로 구현될 수 있다. 읽기·접근 watchpoint의 지원과 크기·개수는 target에 제약된다. [GDB Set Watchpoints](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Set-Watchpoints.html)

### byte 구간이 겹치는지부터 판정한다

관찰 범위를 반열린 구간 $`[a,a+s)`$, 한 memory access 범위를 $`[b,b+n)`$라고 하자. 두 구간이 겹치는 필요충분조건은

```math
\max(a,b)\lt\min(a+s,b+n).
```

끝점만 닿는 접근은 포함하지 않는다. 0x1000부터 4바이트를 보면 0x1004에서 시작하는 접근은 밖이고, 0x0FFF에서 2바이트를 쓰면 한 byte가 겹친다. 실제 하드웨어 comparator가 임의의 이런 구간을 그대로 지원한다는 뜻은 아니다. alignment, 길이, mask와 bus access 관찰 범위는 debug block에 따라 다르다.

`watch_hits()`는 이벤트마다 read/write 종류, 시작 주소, 전후 bytes를 받아 겹침과 관찰 종류를 검사한다. 값 변화 모드에서는 전체 access bytes가 아니라 관찰 범위와 겹친 부분만 비교한다. 큰 write의 관찰 바깥 byte만 바뀌었는데 hit로 판정하면 잘못된 원인을 지목하기 때문이다. access 모드는 같은 값을 다시 쓰는 사건도 센다.

### 명령과 hardware 지원을 연결한다

GDB에서 `watch -location variable`은 그 변수의 저장 위치를 관찰하는 형태다. `watch 0x20000000`처럼 상수 주소 숫자 자체를 관찰하면 메모리가 아니라 변하지 않는 상수 표현식을 지정한 것이다. 타입 크기를 고려해 pointer를 역참조해야 하며 symbol과 ELF가 실제 firmware와 같은지도 확인한다.

OpenOCD `wp address length r|w|a`는 memory access watchpoint를 요청한다. 주소·길이를 지정해도 CPU의 debug 자원이 부족하면 설치되지 않을 수 있다. GDB가 보인 watchpoint 번호와 실제 target에 설치된 comparator 수를 같은 것으로 단정하지 않는다. OpenOCD의 `debug_reason`과 watchpoint 목록으로 정지 이유를 구분할 수 있다. [OpenOCD General Commands](https://openocd.org/doc/html/General-Commands.html#Breakpoint-and-Watchpoint-commands)

### 관찰 자체가 실행 조건을 바꾼다

CPU halt 중에도 주변장치·DMA·다른 core가 계속 진행할 수 있다. CPU comparator가 DMA write까지 관찰하는지도 target별로 다르다. 최적화로 변수가 register에만 있거나 수명이 끝나면 source-level 변수 관찰이 기대와 달라질 수 있다. software watchpoint는 실행을 크게 느리게 하므로 timing race의 재현 조건도 바뀐다.

테스트는 범위 경계, 같은 값을 다시 쓰기, read와 write 구분, 관찰 범위 밖만 바뀐 multi-byte write를 각각 확인한다. 이벤트 수를 N, 비교하는 overlap bytes를 합쳐 M이라 하면 시간은 $`O(N+M)`$이고 결과 저장은 hit 수에 비례한다. demo는 합성 memory trace의 두 hit 목록을 출력한다. JTAG/SWD나 실제 GDB를 실행한 결과가 아니며, 보드의 watchpoint 개수·정지 지연을 측정하지 않았다. 합성 trace에서 조건을 분리해 이해한 뒤 실제 target의 정지 원인을 해석하는 데 쓰는 모델이다.

저장소 루트에서 실행한다. 첫 명령은 입력과 계산 결과를 출력하고, 두 번째 명령은 이 디렉터리의 전체 테스트를 실행한다.

```sh
python "예제_examples/심화_advanced/systems/demo.py" watch
python "예제_examples/심화_advanced/systems/test_advanced_models.py" -v
```

## English

### Find the write rather than only the damaged value

When a neighboring variable is occasionally corrupted, placing breakpoints at many function entries creates too many observation points. A watchpoint observes memory or an expression and stops execution on relevant activity. A write and a value change differ: writing the same value performs an access without changing stored data.

GDB `watch expr` observes expression value changes, `rwatch` reads, and `awatch` reads or writes. Hardware assistance is used when available; value-change watching can otherwise single-step in software. Read/access support, widths, and counts depend on the target. [GDB Set Watchpoints](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Set-Watchpoints.html)

### First decide whether byte intervals overlap

Let the watched interval be $`[a,a+s)`$ and an access cover $`[b,b+n)`$. They overlap exactly when

```math
\max(a,b)\lt\min(a+s,b+n).
```

Touching endpoints do not overlap. Watching four bytes from 0x1000 excludes an access starting at 0x1004, while a two-byte access from 0x0FFF overlaps one byte. This logical rule does not claim that hardware supports every arbitrary interval: alignment, size, masks, and observable bus accesses depend on the debug block.

`watch_hits()` examines access type, starting address, and before/after bytes. Value-change mode compares only the overlapping watched slice. A multi-byte write changing only bytes outside that slice must not be blamed. Access mode includes same-value writes.

### Relate commands to hardware resources

GDB `watch -location variable` observes the variable's storage. `watch 0x20000000` instead names a constant numeric expression; observing memory requires dereferencing a suitably typed pointer. Type size, symbols, and agreement between ELF and installed firmware all matter.

OpenOCD `wp address length r|w|a` requests an access watchpoint. A syntactically valid request can still exceed available CPU debug resources. A GDB watchpoint number does not establish a one-to-one count of installed comparators. OpenOCD's watchpoint list and `debug_reason` help distinguish stop causes. [OpenOCD General Commands](https://openocd.org/doc/html/General-Commands.html#Breakpoint-and-Watchpoint-commands)

### Observation changes execution conditions

Peripherals, DMA, or another core may continue during CPU halt. Whether a CPU comparator sees DMA writes is target-specific. Optimized-away or register-only variables and expired lifetimes affect source-level observation. Software watchpoints slow execution substantially and can alter a timing race.

Tests cover exact boundaries, same-value writes, read/write filtering, and multi-byte changes entirely outside the watched slice. With N events and M compared overlap bytes, time is $`O(N+M)`$; result storage scales with hit count. The demo prints hit lists for a synthetic memory trace. It neither runs GDB/JTAG/SWD nor measures target watchpoint count or halt latency. Its purpose is to separate observation conditions before interpreting target evidence.

Run the following commands from the repository root. The first prints the input and computed observations; the second runs the complete test suite in this example directory.

```sh
python "예제_examples/심화_advanced/systems/demo.py" watch
python "예제_examples/심화_advanced/systems/test_advanced_models.py" -v
```

## 출처 / Sources

- [GDB: Setting Watchpoints](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Set-Watchpoints.html): 값 변화·접근·hardware 제한 / value changes, accesses, hardware limits
- [OpenOCD: General Commands](https://openocd.org/doc/html/General-Commands.html): wp·debug_reason·target 상태 / wp, debug_reason, target state
