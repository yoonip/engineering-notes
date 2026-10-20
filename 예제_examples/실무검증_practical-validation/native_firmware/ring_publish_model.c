/* 단일 스레드가 명시적 사건 순서를 열거하는 모델입니다. 실제 ISR 실행은 아닙니다. */
#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdatomic.h>
#ifdef NDEBUG
#error "This executable requires active assertions; compile with -UNDEBUG."
#endif

typedef struct {
    int slot, head, tail, read_value;
    bool available, consumed;
} State;

enum { CAPACITY = 8 };
typedef struct {
    unsigned char bytes[CAPACITY];
    _Atomic unsigned head, tail;
} Spsc;

static bool spsc_push(Spsc *q, unsigned char value) {
    unsigned head = atomic_load_explicit(&q->head, memory_order_relaxed);
    unsigned next = (head + 1u) % CAPACITY;
    unsigned tail = atomic_load_explicit(&q->tail, memory_order_acquire);
    if (next == tail) return false; // 한 칸을 비워 가득 참과 비어 있음을 구별합니다.
    q->bytes[head] = value;
    atomic_store_explicit(&q->head, next, memory_order_release); // 데이터 뒤에 공개합니다.
    return true;
}

static bool spsc_pop(Spsc *q, unsigned char *out) {
    unsigned tail = atomic_load_explicit(&q->tail, memory_order_relaxed);
    unsigned head = atomic_load_explicit(&q->head, memory_order_acquire);
    if (tail == head) return false;
    *out = q->bytes[tail];
    atomic_store_explicit(&q->tail, (tail + 1u) % CAPACITY, memory_order_release);
    return true;
}

static bool simulate(const char *schedule, bool correct_order) {
    State s = {0};
    unsigned producer_step = 0, consumer_step = 0;
    for (unsigned i = 0; i < 4; ++i) {
        if (schedule[i] == 'P') {
            bool write_slot = correct_order ? producer_step == 0 : producer_step == 1;
            if (write_slot) s.slot = 42; else s.head = 1;
            ++producer_step;
        } else {
            if (consumer_step == 0) s.available = s.head != s.tail;
            else if (s.available) {
                s.read_value = s.slot;
                s.tail = 1;
                s.consumed = true;
            }
            ++consumer_step;
        }
    }
    return s.consumed && s.read_value != 42;
}

int main(void) {
    const char *orders[] = {"PPCC", "PCPC", "PCCP", "CPPC", "CPCP", "CCPP"};
    unsigned bad = 0, corrected_bad = 0;
    for (unsigned i = 0; i < sizeof orders / sizeof orders[0]; ++i) {
        bool wrong = simulate(orders[i], false);
        bool right = simulate(orders[i], true);
        bad += wrong;
        corrected_bad += right;
        printf("schedule=%s faulty_stale_read=%d corrected_stale_read=%d\n",
               orders[i], wrong, right);
    }
    assert(bad == 1 && corrected_bad == 0);

    /* used++와 used--가 각각 읽기/쓰기로 나뉘는 별도의 카운터 유실 예입니다. */
    int used = 1;
    int consumer_local = used; // 전경 소비자가 이전 카운터를 읽고 중단됩니다.
    int producer_local = used; // 인터럽트 생산자도 동일한 이전 값을 읽습니다.
    used = producer_local + 1;
    used = consumer_local - 1; // 나중 쓰기가 먼저 쓰기를 덮어씁니다.
    assert(used == 0); // 순차적으로 +1,-1이면 기대값은 1입니다.
    printf("shared_counter_observed=%d expected=1\n", used);
    Spsc q = {0};
    atomic_init(&q.head, 0); // 공유를 시작하기 전에 원자 객체의 상태를 초기화합니다.
    atomic_init(&q.tail, 0);
    unsigned char value = 0;
    assert(!spsc_pop(&q, &value));
    for (unsigned i = 0; i < CAPACITY - 1; ++i) assert(spsc_push(&q, (unsigned char)i));
    assert(!spsc_push(&q, 99));
    for (unsigned i = 0; i < CAPACITY - 1; ++i) {
        assert(spsc_pop(&q, &value));
        assert(value == i);
    }
    for (unsigned i = 0; i < 10000; ++i) {
        assert(spsc_push(&q, (unsigned char)i));
        assert(spsc_pop(&q, &value));
        assert(value == (unsigned char)i);
    }
    printf("spsc_capacity=7 wrap_pairs=10000 head_lock_free=%d\n", atomic_is_lock_free(&q.head));
    puts("schedules=6 faulty_stale_reads=1 corrected_stale_reads=0");
    puts("ring publication model checks passed");
    return 0;
}
