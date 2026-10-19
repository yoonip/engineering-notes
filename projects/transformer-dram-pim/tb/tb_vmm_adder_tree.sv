// [코드 읽기 안내] 이 파일의 16 비트 원소는 signed Q8.8 raw 값입니다.
// raw/256이 실제 수입니다. 256→1.0, -128→-0.5이며 범위는 -128~127.99609375입니다.
// *_flat은 여러 원소를 한 긴 비트벡터에 포장한 것입니다. i*16 +:16은 i번째 원소이며
// Python list[i]에 대응합니다. 비트 조각은 signed 속성을 잃을 수 있어 $signed로 해석합니다.
// function은 Python 함수처럼 읽을 수 있지만 합성 시 조합 회로가 됩니다. 함수 호출을
// 여러 번 쓰면 회로가 복제될 수도 있습니다. automatic은 호출별 임시 변수 공간을 뜻합니다.
// always @*의 blocking 대입(=)은 현재 입력에서 바로 결과를 만드는 조합 연산을 기술합니다.
// posedge 블록의 nonblocking 대입(<=)은 다음 레지스터 값을 예약합니다. 모든 우변은
// 그 클록 직전 상태를 기준으로 읽습니다. Python 순차 대입과 다른 가장 중요한 부분입니다.
// for/generate의 고정 반복은 합성할 때 회로를 펼치는 표현입니다. 시뮬레이터에서 반복문이
// 끝났다고 FPGA의 물리 지연이 0인 것은 아닙니다. 실제 경로 지연은 Vivado timing으로 봅니다.
// `timescale 1 ns/1ps는 시뮬레이션 시간 단위/해상도이며 FPGA 클록 주파수를 설정하지 않습니다.
`timescale 1ns/1ps

// VMM 안에 들어간 balanced adder tree의 단독 검증용 테스트벤치다.
// K=3으로 설정해 실제 3 개 곱과 0으로 채운 한 잎을 함께 확인한다.
// [테스트벤치 읽기] 이 파일은 FPGA에 내려갈 회로가 아니라 RTL 시뮬레이터를 구동하는 검사 프로그램입니다.
// Python run_tests.py가 iverilog로컴파일한 뒤 vvp로실행하고 출력값을 Python 정수 기준과비교합니다.
// initial은 시뮬레이션 0시점에한번실행합니다. #1은 1 ns 시뮬레이션대기이고물리딜레이소자가아닙니다.
// @(posedge/negedge clk)는시뮬레이션에서해당 edge까지기다립니다. always #5는 10 ns 테스트 클록을만듭니다.
// 이클록에서시뮬레이션통과해도 FPGA 배선 지연은별도로모델링되지 않으므로 Vivado timing 통과를뜻하지 않습니다.
// ===/!==는 0/1뿐아니라 X(미정)/Z(고임피던스)도비교해미초기화신호를검출합니다.
// $fatal은 실패하면즉시종료하는 assert 역할,$display/$write는 자동검증이읽는텍스트출력입니다.
// 정답출력이존재한다는확인과학습언어모델의문장 품질은다른검증입니다.이 bench는 기능/제어/산술규칙을 확인합니다.
module tb_vmm_adder_tree;
    // 3 항내적은 PAD_K4가 되어한잎이 0입니다.2의 거듭제곱전용구조가아닌지확인하는작은 case입니다.
    localparam integer K = 3;

    // activation/weight는 각 3 개의 Q8.8 숫자,출력은하나의 dot product입니다.
    // Python qmat([[256,512,-768]],[[128],[384],[256]])[0][0]에해당합니다.
    reg  [K*16-1:0] activation_flat;
    reg  [K*16-1:0] weight_flat;
    wire [15:0] result_flat;

    dram_pim_vmm_bank #(.ROWS(1), .K(K), .COLS(1)) dut (
        .activation_flat(activation_flat),
        .weight_flat(weight_flat),
        .result_flat(result_flat)
    );

    // 0초기화→정상 3 항 sum→큰항상쇄→양수포화순서로위험수치조건을 확인합니다.
    // 정확한기대값을손으로 계산할 수 있어임의의출력만 확인하는테스트보다버그원인을쉽게찾습니다.
    initial begin
        activation_flat = 0;
        weight_flat = 0;
        #1;

        // 1.0*0.5 + 2.0*1.5 + (-3.0)*1.0 = 0.5
        // Q8.8에서 1.0=256, 0.5=128이므로 기대 출력은 128이 다.
        activation_flat[0*16 +: 16] = 16'sd256;
        activation_flat[1*16 +: 16] = 16'sd512;
        activation_flat[2*16 +: 16] = -16'sd768;
        weight_flat[0*16 +: 16] = 16'sd128;
        weight_flat[1*16 +: 16] = 16'sd384;
        weight_flat[2*16 +: 16] = 16'sd256;
        #1;
        // 기대 raw 128=0.5.과정을펼치면 32768+196608-196608=32768,>>>8=128입니다.
        if ($signed(result_flat) !== 16'sd128)
            $fatal(1, "3-term adder tree mismatch: expected 128, got %0d", $signed(result_flat));

        // 두 큰 곱이 정확히 상쇄되고 작은 값 하나가 남는 경우다.
        // 왼쪽/오른쪽 트리 부분합 중 한쪽이 커도 내부 폭이 충분해야 1.0이 보존된다.
        activation_flat[0*16 +: 16] = 16'sd25600; // 100.0
        activation_flat[1*16 +: 16] = -16'sd25600;
        activation_flat[2*16 +: 16] = 16'sd256;
        weight_flat[0*16 +: 16] = 16'sd25600;
        weight_flat[1*16 +: 16] = 16'sd25600;
        weight_flat[2*16 +: 16] = 16'sd256;
        #1;
        // 100*100-100*100+1*1=1.0. 각곱을 16 bit로미리포화했으면상쇄와작은잔여값이왜곡될 수 있습니다.
        if ($signed(result_flat) !== 16'sd256)
            $fatal(1, "wide cancellation mismatch: expected 256, got %0d", $signed(result_flat));

        // 출력 표현 범위를 넘는 합은 wrap-around 대신 양의 최대값으로 포화한다.
        activation_flat[0*16 +: 16] = 16'sd32767;
        activation_flat[1*16 +: 16] = 16'sd32767;
        activation_flat[2*16 +: 16] = 16'sd0;
        weight_flat[0*16 +: 16] = 16'sd32767;
        weight_flat[1*16 +: 16] = 16'sd32767;
        weight_flat[2*16 +: 16] = 16'sd0;
        #1;
        // 최대 raw 32767을 넘는양수합은최대 표현값으로포화.음수로 wrap되는잘못된구현을잡습니다.
        if ($signed(result_flat) !== 16'sd32767)
            $fatal(1, "positive saturation mismatch: got %0d", $signed(result_flat));

        $display("PASS: balanced Q8.8 VMM adder tree, odd K padding, cancellation, saturation");
        $finish;
    end
endmodule
