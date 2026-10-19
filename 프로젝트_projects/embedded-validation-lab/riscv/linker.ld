ENTRY(_start)
MEMORY {
 ROM (rx)  : ORIGIN = 0x00000000, LENGTH = 16K
 RAM (rwx) : ORIGIN = 0x00004000, LENGTH = 48K
}
SECTIONS {
 .text : { *(.text.start) *(.text*) *(.rodata*) } > ROM
 .data : {
  . = ALIGN(4); _data_start = .; *(.data*) *(.sdata*) . = ALIGN(4); _data_end = .;
 } > RAM AT> ROM
 _data_load = LOADADDR(.data);
 .bss (NOLOAD) : {
   . = ALIGN(4); _bss_start = .;
   *(.bss*) *(.sbss*) *(COMMON)
   . = ALIGN(4); _bss_end = .;
 } > RAM
 _stack_top = ORIGIN(RAM) + LENGTH(RAM);
}
