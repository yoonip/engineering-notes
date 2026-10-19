# Verilog·SystemVerilog·RTL

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

HDL은 하드웨어의 구조와 동작을 기술하는 언어입니다. 여러 회로 블록이 동시에 동작합니다. RTL은 레지스터와 그 사이의 조합논리로 데이터 이동을 표현하며, 합성 도구는 이를 논리 회로로 변환합니다.

## 조합논리와 순차논리

조합논리의 출력은 현재 입력으로 결정됩니다. 순차논리는 레지스터에 저장된 상태를 함께 사용합니다. SystemVerilog의 `always_comb`는 조합논리, `always_ff`는 플립플롭 기반 동작을 명확히 표현합니다. 조합 블록에서 출력이 모든 경로에 할당되지 않으면 래치가 추론될 수 있습니다.

```systemverilog
module counter (
    input  logic       clk,
    input  logic       rst_n,
    input  logic       enable,
    output logic [7:0] count
);
    always_ff @(posedge clk) begin
        if (!rst_n)
            count <= '0;
        else if (enable)
            count <= count + 8'd1;
    end
endmodule
```

이 카운터는 동기식 active-low 리셋을 사용합니다. `rst_n`이 낮은 상태에서 클록 상승 에지가 들어오면 0이 되고, 8비트 범위를 넘으면 0으로 순환합니다. 순차논리의 nonblocking assignment는 같은 에지에서 이전 상태를 기준으로 다음 상태를 계산하게 합니다.

## FSM·파이프라인·메모리

FSM은 상태와 전이 조건을, 파이프라인은 연산을 여러 클록 단계로 나누는 구조를 표현합니다. FIFO는 생산자·소비자의 속도 차이를 흡수합니다. CDC는 서로 다른 클록 도메인 사이의 신호 전달 문제이며 메타안정성과 데이터 일관성을 함께 다룹니다. 고정소수점에서는 비트 폭·부호·소수점 위치·오버플로 처리가 정확도에 영향을 줍니다.

VHDL도 HDL입니다. Chisel·SpinalHDL·Amaranth는 다른 언어 기반으로 하드웨어를 구성하고, HLS는 더 높은 수준의 프로그램에서 하드웨어 구조를 생성합니다.

## 관련 기술

Verilog, SystemVerilog, VHDL, Verilog-A/AMS, Chisel, SpinalHDL, Amaranth, HLS

## 참고 자료

- [Verilator documentation](https://verilator.org/guide/latest/)


## 개념·유도·모델·검증

[기초부터 읽기](../../공학기초_foundations/README.md)

- [FSM과 FIFO: 요청과 실제 전송을 구분하기](해설_notes/FSM과FIFO_synchronous-fifo-invariants.md)

## English

A hardware description language expresses circuit structure and behavior. Multiple circuit blocks operate concurrently. RTL describes data movement between registers through combinational logic, and synthesis maps that description into a logic circuit.

### Combinational and sequential logic

Combinational outputs depend on current inputs. Sequential logic also depends on stored state. SystemVerilog's `always_comb` expresses combinational logic, while `always_ff` expresses flip-flop-based behavior. A combinational block can infer a latch if an output is not assigned on every path.

The counter above uses a synchronous active-low reset. It clears on a rising clock edge when `rst_n` is low and wraps to zero beyond its 8-bit range. Nonblocking assignments calculate next-state values from the pre-edge state.

### Building larger structures

An FSM describes states and transition conditions. Pipelining divides computation into clocked stages, and a FIFO absorbs differences in producer and consumer rates. Clock-domain crossing involves both metastability and data consistency. For fixed-point arithmetic, width, signedness, binary-point position, and overflow handling affect numerical accuracy.

VHDL is another HDL. Chisel, SpinalHDL, and Amaranth build hardware using other host languages, while HLS generates hardware structures from higher-level programs.


### Concepts, derivations, models, and verification

[Foundations reading guide](../../공학기초_foundations/README.md#english)

- [Synchronous FIFO state and invariants](해설_notes/FSM과FIFO_synchronous-fifo-invariants.md#english)


## 심화 해설 | Advanced article

- [고정소수점 곱셈: 비트 폭, 반올림, 포화를 따로 결정하기](해설_notes/고정소수점의경계_fixed-point.md) · [English](해설_notes/고정소수점의경계_fixed-point.md#english)
