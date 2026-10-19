/* Same C source for Cortex-M7 and RV64IMAC. */
#include <stdint.h>

volatile uint32_t input_a = 1;
volatile uint32_t input_b = 3;
volatile uint32_t result;
volatile uint32_t trace[2];

__attribute__((noinline, noreturn)) void lesson_done(void)
{
    for (;;) { __asm__ volatile ("nop"); }
}

int main(void)
{
    result = input_a + input_b;
    trace[0] = result;
    trace[1] = result + 1;
    lesson_done();
}
