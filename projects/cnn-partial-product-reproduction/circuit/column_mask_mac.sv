// Optional synthesizable reference. The delivered execution uses ngspice MOS netlists.
// This RTL was not synthesized/timed; SPICE and Python validations are separate.
// Signed N-bit operands. Restrict k to 0..N-1 so sign columns stay enabled.
module column_mask_mac #(
    parameter integer N = 6,
    parameter integer ACC_WIDTH = 32
) (
    input logic clk,
    input logic reset,
    input logic valid,
    input logic signed [N-1:0] a,
    input logic signed [N-1:0] b,
    input logic [$clog2(N)-1:0] k,
    output logic signed [2*N-1:0] product,
    output logic signed [ACC_WIDTH-1:0] accumulator
);
    logic [2*N-1:0] matrix_sum;
    logic pp;
    integer i, j;
    always_comb begin
        matrix_sum = ({{(2*N-1){1'b0}},1'b1} << N)
                   + ({{(2*N-1){1'b0}},1'b1} << (2*N-1));
        pp = 1'b0;
        for (i=0; i<N; i=i+1) begin
            for (j=0; j<N; j=j+1) begin
                if (i+j >= k) begin
                    if ((i==N-1) != (j==N-1)) pp = ~(a[i] & b[j]);
                    else pp = a[i] & b[j];
                    matrix_sum = matrix_sum + ({{(2*N-1){1'b0}},pp} << (i+j));
                end
            end
        end
        product = $signed(matrix_sum);
    end
    always_ff @(posedge clk) begin
        if (reset) accumulator <= '0;
        else if (valid) accumulator <= accumulator +
            $signed({{(ACC_WIDTH-2*N){product[2*N-1]}},product});
    end
endmodule
