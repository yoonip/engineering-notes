module tb_qmul16;
    parameter N = 10121;
    logic signed [15:0] a, b, y;
    logic [47:0] vectors [0:N-1];
    integer k;
    qmul16 dut(a, b, y);
    initial begin
        $readmemh("vectors.hex", vectors);
        for (k = 0; k < N; k = k + 1) begin
            a = vectors[k][47:32]; b = vectors[k][31:16];
            #1;
            if (y !== vectors[k][15:0])
                $fatal(1, "qmul mismatch k=%0d a=%0d b=%0d y=%0d expected=%0d", k,a,b,y,$signed(vectors[k][15:0]));
        end
        $display("PASS qmul16 vectors=%0d", N);
        $finish;
    end
endmodule
