#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

int* solution(int e, int starts[], size_t starts_len) {
    int* divisors = malloc(((size_t)e + 1) * sizeof(*divisors)); int* winner = malloc(((size_t)e + 1) * sizeof(*winner));
    for (int i = 0; i <= e; ++i) divisors[i] = 1;
    for (int prime = 2; prime <= e; ++prime) if (divisors[prime] == 1) {
        long long power = prime; int exponent = 1;
        while (power <= e) { for (int multiple = (int)power; multiple <= e; multiple += (int)power) divisors[multiple] = divisors[multiple] / exponent * (exponent + 1); power *= prime; ++exponent; }
    }
    int best = e;
    for (int i = e; i >= 1; --i) { if (divisors[i] >= divisors[best]) best = i; winner[i] = best; }
    int* answer = malloc(starts_len * sizeof(*answer)); for (size_t i = 0; i < starts_len; ++i) answer[i] = winner[starts[i]];
    free(divisors); free(winner);
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
// int* solution(int e, int starts[], size_t starts_len) {  // 정수 x가 곱셈표에 나타나는 횟수는 x의 약수 개수입니다. 각 소인수의 지수가 a이면 약수 개수에 a+1을 곱하는 원리를 체에 적용합니다.
//     int* divisors = malloc(((size_t)e + 1) * sizeof(*divisors)); int* winner = malloc(((size_t)e + 1) * sizeof(*winner));  // 정수별 약수 개수 / 각 시작 이상에서 최선인 정수 공간 확보
//     for (int i = 0; i <= e; ++i) divisors[i] = 1;  // 뒤에서 확인할 정수 또는 질의 순서대로 확인; 정수별 약수 개수 갱신
//     for (int prime = 2; prime <= e; ++prime) if (divisors[prime] == 1) {  // 아직 약수 정보가 없는 수를 소수로 잡아 배수의 약수 수 계산
//         long long power = prime; int exponent = 1;  // 현재 소수 거듭제곱 / 해당 소수의 지수 저장
//         while (power <= e) { for (int multiple = (int)power; multiple <= e; multiple += (int)power) divisors[multiple] = divisors[multiple] / exponent * (exponent + 1); power *= prime; ++exponent; }  // 소수 거듭제곱의 배수마다 해당 소수 지수에 따른 약수 수 갱신
//     }  // 이 범위 끝
//     int best = e;  // 지금까지 약수가 가장 많은 정수 저장
//     for (int i = e; i >= 1; --i) { if (divisors[i] >= divisors[best]) best = i; winner[i] = best; }  // 뒤에서 확인할 정수 또는 질의 순서대로 확인; 지금까지 약수가 가장 많은 정수 / 각 시작 이상에서 최선인 정수 갱신
//     int* answer = malloc(starts_len * sizeof(*answer)); for (size_t i = 0; i < starts_len; ++i) answer[i] = winner[starts[i]];  // 시작값별 최선의 정수 / 뒤에서 확인할 정수 또는 질의 공간 확보
//     free(divisors); free(winner);  // 정수별 약수 개수 / 각 시작 이상에서 최선인 정수 임시 공간 정리
//     return answer;  // 시작값별 최선의 정수 반환
// }  // 이 범위 끝

// 풀이 요약
// 정수 x가 곱셈표에 나타나는 횟수는 x의 약수 개수입니다. 각 소인수의 지수가 a이면 약수 개수에 a+1을 곱하는 원리를 체에 적용합니다.
// 끝값 E부터 1까지 내려오며 각 구간 [i,E]의 최선인 수를 winner[i]에 저장합니다. 약수 개수가 같으면 더 작은 수를 고르고, Q개 질의는 배열에서 바로 조회합니다. 시간은 O(E log log E+Q), 반환 배열을 포함한 공간은 O(E+Q)입니다.
// 예를 들어 1~8에서는 6과 8의 약수가 각각 네 개로 가장 많습니다. [1,8]과 [3,8]의 답은 더 작은 6이고, [7,8]의 답은 8입니다.
