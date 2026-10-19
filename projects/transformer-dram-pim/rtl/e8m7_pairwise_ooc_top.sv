// Vivado 2024.1 OOC 비교를 위한 짧은 top 이름의 연결 wrapper입니다.
// 일부 합성 시도에서는 긴 top 이름의 내부 보조 Tcl 파일을 읽지 못했습니다.
// 같은 수치 회로를 짧은 이름으로 연결해 그 도구 경로를 따로 확인합니다.
// 이 모듈은 register, 연산, pipeline을 추가하지 않습니다. 아래 실제 등록형
// core의 edge N 입력 → edge N+1 출력 및 valid/reset 계약을 그대로 전달합니다.
module pw_top (
    input wire clk,
    input wire reset_n,
    input wire input_valid,
    input wire [255:0] a_packed,
    input wire [255:0] b_packed,
    output wire [15:0] result,
    output wire output_valid
);
    // 비교하는 내적은 16lane입니다. lane i의 16bit E8M7 word는
    // [16*i +: 16]에 놓이며 Python의 packed memory와 순서가 같습니다.
    // 실제 연산은 곱마다 RNE, 이어 balanced tree의 덧셈마다 RNE합니다.
    e8m7_pairwise_registered_top #(.LANES(16)) core (
        .clk(clk), .reset_n(reset_n), .input_valid(input_valid),
        .a_packed(a_packed), .b_packed(b_packed),
        .result(result), .output_valid(output_valid)
    );
endmodule
