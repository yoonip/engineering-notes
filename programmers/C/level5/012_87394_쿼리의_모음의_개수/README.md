# 쿼리의 모음의 개수 — C

[레벨 5 목록](../README.md) · [언어별 목록](../../README.md) · [문제](https://school.programmers.co.kr/learn/courses/30/lessons/87394?language=c)

레벨 5 · C

## 풀이 요약

목표를 넘지 않는 쿼리만 허용하면, 각 i가 높이 a[i]의 쿼리에 한 번 이상 덮이는 것이 최종 배열과 같아지는 조건.

구간의 최솟값 h 위치들을 나누면 높이 h 쿼리는 이 구간 안에서만 움직이고, 더 높은 쿼리는 최솟값 사이 구간들로 분리됨. 부모 높이와 h 사이 빠진 높이는 무제약 쿼리 종류로 누적.

높이 h의 필수 위치를 못 덮는 사건에 포함배제 적용. 선택한 미덮임 위치 사이 길이가 L이면 허용 부분구간 수는 L(L+1)/2라 그 쿼리들의 지수생성함수는 exp(L(L+1)z/2).

선택한 미덮임 위치들을 왼쪽부터 잇는 DP로 포함배제를 계산. 실제 위치를 선택할 때만 부호를 뒤집고, 가상 오른쪽 경계에서 덮기 조건의 합계를 받음.

독립된 높이별 생성함수와 무제약 exp(Uz)를 곱한 q차 계수에 q!를 곱하면 순서를 구분한 q개 쿼리 수. 같은 쿼리를 여러 번 고르는 경우도 지수함수 계수에 포함.

배열 길이 N, 쿼리 수 Q에서 시간 O(N²Q²), 공간 O(NQ). 모든 계수는 998244353으로 계산.

## 코드와 줄별 설명

[제출 코드](solution.c) · [사이트 채점 기록](grading.json) · [별도 로컬 검사](local_checks.json)

~~~c
#include <stddef.h>
#include <string.h>

#define MOD 998244353

typedef struct {
    int left, right, floor;
} Range;

static void multiply(int product[51], const int factor[51], int q) {
    int next[51] = {0};
    for (int used = 0; used <= q; ++used) {
        if (product[used] == 0) continue;
        for (int added = 0; used + added <= q; ++added) {
            next[used + added] = (int)((next[used + added] + 1LL * product[used] * factor[added]) % MOD);
        }
    }
    memcpy(product, next, sizeof(next));
}

int solution(int q, int a[], size_t a_len) {
    int n = (int)a_len;
    int inverse[51] = {0};
    inverse[1] = 1;
    for (int degree = 2; degree <= q; ++degree) {
        inverse[degree] = (int)(MOD - 1LL * (MOD / degree) * inverse[MOD % degree] % MOD);
    }
    int exponential[51][51] = {{0}};
    for (int length = 0; length <= n; ++length) {
        int intervals = length * (length + 1) / 2;
        exponential[length][0] = 1;
        for (int degree = 1; degree <= q; ++degree) {
            exponential[length][degree] = (int)(1LL * exponential[length][degree - 1] * intervals % MOD * inverse[degree] % MOD);
        }
    }
    int product[51] = {1};
    long long unrestricted = 0;
    Range stack[51];
    int top = 0;
    stack[top++] = (Range){0, n - 1, 0};
    while (top > 0) {
        Range range = stack[--top];
        int minimum = a[range.left];
        for (int i = range.left + 1; i <= range.right; ++i) if (a[i] < minimum) minimum = a[i];
        int length = range.right - range.left + 1;
        unrestricted += 1LL * (minimum - range.floor - 1) * length * (length + 1) / 2;
        int positions[52], count = 0;
        positions[count++] = range.left - 1;
        for (int i = range.left; i <= range.right; ++i) if (a[i] == minimum) positions[count++] = i;
        positions[count++] = range.right + 1;
        int paths[52][51] = {{0}};
        paths[0][0] = 1;
        for (int boundary = 1; boundary < count; ++boundary) {
            for (int previous = 0; previous < boundary; ++previous) {
                int gap = positions[boundary] - positions[previous] - 1;
                for (int used = 0; used <= q; ++used) {
                    if (paths[previous][used] == 0) continue;
                    for (int added = 0; used + added <= q; ++added) {
                        int term = (int)(1LL * paths[previous][used] * exponential[gap][added] % MOD);
                        int* cell = &paths[boundary][used + added];
                        if (boundary + 1 == count) {
                            *cell += term;
                            if (*cell >= MOD) *cell -= MOD;
                        } else {
                            *cell -= term;
                            if (*cell < 0) *cell += MOD;
                        }
                    }
                }
            }
        }
        multiply(product, paths[count - 1], q);
        for (int boundary = 1; boundary < count; ++boundary) {
            int left = positions[boundary - 1] + 1, right = positions[boundary] - 1;
            if (left <= right) stack[top++] = (Range){left, right, minimum};
        }
    }
    int free_queries[51] = {1};
    for (int degree = 1; degree <= q; ++degree) {
        free_queries[degree] = (int)(1LL * free_queries[degree - 1] * (unrestricted % MOD) % MOD * inverse[degree] % MOD);
    }
    long long coefficient = 0, factorial = 1;
    for (int used = 0; used <= q; ++used) {
        coefficient = (coefficient + 1LL * product[used] * free_queries[q - used]) % MOD;
        if (used > 0) factorial = factorial * used % MOD;
    }
    return (int)(coefficient * factorial % MOD);
}

// 전체 코드 줄별 설명
// #include <stddef.h>  // 입력 배열 길이를 받을 size_t
// #include <string.h>  // 다항식 곱셈 결과를 원래 배열로 복사할 memcpy
//
// #define MOD 998244353  // 경우의 수를 계산할 소수 나머지
//
// typedef struct {  // 최솟값으로 나눈 연속 구간과 바로 아래 높이를 함께 보관
//     int left, right, floor;  // 구간 양끝과 부모 구간의 최솟값
// } Range;  // 처리할 구간 자료형 끝
//
// static void multiply(int product[51], const int factor[51], int q) {  // q차까지만 필요한 두 지수생성함수의 계수 곱셈
//     int next[51] = {0};  // 곱셈 중 기존 계수가 덮이지 않게 별도 결과 배열
//     for (int used = 0; used <= q; ++used) {  // 앞서 처리한 쿼리 종류들의 쿼리 수
//         if (product[used] == 0) continue;  // 계수가 0인 차수는 곱셈을 생략
//         for (int added = 0; used + added <= q; ++added) {  // 새 쿼리 종류가 차지할 개수를 합쳐 q차까지만 계산
//             next[used + added] = (int)((next[used + added] + 1LL * product[used] * factor[added]) % MOD);  // 같은 총 쿼리 수가 되는 계수 곱을 누적
//         }  // 현재 차수에 새 인자를 곱하는 작업 끝
//     }  // 잘린 다항식 곱셈 끝
//     memcpy(product, next, sizeof(next));  // 계산한 곱을 누적 생성함수로 교체
// }  // 생성함수 곱셈 끝
//
// int solution(int q, int a[], size_t a_len) {  // 구간 chmax 쿼리 q개로 목표 배열을 만드는 순서열 수 반환
//     int n = (int)a_len;  // 목표 배열 길이
//     int inverse[51] = {0};  // k차 계수를 만들 때 나눌 정수 k의 모듈러 역원
//     inverse[1] = 1;  // 1로 나누는 연산은 그대로 유지
//     for (int degree = 2; degree <= q; ++degree) {  // 소수 나머지에서 2~q의 역원을 선형 시간에 준비
//         inverse[degree] = (int)(MOD - 1LL * (MOD / degree) * inverse[MOD % degree] % MOD);  // 이미 구한 더 작은 나머지의 역원을 이용
//     }  // 차수별 나눗셈 준비 끝
//     int exponential[51][51] = {{0}};  // 길이 L의 구간 안 모든 부분구간 수에 대한 exp(L(L+1)z/2) 계수
//     for (int length = 0; length <= n; ++length) {  // 포함배제에서 생길 수 있는 빈 구간 길이를 모두 준비
//         int intervals = length * (length + 1) / 2;  // 그 길이 안에서 고를 수 있는 비어 있지 않은 쿼리 구간 수
//         exponential[length][0] = 1;  // 쿼리를 0개 쓰는 계수는 1
//         for (int degree = 1; degree <= q; ++degree) {  // 직전 계수에 구간 수를 곱하고 차수로 나누기
//             exponential[length][degree] = (int)(1LL * exponential[length][degree - 1] * intervals % MOD * inverse[degree] % MOD);  // intervals^degree/degree!를 모듈러로 저장
//         }  // 한 길이의 지수생성함수 준비 끝
//     }  // 모든 빈 구간 길이의 계수 준비 끝
//     int product[51] = {1};  // 높이별 덮기 조건을 아직 곱하지 않은 생성함수 1
//     long long unrestricted = 0;  // 목표 높이와 일치하는 정점이 없어 덮기 의무가 없는 쿼리 종류 수
//     Range stack[51];  // 최솟값으로 분리한 높은 구간들을 처리할 작은 스택
//     int top = 0;  // 대기 중인 구간 수
//     stack[top++] = (Range){0, n - 1, 0};  // 0 배열 위에 전체 목표 구간을 만드는 작업부터 시작
//     while (top > 0) {  // 모든 최솟값 높이의 독립된 덮기 조건을 처리
//         Range range = stack[--top];  // 마지막에 추가한 연속 구간 꺼내기
//         int minimum = a[range.left];  // 현재 구간의 최솟값을 찾을 시작값
//         for (int i = range.left + 1; i <= range.right; ++i) if (a[i] < minimum) minimum = a[i];  // 높이가 minimum인 쿼리로 반드시 덮어야 할 정점들을 구분
//         int length = range.right - range.left + 1;  // 현재 높이 쿼리가 자유롭게 고를 수 있는 전체 구간 길이
//         unrestricted += 1LL * (minimum - range.floor - 1) * length * (length + 1) / 2;  // 부모 높이와 현재 최솟값 사이의 높이들은 목표 정점이 없어 모든 부분구간 쿼리가 무제약
//         int positions[52], count = 0;  // 최솟값 위치들과 양끝의 가상 경계 저장
//         positions[count++] = range.left - 1;  // 선택한 미덮임 위치가 하나도 없을 때의 왼쪽 시작 경계
//         for (int i = range.left; i <= range.right; ++i) if (a[i] == minimum) positions[count++] = i;  // 현재 높이의 쿼리에 적어도 한 번 덮여야 하는 모든 위치
//         positions[count++] = range.right + 1;  // 포함배제 합계를 받을 오른쪽 가상 경계
//         int paths[52][51] = {{0}};  // 선택한 미덮임 위치들을 왼쪽부터 잇는 포함배제 생성함수 DP
//         paths[0][0] = 1;  // 왼쪽 가상 경계만 놓인 빈 선택의 계수
//         for (int boundary = 1; boundary < count; ++boundary) {  // 다음 미덮임 위치 또는 마지막 가상 경계를 선택
//             for (int previous = 0; previous < boundary; ++previous) {  // 바로 직전에 고른 경계의 위치를 모두 시도
//                 int gap = positions[boundary] - positions[previous] - 1;  // 두 미덮임 위치를 피하는 쿼리가 들어갈 빈 구간 길이
//                 for (int used = 0; used <= q; ++used) {  // 이전 경계까지 포함배제 생성함수의 차수
//                     if (paths[previous][used] == 0) continue;  // 기여가 없는 계수는 생략
//                     for (int added = 0; used + added <= q; ++added) {  // 이번 빈 구간 안 쿼리들을 기존 계수에 곱하기
//                         int term = (int)(1LL * paths[previous][used] * exponential[gap][added] % MOD);  // 이전 선택과 현재 빈 구간을 함께 쓰는 생성함수 계수
//                         int* cell = &paths[boundary][used + added];  // 총 쿼리 수에 해당하는 다음 경계의 계수
//                         if (boundary + 1 == count) {  // 가상 끝 경계는 실제 미덮임 조건이 아니므로 부호를 바꾸지 않기
//                             *cell += term;  // 해당 포함배제 경로의 기여를 더하기
//                             if (*cell >= MOD) *cell -= MOD;  // 덧셈 결과를 나머지 범위로 유지
//                         } else {  // 실제 최솟값 위치를 미덮임으로 선택하면 포함배제 부호 반전
//                             *cell -= term;  // 미덮임 사건 하나를 추가한 기여는 빼기
//                             if (*cell < 0) *cell += MOD;  // 음수가 된 나머지를 0 이상으로 맞추기
//                         }  // 다음 경계의 포함배제 부호 반영 끝
//                     }  // 빈 구간 안 쿼리 수 조합 끝
//                 }  // 이전 경계 생성함수의 모든 차수 처리 끝
//             }  // 직전 경계 후보 처리 끝
//         }  // 현재 높이의 모든 필수 위치를 덮는 생성함수 완성
//         multiply(product, paths[count - 1], q);  // 이 높이의 독립된 쿼리 종류를 전체 생성함수에 곱하기
//         for (int boundary = 1; boundary < count; ++boundary) {  // 최솟값 위치 사이의 더 높은 연속 구간들로 분리
//             int left = positions[boundary - 1] + 1, right = positions[boundary] - 1;  // 두 최솟값 경계 사이에 남은 실제 정점 구간
//             if (left <= right) stack[top++] = (Range){left, right, minimum};  // 비어 있지 않은 높은 구간만 다음 높이 조건으로 처리
//         }  // 자식 구간 등록 끝
//     }  // 모든 높이의 필수 덮기 조건 처리 끝
//     int free_queries[51] = {1};  // 무제약 쿼리 종류의 exp(unrestricted*z) 계수
//     for (int degree = 1; degree <= q; ++degree) {  // 무제약 종류를 순서열에 원하는 개수만큼 섞는 계수 준비
//         free_queries[degree] = (int)(1LL * free_queries[degree - 1] * (unrestricted % MOD) % MOD * inverse[degree] % MOD);  // unrestricted^degree/degree!를 차례대로 계산
//     }  // 무제약 쿼리 생성함수 준비 끝
//     long long coefficient = 0, factorial = 1;  // q차 최종 계수와 순서를 복원할 q!
//     for (int used = 0; used <= q; ++used) {  // 필수 높이 종류와 무제약 종류가 나눠 쓰는 쿼리 수
//         coefficient = (coefficient + 1LL * product[used] * free_queries[q - used]) % MOD;  // 두 생성함수 곱의 q차 계수만 합산
//         if (used > 0) factorial = factorial * used % MOD;  // 1부터 q까지 곱해 순서열의 라벨 수 q! 준비
//     }  // 최종 계수와 팩토리얼 계산 끝
//     return (int)(coefficient * factorial % MOD);  // 생성함수의 q차 계수에 q!를 곱해 실제 쿼리 순서열 수 반환
// }  // solution 함수 끝

// 풀이 요약
// 목표를 넘지 않는 쿼리만 허용하면, 각 i가 높이 a[i]의 쿼리에 한 번 이상 덮이는 것이 최종 배열과 같아지는 조건.
// 구간의 최솟값 h 위치들을 나누면 높이 h 쿼리는 이 구간 안에서만 움직이고, 더 높은 쿼리는 최솟값 사이 구간들로 분리됨. 부모 높이와 h 사이 빠진 높이는 무제약 쿼리 종류로 누적.
// 높이 h의 필수 위치를 못 덮는 사건에 포함배제 적용. 선택한 미덮임 위치 사이 길이가 L이면 허용 부분구간 수는 L(L+1)/2라 그 쿼리들의 지수생성함수는 exp(L(L+1)z/2).
// 선택한 미덮임 위치들을 왼쪽부터 잇는 DP로 포함배제를 계산. 실제 위치를 선택할 때만 부호를 뒤집고, 가상 오른쪽 경계에서 덮기 조건의 합계를 받음.
// 독립된 높이별 생성함수와 무제약 exp(Uz)를 곱한 q차 계수에 q!를 곱하면 순서를 구분한 q개 쿼리 수. 같은 쿼리를 여러 번 고르는 경우도 지수함수 계수에 포함.
// 배열 길이 N, 쿼리 수 Q에서 시간 O(N²Q²), 공간 O(NQ). 모든 계수는 998244353으로 계산.
~~~

## 채점 기록

2026-10-24 사이트 채점: 정답 100/100. 1번째 제출에서 통과. C 제출 내역에서도 같은 날짜의 정답 기록 확인.

줄별 설명과 풀이 요약을 포함한 코드를 제출. 로컬 검사 횟수와 실행 시간은 사이트 채점 기록과 별도로 보관.
