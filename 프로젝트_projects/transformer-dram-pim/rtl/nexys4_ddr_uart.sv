// [처음 읽는 사람을 위한 안내] 이 파일은 Transformer의 수학 연산을 연결하는 보드 계층입니다.
// Python이 prompt 문자를 vocabulary ID로 바꾸고 UART로 보내면, 이 회로가 실제 FPGA 핀과
// 코어 handshake를 구동합니다. 회로는 학습을 수행하지 않고 이미 학습한 Q8.8 가중치를 사용합니다.
// always의 <=는 현재 clock의 이전 값을 읽어 다음 레지스터 값을 예약합니다. 함수 호출 순서를
// CPU처럼 실행하는 코드가 아니라, 클록마다 상태가 바뀌는 실제 회로 연결을 기술합니다.
// 이 코드가 존재한다는 사실과 실제 보드에서 정상 동작했다는 사실은 다릅니다. 보드별 part/XDC,
// timing 통과, bitstream 생성, 실제 USB/UART 연결과 65 개 logit 비교까지 순서대로 확인합니다.
`timescale 1ns/1ps
// -----------------------------------------------------------------------------
// PC와 FPGA가 8-bit 한 바이트씩 주고받는 UART(8 data, no parity, 1 stop bit).
// Transformer 연산 모듈이 아니라 token ID와 결과 정수를 운반하는 통신 회로다.
// Python에서 는 serial.Serial(...).write(bytes([token_id])) / read(n)에 대응한다.
// 5 MHz에서 BAUD115200의 정수 분주값은 43, 실제 baud는 116279로 약 0.94% 높다.
// PC/보드 양쪽 오차의 합이 허용범위인지 실제 장비 시험에서 확인해야 한다.
// -----------------------------------------------------------------------------
// [UART 수신기] 8N1 serial line에서 한 byte를 복원합니다. Transformer의 token 계산을 하지 않습니다.
// PC의 pyserial.write는 byte를 전송하고 이 receiver가 byte의 8 개 data bit를 다시 모읍니다.
// valid는 한 clock pulse이며 data는 다음 성공 byte가 들어올 때까지 보존됩니다.
module nexys4_ddr_uart_rx #(
    // CLOCK_HZ는 실제 입력 clock의 Hz입니다. parameter만 바꾸어 실제 보드 clock을 바꿀 수는 없습니다.
    // 최상위 MMCM 출력과 이 값이 같아야 UART bit 길이가 올바르게 생성됩니다.
    parameter integer CLOCK_HZ=5000000,
    // BAUD는 PC와 맞출 목표 bit/s입니다. 정수 DIVISOR 때문에 정확한 baud와 작은 오차가 있습니다.
    parameter integer BAUD=115200
) (
    // clk는 5 MHz 수신 sampling clock, reset_n은 0에서 초기화, rx는 PC에서 들어오는 비동기 UART 선입니다.
    // rx는 무신호 상태가 1이며 start0을 보고 수신을 시작합니다. 매 bit를 clock 중앙 근처에서 읽습니다.
    input wire clk, input wire reset_n, input wire rx,
    // data는 복원된 8 bit byte, valid는 정상 stop bit를 확인한 1 clock pulse입니다.
    // framing_error는 stop이 0일 때의 1 clock error pulse이며 상위 bridge가 sticky LED에 보존합니다.
    output reg [7:0] data, output reg valid, output reg framing_error
);
    // 5,000,000/115,200을 정수 나눗셈하면 43입니다. 한 bit가 43 clock=8.6us입니다.
    // COUNTER_BITS는 0~42 countdown을 보관할 최소 bit 폭이며 현재 6 비트입니다.
    localparam integer DIVISOR=CLOCK_HZ/BAUD;
    localparam integer COUNTER_BITS=$clog2(DIVISOR+1);
    // 상태 번호는유휴→start 중앙 확인→8 bit 모으기→stop 확인을 구분합니다.
    // state 2 bit, bit_index 3 bit는 각각 4 상태와 8 개의 data bit 주소를 표현합니다.
    localparam [1:0] IDLE=0, START=1, DATA=2, STOP=3;
    reg [1:0] state;
    reg [COUNTER_BITS-1:0] counter;
    reg [2:0] bit_index;
    reg [7:0] shift;
    // UART 신호는 FPGA clock에 맞춰 도착하지 않는다. 두 FF를 거쳐 메타안정성
    // 전파 확률을 낮춘 뒤 샘플한다. 두 FF가 메타안정성을 수학적으로 없애지는 않는다.
    // ASYNC_REG는 Vivado에 이 2 개 FF가 비동기 신호 동기화기임을 알려 배치/해석을 돕는 속성입니다.
    // rx_meta가 raw 입력을받고 다음 clock에 rx_sync가 받습니다. 이후 FSM은 rx_sync만 읽습니다.
    (* ASYNC_REG="TRUE" *) reg rx_meta, rx_sync;
    always @(posedge clk or negedge reset_n) begin
        if (!reset_n) begin rx_meta<=1'b1; rx_sync<=1'b1; end
        else begin rx_meta<=rx; rx_sync<=rx_meta; end
    end
    // 아래 FSM은 매 clock counter를 줄이고 0일 때만 다음 bit를 샘플합니다.
    // 초기화 후 valid/framing_error를 매 clock 0으로 내리고 정상/실패 경계에서만 1로 덮어 pulse를 만듭니다.
    always @(posedge clk or negedge reset_n) begin
        if (!reset_n) begin
            state<=IDLE; counter<=0; bit_index<=0; shift<=0;
            data<=0; valid<=0; framing_error<=0;
        end else begin
            valid<=0; framing_error<=0;
            case(state)
                // start 하강을 보면반 bit 지점까지 기다립니다. 짧은 잡음이 0으로 보였더라도 START의 재검사에서 1이면 취소합니다.
                IDLE: if (!rx_sync) begin counter<=DIVISOR/2-1; state<=START; end
                // start bit 중간에서 여전히 0인지 확인해 짧은 잡음 펄스를 거른다.
                START: if(counter!=0) counter<=counter-1'b1;
                       else if(rx_sync) state<=IDLE;
                       else begin counter<=DIVISOR-1; bit_index<=0; state<=DATA; end
                // bit_index 0부터 7까지 순서대로 저장합니다. 입력은 LSB-first이므로 bit 순서를 뒤집지 않습니다.
                // 마지막 data bit 저장 뒤 STOP을 1 bit 후 확인합니다. shift와 data의 갱신은서로 다른 clock입니다.
                DATA: if(counter!=0) counter<=counter-1'b1;
                      else begin
                          // UART의 첫 data bit는 최하위 비트(bit0)다.
                          shift[bit_index]<=rx_sync; counter<=DIVISOR-1;
                          if(bit_index==7) state<=STOP; else bit_index<=bit_index+1'b1;
                      end
                STOP: if(counter!=0) counter<=counter-1'b1;
                      else begin
                          // stop bit1이 확인된 바이트만 소비자에게 1cycle valid로 알린다.
                          if(rx_sync) begin data<=shift; valid<=1; end
                          else framing_error<=1;
                          state<=IDLE;
                      end
                default: state<=IDLE;
            endcase
        end
    end
endmodule

// [UART 송신기] Python struct.pack으로 만든 응답 byte 하나를 serial 8N1 frame으로 바꿉니다.
// Transformer 계산 완료 core_done과 UART 한 byte 완료 done은 다른 신호입니다.
// start는 busy0일 때만 받고, 전송 중 data가 바뀌어도처음 받은 frame을 끝까지보냅니다.
module nexys4_ddr_uart_tx #(
    parameter integer CLOCK_HZ=5000000,
    parameter integer BAUD=115200
) (
    // clk/reset_n은 수신기와 같은 clock/domain. start1 clock pulse와 data를 함께제시합니다.
    // 상위 bridge는 tx_busy0을 확인하고 시작한뒤 tx_done을 기다리는 stop-and-wait를 사용합니다.
    input wire clk, input wire reset_n, input wire start, input wire [7:0] data,
    // tx는 PC로가는출력 선, busy는 10 bit frame전송 중, done은 마지막 stop 시간 완료 후 1 clock pulse입니다.
    output wire tx, output reg busy, output reg done
);
    localparam integer DIVISOR=CLOCK_HZ/BAUD;
    localparam integer COUNTER_BITS=$clog2(DIVISOR+1);
    reg [COUNTER_BITS-1:0] counter;
    reg [3:0] bit_index;
    // frame 10 bit=stop1+data8+start1. {1'b1,data,1'b0} 연결에서 start가 최하위 bit0입니다.
    // bit_index는 0~9를 차례로 지정하며총 clock은 대략 10*DIVISOR입니다.
    reg [9:0] frame;
    // 유휴 선은 1이 다. frame bit0부터 start0,data[0..7],stop1을 차례로 내보낸다.
    // 조합 mux는 현재 frame bit를 wire로내보냅니다. busy0일 때 1을 내보내야 PC가 새 start0을 구분합니다.
    assign tx=busy ? frame[bit_index] : 1'b1;
    always @(posedge clk or negedge reset_n) begin
        if(!reset_n) begin counter<=0; bit_index<=0; frame<=10'h3ff; busy<=0; done<=0; end
        else begin
            done<=0;
            // 유휴 clock에서 만 start를 받아 frame을 저장합니다. 기존 frame을 중간에 덮어쓰지않도록 busy로차단합니다.
            if(!busy) begin
                if(start) begin frame<={1'b1,data,1'b0}; counter<=DIVISOR-1; bit_index<=0; busy<=1; end
            end else if(counter!=0) counter<=counter-1'b1;
            // bit9는 stop1입니다. 그 43clock이 끝난 후 busy를 내리고 done pulse를 만들어 bridge가 다음 byte를 보낼수있게합니다.
            else if(bit_index==9) begin busy<=0; done<=1; end
            else begin counter<=DIVISOR-1; bit_index<=bit_index+1'b1; end
        end
    end
endmodule
