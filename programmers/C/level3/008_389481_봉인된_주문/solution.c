#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

static int compare(const void* p, const void* q) { long long a = *(const long long*)p, b = *(const long long*)q; return (a > b) - (a < b); }
char* solution(long long n, const char* bans[], size_t bans_len) {
    long long* removed = malloc(bans_len * sizeof(*removed));
    for (size_t i = 0; i < bans_len; ++i) { removed[i] = 0; for (size_t j = 0; bans[i][j]; ++j) removed[i] = removed[i] * 26 + bans[i][j] - 'a' + 1; }
    qsort(removed, bans_len, sizeof(*removed), compare); for (size_t i = 0; i < bans_len && removed[i] <= n; ++i) ++n;
    char digits[32]; int len = 0; while (n) { --n; digits[len++] = 'a' + n % 26; n /= 26; }
    char* answer = malloc((size_t)len + 1); for (int i = 0; i < len; ++i) answer[i] = digits[len - 1 - i]; answer[len] = '\0'; free(removed);
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
// #include <stdint.h>  // 비트 마스크와 해시 키에 쓸 고정 폭 정수
//
// static int compare(const void* p, const void* q) { long long a = *(const long long*)p, b = *(const long long*)q; return (a > b) - (a < b); }  // 금지 주문의 순번을 작은 값부터 정렬
// char* solution(long long n, const char* bans[], size_t bans_len) {  // 각 주문을 a=1~z=26인 자릿수로 해석하면 길이 우선·사전순과 같은 원래 순번을 얻기
//     long long* removed = malloc(bans_len * sizeof(*removed));  // 금지 주문의 26진 순번 공간 확보
//     for (size_t i = 0; i < bans_len; ++i) { removed[i] = 0; for (size_t j = 0; bans[i][j]; ++j) removed[i] = removed[i] * 26 + bans[i][j] - 'a' + 1; }  // 금지 주문 또는 결과 자리 순서대로 확인; 금지 주문의 26진 순번 / 금지 주문의 문자 위치 갱신
//     qsort(removed, bans_len, sizeof(*removed), compare); for (size_t i = 0; i < bans_len && removed[i] <= n; ++i) ++n;  // 금지 순번을 정렬하고 목표 이하인 금지 주문 수만큼 목표 순번 뒤로 밀기
//     char digits[32]; int len = 0; while (n) { --n; digits[len++] = 'a' + n % 26; n /= 26; }  // 주문 길이 / 뒤에서 꺼낸 주문 문자 저장
//     char* answer = malloc((size_t)len + 1); for (int i = 0; i < len; ++i) answer[i] = digits[len - 1 - i]; answer[len] = '\0'; free(removed);  // n번째 허용 주문 / 금지 주문 또는 결과 자리 공간 확보
//     return answer;  // n번째 허용 주문 반환
// }  // 이 범위 끝

// 풀이 요약
// 각 주문을 a=1~z=26인 자릿수로 해석하면 길이 우선·사전순과 같은 원래 순번을 얻기
// 삭제 순번을 정렬해 목표 앞의 삭제를 하나씩 건너뛴 후, 원래 순번을 다시 문자열로 바꾸기; 주문 길이 L·삭제 수 B에 대해 시간 O(BL+B log B), 공간 O(B)
// 예: 30번째를 찾을 때 d·e·aa·ae가 앞에서 삭제되므로 원래 34번째 주문 ah를 반환
