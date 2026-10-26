module top_module(input [31:0] in, output [31:0] out); // 32비트 입력과 바이트 순서를 바꾼 출력
    assign out = {in[7:0], in[15:8], in[23:16], in[31:24]}; // 네 바이트의 위치만 뒤집어 연결
endmodule // 바이트 순서 변환 회로 끝
