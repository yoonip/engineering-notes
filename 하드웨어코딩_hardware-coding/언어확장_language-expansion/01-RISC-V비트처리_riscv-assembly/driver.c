#include <stdint.h> // 정확한32비트·8비트 정수 자료형
extern uint32_t update_field(uint32_t original, uint32_t value, uint32_t shift, uint32_t width); // a0~a3 인자로 호출할 어셈블리 함수
extern uint32_t byte_sum(const uint8_t *bytes, uint32_t length); // RAM 바이트 검사합 함수
extern uint32_t abi_probe(void); // s레지스터와 스택 정렬의 별도 검사
_Static_assert(sizeof(uint32_t) == 4, "u32 width"); // 32비트 기준의 C 검사 전제
_Static_assert(sizeof(void *) == 4, "RV32 pointer"); // 실제32비트 타깃으로 빌드되는지 확인
static uint32_t field_checks, checksum_checks, abi_checks; // 실제 함수 결과 비교 수
static volatile uint8_t *const uart = (volatile uint8_t *)0x10000000u; // QEMU virt의 로그 출력 MMIO
static volatile uint32_t *const finisher = (volatile uint32_t *)0x00100000u; // QEMU 전용 종료 장치의 정렬된 워드 주소
static void put_char(char value) { // UART를 통한 한 문자 출력
    while ((uart[5] & 0x20u) == 0) { } // 송신 레지스터가 빌 때까지 MMIO 상태 확인
    uart[0] = (uint8_t)value; // 한 문자를 장치 레지스터에 기록
} // 문자 출력 끝
static void put_text(const char *text) { // 0으로 끝나는 로그 문자열 출력
    while (*text) put_char(*text++); // 문자열 끝까지 한 글자씩 전송
} // 문자열 출력 끝
static void put_hex(uint32_t value) { // 라이브러리 나눗셈 없이8자리16진수 출력
    const char *digits = "0123456789abcdef"; // 각4비트의 출력 문자 표
    for (int shift = 28; shift >= 0; shift -= 4) put_char(digits[(value >> shift) & 15u]); // 높은4비트부터 차례로 출력
} // 32비트 수 출력 끝
static _Noreturn void finish(uint32_t status) { // QEMU 종료와 실패 코드 전달
    while ((uart[5] & 0x40u) == 0) { } // 남은 로그의 송신 완료 확인
    __asm__ volatile ("fence iorw, iorw" ::: "memory"); // 컴파일러와 ISA 수준에서 앞선 I/O 순서 구분
    *finisher = status ? (status << 16) | 0x3333u : 0x5555u; // 이 가상 장치의 실패 또는 정상 종료 값
    for (;;) { __asm__ volatile ("j ."); } // 장치가 없을 때 무관한 주소로 실행하지 않기
} // 플랫폼 전용 종료 함수 끝
static void require_equal(uint32_t actual, uint32_t expected, const char *name) { // 어셈블리 결과와 독립 기준 비교
    if (actual != expected) { // 첫 잘못된 결과 분리
        put_text("FAIL RV32I "); put_text(name); put_text(" expected="); put_hex(expected); // 기준값 기록
        put_text(" actual="); put_hex(actual); put_text("\n"); // 실제 결과 기록
        finish(1); // 실패 코드로 실제 CPU 실행 종료
    } // 결과 불일치 처리 끝
} // 공통 비교 함수 끝
static uint32_t reference_field(uint32_t original, uint32_t value, uint32_t shift, uint32_t width) { // 마스크식 대신 비트별 덮어쓰기 기준
    uint32_t result = original; // 필드 밖의 비트는 원래값에서 시작
    for (uint32_t bit = 0; bit < 32; ++bit) { // 모든 결과 비트 독립 확인
        if (bit >= shift && bit - shift < width) { // 해당 위치가 유효 필드 안인지 검사
            uint32_t mask = 1u << bit; // 0~31 사이의 한 비트 마스크
            if ((value >> (bit - shift)) & 1u) result |= mask; // 새 비트가1이면 해당 위치 설정
            else result &= ~mask; // 새 비트가0이면 해당 위치 해제
        } // 필드 안의 선택 갱신 끝
    } // 32개 비트 기준 완성
    return result; // 독립적인 새 레지스터값 반환
} // 비트필드 기준 함수 끝
static uint32_t reference_sum(const uint8_t *bytes, uint32_t length) { // 역방향으로 합산하는 독립 바이트 기준
    uint32_t result = 0; // 빈 배열의 합0
    while (length > 0) result += bytes[--length]; // 어셈블리와 반대 순서로 같은 RAM 바이트 합산
    return result; // 32비트 모듈러 합 반환
} // 검사합 기준 함수 끝
int main(void) { // QEMU의 RISC-V CPU에서 실행할 C 검사 드라이버
    static const uint32_t patterns[6] = {0u, 0xffffffffu, 0x80000000u, 0x55555555u, 0xaaaaaaaau, 0x12345678u}; // 0·전체1·최상위 비트·교대·혼합 패턴
    static const uint8_t demo[4] = {0x00u, 0x7fu, 0x80u, 0xffu}; // 부호 확장 오류도 구분할 네 바이트
    uint8_t bytes[68]; // 오프셋0~3에서 최대64바이트를 읽을 RAM 버퍼
    uint32_t field_demo = update_field(0xf0f00f0fu, 0x1abu, 8, 8); // 넘치는 새 비트도 잘라 넣는 실제 어셈블리 호출
    require_equal(field_demo, 0xf0f0ab0fu, "field demo"); ++field_checks; // 직접 계산한 결과와 대조
    put_text("TRACE field result="); put_hex(field_demo); put_text("\n"); // 실제 호출 결과를 로그로 확인
    for (uint32_t shift = 0; shift < 32; ++shift) { // 필드 시작의 모든 유효 위치
        for (uint32_t width = 0; width <= 32 - shift; ++width) { // 빈 필드와 전체32비트를 포함한 폭
            for (uint32_t old = 0; old < 6; ++old) { // 원래값의 여섯 패턴
                for (uint32_t value = 0; value < 6; ++value) { // 새값의 여섯 패턴
                    uint32_t actual = update_field(patterns[old], patterns[value], shift, width); // 외부 어셈블리 함수 실행
                    require_equal(actual, reference_field(patterns[old], patterns[value], shift, width), "field cross product"); // 비트별 C 기준과 비교
                    ++field_checks; // 실제 비트필드 비교 수 누적
                } // 새값 패턴 끝
            } // 원래값 패턴 끝
        } // 시작 위치에 맞는 폭 끝
    } // 전체560개 시작·폭 조합 끝
    uint32_t sum_demo = byte_sum(demo, 4); // 0·127·128·255의 실제 어셈블리 검사합
    require_equal(sum_demo, 510u, "unsigned byte demo"); ++checksum_checks; // lbu의 부호 없는 결과 확인
    put_text("TRACE byte sum="); put_hex(sum_demo); put_text("\n"); // 실제 합510을16진수로 출력
    require_equal(byte_sum((const uint8_t *)0, 0), 0, "empty null pointer"); ++checksum_checks; // 길이0이면 주소를 읽지 않는 경계
    for (uint32_t index = 0; index < 68; ++index) bytes[index] = (uint8_t)(index * 37u + 11u); // 재현 가능한 RAM 자료 초기화
    for (uint32_t offset = 0; offset < 4; ++offset) { // 워드 경계와 어긋나는 바이트 주소도 사용
        for (uint32_t length = 0; length <= 64; ++length) { // 빈 길이부터 버퍼 안의 최대 길이
            require_equal(byte_sum(bytes + offset, length), reference_sum(bytes + offset, length), "byte ranges"); // 순방향 ASM과 역방향 C의 합 비교
            ++checksum_checks; // 실제 검사합 비교 수 누적
        } // 길이 경계 검사 끝
    } // 네 시작 오프셋 검사 끝
    require_equal(abi_probe(), 0, "callee saved registers and aligned stack"); ++abi_checks; // 12개 s레지스터와 호출 뒤 스택 정렬 확인
    put_text("PASS RV32I field_checks="); put_hex(field_checks); // 실제 비트필드 검사 수
    put_text(" checksum_checks="); put_hex(checksum_checks); // 실제 바이트 합 검사 수
    put_text(" abi_checks="); put_hex(abi_checks); // 별도 ABI 검사 시나리오 수
    put_text(" total_checks="); put_hex(field_checks + checksum_checks + abi_checks); put_text("\n"); // 전체 결과 집계
    finish(0); // 성공 로그 뒤 QEMU를 정상 종료
} // 독립 검사 드라이버 끝
