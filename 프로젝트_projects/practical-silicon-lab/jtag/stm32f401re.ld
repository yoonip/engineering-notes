/* STM32F401RE: main flash 512 KiB, SRAM 96 KiB. */
ENTRY(Reset_Handler)
MEMORY {
    FLASH (rx)  : ORIGIN = 0x08000000, LENGTH = 512K
    RAM   (rwx) : ORIGIN = 0x20000000, LENGTH = 96K
}
_estack = ORIGIN(RAM) + LENGTH(RAM);
SECTIONS {
    .isr_vector : ALIGN(4) {
        KEEP(*(.isr_vector)) /* --gc-sections must keep the reset table. */
    } > FLASH
    .text : ALIGN(4) {
        *(.text .text.*)
        *(.rodata .rodata.*)
        . = ALIGN(4);
    } > FLASH
    .data : ALIGN(4) {
        _sdata = .;
        *(.data .data.*)
        . = ALIGN(4);
        _edata = .;
    } > RAM AT > FLASH      /* VMA=SRAM; LMA=flash. Startup copies it. */
    _sidata = LOADADDR(.data);
    .bss (NOLOAD) : ALIGN(4) {
        _sbss = .;
        *(.bss .bss.* COMMON)
        . = ALIGN(4);
        _ebss = .;
    } > RAM
    ASSERT(_ebss + 0x1000 < _estack, "Reserve 4 KiB for stack")
    /DISCARD/ : { *(.comment) *(.note*) *(.eh_frame*) }
}
