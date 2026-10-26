module top_module(input [7:0] in, output [7:0] out); // 8비트 입력과 비트 순서를 바꾼 출력
    assign out = {in[0], in[1], in[2], in[3], in[4], in[5], in[6], in[7]}; // 낮은 입력 비트부터 높은 출력 자리에 연결
endmodule // 비트 순서 반전 회로 끝
