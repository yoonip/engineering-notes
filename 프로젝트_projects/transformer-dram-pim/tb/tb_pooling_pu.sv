`timescale 1ns/1ps
// =============================================================================
// Pooling의 조합 산술과 등록 wrapper 프로토콜을 한 설정씩 실제 RTL로 검증한다.
// Python verify_pooling_pu.py가 signed raw 기준과 schedule/mem을 생성한다.
// max/avg·mask·sum/count·packed lane·1clock latency·bubble·동기 reset을 검사한다.
// clock 200ns는 TB의 관찰 간격이다. 지연 없는 Icarus RTL 기능 시험이므로
// 5MHz FPGA timing 통과, SDF, DRAM-PIM 실물 측정이라고 주장하지 않는다.
// =============================================================================
module tb_pooling_pu #(
    parameter integer WINDOW = 16,
    parameter integer VECTORS = 64,
    parameter integer CYCLES = 128
);
    localparam integer COUNT_WIDTH = $clog2(WINDOW+1);
    localparam integer SUM_WIDTH = 16+$clog2(WINDOW);
    reg [WINDOW*16-1:0] values_mem [0:VECTORS-1];
    reg [WINDOW-1:0] masks_mem [0:VECTORS-1];
    reg operations_mem [0:VECTORS-1];
    reg [15:0] expected_mem [0:VECTORS-1];
    reg [COUNT_WIDTH-1:0] counts_mem [0:VECTORS-1];
    reg [SUM_WIDTH-1:0] sums_mem [0:VECTORS-1];
    reg [1:0] controls_mem [0:CYCLES-1];
    reg [31:0] indices_mem [0:CYCLES-1];

    reg [WINDOW*16-1:0] comb_values = 0;
    reg [WINDOW-1:0] comb_mask = 0;
    reg comb_operation = 0;
    wire signed [15:0] comb_result;
    wire [COUNT_WIDTH-1:0] comb_count;
    dram_pim_pooling_pu #(.WINDOW(WINDOW)) comb_dut (
        .values_packed(comb_values), .valid_mask(comb_mask), .operation_avg(comb_operation),
        .result(comb_result), .valid_count(comb_count)
    );

    reg clk = 0;
    reg reset_n = 0;
    reg input_valid = 0;
    reg [WINDOW*16-1:0] registered_values = 0;
    reg [WINDOW-1:0] registered_mask = 0;
    reg registered_operation = 0;
    wire signed [15:0] registered_result;
    wire [COUNT_WIDTH-1:0] registered_count;
    wire output_valid;
    dram_pim_pooling_registered_top #(.WINDOW(WINDOW)) registered_dut (
        .clk(clk), .reset_n(reset_n), .input_valid(input_valid),
        .values_packed(registered_values), .valid_mask(registered_mask),
        .operation_avg(registered_operation), .result(registered_result),
        .valid_count(registered_count), .output_valid(output_valid)
    );
    always #100 clk = ~clk;

    integer vector_index;
    integer cycle;
    integer lane;
    integer current_index;
    integer comb_checks = 0;
    integer exact = 0;
    integer accepted = 0;
    integer cancelled = 0;
    integer resets = 0;
    integer valid_checks = 0;
    integer packed_checks = 0;
    integer synchronous_checks = 0;
    integer burst = 0;
    integer maximum_burst = 0;
    reg pending_valid = 0;
    reg [15:0] pending_word = 0;
    reg [COUNT_WIDTH-1:0] pending_count = 0;
    reg [15:0] before_word;
    reg [COUNT_WIDTH-1:0] before_count;
    reg before_valid;

    initial begin
        $readmemh("values.mem", values_mem);
        $readmemh("masks.mem", masks_mem);
        $readmemh("operations.mem", operations_mem);
        $readmemh("expected.mem", expected_mem);
        $readmemh("counts.mem", counts_mem);
        $readmemh("sums.mem", sums_mem);
        $readmemh("controls.mem", controls_mem);
        $readmemh("indices.mem", indices_mem);

        // 먼저 모든 벡터의 조합 출력과 넓은 tree root 합을 검사한다.
        // 결과만 보면 max 연산에서 sum overflow가 드러나지 않을 수 있으므로
        // count/root sum도 Python의 넓은 정수 합과 독립적으로 비교한다.
        for (vector_index=0; vector_index<VECTORS; vector_index=vector_index+1) begin
            comb_values = values_mem[vector_index];
            comb_mask = masks_mem[vector_index];
            comb_operation = operations_mem[vector_index];
            #1;
            if (comb_result !== expected_mem[vector_index] || comb_count !== counts_mem[vector_index])
                $fatal(1,"pool mismatch window=%0d vector=%0d op=%0d got=%h expected=%h count=%0d expected_count=%0d",
                       WINDOW, vector_index, comb_operation, comb_result,
                       expected_mem[vector_index], comb_count, counts_mem[vector_index]);
            if (comb_dut.sum_tree[1] !== sums_mem[vector_index])
                $fatal(1,"wide sum mismatch vector=%0d got=%h expected=%h",
                       vector_index, comb_dut.sum_tree[1], sums_mem[vector_index]);
            comb_checks = comb_checks+1;
            $display("CHECK_POOL vector=%0d op=%0d count=%0d result=%h sum=%0d",
                     vector_index, comb_operation, comb_count, comb_result, $signed(comb_dut.sum_tree[1]));
        end

        // controls[1]=reset_n, controls[0]=input_valid다. 각 cycle의 입력은
        // indices.mem이 지정한 벡터이고 직전 accepted 입력이 이번 출력이다.
        for (cycle=0; cycle<CYCLES; cycle=cycle+1) begin
            @(negedge clk);
            before_word = registered_result;
            before_count = registered_count;
            before_valid = output_valid;
            reset_n = controls_mem[cycle][1];
            input_valid = controls_mem[cycle][0];
            current_index = indices_mem[cycle];
            registered_values = values_mem[current_index];
            registered_mask = masks_mem[current_index];
            registered_operation = operations_mem[current_index];
            #1;
            // falling edge에 reset을 낮춰도 출력이 즉시 바뀌면 안 된다.
            if (registered_result !== before_word || registered_count !== before_count || output_valid !== before_valid)
                $fatal(1,"pooling synchronous contract changed before edge cycle=%0d",cycle);
            synchronous_checks = synchronous_checks+1;
            @(posedge clk); #1;
            if (!reset_n) begin
                if (registered_result !== 16'h0000 || registered_count !== 0 || output_valid !== 0)
                    $fatal(1,"pooling reset output failed cycle=%0d",cycle);
                if (registered_dut.values_registered !== 0 || registered_dut.mask_registered !== 0 ||
                    registered_dut.operation_registered !== 0 || registered_dut.registered_valid !== 0)
                    $fatal(1,"pooling reset input registers failed cycle=%0d",cycle);
                if (pending_valid) cancelled = cancelled+1;
                pending_valid = 0;
                resets = resets+1;
                burst = 0;
            end else begin
                if (output_valid !== pending_valid)
                    $fatal(1,"pooling one-clock valid failed cycle=%0d",cycle);
                if (pending_valid) begin
                    if (registered_result !== pending_word || registered_count !== pending_count)
                        $fatal(1,"registered pooling mismatch cycle=%0d got=%h wanted=%h",cycle,registered_result,pending_word);
                    exact = exact+1;
                end else if (registered_result !== 0 || registered_count !== 0)
                    $fatal(1,"invalid output must be zero cycle=%0d",cycle);
                if (input_valid) begin
                    // lane 순서를 함께 뒤집어도 max/sum은 같을 수 있으므로
                    // 최종 결과만으로 endian을 증명하지 않고 각 register도 검사한다.
                    for (lane=0; lane<WINDOW; lane=lane+1) begin
                        if (registered_dut.values_registered[16*lane +: 16] !== registered_values[16*lane +: 16])
                            $fatal(1,"packed pooling lane mismatch cycle=%0d lane=%0d",cycle,lane);
                        packed_checks = packed_checks+1;
                    end
                    if (registered_dut.mask_registered !== registered_mask ||
                        registered_dut.operation_registered !== registered_operation)
                        $fatal(1,"registered mask/op mismatch cycle=%0d",cycle);
                    packed_checks = packed_checks+2;
                    accepted = accepted+1;
                    pending_word = expected_mem[current_index];
                    pending_count = counts_mem[current_index];
                    burst = burst+1;
                    if (burst>maximum_burst) maximum_burst = burst;
                end else burst = 0;
                pending_valid = input_valid;
            end
            valid_checks = valid_checks+1;
            $display("CHECK_POOL_REG cycle=%0d valid=%0d result=%h count=%0d exact=%0d",
                     cycle,output_valid,registered_result,registered_count,exact);
        end
        if (pending_valid) $fatal(1,"unflushed pooling input");
        $display("PASS_POOL window=%0d vectors=%0d comb_checks=%0d cycles=%0d exact=%0d accepted=%0d cancelled=%0d resets=%0d valid_checks=%0d packed_checks=%0d synchronous_checks=%0d maximum_burst=%0d",
                 WINDOW,VECTORS,comb_checks,CYCLES,exact,accepted,cancelled,resets,valid_checks,packed_checks,synchronous_checks,maximum_burst);
        $finish;
    end
    initial begin #100000000.0; $fatal(1,"pooling RTL timeout"); end
endmodule
