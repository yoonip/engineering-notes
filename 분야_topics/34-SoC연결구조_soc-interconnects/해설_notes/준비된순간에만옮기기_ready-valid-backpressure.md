# 준비된 순간에만 옮기기: ready/valid와 backpressure

[SoC interconnect](../README.md) · [참조 모델](../../../예제_examples/확장기초_extended/hardware/models.py) · [검산](../../../예제_examples/확장기초_extended/hardware/test_models.py)

## 한국어

### 보냈다는 것과 받아졌다는 것

생산자는 데이터를 준비했지만 소비자는 잠시 바쁠 수 있다. Valid는 생산자가 유효한 payload를 내놓았다는 뜻이고 ready는 소비자가 받을 수 있다는 뜻이다. 공통 clock의 상승 에지에서 둘 다 1일 때 한 transfer가 일어난다. Valid가 여러 cycle 동안 1이어도 ready가 0이면 전송 횟수는 0이다. [Arm AMBA AXI, A3.2](https://developer.arm.com/-/media/Arm%20Developer%20Community/PDF/IHI0022H_amba_axi_protocol_spec.pdf)

이 글은 단일 clock·단일 순서의 beat 채널을 다룬다. AXI memory-mapped 전체의 address/data/response, ID, burst, ordering을 구현하는 글은 아니다. Reset과 clock enable 조건이 있는 IP는 그 조건까지 transfer 정의에 넣어야 한다. AMD의 video AXI4-Stream 예는 READY·VALID뿐 아니라 ACLKEN과 ARESETn도 명시한다. [AMD PG043](https://docs.amd.com/r/en-US/pg043_v_vid_in_axi4s/READY/VALID-Handshake)

### 지켜야 하는 두 가지 약속

첫째, 생산자는 ready가 올라오기를 기다린 뒤에만 valid를 올리도록 만들지 않는다. 소비자가 valid를 기다리도록 허용된 구조와 만나면 둘 다 기다리는 deadlock이 생길 수 있다. 둘째, valid를 올렸는데 수락되지 않았다면 valid와 해당 payload를 유지한다. Payload에는 data뿐 아니라 last, byte enable 등 그 beat에 속한 부가 정보도 포함된다. [Arm의 handshake 의존성](https://developer.arm.com/-/media/Arm%20Developer%20Community/PDF/IHI0022H_amba_axi_protocol_spec.pdf)

샘플 t에서 transfer를 $`h_t=v_t\land r_t`$로 정의하면, stall 조건은 $`v_t\land\neg r_t`$다. Reset에 의해 취소되는 경우를 제외하고

$$v_t\land\neg r_t\Rightarrow v_{t+1}\land(data_{t+1}=data_t)$$

가 필요하다. Valid와 ready가 연속으로 1이면 매 edge마다 서로 다른 beat를 받을 수 있다. Valid의 상승 에지만 세거나 ready를 acknowledgement pulse처럼 해석하면 전송을 놓친다.

### 2-entry 버퍼의 상태 모델

버퍼에 저장한 ordered queue를 Q, 크기를 n이라 하자. 아래 참조 모델은 empty bypass 없이 다음처럼 정한다.

$$in\_ready=(n<2),\quad out\_valid=(n>0),\quad out\_data=Q[0].$$

$$a_t=in\_valid\land in\_ready,\quad b_t=out\_valid\land out\_ready,\quad
n_{t+1}=n_t+a_t-b_t.$$

모든 판단은 갱신 전 상태를 쓴다. 먼저 수락한 출력 하나를 제거하고 수락한 입력 하나를 뒤에 추가한다. 크기 1에서 동시 수락하면 한 beat/cycle을 유지할 수 있다. Full에서는 같은 에지에 출력이 나가더라도 새 입력을 받지 않아, full에서 회복하는 cycle에 입력 bubble이 생긴다. 이는 downstream ready를 입력 ready에 조합 연결하지 않는 간단한 계약의 대가다. 다른 elastic/skid-buffer 설계는 여유 공간과 register를 달리 구성할 수 있다.

| 에지 전 상태 | 입력 수락 | 출력 수락 | 다음 크기 |
|---|---|---|---|
| n=0, 입력 valid=1 | 가능 | 불가 | 1 |
| n=1, 양쪽 요청 있음 | 가능 | 가능 | 1 |
| n=2, 출력 ready=1 | 불가 | 가능 | 1 |
| n=1, 출력 ready=0, 입력 valid=1 | 가능 | 불가 | 2 |

Arm AXI는 interface의 입력과 출력 사이 조합 경로 제한도 둔다. Ready/valid라는 이름만 붙였다고 AXI에 자동으로 적합한 것은 아니다. 서로 다른 clock 사이에서는 이 handshake만으로 CDC가 해결되지 않으며 asynchronous FIFO 등 별도 구조가 필요하다.

### 구현과 독립 검증

`ReadyValidBuffer.cycle`은 에지 직전의 ready/valid/data와 실제 수락 여부를 반환한 뒤 상태를 바꾸는 Python 모델이다. Reset cycle은 transfer로 세지 않고 queue를 비운다. 이 reset 계약을 실제 IP의 정확한 reset 사양과 구분한다.

테스트 생산자는 아직 수락되지 않은 token을 유지하고, 소비자의 ready를 무작위로 바꾼다. 별도 list scoreboard에 수락된 입력을 쌓고 수락된 출력과 비교하여 5,000 cycle 동안 순서·중복·유실을 점검한다. Stall 전후의 payload 유지, 점유량 한계, drain과 reset도 확인한다. 단순 최종 개수 비교가 아니라 token 순서까지 검사한다.

RTL 검증에서는 에지의 sampling/NBA 시점을 맞춘 monitor로 같은 계약을 기록하고, stall 유지 assertion과 입력·출력 scoreboard를 함께 쓴다. Empty, full, 연속 전송, 동시 수락, 장시간 backpressure, reset을 directed test와 coverage로 확인한다. Throughput은 수락된 beat 수/관찰 cycle, latency는 같은 token의 입력 수락부터 출력 수락까지로 정의한다. Python 통과는 실제 RTL·AXI VIP·timing closure 실행 결과가 아니다.

## English

### Offered is not the same as accepted

A producer may have data while a consumer is busy. Valid means a payload is available; ready means the receiver can accept it. A transfer occurs on a shared rising edge with both asserted. Valid held high while ready is low represents no accepted transfers. [Arm AXI A3.2](https://developer.arm.com/-/media/Arm%20Developer%20Community/PDF/IHI0022H_amba_axi_protocol_spec.pdf)

This article covers one ordered beat channel in one clock domain, not complete memory-mapped AXI addresses, data, responses, IDs, bursts and ordering. IP-specific reset and clock-enable conditions also matter: AMD's video-stream definition explicitly includes ACLKEN and ARESETn. [AMD PG043](https://docs.amd.com/r/en-US/pg043_v_vid_in_axi4s/READY/VALID-Handshake)

### Two essential promises

A producer must not require ready before asserting valid; it could deadlock with a receiver allowed to wait for valid. Once valid is offered without acceptance, retain both valid and payload, including associated last/byte-enable information. [Arm handshake dependencies](https://developer.arm.com/-/media/Arm%20Developer%20Community/PDF/IHI0022H_amba_axi_protocol_spec.pdf)

Define $`h_t=v_t\land r_t`$. Except for reset cancellation, $`v_t\land\neg r_t`$ requires $`v_{t+1}`$ and unchanged payload. When valid and ready remain high, each edge can accept a new beat. Counting only valid rising edges or treating ready as a one-shot acknowledgement loses transfers.

### A two-entry state model

Let Q be an ordered queue of size n. The reference has no empty bypass:

$$in\_ready=(n<2),\quad out\_valid=(n>0),\quad out\_data=Q[0],$$

$$a_t=in\_valid\land in\_ready,\quad b_t=out\_valid\land out\_ready,\quad
n_{t+1}=n_t+a_t-b_t.$$

All decisions use pre-edge state; remove an accepted output and append an accepted input. At n=1, simultaneous acceptance sustains one beat per cycle. At full, an outgoing beat does not permit an incoming beat on that same edge, creating an input bubble during recovery. This trades some full-state performance for a simple contract without a combinational downstream-ready-to-upstream-ready path. Other elastic/skid-buffer structures make different choices.

At empty, valid input can fill one slot but no output is accepted. At n=1 with both ends ready, one beat enters and another leaves. At n=2 with output ready, only the output leaves. At n=1 with output stalled and valid input, the second slot fills.

Arm AXI also restricts combinational input-to-output paths at interfaces; signal names alone do not establish compliance. Ready/valid alone does not solve clock-domain crossing. Separate CDC structures such as asynchronous FIFOs are needed.

### Implementation and independent checks

`ReadyValidBuffer.cycle` returns pre-edge signals and accepted events before changing Python state. Reset clears the queue and counts no transfers for that cycle; actual IP reset rules must be checked separately.

The test producer retains unaccepted tokens while the receiver varies ready randomly. A separate list scoreboard tracks accepted inputs and compares accepted outputs over 5,000 cycles, checking token order, duplication/loss, stall stability, capacity, drain and reset. It does more than compare final counts.

For RTL, align monitor sampling with HDL nonblocking-update semantics and combine a stall-stability assertion with an input/output scoreboard. Directed tests and coverage must exercise empty/full, continuous traffic, simultaneous acceptance, long backpressure and reset. Define throughput as accepted beats per observed cycle and token latency from input acceptance to output acceptance. Python passes are not RTL, AXI VIP or timing-closure results.

## 출처 대조 / Source cross-check

Arm의 일반 AXI handshake와 AMD의 실제 stream IP 조건을 대조했다. 버퍼의 경계 정책은 위에 별도로 정의했다. / Arm's protocol was cross-checked against AMD's concrete stream-IP conditions; buffer boundary choices are specified separately. 확인 / checked: 2026-10-19.
