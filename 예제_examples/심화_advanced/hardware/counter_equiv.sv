module counter_behavioral(input logic clk, reset, enable, output logic [7:0] q);
    always_ff @(posedge clk)
        if (reset) q <= 0;
        else if (enable) q <= q + 8'd1;
endmodule

module counter_structural(input logic clk, reset, enable, output logic [7:0] q);
    logic [8:0] carry;
    logic [7:0] next_q;
    assign carry[0] = enable;
    genvar k;
    generate for (k=0; k<8; k=k+1) begin: bitslice
        // 각 자리의 올림은 현재 비트와 들어온 올림의 논리곱이다.
        assign next_q[k] = q[k] ^ carry[k];
        assign carry[k+1] = q[k] & carry[k];
    end endgenerate
    always_ff @(posedge clk)
        if (reset) q <= 0;
        else q <= next_q;
endmodule
