#include <stddef.h> // offsetof로 실제 구조체 멤버 위치 확인
#include <stdio.h> // 검사 결과 한 줄 출력
#include "registers.h" // 실제 PeakRDL 생성물의 선언과 매크로

_Static_assert(BENCH_CSR__VERSION__REVISION_bm == 0xffffffffu, "revision mask"); // 버전 필드의 32비트 마스크
_Static_assert(BENCH_CSR__VERSION__REVISION_bp == 0, "revision position"); // 버전값 시작 비트0
_Static_assert(BENCH_CSR__VERSION__REVISION_bw == 32, "revision width"); // 버전값 폭32
_Static_assert(BENCH_CSR__VERSION__REVISION_reset == 0x10002, "revision reset"); // 명세와 별도로 적은 버전 초기값
_Static_assert(BENCH_CSR__CONTROL__RUN_EN_bm == 0x1, "run mask"); // 실행 허용 비트만 선택
_Static_assert(BENCH_CSR__CONTROL__RUN_EN_bp == 0, "run position"); // 실행 허용 위치0
_Static_assert(BENCH_CSR__CONTROL__RUN_EN_bw == 1, "run width"); // 단일 비트 필드
_Static_assert(BENCH_CSR__CONTROL__RUN_EN_reset == 0, "run reset"); // 기본 실행 금지
_Static_assert(BENCH_CSR__CONTROL__MODE_SEL_bm == 0xe, "mode mask"); // 비트3부터1까지의 마스크1110
_Static_assert(BENCH_CSR__CONTROL__MODE_SEL_bp == 1, "mode position"); // 모드값을 한 비트 왼쪽에 배치
_Static_assert(BENCH_CSR__CONTROL__MODE_SEL_bw == 3, "mode width"); // 모드 범위0부터7
_Static_assert(BENCH_CSR__CONTROL__MODE_SEL_reset == 2, "mode reset"); // 필드 자체의 초기값2
_Static_assert(BENCH_CSR__EVENTS__FLAGS_bm == 0xf, "flags mask"); // 상태 비트3부터0까지만 선택
_Static_assert(BENCH_CSR__EVENTS__FLAGS_bp == 0, "flags position"); // 상태 필드 시작 비트0
_Static_assert(BENCH_CSR__EVENTS__FLAGS_bw == 4, "flags width"); // 네 상태 비트
_Static_assert(BENCH_CSR__EVENTS__FLAGS_reset == 0, "flags reset"); // 초기 상태값0
_Static_assert(offsetof(bench_csr_t, version) == 0, "version offset"); // 첫 레지스터의 바이트 위치
_Static_assert(offsetof(bench_csr_t, control) == 4, "control offset"); // 두 번째 레지스터의 바이트 위치
_Static_assert(offsetof(bench_csr_t, events) == 8, "events offset"); // 세 번째 레지스터의 바이트 위치
_Static_assert(sizeof(bench_csr_t) == 12, "block size"); // 패딩까지 포함한 전체 주소 공간
_Static_assert((BENCH_CSR__CONTROL__MODE_SEL_reset << BENCH_CSR__CONTROL__MODE_SEL_bp) == 4, "control reset word"); // 필드 초기값2를 비트1에 놓으면 레지스터값4

int main(void) { // 메모리 장치 없이 호스트에서 검사 결과 출력
    printf("PASS header assertions=21 size=%zu offsets=%zu,%zu,%zu control_reset=4\n", sizeof(bench_csr_t), offsetof(bench_csr_t, version), offsetof(bench_csr_t, control), offsetof(bench_csr_t, events)); // 컴파일이 통과한 실제 배치 출력
    return 0; // 정적 단언을 모두 만족한 정상 종료
} // 호스트 검사 끝
