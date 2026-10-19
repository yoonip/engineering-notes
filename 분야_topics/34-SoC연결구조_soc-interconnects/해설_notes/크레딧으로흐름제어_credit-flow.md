# 멀리 있는 버퍼를 넘치지 않게 쓰기: credit flow control

[SoC 연결 구조 목차](../README.md) · [주기 모델](../../../예제_examples/심화_advanced/hardware/models.py) · [검산](../../../예제_examples/심화_advanced/hardware/test_models.py)

## 한국어

### 빈자리 표를 먼저 받는다

ready 신호가 멀리서 돌아오는 데 여러 cycle이 걸리면, 상대가 가득 찬 것을 보고 멈출 때 이미 추가 데이터가 이동 중일 수 있다. credit은 아직 사용할 수 있는 버퍼 자리의 표다. 보낼 때 표 하나를 쓰고, 수신자가 데이터를 꺼낸 뒤 반환한 표가 돌아와야 다시 쓴다. 지연을 없애는 대신 이동 중인 데이터까지 자리에 미리 계산하는 방법이다.

[Altera P-Tile PCIe의 TX flow-control 설명](https://docs.altera.com/r/docs/683059/25.3/p-tile-avalon-streaming-ip-for-pci-express-user-guide/tx-flow-control-interface)은 전송 전에 수신 버퍼 공간을 credit으로 확인하는 구조를 설명한다. [PCI-SIG의 flow-control 변경 설명](https://pcisig.com/blog/pci-express%C2%AE-60-specification-functionality-updates-%E2%80%93-part-2)은 shared buffer와 virtual channel 같은 실제 프로토콜의 확장을 보여 준다. 아래 모델은 이 아이디어를 한 종류의 unit-sized token으로 단순화한 것이며 PCIe 규격 구현이 아니다.

### 자리는 네 곳 중 하나에 있다

전체 수신 용량을 B, 송신자가 가진 credit을 c, data link에서 이동 중인 token 수를 d, 수신 queue의 데이터를 q, 반환 link에서 이동 중인 credit을 r이라 하자. 초기에는 c=B, 나머지는 0이다. 단위는 모두 자리 수다.

```math
c+d+q+r=B.
```

전송은 c를 하나 줄이고 d를 늘린다. 도착은 d를 줄이고 q를 늘린다. 소비는 q를 줄이고 r을 늘린다. credit 반환은 r을 줄이고 c를 늘린다. 매 사건이 한 곳에서 다른 곳으로 표를 옮기므로 합은 변하지 않는다. 반환 credit을 잃으면 성능이 내려가고, 중복 반환하면 합이 늘어 overflow가 가능해진다.

| 사건 | 감소 | 증가 |
|---|---|---|
| send | c | d |
| data arrival | d | q |
| consume | q | r |
| credit arrival | r | c |

link가 신뢰 가능하고 순서를 지키며, 각 지연이 1 cycle 이상이고, credit은 실제 소비 이후에만 반환된다고 가정한다. reset 중 이동 중인 token을 어떻게 버리고 초기 credit을 다시 맞추는지는 실제 프로토콜에 필요하지만 이 정상 동작 모델에서는 reset을 넣지 않는다.

### 왕복 시간과 필요한 buffer

송신 뒤 데이터가 도착하는 데 F cycle, 소비 즉시 credit이 돌아오는 데 R cycle이면 가장 빠른 credit 재사용 시간은 F+R cycle이다. 한 cycle에 하나씩 보내려면 각 credit이 돌아오기 전 다른 credit으로 계속 보내야 한다.

```math
Throughput\le\min\left(1,\frac{B}{F+R}\right)
\quad\mathrm{tokens/cycle}.
```

이는 한 cycle당 최대 한 token, 즉시 소비, 일정 지연, 충분한 입력이라는 이상 조건에서의 장기 상한이다. 가변 packet 크기, arbitration, credit batching, 소비 지연이 있으면 더 낮아질 수 있다. F=R=3이면 B=6은 매 cycle 전송을 유지하고 B=3은 장기적으로 절반 속도다. latency를 숨기려면 대략 bandwidth×round-trip만큼의 자리가 필요하다는 관계다.

### 구현과 검산

```bash
python demo.py --case credits
python -m unittest -v test_models.HardwareModels.test_credit_conservation_order_stalls test_models.HardwareModels.test_credit_round_trip_throughput
```

모델은 각 cycle에 반환 credit 도착, data 도착, 소비, 신규 전송 순서로 처리한다. 같은 cycle에 돌아온 credit을 그 cycle의 전송에 쓸 수 있다는 규약이다. data와 credit link는 event queue로 따로 유지한다. 무작위 소비·입력 stall에서도 보존식, 최대 q≤B, consumed stream이 sent stream의 prefix인지 확인한다. 600 cycle 고정 지연 예에서는 B=6이 600개, B=3이 300개를 전송한다.

실제 하드웨어는 token 크기와 credit 단위, counter overflow, reset·link recovery, 서로 다른 clock domain, data integrity와 deadlock을 추가로 다룬다. 여러 virtual channel의 합이 보존돼도 cyclic dependency가 있으면 deadlock이 생길 수 있다. 이 Python 실행은 단일 link의 회계·순서·성능 모델이며 실제 SoC fabric의 timing이나 프로토콜 적합성 검증은 아니다.

## English

### Reserve capacity before sending

When a ready response takes several cycles to return, additional data can already be in flight when the sender learns that the receiver is full. A credit represents one reserved buffer slot. Sending spends a credit; only a credit returned after consumption can be reused. This accounts for propagation delay rather than removing it.

[Altera's P-Tile PCIe TX flow-control documentation](https://docs.altera.com/r/docs/683059/25.3/p-tile-avalon-streaming-ip-for-pci-express-user-guide/tx-flow-control-interface) describes checking receiver buffer credits before transmission. [PCI-SIG's flow-control discussion](https://pcisig.com/blog/pci-express%C2%AE-60-specification-functionality-updates-%E2%80%93-part-2) gives real-protocol context for shared buffers and virtual channels. The example reduces the idea to a single class of unit tokens; it is not a PCIe implementation.

### Deriving the conservation law

Let B be receiver capacity, c sender credits, d in-flight data, q queued data and r returning credits. Initially c=B and the others are zero. Sending moves one unit from c to d, arrival from d to q, consumption from q to r, and credit arrival from r to c. Therefore $`c+d+q+r=B`$ is invariant.

Lost credits reduce available throughput; duplicated credits can overbook the receiver. Assume reliable ordered links, positive integer delays and credit return only after consumption. Reset-time cancellation and credit reinitialization are essential physical-protocol concerns but are outside this steady-operation model.

### Round-trip delay and throughput

With F forward cycles and R return cycles, immediate consumption permits a credit to be reused no earlier than F+R cycles after sending. For a one-token-per-cycle link and saturated input, long-run throughput is at most min(1,B/(F+R)). Variable packet sizes, arbitration, batched credits or delayed consumption can reduce it further.

For F=R=3, six credits sustain one send each cycle; three credits sustain half that rate in the ideal periodic case. Buffer capacity thus hides latency through a bandwidth-times-round-trip relationship.

### Implementation and validation

Each model cycle processes credit arrivals, data arrivals, consumption and new sends in that order. A credit arriving in a cycle can fund that cycle's send. Separate event queues represent the two links. Under random input and consumption stalls, tests check the conservation law, occupancy bounds and that the consumed sequence is a prefix of the sent sequence. Over 600 cycles, capacities six and three send 600 and 300 tokens respectively.

Physical interconnect verification must additionally cover credit units, packet lengths, counter rollover, reset and recovery, CDC, integrity and deadlock. Global count conservation does not prevent cyclic dependency across virtual channels. The Python execution checks a single-link accounting and performance model, not fabric timing or protocol conformance.

## 출처 / Sources

- Altera, *P-Tile Avalon Streaming PCIe User Guide 25.3*, TX Flow Control, 2026-03-24: receiver-credit checks.
- PCI-SIG, *PCI Express 6.0 Functionality Updates, Part 2*: shared-credit and buffer context. Links appear above.
