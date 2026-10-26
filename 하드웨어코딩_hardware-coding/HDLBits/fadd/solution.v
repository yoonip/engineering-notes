module top_module(input a, b, cin, output cout, sum); // 두 데이터 비트와 이전 자리의 올림
    assign sum = a ^ b ^ cin; // 홀수 개의1이면 합의 낮은 비트가1
    assign cout = (a & b) | (a & cin) | (b & cin); // 둘 이상이1이면 다음 자리로 올림
endmodule // 한 자리 전가산기 끝
