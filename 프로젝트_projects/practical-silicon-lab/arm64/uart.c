#include <stdint.h>

#ifndef UART_BASE
#define UART_BASE 0x09000000UL /* Confirm against this QEMU run's DTB. */
#endif
#ifndef READY_MASK
#define READY_MASK (1u << 5)  /* PL011 TXFF: wait while FIFO is full. */
#endif

#define UART_DR   0x00u
#define UART_FR   0x18u
#define UART_IBRD 0x24u
#define UART_FBRD 0x28u
#define UART_LCRH 0x2cu
#define UART_CR   0x30u
#define UART_ICR  0x44u

volatile uint32_t phase;      /* Milestone visible without a working UART. */
volatile uint32_t scratch[4]; /* Four words: smoke test, not DDR validation. */

static uint32_t reg_read(uint32_t offset)
{
    /* A volatile access preserves the MMIO load in generated code. */
    return *(volatile uint32_t *)(UART_BASE + offset);
}

static void reg_write(uint32_t offset, uint32_t value)
{
    *(volatile uint32_t *)(UART_BASE + offset) = value;
}

static void uart_init(void)
{
    reg_write(UART_CR, 0u);    /* Disable while changing UART settings. */
    reg_write(UART_ICR, 0x7ffu);
    /* Example divider for 24 MHz / 115200; not a real board default. */
    reg_write(UART_IBRD, 13u);
    reg_write(UART_FBRD, 1u);
    reg_write(UART_LCRH, (3u << 5) | (1u << 4)); /* 8 bits + FIFO. */
    reg_write(UART_CR, (1u << 9) | (1u << 8) | 1u); /* RX/TX/UART. */
}

static void uart_putc(char c)
{
    /* stuck mode uses TXFE instead of TXFF and blocks on an empty FIFO. */
    while (reg_read(UART_FR) & READY_MASK) {
        __asm__ volatile ("nop");
    }
    reg_write(UART_DR, (uint32_t)(unsigned char)c); /* Send one byte. */
}

static void uart_puts(const char *s)
{
    for (; *s; ++s) {
        if (*s == '\n') {
            uart_putc('\r');
        }
        uart_putc(*s);
    }
}

static void uart_hex(uint64_t value)
{
    static const char digits[] = "0123456789abcdef";
    uart_puts("0x");
    for (int i = 60; i >= 0; i -= 4) {
        uart_putc(digits[(value >> i) & 0xfu]);
    }
}

void main(void)
{
    uint64_t el;
    __asm__ volatile ("mrs %0, CurrentEL" : "=r"(el)); /* CPU system reg. */
    phase = 1u;
    uart_init();
    phase = 2u;
    uart_puts("B0: C entry; UART alive\nCurrentEL=");
    uart_hex(el >> 2);
    uart_puts("\n");
    phase = 3u;
    for (unsigned int i = 0; i < 4u; ++i) {
        scratch[i] = 0xa5a50000u | i;
    }
    for (unsigned int i = 0; i < 4u; ++i) {
        if (scratch[i] != (0xa5a50000u | i)) {
            uart_puts("B1: RAM smoke FAIL\n");
            phase = 0xeeu;
            return;
        }
    }
    phase = 4u;
    uart_puts("B1: RAM smoke PASS (4 words only)\n");
    uart_puts("B2: idle; attach GDB and inspect phase=4\n");
}
