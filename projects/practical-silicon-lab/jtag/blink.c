#include <stdint.h>

/* RM0368 memory map + register offsets, for STM32F401RE only. */
#define REG32(addr) (*(volatile uint32_t *)(uintptr_t)(addr))
#define RCC_AHB1ENR  REG32(0x40023830u)
#define GPIOA_MODER  REG32(0x40020000u)
#define GPIOA_OTYPER REG32(0x40020004u)
#define GPIOA_OSPEEDR REG32(0x40020008u)
#define GPIOA_PUPDR  REG32(0x4002000cu)
#define GPIOA_BSRR   REG32(0x40020018u)

volatile uint32_t phase;       /* .bss: startup must make this zero. */
volatile uint32_t blink_count;
volatile uint32_t fault_seen;
volatile uint32_t magic = 0x13579bdfu; /* .data: proves flash->SRAM copy. */

static void delay(void)
{
    /* Visible pacing only; loop time is not an accurate clock test. */
    for (volatile uint32_t i = 0; i < 800000u; ++i) {
        __asm__ volatile ("nop");
    }
}

int main(void)
{
    phase = 2u;
    if (magic != 0x13579bdfu || blink_count != 0u) {
        fault_seen = 2u;       /* Startup data invariant failed. */
        for (;;) { __asm__ volatile ("nop"); }
    }
    RCC_AHB1ENR |= 1u;         /* GPIOAEN: enable GPIOA's AHB1 clock. */
    (void)RCC_AHB1ENR;         /* Read back after the clock-enable write. */

    /* PA5 uses two MODER bits [11:10]: 01 means general output. */
    GPIOA_MODER = (GPIOA_MODER & ~(3u << 10)) | (1u << 10);
    GPIOA_OTYPER &= ~(1u << 5); /* Push-pull, not open-drain. */
    GPIOA_OSPEEDR &= ~(3u << 10); /* Low output slew is enough for LED. */
    GPIOA_PUPDR &= ~(3u << 10); /* No pull resistor needed for this LED. */
    phase = 3u;

    for (;;) {
        GPIOA_BSRR = 1u << 5;  /* Set PA5 atomically: LD2 on. */
        phase = 4u;
        delay();
        GPIOA_BSRR = 1u << 21; /* Reset PA5: upper-half reset bit. */
        ++blink_count;        /* Observable progress even if LED is broken. */
        delay();
    }
}
