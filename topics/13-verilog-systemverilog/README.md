# Verilog · SystemVerilog · RTL

[전체 목차](../../CATALOG.md) · [처음으로](../../README.md)

HDL은 하드웨어의 구조와 동작을 기술하는 언어다. 소프트웨어의 문장 실행과 달리 여러 회로 블록이 동시에 동작한다. RTL은 레지스터와 그 사이의 조합논리로 데이터 이동을 표현하며, 합성 도구는 이를 논리 회로로 변환한다.

## 조합논리와 순차논리

조합논리의 출력은 현재 입력으로 결정된다. 순차논리는 레지스터에 저장된 상태를 함께 사용한다. SystemVerilog의 `always_comb`는 조합논리, `always_ff`는 플립플롭 기반 동작을 명확히 표현한다. 조합 블록에서 출력이 모든 경로에 할당되지 않으면 래치가 추론될 수 있다.

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

이 카운터는 동기식 active-low 리셋을 사용한다. `rst_n`이 낮은 상태에서 클록 상승 에지가 들어오면 0이 되고, 8비트 범위를 넘으면 0으로 순환한다. 순차논리의 nonblocking assignment는 같은 에지에서 이전 상태를 기준으로 다음 상태를 계산하게 한다.

## 구조를 만드는 개념

FSM은 상태와 전이 조건을, 파이프라인은 연산을 여러 클록 단계로 나누는 구조를 표현한다. FIFO는 생산자·소비자의 속도 차이를 흡수한다. CDC는 서로 다른 클록 도메인 사이의 신호 전달 문제이며 메타안정성과 데이터 일관성을 함께 다룬다. 고정소수점에서는 비트 폭·부호·소수점 위치·오버플로 처리가 정확도에 영향을 준다.

VHDL도 HDL이다. Chisel·SpinalHDL·Amaranth는 다른 언어 기반으로 하드웨어를 구성하고, HLS는 더 높은 수준의 프로그램에서 하드웨어 구조를 생성한다.

## 관련 기술

Verilog, SystemVerilog, VHDL, Verilog-A/AMS, Chisel, SpinalHDL, Amaranth, HLS

## 참고 자료

- [Verilator documentation](https://verilator.org/guide/latest/)
