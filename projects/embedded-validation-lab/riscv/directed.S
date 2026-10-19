.section .text.start
.globl _start
_start:
    li sp, 0xfff0
    li a0, 0x80000001
    li a1, 31
    add a2,a0,a1
    sub a2,a0,a1
    slt a2,a0,a1
    sltu a2,a0,a1
    sll a2,a0,a1
    srl a2,a0,a1
    sra a2,a0,a1
    and a2,a0,a1
    or a2,a0,a1
    xor a2,a0,a1
    slti a2,a0,-1
    sltiu a2,a0,-1
    slli a2,a0,3
    srli a2,a0,3
    srai a2,a0,3
    xori a2,a0,-1
    ori a2,a0,3
    andi a2,a0,3
    auipc a2,0
    li t0,0x5000
    sw a0,0(t0)
    lw a2,0(t0)
    li a1,0x80
    sb a1,1(t0)
    lb a2,1(t0)
    lbu a2,1(t0)
    li a1,0x8001
    sh a1,2(t0)
    lh a2,2(t0)
    lhu a2,2(t0)
    lw zero,0(t0)
    addi zero,zero,99
    beq zero,zero,1f
    ecall
1:  bne zero,a0,2f
    ecall
2:  blt a0,zero,3f
    ecall
3:  bge zero,a0,4f
    ecall
4:  bltu zero,a0,5f
    ecall
5:  bgeu a0,zero,6f
    ecall
6:  beq a0,zero,7f       # not taken 분기도 테스트.
    jal ra,8f
7:  ecall
8:  la t1,9f
    ori t1,t1,1         # JALR가 target bit0를 지우는지 검사.
    jalr ra,0(t1)
    ecall
9:  fence rw,rw
    ebreak
