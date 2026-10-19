/* RAM placement for the QEMU virt machine. */
ENTRY(_start)
MEMORY {
    RAM (rwx) : ORIGIN = 0x40080000, LENGTH = 16M
}
SECTIONS {
    .text : ALIGN(16) {
        KEEP(*(.text.boot)) /* Startup must survive section collection. */
        *(.text .text.*)
    } > RAM
    .rodata : ALIGN(16) { *(.rodata .rodata.*) } > RAM
    .data : ALIGN(16) { *(.data .data.*) } > RAM
    .bss (NOLOAD) : ALIGN(16) { /* Reserve runtime RAM; no payload bytes. */
        __bss_start = .;
        *(.bss .bss.* COMMON)
        __bss_end = .;
    } > RAM
    . = ALIGN(16);
    . += 0x4000;          /* Reserve 16 KiB below the descending stack. */
    __stack_top = .;
    ASSERT(__stack_top < ORIGIN(RAM) + LENGTH(RAM), "RAM overflow")
    /DISCARD/ : { *(.comment) *(.note*) *(.eh_frame*) }
}
