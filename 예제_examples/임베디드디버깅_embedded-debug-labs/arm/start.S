.syntax unified
.cpu cortex-m7
.thumb

.section .isr_vector,"a",%progbits
.global vector_table
vector_table:
    .word __stack_top
    .word Reset_Handler
    .rept 142
    .word Default_Handler
    .endr

.section .text.start,"ax",%progbits
.global Reset_Handler
.type Reset_Handler,%function
.thumb_func
Reset_Handler:
    ldr sp, =__stack_top
    ldr r0, =__data_load
    ldr r1, =__data_start
    ldr r2, =__data_end
1:
    cmp r1, r2
    bcs 2f
    ldr r3, [r0], #4
    str r3, [r1], #4
    b 1b
2:
    ldr r1, =__bss_start
    ldr r2, =__bss_end
    movs r3, #0
3:
    cmp r1, r2
    bcs 4f
    str r3, [r1], #4
    b 3b
4:
    bl main
5:
    b 5b
.size Reset_Handler, .-Reset_Handler

.thumb_func
.type Default_Handler,%function
Default_Handler:
    b Default_Handler
.size Default_Handler, .-Default_Handler
