/* 직접 작성한 C 검증 코드이며 외부 통신·실제 장치를 사용하지 않습니다. */
#ifdef NDEBUG /* assert를 제거하는 빌드라면 검사 성공을 표시하지 않습니다. */
#error "Tests require assertions: compile with -UNDEBUG" /* 컴파일을 중단해 검사 누락을 알립니다. */
#endif /* NDEBUG 검사 구간을 닫습니다. */
#include <assert.h> /* assert는 기대 조건이 거짓이면 검사를 중단합니다. */
#include <stdio.h> /* printf는 검사 결과를 표준 출력에 씁니다. */
#include "frame_bounds.c" /* 이 실습의 작은 구현을 같은 번역 단위에 포함합니다. */
int main(void) { /* 운영체제가 호출하는 검사 시작 함수입니다. */
    uint8_t input[5] = {0, 3, 10, 20, 30}; /* 길이3과 실제 자료3바이트를 준비합니다. */
    uint8_t output[5] = {99, 99, 99, 99, 99}; /* 앞뒤 경계 확인용 값과 목적지를 준비합니다. */
    size_t count = 99; /* 복사 길이의 초기값입니다. */
    assert(copy_frame(input, 5, output + 1, 3, &count) == 1); /* 정확한 목적지 용량은 허용해야 합니다. */
    assert(count == 3 && output[1] == 10 && output[3] == 30 && output[0] == 99 && output[4] == 99); /* 자료와 양끝 경계를 독립 대조합니다. */
    assert(copy_frame(input, 5, output + 1, 2, &count) == 0 && count == 0); /* 한 바이트 작은 목적지를 거부합니다. */
    assert(copy_frame(input, 1, output, 5, &count) == 0); /* 헤더가 모자라는 입력을 거부합니다. */
    assert(copy_frame(NULL, 5, output, 5, &count) == 0); /* NULL 입력 포인터를 거부합니다. */
    assert(copy_frame(input, 5, NULL, 5, &count) == 0); /* NULL 출력 포인터를 거부합니다. */
    assert(copy_frame(input, 5, output, 5, NULL) == 0); /* NULL 길이 포인터를 거부합니다. */
    uint8_t empty[2] = {0, 0}; /* 길이가0인 정상 프레임입니다. */
    assert(copy_frame(empty, 2, output, 0, &count) == 1 && count == 0); /* 빈 자료와 용량0은 유효합니다. */
    for (unsigned n = 0; n < 65536; ++n) { /* 헤더의 모든 16비트 길이를 전수 검사합니다. */
        input[0] = (uint8_t)(n >> 8); /* 상위8비트를 헤더에 씁니다. */
        input[1] = (uint8_t)n; /* 하위8비트를 헤더에 씁니다. */
        memset(output, 99, sizeof output); /* 입력마다 목적지·경계의 기준값을 초기화합니다. */
        int result = copy_frame(input, 5, output + 1, 3, &count); /* 실제 자료 길이는 항상3바이트입니다. */
        assert(result == (n == 3)); /* 독립 기대값: 헤더가3일 때만 받아야 합니다. */
        if (n != 3) assert(count == 0 && output[1] == 99 && output[3] == 99); /* 거부된 입력은 자료를 복사하면 안 됩니다. */
        assert(output[0] == 99 && output[4] == 99); /* 모든 경우 앞뒤 경계가 유지돼야 합니다. */
    } /* 전수 반복을 닫습니다. */
    printf("C boundaries: 7 cases + 65536 length headers passed\n"); /* 실제 완료한 검사 범위를 출력합니다. */
    return 0; /* 성공 종료 코드입니다. */
} /* main을 닫습니다. */
