ENTRY(Reset_Handler)
MEMORY {
 FLASH (rx) : ORIGIN = 0x08000000, LENGTH = 2M
 DTCM (rwx) : ORIGIN = 0x20000000, LENGTH = 128K
 SRAM1(rwx) : ORIGIN = 0x20020000, LENGTH = 368K
}
SECTIONS {
 .text : { KEEP(*(.isr_vector)) *(.text*) *(.rodata*) } > FLASH
 .data : {
  . = ALIGN(4); _data_start = .; *(.data*) . = ALIGN(4); _data_end = .;
 } > DTCM AT> FLASH
 _data_load = LOADADDR(.data);
 .bss (NOLOAD) : {
  . = ALIGN(4); _bss_start = .; *(.bss*) *(COMMON); . = ALIGN(4); _bss_end = .;
 } > DTCM
 .dma (NOLOAD) : { . = ALIGN(32); *(.dma) . = ALIGN(32); } > SRAM1
 _stack_top = ORIGIN(DTCM) + LENGTH(DTCM);
}
