// [처음 읽는 사람을 위한 안내] 이 파일은 Transformer의 수학 연산을 연결하는 보드 계층입니다.
// Python이 prompt 문자를 vocabulary ID로 바꾸고 UART로 보내면, 이 회로가 실제 FPGA 핀과
// 코어 handshake를 구동합니다. 회로는 학습을 수행하지 않고 이미 학습한 Q8.8 가중치를 사용합니다.
// always의 <=는 현재 clock의 이전 값을 읽어 다음 레지스터 값을 예약합니다. 함수 호출 순서를
// CPU처럼 실행하는 코드가 아니라, 클록마다 상태가 바뀌는 실제 회로 연결을 기술합니다.
// 이 코드가 존재한다는 사실과 실제 보드에서 정상 동작했다는 사실은 다릅니다. 보드별 part/XDC,
// timing 통과, bitstream 생성, 실제 USB/UART 연결과 65 개 logit 비교까지 순서대로 확인합니다.
`timescale 1ns/1ps
// Nexys 4 DDR의 100 MHz oscillator를 실제 MMCM/BUFG로 5 MHz 또는2.5 MHz core clock으로 변환한다.
// RTL에 #delay를 쓰는시뮬레이션 clock과 달리, 아래 primitive는 칩의전용 clock회로다.
// 느린 clock은 현재긴 조합 PU의 setup여유를늘린다. 실제통과여부는 route후 timing으로 판정한다.
// VCO600 MHz에서 기본은CLKOUT0 /120=5 MHz, 저속은내부CLKOUT6 /120→CLKOUT4 /2=2.5 MHz다.
// 7-series의단일출력분주최대값128을넘는240을CLKOUT0에직접넣지않고정식cascade기능을쓴다.
// [물리보드최상위] 이 module의 port이 름을 XDC의 핀 번호/전압표준과정확히연결합니다.
// FPGA target part과 보드오실레이터가맞아야합성결과를실제 칩에올릴수있습니다.
// 이 top은 DDR2 controller나 DRAM내 PIM을 만들지않고 UART로작은 Transformer결과를 검증합니다.
module nexys4_ddr_gpt_top #(
    // 검증된 기본 보드 경로는8이다. 더 큰 cache의 자원/timing은 별도 빌드로 검증해야 한다.
    parameter integer MAX_CONTEXT=8,
    // 새 K/V 저장 형태를 선택하는 합성 옵션이다. 기본0은 기존 검증된 보드 경로를 유지한다.
    // 1의 RAM mapping·자원·timing은 해당 configuration의 Vivado 결과로 따로 판정한다.
    parameter integer FLAT_DISTRIBUTED_CACHE=0,
    // 실제 MMCM 생성과UART 설정에함께사용하는compile-time 값이다. XDC의숫자만바꾸는옵션이아니다.
    // 기존8-token 기본은5 MHz/200 ns, 큰32-token경로의저속설정은2.5 MHz/400 ns다.
    // 지원하는주파수는5000000과2500000이다. 빌드Tcl/PowerShell에서도이범위를검사한다.
    parameter integer CORE_CLOCK_HZ=5000000,
    // 2.5 MHz/57600과5 MHz/115200은정수UART divider43을공유한다.
    // 따라서저속설정에서도동일한43 clock/bit제어를유지하고실제bit시간만두배로늘린다.
    // PC host도이baud와같게설정해야한다. 다른명시값은해당baud오차와UART시험으로따로검증한다.
    parameter integer HOST_BAUD=(CORE_CLOCK_HZ==2500000) ? 57600 : 115200
) (
    // CLK100MHZ=보드 100 MHz oscillator입력,CPU_RESETN=0에서 누르는 reset,UART_TXD_IN=PC TX→FPGA RX입니다.
    // UART TXD라는보드신호이름은 USB-UART 쪽의송신을기준으로하므로 FPGA수신 모듈에연결됩니다.
    input wire CLK100MHZ, input wire CPU_RESETN, input wire UART_TXD_IN,
    // UART_RXD_OUT=FPGA TX→PC RX입니다. LED4 개는 core ready/busy/valid/error상태를보여줍니다.
    output wire UART_RXD_OUT, output wire [3:0] LED
);
    localparam integer USE_CLOCK_CASCADE=(CORE_CLOCK_HZ==2500000);
    wire clk100, clock_feedback, clock_feedback_buffered;
    wire clock5_unbuffered, clock2p5_unbuffered, core_clock, locked;
    // IBUF는 외부 clock 핀의전기 신호를칩 내부신호로받는 vendor primitive입니다. Python산술함수가아닙니다.
    IBUF input_clock_buffer(.I(CLK100MHZ),.O(clk100));
    // MMCM은 Xilinx7-series의전용clock생성회로이며두설정모두VCO600 MHz를유지합니다.
    // cascade=TRUE이면CLKOUT6 counter의출력을CLKOUT4 counter에내부연결합니다.
    // 외부RTL에서두출력선을연결하는것이아닙니다. 최종2.5 MHz는CLKOUT4단자에서나옵니다.
    // CLKIN1_PERIOD10 ns는입력100 MHz정보입니다. CORE_CLOCK_HZ에따라실제분주회로를선택합니다.
    // 합성시고정된선택으로5 MHz/200 ns 또는2.5 MHz/400 ns를만들며route후STA로실제통과를확인합니다.
    MMCME2_BASE #(
        .BANDWIDTH("OPTIMIZED"),.CLKIN1_PERIOD(10.0),.DIVCLK_DIVIDE(1),
        .CLKFBOUT_MULT_F(6.0),.CLKOUT0_DIVIDE_F(120.0),
        .CLKOUT4_CASCADE(USE_CLOCK_CASCADE ? "TRUE" : "FALSE"),
        .CLKOUT6_DIVIDE(USE_CLOCK_CASCADE ? 120 : 1),
        .CLKOUT4_DIVIDE(USE_CLOCK_CASCADE ? 2 : 1),
        .CLKOUT6_DUTY_CYCLE(0.5),.CLKOUT4_DUTY_CYCLE(0.5),.STARTUP_WAIT("FALSE")
    ) clock_generator (
        .CLKIN1(clk100),.CLKFBIN(clock_feedback_buffered),.RST(!CPU_RESETN),.PWRDWN(1'b0),
        .CLKFBOUT(clock_feedback),.CLKFBOUTB(),.CLKOUT0(clock5_unbuffered),.CLKOUT0B(),
        .CLKOUT1(),.CLKOUT1B(),.CLKOUT2(),.CLKOUT2B(),.CLKOUT3(),.CLKOUT3B(),
        .CLKOUT4(clock2p5_unbuffered),.CLKOUT5(),.CLKOUT6(),.LOCKED(locked)
    );
    // feedback BUFG는 MMCM자기출력을 입력기준에 맞춰피드백하고출력 BUFG는 core전체에 clock을 배포합니다.
    // 일반 LUT나긴신호선으로 clock을 배포하면 skew/글리치문제가생길 수 있어전용 clock망을 사용합니다.
    BUFG feedback_buffer(.I(clock_feedback),.O(clock_feedback_buffered));
    // USE_CLOCK_CASCADE는parameter로정해진상수이므로합성후에는선택한한쪽연결만남습니다.
    // 실행중두clock을바꾸는LUT mux가아닙니다. clock은BUFG로회로전체에배포합니다.
    // clock_generator/core_clock_buffer instance명은기존DCP와대응확인에쓰므로유지합니다.
    BUFG core_clock_buffer(.I(USE_CLOCK_CASCADE ? clock2p5_unbuffered : clock5_unbuffered),.O(core_clock));
    // MMCM이 안정되기전에는계산을시작하지 않는다. reset은 비동기 assert/동기 deassert.
    // reset assert는버튼또는locked저하에즉시반응하고,release는선택한실제core clock두edge에동기화합니다.
    // 첫 clock은 reset_sync01,다음 clock은 11이 되어두 번째 bit가 1로풀립니다.
    // reset이 clock edge근처에풀려레지스터별로다른시점에시작하는위험을줄입니다.
    (* ASYNC_REG="TRUE" *) reg [1:0] reset_sync;
    // CPU_RESETN1과 MMCM locked1이 모두만족해야해제준비가됩니다. locked0이면 계산 중에도 reset됩니다.
    wire clock_reset_n=CPU_RESETN && locked;
    always @(posedge core_clock or negedge clock_reset_n)
        if(!clock_reset_n) reset_sync<=0;
        else reset_sync<={reset_sync[0],1'b1};
    // MMCM/reset계층뒤의모든bridge/UART/Transformer연산은동일한core_clock domain에서진행합니다.
    // UART는하드웨어clock자체를만들지않습니다. .CLOCK_HZ로실제주파수를알고bit길이를계산합니다.
    // 원래32 position표 중 MAX_CONTEXT개를 사용한다. PC host에도 같은 한도를 지정해야 한다.
    nexys4_ddr_gpt_uart_bridge #(.CLOCK_HZ(CORE_CLOCK_HZ),.BAUD(HOST_BAUD),.MAX_CONTEXT(MAX_CONTEXT),
        .FLAT_DISTRIBUTED_CACHE(FLAT_DISTRIBUTED_CACHE)) bridge
        (.clk(core_clock),.reset_n(reset_sync[1]),.uart_rx(UART_TXD_IN),
         .uart_tx(UART_RXD_OUT),.status_led(LED));
endmodule
