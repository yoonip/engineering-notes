/* 직접 작성한 교육 예제: [길이 2바이트][자료] 프레임을 경계 검사 후 복사합니다. */
#include <stddef.h> /* size_t는 메모리 크기를 나타내는 부호 없는 정수형입니다. */
#include <stdint.h> /* uint8_t는 정확히 8비트인 부호 없는 정수형입니다. */
#include <string.h> /* memcpy는 정해진 바이트 수를 복사합니다. */

int copy_frame(const uint8_t *src, size_t len, uint8_t *dst, size_t cap, size_t *written) { /* 포인터와 각각의 실제 용량을 인수로 받습니다. */
    if (written == NULL) return 0; /* 출력 길이를 쓸 주소가 없으면 실패합니다. */
    *written = 0; /* *는 포인터가 가리키는 값이며 실패 시의 출력 길이를 초기화합니다. */
    if (src == NULL || dst == NULL || len < 2) return 0; /* ||는 논리 OR이며 헤더를 읽기 전에 포인터와 길이를 검사합니다. */
    size_t count = ((size_t)src[0] << 8) | src[1]; /* 형 변환·비트 이동·OR로 big-endian 길이를 계산합니다. */
    if (count != len - 2 || count > cap) return 0; /* 먼저 확인한 len에서 2를 빼므로 underflow를 피하고 실제 자료·목적지 길이를 대조합니다. */
    if (count != 0) memcpy(dst, src + 2, count); /* 포인터 덧셈으로 헤더 뒤를 가리키며 용량 검사를 통과한 바이트만 복사합니다. */
    *written = count; /* 성공한 복사 길이를 호출자에게 기록합니다. */
    return 1; /* int의 1을 성공 값으로 반환합니다. */
} /* 함수 본문을 닫습니다. */
