ENTRY(_start) /* ELF 진입점은 직접 작성한 시작 코드 */
MEMORY { /* 예제에서 사용할 메모리 영역 */
    RAM (rwx) : ORIGIN = 0x80000000, LENGTH = 128K /* QEMU virt DRAM의 첫128KiB만 사용 */
} /* 영역 정의 끝 */
PHDRS { /* ELF 적재 구간의 권한 분리 */
    text PT_LOAD FLAGS(5); /* 읽기·실행 코드 구간 */
    data PT_LOAD FLAGS(6); /* 읽기·쓰기 자료 구간 */
} /* 적재 권한 정의 끝 */
SECTIONS { /* 코드·자료·스택 심볼의 배치 */
    .text : { *(.text.start) *(.text .text.*) *(.rodata .rodata.*) } > RAM :text /* 시작 코드와 함수·읽기 전용 자료 배치 */
    . = ALIGN(16); /* 다음 자료 경계 정렬 */
    .data : { *(.data .data.*) *(.sdata .sdata.*) } > RAM :data /* 초기값 있는 자료를 같은 RAM에 직접 적재 */
    __global_pointer$ = ADDR(.data) + 0x800; /* gp 초기화에 쓸 전역 포인터 기준 */
    .bss (NOLOAD) : { /* 파일에0을 저장하지 않는 초기화 영역 */
        . = ALIGN(4); __bss_start = .; /* 워드 저장이 가능한 시작 주소 */
        *(.bss .bss.*) *(.sbss .sbss.*) *(COMMON) /* 초기값 없는 자료 수집 */
        . = ALIGN(4); __bss_end = .; /* 4바이트 단위 초기화의 끝 */
    } > RAM :data /* BSS를 쓰기 가능한 RAM에 배치 */
    __stack_top = ORIGIN(RAM) + LENGTH(RAM); /* 16바이트 정렬 RAM 상단에서 스택 시작 */
    ASSERT(__bss_end + 4096 < __stack_top, "RAM overlaps stack") /* 최소4KiB의 스택 여유 확인 */
} /* 메모리 배치 끝 */
