#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

long long solution(int a, int b, int g[], size_t g_len, int s[], size_t s_len, int w[], size_t w_len, int t[], size_t t_len) {
    (void)s_len; (void)w_len; (void)t_len;
    long long low = 0, high = 400000000000000LL;
    while (low < high) {
        long long mid = low + (high - low) / 2, gold = 0, silver = 0, total = 0;
        for (size_t i = 0; i < g_len; ++i) {
            long long capacity = ((mid + t[i]) / (2LL * t[i])) * w[i];
            gold += g[i] < capacity ? g[i] : capacity; silver += s[i] < capacity ? s[i] : capacity;
            long long all = (long long)g[i] + s[i]; total += all < capacity ? all : capacity;
        }
        if (gold >= a && silver >= b && total >= (long long)a + b) high = mid; else low = mid + 1;
    }
    return low;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
// #include <stdint.h>  // 비트 마스크와 해시 키에 쓸 고정 폭 정수
//
// long long solution(int a, int b, int g[], size_t g_len, int s[], size_t s_len, int w[], size_t w_len, int t[], size_t t_len) {  // 주어진 시간 안에 운반 가능한 최대 금·은·총량을 계산; 개별량이 각각 충분해도 같은 트럭 용량을 중복 사용하지 않도록 합계 조건이 필요하기
//     (void)s_len; (void)w_len; (void)t_len;  // (void)s_len; (void)w_len; (void)t_len
//     long long low = 0, high = 400000000000000LL;  // 운반 완료 시간 하한 / 시간 상한 저장
//     while (low < high) {  // 이분 탐색 범위가 한 값으로 좁혀질 때까지 가능 여부를 확인
//         long long mid = low + (high - low) / 2, gold = 0, silver = 0, total = 0;  // 시험할 운반 시간 / 그 시간에 옮길 수 있는 금 / 그 시간에 옮길 수 있는 은 / 금과 은을 함께 옮길 수 있는 양 저장
//         for (size_t i = 0; i < g_len; ++i) {  // 도시 번호 순서대로 확인
//             long long capacity = ((mid + t[i]) / (2LL * t[i])) * w[i];  // 현재 도시의 시간 내 운송 용량 저장
//             gold += g[i] < capacity ? g[i] : capacity; silver += s[i] < capacity ? s[i] : capacity;  // 그 시간에 옮길 수 있는 금 / 도시 번호 / 현재 도시의 시간 내 운송 용량 더해 누적
//             long long all = (long long)g[i] + s[i]; total += all < capacity ? all : capacity;  // 현재 도시의 금과 은 합 저장
//         }  // 이 범위 끝
//         if (gold >= a && silver >= b && total >= (long long)a + b) high = mid; else low = mid + 1;  // 금·은 각각의 수요와 전체 수요를 모두 옮길 수 있으면 시간 상한 줄이기
//     }  // 이 범위 끝
//     return low;  // 운반 완료 시간 하한 반환
// }  // 이 범위 끝

// 풀이 요약
// 주어진 시간 안에 운반 가능한 최대 금·은·총량을 계산; 개별량이 각각 충분해도 같은 트럭 용량을 중복 사용하지 않도록 합계 조건이 필요하기
// 시간이 늘면 운반 가능량이 줄지 않으므로 이진 탐색으로 최소 시간을 찾기; 마지막 운반은 편도만 필요하기; 도시 수 N·시간 상한 T에 대해 시간 O(N log T), 추가 공간 O(1)
// 예: 편도 10·적재량 7인 트럭은 10,30,50에 각각 배달하기; 금·은 합계 20을 운반하려면 세 번 필요해 답은 50
