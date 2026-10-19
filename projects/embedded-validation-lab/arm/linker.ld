ENTRY(Reset_Handler)
MEMORY {
 ROM (rx) : ORIGIN = 0x00000000, LENGTH = 1M
 RAM (rwx): ORIGIN = 0x20000000, LENGTH = 128K
}
SECTIONS {
 .text : { KEEP(*(.isr_vector)) *(.text*) *(.rodata*) } > ROM
 .data : {
  . = ALIGN(4); _data_start = .; *(.data*) . = ALIGN(4); _data_end = .;
 } > RAM AT> ROM
 _data_load = LOADADDR(.data);
 .bss (NOLOAD) : {
  . = ALIGN(4); _bss_start = .; *(.bss*) *(COMMON); . = ALIGN(4); _bss_end = .;
 } > RAM
 _stack_top = ORIGIN(RAM) + LENGTH(RAM);
}
