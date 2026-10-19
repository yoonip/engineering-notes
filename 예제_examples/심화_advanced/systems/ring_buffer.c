/* 단일 실행 흐름용 고정 크기 바이트 큐. ISR·스레드 간 공유 규약은 별도다. */
#include <assert.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>

enum { CAPACITY = 7 };
typedef struct {
    unsigned char bytes[CAPACITY];
    size_t head, tail, used;
} Ring;

static bool push(Ring *q, unsigned char value) {
    if (q->used == CAPACITY) return false;
    q->bytes[q->head] = value;
    q->head = (q->head + 1u) % CAPACITY;
    ++q->used;
    return true;
}

static bool pop(Ring *q, unsigned char *out) {
    if (q->used == 0u) return false;
    *out = q->bytes[q->tail];
    q->tail = (q->tail + 1u) % CAPACITY;
    --q->used;
    return true;
}

int main(void) {
    Ring q = {0};
    unsigned char value = 0;
    assert(!pop(&q, &value));
    for (unsigned i = 0; i < 200u; ++i) {
        assert(push(&q, (unsigned char)i));
        assert(pop(&q, &value));
        assert(value == (unsigned char)i);
    }
    for (unsigned i = 0; i < CAPACITY; ++i) assert(push(&q, (unsigned char)i));
    assert(!push(&q, 99));
    for (unsigned i = 0; i < CAPACITY; ++i) {
        assert(pop(&q, &value));
        assert(value == (unsigned char)i);
    }
    puts("ring invariants passed");
    return 0;
}
