#include "../common/validation.h"
static volatile uint32_t scratch[1024];
volatile struct { uint32_t magic, errors, signature; } debug_result;

static void semihost_write(const char *text)
{
    register uint32_t r0 __asm__("r0") = 4; // SYS_WRITE0: NUL 종료 문자열.
    register const char *r1 __asm__("r1") = text;
    __asm__ volatile ("bkpt 0xab" : "+r"(r0) : "r"(r1) : "memory");
}

static void semihost_exit(uint32_t code)
{
    uint32_t args[2] = {0x20026u, code}; // ADP_Stopped_ApplicationExit.
    register uint32_t r0 __asm__("r0") = 0x20; // SYS_EXIT_EXTENDED.
    register uint32_t *r1 __asm__("r1") = args;
    __asm__ volatile ("bkpt 0xab" : "+r"(r0) : "r"(r1) : "memory");
}

int main(void)
{
    memory_result_t m = march_c_minus(scratch, 1024);
    debug_result.errors = m.errors;
    debug_result.signature = alu_signature();
    // DMB는 접근의 순서를 정한다. volatile은 캐시 flush 또는 barrier가 아니다.
    __asm__ volatile ("dmb sy" ::: "memory");
    debug_result.magic = 0xcafebabeu;
    semihost_write(m.errors == 0 ? "ARM memory PASS\n" : "ARM memory FAIL\n");
    semihost_write(debug_result.signature == EXPECTED_SIGNATURE
                   ? "ARM signature PASS\n" : "ARM signature FAIL\n");
    semihost_exit(m.errors || debug_result.signature != EXPECTED_SIGNATURE);
    for (;;) __asm__ volatile ("wfi");
}
