module top_module(input [99:0] a, b, input sel, output [99:0] out); // 100비트 두 후보와 선택 신호
    assign out = sel ? b : a; // sel1이면b 전체를 고르고0이면a 전체를 연결
endmodule // 벡터 멀티플렉서 끝
