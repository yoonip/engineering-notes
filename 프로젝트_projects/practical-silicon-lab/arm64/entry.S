/* QEMU virt ELF entry; the loader already placed the image in RAM. */
.section .text.boot, "ax"
.global _start
.type _start, %function
_start:
    msr daifset, #0xf      /* Mask D/A/I/F; no vector table in this lab. */
    ldr x0, =__stack_top   /* Linker symbol: not an allocated C variable. */
    mov sp, x0
    ldr x0, =__bss_start   /* C zero-initialized storage starts here. */
    ldr x1, =__bss_end     /* One-past-end; RAM contents need not be zero. */
1:
    cmp x0, x1
    b.hs 2f
    strb wzr, [x0], #1     /* Store one zero byte, then increment x0. */
    b 1b
2:
    bl main               /* Set x30 (link register) and call C. */
3:
    wfe                   /* Idle after main returns; does not exit QEMU. */
    b 3b
.size _start, . - _start
