// [처음 읽는 사람을 위한 안내] 이 파일은 Transformer의 수학 연산을 연결하는 보드 계층입니다.
// Python이 prompt 문자를 vocabulary ID로 바꾸고 UART로 보내면, 이 회로가 실제 FPGA 핀과
// 코어 handshake를 구동합니다. 회로는 학습을 수행하지 않고 이미 학습한 Q8.8 가중치를 사용합니다.
// always의 <=는 현재 clock의 이전 값을 읽어 다음 레지스터 값을 예약합니다. 함수 호출 순서를
// CPU처럼 실행하는 코드가 아니라, 클록마다 상태가 바뀌는 실제 회로 연결을 기술합니다.
// 이 코드가 존재한다는 사실과 실제 보드에서 정상 동작했다는 사실은 다릅니다. 보드별 part/XDC,
// timing 통과, bitstream 생성, 실제 USB/UART 연결과 65 개 logit 비교까지 순서대로 확인합니다.
`timescale 1ns/1ps
// -----------------------------------------------------------------------------
// 문자 자체 대신 문자어휘 0..64의 token ID를 받고 65 개의 Q8.8 logits를 반환한다.
// prompt 'RO'의 Python 문자-ID 변환은 [30,27]. 이 바이트를 순서대로 전송한다.
// 각 바이트의 결과를 끝까지 받은 뒤 다음 바이트를 보낸다(stop-and-wait).
// 0xff는 K/V cache/position 초기화 명령이다. 단어 길이/뜻은 FPGA가 해석하지 않는다.
// 결과 frame: 0x47,0x50,status,token_count,word_count,[little-endian int16 logits].
// status 0=성공(65 words),1=reset완료(0 words),e0=잘못된 ID,e2=context가득참.
// board용 최대 context는 8이 다. D16/H4/L2/GELU/affine 및 학습 가중치는 유지된다.
// 이 한정된 context는 원래 32보다 작지만, 입력이 8 개 이하이면 같은 position/weight와
// causal 계산을 사용한다. DDR2/PIM chip/controller는 이 모듈의 기능에 포함되지 않는다.
// -----------------------------------------------------------------------------
// [통신과 Transformer연결] prompt 자체를이 회로가언어로 해석하지 않습니다.
// PC가 문자→token ID 변환을끝내고보내며, 이 FSM이 core를 시작해 vocab65 개점수를되돌려줍니다.
// 그점수를 greedy로고르거나 sampling하는함수는 fpga/nexys4_ddr/host.py의 process/main에 있습니다.
module nexys4_ddr_gpt_uart_bridge #(
    parameter integer CLOCK_HZ=5000000,
    parameter integer BAUD=115200,
    // board에서 는 K/V cache 깊이를 8로줄여저장/선택자원을줄입니다.원래 학습 position표 0~7을 씁니다.
    // 현재 core context한도에 맞춰 host도 prompt길이+생성 문자수-1<=8을 검사해야합니다.
    parameter integer MAX_CONTEXT=8,
    // K/V 저장의 물리 표현만 하위 core로 전달한다. UART packet·token ID·수치값은 바뀌지 않는다.
    // 기본0은 기존 경로이고1은 distributed RAM 추론을 위한 flat memory 경로다.
    parameter integer FLAT_DISTRIBUTED_CACHE=0
) (
    // clk는 CLOCK_HZ와 같은 실제 MMCM core clock입니다(기본5 MHz, 32 저속profile2.5 MHz).
    // reset_n은 동기 해제된 초기화, uart_rx는 PC→FPGA serial 입력입니다.
    input wire clk, input wire reset_n, input wire uart_rx,
    // uart_tx는 FPGA→PC serial출력. status_led[0]=core_ready,[1]=core_busy,[2]=core_valid,[3]=sticky_error입니다.
    // LED는 문자 출력대신제어 상태를관찰하는디버그표시입니다.
    output wire uart_tx, output wire [3:0] status_led
);
    // received는 RX가 복원한명령 byte. raw 0..64는 token ID,255(0xff)는 cache초기화 명령입니다.
    // ASCII R=82를 직접보내면어휘 ID가 아니므로 e0오류입니다.현재 vocab에서 R=30,O=27을 보냅니다.
    wire [7:0] received;
    wire rx_valid, rx_bad;
    nexys4_ddr_uart_rx #(.CLOCK_HZ(CLOCK_HZ),.BAUD(BAUD)) receiver
        (.clk(clk),.reset_n(reset_n),.rx(uart_rx),.data(received),.valid(rx_valid),.framing_error(rx_bad));
    reg tx_start;
    reg [7:0] tx_data;
    wire tx_busy, tx_done;
    nexys4_ddr_uart_tx #(.CLOCK_HZ(CLOCK_HZ),.BAUD(BAUD)) transmitter
        (.clk(clk),.reset_n(reset_n),.start(tx_start),.data(tx_data),.tx(uart_tx),.busy(tx_busy),.done(tx_done));

    // core_start는 새 token계산요청,core_result_ready는 65 개점수를모두 전송한후결과를해제하는 pulse입니다.
    // core_reset_n은 새 prompt의 cache와 position을 비우기위해 core만초기화하는제어입니다.
    reg core_start, core_result_ready, core_reset_n;
    reg [6:0] core_token;
    // 65 개 vocabulary 점수중하나를 읽는주소.7bit면 0~127을 표현하므로 0~64를 충분히담습니다.
    wire [6:0] core_logit_index;
    // core_logit_data는 Q8.8 signed raw 패턴한 word입니다. UART에서 는 부호 변환하지 않고두 byte로나누어보냅니다.
    // PC가 struct.unpack('<h',...)로부호를복원한뒤 256으로 나누면실수 logit입니다.
    wire [15:0] core_logit_data;
    wire core_ready, core_busy, core_done, core_valid, core_error;
    wire [5:0] core_token_count;
    // 코어의 단자는 clock, Q8.8 tensor와 handshake로 구성된다.
    // Python forward_q88_step(model, token_id, cache) 한 번을 start로 지시한다.
    // 현재 KV core의 reset_n은 동기식이다. 아래 reset_count로 여러 상승 클록에 걸쳐 0을 유지한다.
    // UART/bridge 자체의 비동기 reset과 core의 동기식 reset은 각각 해당 모듈의 계약을 따른다.
    gpt_kvcache_rom_board_top #(.MAX_TOKENS(MAX_CONTEXT),
        .FLAT_DISTRIBUTED_CACHE(FLAT_DISTRIBUTED_CACHE)) core
        (.clk(clk),.reset_n(core_reset_n),.start(core_start),.result_ready(core_result_ready),
         .token_id(core_token),.logit_index(core_logit_index),.input_ready(core_ready),
         .busy(core_busy),.done(core_done),.result_valid(core_valid),.error(core_error),
         .token_count(core_token_count),.logit_data(core_logit_data));

    // FSM5 상태:입력기다림→계산기다림→byte준비→UART완료기다림을반복합니다.
    // RESET_WAIT는 core를 몇 clock동안 reset한뒤 5 byte ACK를 보내는별도경로입니다.
    localparam [2:0] IDLE=0, WAIT_CORE=1, SEND_BYTE=2, WAIT_TX=3, RESET_WAIT=4;
    reg [2:0] state;
    reg [1:0] reset_count;
    // reply_status/count/words는 header의 3 개필드. frame_index는 header+payload의 현재 byte번호입니다.
    // 성공시총 135 byte라 8 bit인덱스 0..134가 충분합니다.65 word는 130 byte입니다.
    reg [7:0] reply_status, reply_count, reply_words, frame_index;
    // sticky는 오류가잠깐 pulse여도 LED에기억하기위한 1 bit레지스터입니다.0xff reset명령으로내립니다.
    reg sticky_error;
    // int16은 하위 바이트→상위 바이트 순서다. byte 5,6은 logit0, 7,8은 logit1이 다.
    // frame_index 5/6→index 0,7/8→index 1,...,133/134→index64입니다.
    // >>1은 양의정수 2로나누기이며 low/highbyte2 개가동일한 logit주소를 쓰게합니다.
    assign core_logit_index=(frame_index>=5) ? ((frame_index-5)>>1) : 7'd0;
    assign status_led={sticky_error,core_valid,core_busy,core_ready};
    // 한 clock pulse를 내보내고수신 모듈이 다음 clock에그 pulse를 읽도록 nonblocking대입을씁니다.
    // tx_data와 tx_start는 동시에 예약되므로 transmitter가 start를 읽을 때 새 tx_data도 함께 준비됩니다.
    always @(posedge clk or negedge reset_n) begin
        if(!reset_n) begin
            state<=IDLE; reset_count<=3; core_reset_n<=0;
            core_start<=0; core_result_ready<=0; core_token<=0;
            tx_start<=0; tx_data<=0; reply_status<=0; reply_count<=0;
            reply_words<=0; frame_index<=0; sticky_error<=0;
        end else begin
            // start/result_ready/tx_start는 1cycle pulse이며 긴계산/긴 UART전송의
            // 진행상태는각수신 모듈이 보유한다. nonblocking 할당은다음 clock에 반영된다.
            core_start<=0; core_result_ready<=0; tx_start<=0;
            // core_reset_n은 reset_count가 0이 될 때해제합니다.초기화직후 3clock의 유지시간을둡니다.
            // 배열의논리 유효 길이 token_count를 0으로 돌려이전 prompt의 K/V가 새 prompt로이어지지않게합니다.
            if(reset_count!=0) reset_count<=reset_count-1'b1;
            else core_reset_n<=1;
            if(rx_bad) sticky_error<=1;
            // 입력 FIFO가 없으므로 계산/응답중새입력은수락하지 못합니다.오류 LED를 올립니다.
            // PC는 반드시이번 135 byte응답을끝까지 읽은다음다음 token을 보내야합니다.
            if(rx_valid && state!=IDLE) sticky_error<=1; // host가응답전에다음바이트를보내면놓칠수있다.
            case(state)
                // 명령우선순위:0xff reset→ID범위오류→cache가득참→core_ready일 때정상계산.
                // FF를 ID범위오류보다먼저처리해야 reset명령으로인식됩니다.
                IDLE: if(rx_valid) begin
                    frame_index<=0;
                    if(received==8'hff) begin
                        core_reset_n<=0; reset_count<=3; sticky_error<=0;
                        reply_status<=1; reply_count<=0; reply_words<=0; state<=RESET_WAIT;
                    // 학습 vocab은 0..64만정의됩니다.e0reply는 0word이며토큰수와 cache를 변경하지 않습니다.
                    end else if(received>=65) begin
                        sticky_error<=1; reply_status<=8'he0; reply_count<=core_token_count;
                        reply_words<=0; state<=SEND_BYTE;
                    // context8을 넘으면 e2reply를 반환해메모리 범위 밖쓰기를막습니다.자동 슬라이딩 window기능은없습니다.
                    end else if(core_token_count>=MAX_CONTEXT) begin
                        sticky_error<=1; reply_status<=8'he2; reply_count<=core_token_count;
                        reply_words<=0; state<=SEND_BYTE;
                    end else if(core_ready) begin
                        core_token<=received[6:0]; core_start<=1; state<=WAIT_CORE;
                    end
                end
                RESET_WAIT: if(reset_count==0) state<=SEND_BYTE;
                // core_valid가 1이면 65개 logit 계산이 완료된 상태입니다. result_ready가 아직0이므로 값이 고정되어 읽을 수 있습니다.
                // core_error는 계산시작이거절되었다는신호이며 logitpayload없이오류 header만보냅니다.
                WAIT_CORE: begin
                    if(core_valid) begin
                        reply_status<=0; reply_count<=core_token_count;
                        reply_words<=65; frame_index<=0; state<=SEND_BYTE;
                    end else if(core_error) begin
                        sticky_error<=1; reply_status<=8'he0; reply_count<=core_token_count;
                        reply_words<=0; frame_index<=0; state<=SEND_BYTE;
                    end
                end
                // 아직전송 중인 byte가 없을때현재 header/payloadbyte를 선택합니다.
                // header의 0x47/0x50은 ASCII GP이며 PC parser가 packet시작/오연결을 검사하는표식입니다.
                SEND_BYTE: if(!tx_busy) begin
                    case(frame_index)
                        0:tx_data<=8'h47;
                        1:tx_data<=8'h50;
                        2:tx_data<=reply_status;
                        3:tx_data<=reply_count;
                        4:tx_data<=reply_words;
                        // payload는 little-endian. frame_index-5의 LSB0이면 logit[7:0],1이면 logit[15:8]입니다.
                        // 음수 raw-128=0xff80도 그대로 80,ff로보내고 PC가 signed로 해석합니다.
                        default: tx_data<=((frame_index-5)&1) ? core_logit_data[15:8] : core_logit_data[7:0];
                    endcase
                    tx_start<=1; state<=WAIT_TX;
                end
                // tx_done이 올라야현재 byte의 stop bit시간까지전송된것입니다.그전에는 frame_index를 바꾸지않습니다.
                WAIT_TX: if(tx_done) begin
                    // word 65이면 마지막 byteindex 134,word 0이면 마지막 headerindex 4입니다.
                    // 5 byteheader의 index는 0..4이므로 4+2*words를 마지막 주소로사용합니다.
                    if(frame_index==4+2*reply_words) begin
                        // 마지막바이트를 PC로 내보낸후에만출력을해제해 65 개 logits가 고정된다.
                        if(reply_words!=0) core_result_ready<=1;
                        state<=IDLE;
                    end else begin frame_index<=frame_index+1'b1; state<=SEND_BYTE; end
                end
                default: state<=IDLE;
            endcase
        end
    end
endmodule
