#ifndef VALIDATION_H
#define VALIDATION_H
#include <stdint.h>
#include <stddef.h>

typedef struct {
    uint32_t errors, first_index, expected, actual;
} memory_result_t;

static inline void observe(memory_result_t *r, uint32_t i,
                           uint32_t expected, uint32_t actual)
{
    if (actual != expected) {
        if (r->errors == 0u) {  // 첫 실패를 보존해야 주소/패턴 원인을 추적 가능.
            r->first_index = i; r->expected = expected; r->actual = actual;
        }
        r->errors++;
    }
}

// 이 함수는 지정된 scratch RAM을 덮어쓴다. 사용 중인 코드/stack을 검사하지 않는다.
static inline memory_result_t march_c_minus(volatile uint32_t *p, size_t n)
{
    memory_result_t r = {0, 0, 0, 0};
    for (size_t i=0; i<n; ++i) p[i] = 0;                    // ↑(w0)
    for (size_t i=0; i<n; ++i) {                           // ↑(r0,w1)
        observe(&r, (uint32_t)i, 0, p[i]); p[i] = UINT32_MAX;
    }
    for (size_t i=0; i<n; ++i) {                           // ↑(r1,w0)
        observe(&r, (uint32_t)i, UINT32_MAX, p[i]); p[i] = 0;
    }
    // i-- > 0을 사용해 unsigned index가 음수가 되는 역방향 반복을 피한다.
    for (size_t i=n; i-- > 0;) {                           // ↓(r0,w1)
        observe(&r, (uint32_t)i, 0, p[i]); p[i] = UINT32_MAX;
    }
    for (size_t i=n; i-- > 0;) {                           // ↓(r1,w0)
        observe(&r, (uint32_t)i, UINT32_MAX, p[i]); p[i] = 0;
    }
    for (size_t i=0; i<n; ++i) observe(&r, (uint32_t)i, 0, p[i]); // ↑(r0)
    return r;  // 메모리 동작은 10*n회. 이것은 software test이지 칩 내부 MBIST가 아님.
}

static inline uint32_t alu_signature(void)
{
    volatile uint32_t x = 0x12345678u;  // 실행 시 접근을 남겨 상수 접기를 방지.
    for (uint32_t i=0; i<256; ++i) {
        // unsigned 연산: overflow가 modulo 2^32로 정의되므로 C undefined behavior 없음.
        x ^= i + 0x9e3779b9u;
        x = (x << 5) | (x >> 27);  // 32bit rotate-left 5.
        x += 0x7f4a7c15u;
    }
    return x;  // Python reference와 비교할 결정적 결과.
}
#endif
