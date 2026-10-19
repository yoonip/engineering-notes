/* Cortex-M4 reset code: no libc, RTOS, PLL, or external IRQ setup. */
.syntax unified
.cpu cortex-m4
.thumb

.section .isr_vector, "a", %progbits
.global vector_table
vector_table:
    .word _estack          /* Hardware loads the initial MSP. */
    .word Reset_Handler    /* Thumb function pointer: bit 0 is one. */
    .word Default_Handler  /* NMI */
    .word Default_Handler  /* HardFault */
    .word Default_Handler  /* MemManage */
    .word Default_Handler  /* BusFault */
    .word Default_Handler  /* UsageFault */
    .word 0, 0, 0, 0       /* Reserved core exception slots. */
    .word Default_Handler  /* SVCall */
    .word Default_Handler  /* DebugMonitor */
    .word 0                /* Reserved */
    .word Default_Handler  /* PendSV */
    .word Default_Handler  /* SysTick; not enabled in this lab. */
/* Only 16 core entries. Do not enable external interrupts in this lab. */

.section .text.Reset_Handler, "ax", %progbits
.global Reset_Handler
.type Reset_Handler, %function
.thumb_func
Reset_Handler:
    cpsid i                /* PRIMASK masks configurable interrupts. */
    ldr r0, =_sidata       /* Initial .data bytes reside in flash. */
    ldr r1, =_sdata        /* Runtime destination is SRAM. */
    ldr r2, =_edata        /* One-past-end SRAM address. */
1:
    cmp r1, r2
    bhs 2f
    ldr r3, [r0], #4
    str r3, [r1], #4
    b 1b
2:
    ldr r1, =_sbss
    ldr r2, =_ebss
    movs r3, #0
3:
    cmp r1, r2
    bhs 4f
    str r3, [r1], #4       /* C requires zero-initialized .bss. */
    b 3b
4:
    ldr r0, =phase
    movs r1, #1
    str r1, [r0]           /* Startup completed; C is not yet entered. */
    bl main
5:
    b 5b                  /* main should not return. */
.size Reset_Handler, . - Reset_Handler

.section .text.Default_Handler, "ax", %progbits
.global Default_Handler
.type Default_Handler, %function
.thumb_func
Default_Handler:
    ldr r0, =fault_seen
    movs r1, #1
    str r1, [r0]           /* Preserve phase for diagnosis. */
6:
    b 6b
.size Default_Handler, . - Default_Handler
