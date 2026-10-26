#include <stdio.h> /* 실행 결과와 실패 위치 출력 */
#include <stdint.h> /* 32비트 정수 경계 */
#include "iec_std_lib.h" /* matiec의 BOOL·DINT·접근 매크로 */
#include "accessor.h" /* 생성 블록의 선언·읽기·쓰기 매크로 */
#include "POUS.h" /* 실제 ST에서 생성한 블록 자료형 */
#pragma GCC diagnostic push /* 생성된 표준 블록의 경고 범위만 분리 */
#pragma GCC diagnostic ignored "-Wunused-function" /* 이 예제에서 쓰지 않는 표준 FB */
#include "POUS.c" /* 실제 ST에서 생성한 초기화·한 스캔 함수 */
#pragma GCC diagnostic pop /* 직접 작성한 검사에는 원래 경고 적용 */
TIME __CURRENT_TIME = {0, 0}; /* 타이머를 쓰지 않는 호스트 검사 */
static unsigned checks = 0; /* 실제 판정한 조건 수 */
static int compare(TEMPINDICATOR_data__ *block, int expected, unsigned sequence, unsigned scan) { /* 출력 한 번 대조 */
    int actual = __GET_VAR(block->LIT); /* 생성 구조체의 접근자로 출력 읽기 */
    ++checks; /* 성공과 실패 모두 판정 수에 포함 */
    if (actual != expected) { /* 독립 기대값과 다른지 확인 */
        fprintf(stderr, "FAIL plc sequence=%u scan=%u expected=%d actual=%d\n", sequence, scan, expected, actual); /* 재현 위치 */
        return 0; /* 불일치를 호출자에게 전달 */
    } /* 실패 처리 끝 */
    return 1; /* 같은 출력이면 통과 */
} /* 출력 대조 끝 */
static void step(TEMPINDICATOR_data__ *block, int enabled, int32_t temperature10) { /* 입력을 고정한 뒤 한 번 호출 */
    __SET_VAR(block->, ENABLE, , enabled); /* 이번 스캔의 사용 여부 */
    __SET_VAR(block->, TEMPERATURE10, , temperature10); /* 이번 스캔의 정수 표본 */
    TEMPINDICATOR_body__(block); /* 갱신 횟수 한 번이며 실제 시간이 아님 */
} /* 호스트의 한 스캔 호출 끝 */
int main(void) { /* 실행 가능한 검사의 시작 */
    const int32_t temperatures[] = {INT32_MIN, -1, 249, 250, 251, 275, 299, 300, 301, INT32_MAX}; /* 부호·경계·유지 구간 */
    for (unsigned sequence = 0; sequence < 8000; ++sequence) { /* 입력 20가지의 길이3 모든 순서 */
        TEMPINDICATOR_data__ block; /* 서로 영향을 주지 않는 새 인스턴스 */
        TEMPINDICATOR_init__(&block, 0); /* 초기 출력 FALSE와 기본 EN 설정 */
        if (!compare(&block, 0, sequence, 0)) return 1; /* 초기 상태 자체도 확인 */
        unsigned encoded = sequence; /* 20진수 자릿수로 입력 선택 */
        int expected = 0; /* 생성 코드와 독립인 이전 출력 */
        for (unsigned scan = 1; scan <= 3; ++scan) { /* 한 호출씩 상태를 이어가기 */
            unsigned choice = encoded % 20; /* 이번 입력 번호 */
            encoded /= 20; /* 다음 입력 번호로 이동 */
            int enabled = (int)(choice % 2); /* 같은 온도에서 FALSE·TRUE 모두 사용 */
            int32_t temperature10 = temperatures[choice / 2]; /* 입력 표의 정수 값 */
            expected = enabled && (temperature10 >= 300 || (expected && temperature10 > 250)); /* 명세의 유지 조건을 논리식으로 계산 */
            step(&block, enabled, temperature10); /* 실제 번역된 ST 한 번 실행 */
            if (!compare(&block, expected, sequence, scan)) return 1; /* 매 호출 직후 외부 출력 비교 */
        } /* 길이3 입력 순서 끝 */
    } /* 전 순서 대조 끝 */
    TEMPINDICATOR_data__ trace; /* 사람이 따라갈 별도 실행 */
    TEMPINDICATOR_init__(&trace, 0); /* 꺼진 상태에서 시작 */
    const int enabled[] = {1, 1, 1, 1, 1, 1, 0, 1}; /* 사용 중단과 재개 포함 */
    const int32_t input[] = {240, 290, 300, 270, 250, 300, 400, 275}; /* 상승·유지·하강·중단 입력 */
    const int expected[] = {0, 0, 1, 1, 0, 1, 0, 0}; /* 상태표에서 직접 적은 결과 */
    for (unsigned i = 0; i < 8; ++i) { /* 예제 입력을 순서대로 전달 */
        step(&trace, enabled[i], input[i]); /* 입력을 넣고 한 번 갱신 */
        if (!compare(&trace, expected[i], 8000, i + 1)) return 1; /* 별도 고정 기대표 비교 */
        printf("TRACE scan=%u enabled=%d temperature10=%d lit=%d\n", i + 1, enabled[i], (int)input[i], __GET_VAR(trace.LIT)); /* 입력과 결과 */
    } /* 흐름 출력 끝 */
    printf("PASS plc sequences=8000 scans=24008 checks=%u\n", checks); /* 실제 집계 출력 */
    return 0; /* 모든 조건을 만족한 경우만 정상 종료 */
} /* 호스트 검사 끝 */
