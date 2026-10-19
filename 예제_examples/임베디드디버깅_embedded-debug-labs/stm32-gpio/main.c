#include "stm32f767xx.h"

/* NUCLEO-F767ZI: green user LED LD1 is connected to PB0. */
volatile uint32_t heartbeat = 0;

int main(void)
{
    RCC->AHB1ENR |= RCC_AHB1ENR_GPIOBEN;
    (void)RCC->AHB1ENR;

    /* Configure PB0 as a general-purpose output. */
    GPIOB->MODER = (GPIOB->MODER & ~GPIO_MODER_MODER0_Msk)
                 | GPIO_MODER_MODER0_0;

    while (1) {
        GPIOB->ODR ^= GPIO_ODR_OD0;
        heartbeat++;
        for (volatile uint32_t delay = 0; delay < 1000000U; ++delay) {
            __NOP();
        }
    }
}
