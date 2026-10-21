`timescale 1ns/1ps
module tb_dot4;
    parameter integer BUG_MODE = 0;
    reg clk=0;
    reg rst=1, in_valid=0, out_ready=0;
    reg [15:0] in_tag=0;
    reg [31:0] in_x=0, in_w=0;
    wire in_ready, out_valid;
    wire [15:0] out_tag;
    wire signed [31:0] out_data;
    dot4 #(.BUG_MODE(BUG_MODE)) dut (
        .clk(clk), .rst(rst), .in_valid(in_valid), .in_ready(in_ready),
        .in_tag(in_tag), .in_x(in_x), .in_w(in_w),
        .out_valid(out_valid), .out_ready(out_ready), .out_tag(out_tag), .out_data(out_data)
    );
    always #5 clk = ~clk; // 10ns는 테스트벤치의 시뮬레이션 주기입니다.
    integer source, trace, count;
    integer cycle, rr, vv, ready_value, tag;
    integer x0, x1, x2, x3, w0, w1, w2, w3;
    initial begin
        source = $fopen("stimulus.txt", "r");
        trace = $fopen("trace.csv", "w");
        if (!source || !trace) $fatal(1, "cannot open stimulus or trace");
        $fwrite(trace, "cycle,rst,in_valid,in_ready,in_tag,out_ready,out_valid,out_tag,out_data\n");
        while (!$feof(source)) begin
            count = $fscanf(source, "%d %d %d %d %d %d %d %d %d %d %d %d %d\n",
                            cycle, rr, vv, ready_value, tag, x0, x1, x2, x3, w0, w1, w2, w3);
            if (count == 13) begin
                @(negedge clk); // 구동과 관측을 다른 반주기에 두어 입력 경합을 피합니다.
                rst=rr; in_valid=vv; out_ready=ready_value; in_tag=tag;
                in_x={x3[7:0],x2[7:0],x1[7:0],x0[7:0]};
                in_w={w3[7:0],w2[7:0],w1[7:0],w0[7:0]};
                @(posedge clk); // DUT의 nonblocking 갱신 전, 전송 edge의 신호를 기록합니다.
                $fwrite(trace, "%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d\n",
                        cycle,rst,in_valid,in_ready,in_tag,out_ready,out_valid,out_tag,$signed(out_data));
            end else if (count != -1) begin
                $fatal(1, "malformed stimulus row");
            end
        end
        $fclose(source);
        $fclose(trace);
        $display("SIMULATION_FINISHED mode=%0d", BUG_MODE); // 이 문자열만으로 통과시키지 않습니다.
        #1 $finish;
    end
endmodule
