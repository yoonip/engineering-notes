.syntax unified
.cpu cortex-m7
.thumb
.section .isr_vector,"a",%progbits
.word _stack_top, Reset_Handler, Default_Handler, HardFault_Handler
.word Default_Handler, Default_Handler, Default_Handler, 0, 0, 0, 0
.word Default_Handler, Default_Handler, 0, Default_Handler, SysTick_Handler
.section .text.Reset_Handler,"ax",%progbits
.thumb_func
.globl Reset_Handler
Reset_Handler:
    ldr r0, =_data_load    // ROM의 초기값 -> RAM .data.
    ldr r1, =_data_start
    ldr r2, =_data_end
1:  cmp r1, r2
    bhs 2f
    ldr r3, [r0], #4
    str r3, [r1], #4
    b 1b
2:  ldr r1, =_bss_start
    ldr r2, =_bss_end
    movs r3, #0
3:  cmp r1, r2
    bhs 4f
    str r3, [r1], #4
    b 3b
4:  bl main
5:  b 5b
.thumb_func
.weak SysTick_Handler
SysTick_Handler:
    bx lr
.thumb_func
.globl Default_Handler
Default_Handler:
    b Default_Handler
.weak HardFault_Handler
.thumb_set HardFault_Handler, Default_Handler
