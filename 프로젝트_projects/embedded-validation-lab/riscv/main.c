#include "../common/validation.h"
static volatile uint32_t scratch[1024];

int main(void)
{
    memory_result_t m = march_c_minus(scratch, 1024);
    uint32_t sig = alu_signature();
    // 이 주소는 우리 testbench의 완료 mailbox. 실제 SoC 주소와 혼동하지 않는다.
    volatile uint32_t *mailbox = (volatile uint32_t *)0x00010000u;
    mailbox[1] = m.errors;
    mailbox[2] = sig;
    mailbox[3] = 1024;
    __asm__ volatile ("fence rw, rw" ::: "memory"); // 결과가 완료 표식보다 앞서 관찰되게.
    mailbox[0] = 0xcafebabeu;
    return 0;
}
