OUTPUT_ARCH(riscv)
ENTRY(_start)
MEMORY { RAM (rwx) : ORIGIN = 0x80000000, LENGTH = 128K }
SECTIONS {
  .text : { KEEP(*(.text.start)) *(.text*) } > RAM
  .rodata : { *(.rodata*) } > RAM
  .data : { *(.data*) *(.sdata*) } > RAM
  .tohost : { *(.tohost) } > RAM
  .bss (NOLOAD) : {
    . = ALIGN(8); __bss_start = .;
    *(.bss*) *(.sbss*) *(COMMON)
    . = ALIGN(8); __bss_end = .;
  } > RAM
  __stack_top = ORIGIN(RAM) + LENGTH(RAM) - 16;
}
