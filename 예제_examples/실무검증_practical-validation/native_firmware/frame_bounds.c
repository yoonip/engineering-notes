/* 교육용 결함 주입: 잘못된 길이 판정도 실제 버퍼 밖을 읽지는 않습니다. */
#include <assert.h>   /* assert: 기대 조건이 거짓이면 실행을 중단합니다. */
#include <stdbool.h>  /* bool: 참과 거짓을 나타냅니다. */
#include <stdint.h>   /* uint32_t: 정확히 32비트인 부호 없는 정수입니다. */
#include <stdio.h>    /* printf: 관측값을 출력합니다. */
#ifdef NDEBUG
#error "This executable requires active assertions; compile with -UNDEBUG."
#endif

enum { HEADER = 4, ITEM = 2, MAX_ITEMS = 1024 };

static uint32_t read_u32_le(const uint8_t *p) {
    return (uint32_t)p[0] | ((uint32_t)p[1] << 8) |
           ((uint32_t)p[2] << 16) | ((uint32_t)p[3] << 24);
}

static uint16_t read_u16_le(const uint8_t *p) {
    return (uint16_t)((uint16_t)p[0] | ((uint16_t)p[1] << 8));
}

static bool faulty_length(uint32_t count, size_t available) {
    /* uint32_t로 좁히면 2^32를 넘는 상위 비트가 사라집니다. */
    uint32_t required = (uint32_t)((uint64_t)HEADER + (uint64_t)count * ITEM);
    return required == available;
}

static bool safe_parse(const uint8_t *p, size_t available, uint32_t *count_out) {
    if (available < HEADER) return false; /* 뺄셈과 헤더 읽기 전에 검사합니다. */
    uint32_t count = read_u32_le(p);
    size_t room = (available - HEADER) / ITEM; /* 곱셈 대신 남은 공간으로 비교합니다. */
    if ((uintmax_t)count > (uintmax_t)room) return false;
    if (count > MAX_ITEMS) return false; /* 메모리 범위와 별개인 서비스 정책입니다. */
    size_t required = HEADER + (size_t)count * ITEM; /* 위의 상한으로 안전해집니다. */
    if (required != available) return false; /* 이 예제는 한 프레임 전체만 받습니다. */
    *count_out = count; /* 성공했을 때만 호출자의 결과를 바꿉니다. */
    return true;
}

int main(void) {
    const uint8_t valid[] = {2, 0, 0, 0, 0x34, 0x12, 0xcd, 0xab};
    const uint8_t huge[] = {0, 0, 0, 0x80};
    const uint8_t empty[] = {0, 0, 0, 0};
    const uint8_t extra[] = {0, 0, 0, 0, 99};
    const uint8_t maximum[] = {0xff, 0xff, 0xff, 0xff};
    uint32_t count = 99;
    assert(safe_parse(valid, sizeof valid, &count) && count == 2);
    assert(read_u16_le(valid + HEADER) == 0x1234);
    assert(read_u16_le(valid + HEADER + ITEM) == 0xabcd);
    assert(!safe_parse(valid, 3, &count));
    assert(!safe_parse(valid, sizeof valid - 1, &count));
    assert(!safe_parse(huge, sizeof huge, &count));
    assert(!safe_parse(maximum, sizeof maximum, &count));
    assert(safe_parse(empty, sizeof empty, &count) && count == 0);
    assert(!safe_parse(extra, sizeof extra, &count));
    assert(faulty_length(read_u32_le(huge), sizeof huge));
    const uint32_t counts[] = {0, 1, 2, 3, 1024, 1025, UINT32_MAX, UINT32_C(0x80000000)};
    uint8_t fixture[2061] = {0};
    unsigned combinations = 0;
    for (size_t i = 0; i < sizeof counts / sizeof counts[0]; ++i) {
        uint32_t n = counts[i];
        for (unsigned b = 0; b < HEADER; ++b) fixture[b] = (uint8_t)(n >> (8 * b));
        for (size_t available = 0; available <= sizeof fixture; ++available) {
            bool expected = n <= MAX_ITEMS && (uint64_t)available == HEADER + (uint64_t)n * ITEM;
            assert(safe_parse(fixture, available, &count) == expected);
            ++combinations;
        }
    }
    unsigned first = read_u16_le(valid + HEADER);
    unsigned second = read_u16_le(valid + HEADER + ITEM);
    unsigned wrong_endian = ((unsigned)valid[HEADER] << 8) | valid[HEADER + 1];
    assert(wrong_endian != first);
    printf("valid_count=2 sample0=%u sample1=%u\n", first, second);
    printf("wrapped_count=%lu faulty_accept=1 safe_accept=0\n",
           (unsigned long)read_u32_le(huge));
    printf("wrong_endian_sample0=%u expected=%u\n", wrong_endian, first);
    printf("length_count_combinations=%u\n", combinations);
    puts("frame contract checks passed");
    return 0;
}
