# Lamport clock: 시각을 맞추지 않고 인과 순서를 기록하기

[상태 코드](../../../예제_examples/심화_advanced/ai_data/advanced_ai_models.py) · [CLI](../../../예제_examples/심화_advanced/ai_data/demo.py) · [검증](../../../예제_examples/심화_advanced/ai_data/test_advanced_ai.py)

## 시각과 인과적 순서의 차이

두 컴퓨터의 화면 시계가 조금 어긋나도, 한쪽에서 보낸 메시지를 다른 쪽에서 받은 사건이 송신보다 앞설 수는 없습니다. 분산 시스템의 논리 시계는 초 단위를 정확히 맞추는 대신 이런 사건 사이의 관계를 기록합니다. 로그의 timestamp가 더 작다는 이유만으로 실제 원인이었다고 결론내리면 안 된다는 점이 핵심입니다.

이 글은 process 내부의 사건 순서와 메시지의 송신·수신이 정해진 비동기 메시지 모델을 사용합니다. 메시지 지연에 상한을 두지 않으며 timestamp는 정수입니다. 운영체제의 wall clock이나 stopwatch를 읽어 시간을 잰 결과가 아닙니다. [Lamport 원 논문](https://lamport.azurewebsites.net/pubs/time-clocks.pdf), [Yale 논리 시계 강의](https://www.cs.yale.edu/homes/aspnes/pinewiki/LogicalClocks.html)

## Happens-before의 세 규칙

사건 a가 b보다 인과적으로 앞선다는 관계를 $`a\to b`$로 씁니다. 같은 process 안에서 a 다음에 b가 일어나면 관계가 있습니다. 같은 메시지의 송신은 수신보다 앞섭니다. 그리고 $`a\to b`$, $`b\to c`$이면 $`a\to c`$입니다. 이 추이성으로 여러 번의 메시지를 거친 간접 관계도 표현합니다.

서로 다른 process에서 메시지 경로가 없는 두 사건은 이 관계에서 비교되지 않을 수 있습니다. 이를 concurrent라고 부르며, 물리적으로 정확히 같은 순간에 일어났다는 뜻은 아닙니다. 전역 사건 목록이 편의상 한 줄로 나열되어도, 그 나열의 모든 앞뒤가 인과관계인 것은 아닙니다. [Cornell의 사건·논리 시계 설명](https://www.cs.cornell.edu/courses/cs614/1999sp/notes99/clocks.html)

## Max-plus 갱신을 유도하기

각 process가 정수 C를 갖습니다. 내부 사건이나 송신 때는 C를 1 늘리고 그 값을 사건에 붙입니다. 송신 메시지에는 송신 사건의 값을 함께 보냅니다. Timestamp t를 받은 수신 사건은 현재 C와 t 모두보다 커야 합니다.

```math
C_{\mathrm{receive}}=\max(C_{\mathrm{local}},t_{\mathrm{message}})+1.
```

그러면 같은 process의 앞 사건보다 크고 송신 timestamp보다도 큽니다. 기본 두 관계에서 숫자가 증가하므로 추이적인 경로에서도 증가합니다. 따라서 clock condition이 성립합니다.

```math
a\to b\quad\Longrightarrow\quad C(a)\lt C(b).
```

반대 방향은 일반적으로 성립하지 않습니다. A가 내부 사건 두 개로 C=2가 되고 B가 독립적인 내부 사건 하나로 C=1이 되어도 B→A라는 메시지 경로는 없습니다. 숫자 1과 2를 정렬하는 일과 인과관계를 발견하는 일은 다릅니다. 원 논문도 이 converse의 한계를 명시합니다.

## 동점과 전체 순서

서로 독립적인 A.local과 B.local은 둘 다 timestamp 1일 수 있습니다. 로그에 전체 순서가 필요하면 process ID 등을 추가한 tuple로 정렬할 수 있습니다. 예를 들어 $`(C,\mathrm{processID})`$의 사전 순서는 동점을 깨면서 기존 인과 방향을 거스르지 않습니다. 하지만 동시에 가능했던 사건의 상대 순서는 약속으로 추가한 것입니다.

이 정렬만으로 모든 복제본이 같은 명령 목록을 받았는지, 더 작은 timestamp 메시지가 앞으로 오지 않는지, 실패한 process를 어떻게 처리하는지 해결되지 않습니다. 논리 시계는 consensus나 복제 로그 commit의 대체물이 아닙니다. Snapshot·상태 동기화에서도 일관된 사건 경계와 전송 중 메시지의 처리가 필요합니다. 단순히 여러 서버의 “현재 dict”를 모아 같은 물리 순간의 상태라고 부를 수는 없습니다.

## 실행 예

```bash
python "예제_examples/심화_advanced/ai_data/demo.py" clocks
python -m unittest discover -s "예제_examples/심화_advanced/ai_data" -p "test_*.py" -v
```

출력 순서는 A.local=1, B.local=1, A.send=2, B.receive=3, B.local=4입니다. 첫 두 사건의 숫자가 같은 것은 오류가 아닙니다. B의 수신은 A의 송신 2보다 크고, B의 이전 사건 1보다도 큽니다. 이후 B의 내부 사건은 다시 증가합니다.

`LamportClock`은 clock 한 개의 갱신을 실행합니다. 테스트는 송신→수신, process 내부 순서, 같은 초기값의 독립 사건을 별도 조건으로 비교합니다. 실제 네트워크 전송을 하지 않고 호출 순서로 메시지 상태를 재현합니다. 시간 동기화 오차·전송 지연·장애 복구를 측정했다고 주장하지 않습니다.

## 운영 상태와 연결할 때의 전제

재시작 뒤 clock이 0으로 돌아오면 이전 로그와 단순 숫자만으로 섞을 수 없습니다. Process incarnation이나 영속 counter 등 수명 정책이 필요합니다. 정수 크기 제한이 있는 구현은 overflow를 다뤄야 하고, 동시 thread가 한 clock을 갱신하면 원자성이 필요합니다. 예제는 한 호출씩 순차 실행하는 상태 모델입니다.

Timeout은 실제 경과 시간의 기준이 필요하므로 Lamport 숫자 차이를 millisecond로 읽을 수 없습니다. 물리 시계 보정과 인과 timestamp는 서로 보완할 수 있지만 같은 계측량은 아닙니다. 이 구분을 유지해야 정렬된 로그를 보고 일어나지 않은 원인 관계를 만들어 내지 않습니다.

## English

### Time of day versus causal precedence

Unsynchronized computers can still know that sending a message precedes receiving that same message. Logical clocks record event relations instead of accurately measuring seconds. A smaller timestamp alone does not prove that an event caused another.

The model uses process-local order and message send/receive relations in an asynchronous system with no delay bound. Integer timestamps are not wall-clock or stopwatch measurements. [Lamport](https://lamport.azurewebsites.net/pubs/time-clocks.pdf) and [Yale's notes](https://www.cs.yale.edu/homes/aspnes/pinewiki/LogicalClocks.html) distinguish these roles.

### Define the relation before its numbers

Happens-before includes local precedence, a message's send-before-receive relation and transitive closure. Different-process events without a connecting causal path may be concurrent. Concurrency does not mean precisely simultaneous physical instants. An arbitrary global listing includes order choices that may not be causal. [Cornell notes](https://www.cs.cornell.edu/courses/cs614/1999sp/notes99/clocks.html)

For local/send events increment C and attach that result. On receive, choose $`\max(C,t)+1`$. The result exceeds both the preceding local value and the message's send time. Since both generating relations increase and increases compose transitively, $`a\to b`$ implies $`C(a)\lt C(b)`$.

The converse fails: two local events at A can reach two while an independent event at B has one. No B-to-A path follows merely from the comparison. Lamport explicitly discusses that limitation.

### Total order is an additional convention

Independent first events can both have timestamp one. A lexicographic tuple such as $`(C,\mathrm{processID})`$ can break ties while respecting causal precedence. It deliberately chooses relative order for some concurrent events.

This does not show that replicas received the same commands, that earlier messages cannot arrive later or how failures are handled. Logical clocks do not replace consensus or log-commit protocols. Consistent snapshots additionally need an event boundary and treatment of in-flight messages; collecting current dictionaries is not automatically one physical-time snapshot.

### Executed state transitions and limits

Run the commands above. The example emits A.local=1, B.local=1, A.send=2, B.receive=3 and B.local=4. Equal independent timestamps are valid; receive three exceeds both send two and B's previous one.

Tests check local and message precedence plus independent equal timestamps. The class simulates ordered calls and message timestamps without a network, clock synchronization or latency measurement.

Restarting a counter at zero needs a process-incarnation or persistence policy before merging old and new histories. Fixed-width implementations require overflow handling; concurrent updates require synchronization. This example is sequential. Timeouts need elapsed-time clocks: logical-clock differences cannot be interpreted as milliseconds. Physical synchronization and causal timestamps can complement one another without representing the same quantity.

## 출처 / Sources

- [Lamport, Time, Clocks, and the Ordering of Events](https://lamport.azurewebsites.net/pubs/time-clocks.pdf): happened-before, clock condition and converse limitation.
- [Yale, James Aspnes: LogicalClocks](https://www.cs.yale.edu/homes/aspnes/pinewiki/LogicalClocks.html): operational max-plus rule and causal ordering.
- [Cornell CS614, Time, Clocks, Events](https://www.cs.cornell.edu/courses/cs614/1999sp/notes99/clocks.html): partial order and logical timestamp interpretation. 확인 / checked: 2026-10-19.
