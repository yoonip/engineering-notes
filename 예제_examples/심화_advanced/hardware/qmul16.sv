module qmul16(input logic signed [15:0] a, b, output logic signed [15:0] y);
    logic signed [31:0] product;
    logic [31:0] magnitude, whole;
    logic signed [32:0] rounded;
    always_comb begin
        // 전체 곱을 보존한 뒤 크기에서 짝수 반올림하고 부호를 복원한다.
        product = a * b;
        magnitude = product < 0 ? $unsigned(-product) : $unsigned(product);
        whole = magnitude >> 8;
        if ((magnitude[7:0] > 8'd128) ||
            ((magnitude[7:0] == 8'd128) && whole[0])) whole = whole + 1;
        rounded = product < 0 ? -$signed({1'b0, whole}) : $signed({1'b0, whole});
        if (rounded > 33'sd32767) y = 16'sh7fff;
        else if (rounded < -33'sd32768) y = 16'sh8000;
        else y = rounded[15:0];
    end
endmodule
