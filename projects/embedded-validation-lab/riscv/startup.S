.section .text.start
.globl _start
_start:
    la sp, _stack_top       # C 함수가 stack을 쓸 수 있도록 먼저 설정.
    la t0, _data_load
    la t1, _data_start
    la t2, _data_end
3:  bgeu t1, t2, 4f
    lw t3, 0(t0)
    sw t3, 0(t1)
    addi t0, t0, 4
    addi t1, t1, 4
    j 3b
4:
    la t0, _bss_start
    la t1, _bss_end
1:  bgeu t0, t1, 2f
    sw zero, 0(t0)          # 초기값 없는 전역 변수는 0으로 초기화.
    addi t0, t0, 4
    j 1b
2:  call main
    ebreak                 # 이 예제 EEI는 EBREAK를 종료 신호로 받는다.
