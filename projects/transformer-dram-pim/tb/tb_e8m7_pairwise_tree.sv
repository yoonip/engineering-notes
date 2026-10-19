`timescale 1ns/1ps
// 독립 pairwise E8M7 tree와 등록 경계를 검사한다. Python이 mem 정답을 만든다.
// REGISTERED=0은 모든 product/adder node와 scalar mul/add를 대조하고,
// REGISTERED=1은 연속 입력·bubble·동기 reset 취소·lane 순서·N->N+1을 대조한다.
// #1은 delta/NBA가 안정된 뒤 읽는 TB 규칙이며 실제 물리 지연의 측정이 아니다.
module tb_e8m7_pairwise_tree #(
    parameter integer LANES=16,
    parameter integer CASES=1,
    parameter integer SCALAR_CASES=0,
    parameter integer REGISTERED=0
);
    localparam integer LEAVES=1<<((LANES<=1)?0:$clog2(LANES));
    reg [15:0] a [0:LANES-1];
    reg [15:0] b [0:LANES-1];
    reg [15:0] a_memory [0:CASES*LANES-1];
    reg [15:0] b_memory [0:CASES*LANES-1];
    reg [15:0] expected_memory [0:CASES-1];
    reg [15:0] expected_tree [0:CASES*(2*LEAVES-1)-1];
    reg [15:0] scalar_a [0:((SCALAR_CASES>0)?SCALAR_CASES:1)-1];
    reg [15:0] scalar_b [0:((SCALAR_CASES>0)?SCALAR_CASES:1)-1];
    reg [15:0] expected_mul [0:((SCALAR_CASES>0)?SCALAR_CASES:1)-1];
    reg [15:0] expected_add [0:((SCALAR_CASES>0)?SCALAR_CASES:1)-1];
    reg [15:0] scalar_left=0, scalar_right=0;
    wire [15:0] scalar_mul, scalar_add;
    wire [15:0] observed_tree [0:2*LEAVES-1];
    wire [15:0] result;
    integer vector_index, lane_index, node_index;

    generate
        if (REGISTERED==0) begin: kernel_test
            // Icarus 12의 길이1 unpacked array 연결은 TB에서 scalar로 지정한다.
            // 제품 포트나 알고리즘을 바꾸는 우회가 아니다.
            if (LANES==1) begin: single_lane
                e8m7_pairwise_tree_mac #(.LANES(LANES)) dut(.a(a[0]),.b(b[0]),.result(result));
                assign scalar_mul=dut.multiply_rne(scalar_left,scalar_right);
                assign scalar_add=dut.add_rne(scalar_left,scalar_right);
                for (genvar node=0;node<2*LEAVES;node=node+1)
                    assign observed_tree[node]=dut.tree[node];
            end else begin: multiple_lanes
                e8m7_pairwise_tree_mac #(.LANES(LANES)) dut(.a(a),.b(b),.result(result));
                assign scalar_mul=dut.multiply_rne(scalar_left,scalar_right);
                assign scalar_add=dut.add_rne(scalar_left,scalar_right);
                for (genvar node=0;node<2*LEAVES;node=node+1)
                    assign observed_tree[node]=dut.tree[node];
            end
            initial begin
                $readmemh("a.mem",a_memory); $readmemh("b.mem",b_memory);
                $readmemh("expected.mem",expected_memory); $readmemh("tree.mem",expected_tree);
                for (vector_index=0;vector_index<CASES;vector_index=vector_index+1) begin
                    for (lane_index=0;lane_index<LANES;lane_index=lane_index+1) begin
                        a[lane_index]=a_memory[vector_index*LANES+lane_index];
                        b[lane_index]=b_memory[vector_index*LANES+lane_index];
                    end
                    #1;
                    // 최종 합만 우연히 맞는 일을 막기 위해 product와 모든 중간
                    // adder word까지 확인한다. tree.mem은 root=1의 heap 순서다.
                    for (node_index=1;node_index<2*LEAVES;node_index=node_index+1) begin
                        if (observed_tree[node_index]!==expected_tree[vector_index*(2*LEAVES-1)+node_index-1])
                            $fatal(1,"PAIRWISE tree mismatch case=%0d node=%0d got=%h expected=%h",vector_index,node_index,
                                observed_tree[node_index],expected_tree[vector_index*(2*LEAVES-1)+node_index-1]);
                    end
                    if (result!==expected_memory[vector_index])
                        $fatal(1,"PAIRWISE result mismatch case=%0d got=%h expected=%h",vector_index,result,expected_memory[vector_index]);
                    $display("PAIRWISE case=%0d result=%04h nodes=%0d",vector_index,result,2*LEAVES-1);
                end
                if (SCALAR_CASES>0) begin
                    $readmemh("scalar_a.mem",scalar_a); $readmemh("scalar_b.mem",scalar_b);
                    $readmemh("scalar_mul.mem",expected_mul); $readmemh("scalar_add.mem",expected_add);
                    for (vector_index=0;vector_index<SCALAR_CASES;vector_index=vector_index+1) begin
                        scalar_left=scalar_a[vector_index]; scalar_right=scalar_b[vector_index]; #1;
                        if (scalar_mul!==expected_mul[vector_index] || scalar_add!==expected_add[vector_index])
                            $fatal(1,"PAIRWISE scalar mismatch case=%0d a=%h b=%h mul=%h expectedmul=%h add=%h expectedadd=%h",vector_index,
                                scalar_left,scalar_right,scalar_mul,expected_mul[vector_index],scalar_add,expected_add[vector_index]);
                        $display("SCALAR case=%0d mul=%04h add=%04h",vector_index,scalar_mul,scalar_add);
                    end
                end
                $display("PAIRWISE PASS lanes=%0d cases=%0d scalar=%0d",LANES,CASES,SCALAR_CASES); $finish;
            end
        end else begin: registered_test
            reg clk=0, reset_n=0, input_valid=0;
            reg [16*LANES-1:0] a_packed=0,b_packed=0;
            wire output_valid;
            reg [1:0] controls [0:CASES-1];
            reg pending_valid=0;
            reg [15:0] pending_word=0,before_result;
            reg before_valid;
            integer exact_count=0,accepted_count=0,cancelled_count=0,lane_checks=0;
            integer reset_count=0,burst=0,maximum_burst=0;
            e8m7_pairwise_registered_top #(.LANES(LANES)) dut(
                .clk(clk),.reset_n(reset_n),.input_valid(input_valid),.a_packed(a_packed),.b_packed(b_packed),
                .result(result),.output_valid(output_valid));
            always #100 clk=~clk;
            initial begin
                $readmemh("a.mem",a_memory); $readmemh("b.mem",b_memory);
                $readmemh("expected.mem",expected_memory); $readmemh("controls.mem",controls);
                for (vector_index=0;vector_index<CASES;vector_index=vector_index+1) begin
                    @(negedge clk);
                    before_result=result;before_valid=output_valid;
                    reset_n=controls[vector_index][1];input_valid=controls[vector_index][0];
                    for (lane_index=0;lane_index<LANES;lane_index=lane_index+1) begin
                        a_packed[16*lane_index+:16]=a_memory[vector_index*LANES+lane_index];
                        b_packed[16*lane_index+:16]=b_memory[vector_index*LANES+lane_index];
                    end
                    #1;
                    if(result!==before_result || output_valid!==before_valid)
                        $fatal(1,"PAIRWISE output changed before rising edge cycle=%0d",vector_index);
                    @(posedge clk);#1;
                    if(!reset_n) begin
                        if(result!==0 || output_valid!==0) $fatal(1,"PAIRWISE synchronous reset failed");
                        for(lane_index=0;lane_index<LANES;lane_index=lane_index+1)
                            if(dut.a[lane_index]!==0 || dut.b[lane_index]!==0) $fatal(1,"PAIRWISE reset lane failed");
                        if(pending_valid)cancelled_count=cancelled_count+1;
                        pending_valid=0;reset_count=reset_count+1;burst=0;
                    end else begin
                        if(output_valid!==pending_valid) $fatal(1,"PAIRWISE one-clock valid latency failed");
                        if(pending_valid) begin
                            if(result!==pending_word) $fatal(1,"PAIRWISE registered mismatch cycle=%0d got=%h expected=%h",vector_index,result,pending_word);
                            exact_count=exact_count+1;
                        end
                        if(input_valid) begin
                            for(lane_index=0;lane_index<LANES;lane_index=lane_index+1) begin
                                if(dut.a[lane_index]!==a_packed[16*lane_index+:16] || dut.b[lane_index]!==b_packed[16*lane_index+:16])
                                    $fatal(1,"PAIRWISE packed lane order failed");
                                lane_checks=lane_checks+2;
                            end
                            pending_word=expected_memory[vector_index];accepted_count=accepted_count+1;
                            burst=burst+1;if(burst>maximum_burst)maximum_burst=burst;
                        end else burst=0;
                        pending_valid=input_valid;
                    end
                    $display("PAIRWISE_REG cycle=%0d valid=%0d result=%04h exact=%0d",vector_index,output_valid,result,exact_count);
                end
                if(pending_valid)$fatal(1,"PAIRWISE schedule not flushed");
                $display("PAIRWISE_REG PASS lanes=%0d cycles=%0d exact=%0d accepted=%0d cancelled=%0d resets=%0d lane_checks=%0d maximum_burst=%0d",
                    LANES,CASES,exact_count,accepted_count,cancelled_count,reset_count,lane_checks,maximum_burst);$finish;
            end
        end
    endgenerate
    initial begin #10000000.0;$fatal(1,"PAIRWISE test timeout");end
endmodule
