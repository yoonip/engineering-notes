ENTRY(Reset_Handler)
MEMORY {
  FLASH (rx) : ORIGIN = 0x08000000, LENGTH = 2M
  RAM (rwx) : ORIGIN = 0x20000000, LENGTH = 128K
}
SECTIONS {
  .isr_vector : { KEEP(*(.isr_vector)) } > FLASH
  .text : { *(.text.start) *(.text*) *(.rodata*) } > FLASH
  .ARM.exidx : { *(.ARM.exidx*) } > FLASH
  .data : {
    . = ALIGN(4); __data_start = .;
    *(.data*) *(.sdata*)
    . = ALIGN(4); __data_end = .;
  } > RAM AT> FLASH
  __data_load = LOADADDR(.data);
  .bss (NOLOAD) : {
    . = ALIGN(4); __bss_start = .;
    *(.bss*) *(.sbss*) *(COMMON)
    . = ALIGN(4); __bss_end = .;
  } > RAM
  __stack_top = ORIGIN(RAM) + LENGTH(RAM);
}
