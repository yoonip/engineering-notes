`timescale 1ns/1ps
// 이 DUT는 원본 RTL이 아니라 실제 배선 DCP에서 export한 pool_top이다.
// __VECTORS__/__CYCLES__는 Python이 고정된 실제 입력 파일 개수로 치환한다.
// 이 시험은 SDF 없는 기능 시험이다. clock 200ns가 실제 지연 검증은 아니다.
module tb_pooling_netlist;
    localparam VECTORS = __VECTORS__;
    localparam CYCLES = __CYCLES__;
    reg clk=0, reset_n=0, input_valid=0, operation_avg=0;
    reg [255:0] values_packed=0;
    reg [15:0] valid_mask=0;
    wire [15:0] result;
    wire [4:0] valid_count;
    wire output_valid;
    reg [255:0] values_mem[0:VECTORS-1];
    reg [15:0] masks_mem[0:VECTORS-1], expected_mem[0:VECTORS-1];
    reg operations_mem[0:VECTORS-1];
    reg [4:0] counts_mem[0:VECTORS-1];
    reg [1:0] controls_mem[0:CYCLES-1];
    reg [31:0] indices_mem[0:CYCLES-1];
    reg pending_valid=0;
    reg [15:0] pending_word=0, before_word;
    reg [4:0] pending_count=0, before_count;
    reg before_valid;
    integer cycle, index, exact=0, accepted=0, cancelled=0, resets=0;
    integer burst=0, maximum_burst=0;
    pool_top dut(.clk(clk),.reset_n(reset_n),.input_valid(input_valid),
        .values_packed(values_packed),.valid_mask(valid_mask),.operation_avg(operation_avg),
        .result(result),.valid_count(valid_count),.output_valid(output_valid));
    always #100 clk=~clk;
    initial begin
        $readmemh("values.mem",values_mem); $readmemh("masks.mem",masks_mem);
        $readmemh("operations.mem",operations_mem); $readmemh("expected.mem",expected_mem);
        $readmemh("counts.mem",counts_mem); $readmemh("controls.mem",controls_mem);
        $readmemh("indices.mem",indices_mem);
        for(cycle=0;cycle<CYCLES;cycle=cycle+1) begin
            // 입력은 falling edge에서 바꾸고 다음 rising edge 직후 관찰한다.
            // reset은 동기식이므로 falling edge에서 즉시 출력이 바뀌면 실패다.
            @(negedge clk);
            before_word=result; before_count=valid_count; before_valid=output_valid;
            reset_n=controls_mem[cycle][1]; input_valid=controls_mem[cycle][0];
            index=indices_mem[cycle]; values_packed=values_mem[index];
            valid_mask=masks_mem[index]; operation_avg=operations_mem[index];
            #1;
            if(result!==before_word || valid_count!==before_count || output_valid!==before_valid)
                $fatal(1,"POOL_NET synchronous output changed cycle=%0d",cycle);
            @(posedge clk); #1;
            if(!reset_n) begin
                if(output_valid!==0 || result!==0 || valid_count!==0)
                    $fatal(1,"POOL_NET reset failed cycle=%0d",cycle);
                if(pending_valid) cancelled=cancelled+1;
                pending_valid=0; resets=resets+1; burst=0;
            end else begin
                // 직전 rising edge에서 수락한 입력이 이번 출력이어야 한다.
                if(output_valid!==pending_valid)
                    $fatal(1,"POOL_NET valid latency failed cycle=%0d",cycle);
                if(pending_valid) begin
                    if(result!==pending_word || valid_count!==pending_count)
                        $fatal(1,"POOL_NET value failed cycle=%0d got=%h wanted=%h count=%0d",cycle,result,pending_word,valid_count);
                    exact=exact+1;
                end else if(result!==0 || valid_count!==0)
                    $fatal(1,"POOL_NET invalid output must be zero cycle=%0d",cycle);
                if(input_valid) begin
                    pending_word=expected_mem[index]; pending_count=counts_mem[index];
                    accepted=accepted+1; burst=burst+1;
                    if(burst>maximum_burst) maximum_burst=burst;
                end else burst=0;
                pending_valid=input_valid;
            end
            $display("CHECK_POOL_NET cycle=%0d valid=%0d result=%h count=%0d exact=%0d",cycle,output_valid,result,valid_count,exact);
        end
        if(pending_valid) $fatal(1,"POOL_NET pending input remains");
        $display("PASS_POOL_NET cycles=%0d exact=%0d accepted=%0d cancelled=%0d resets=%0d maximum_burst=%0d",CYCLES,exact,accepted,cancelled,resets,maximum_burst);
        $finish;
    end
    initial begin #10000000.0; $fatal(1,"POOL_NET virtual timeout"); end
endmodule
