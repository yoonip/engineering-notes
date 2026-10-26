module top_module(input [2:0] in, output [1:0] out); // 세 입력 비트와0~3을 담는 두 출력 비트
    assign out = {1'b0, in[0]} + {1'b0, in[1]} + {1'b0, in[2]}; // 각 비트를2비트로 넓혀 캐리까지 포함한 개수 합산
endmodule // 1의 개수 회로 끝
