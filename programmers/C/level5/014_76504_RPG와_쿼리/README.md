# RPG와 쿼리 — C

[레벨 5 목록](../README.md) · [언어별 목록](../../README.md) · [문제](https://school.programmers.co.kr/learn/courses/30/lessons/76504?language=c)

레벨 5 · C

## 풀이 요약

한 턴에 최대 z원을 얻으므로, 손실을 z×턴수−획득액으로 정의. 같은 목표 금액에서는 손실이 작을수록 턴 수도 작음.

가만히 z원 얻기는 위치를 바꾸지 않으므로 마지막에 몰아서 처리해도 됨. 전처리에서는 도로와 순간이동만 사용한 기본 경로를 찾기.

각 나머지의 최소 손실 경로 중 획득액도 최소인 것을 선택. 도로를 지난 직후의 나머지가 반복되면 그 사이 획득액과 손실은 모두 z의 양의 배수.

그 반복 구간을 순간이동 한 번으로 바꾸면 손실이 줄거나, 같은 손실에서 기본 획득액이 줄어들어 모순. 따라서 기본 경로의 도로는 최대 z−1번이고 획득액은 (z−1)^2 이하.

이 상한까지 금액·도시별 최소 턴을 계산. 순간이동은 현재 금액의 전역 최소 턴+1로 모든 도로 출발점을 고려해 도시 사이 간선을 따로 만들지 않음.

도로 획득액이 1..z−1이라 금액 행 z개만 순환 저장. 처리한 행은 비우고 미래 행만 갱신하면 전체 금액×도시 배열이 필요 없음.

금액을 증가시키며 나머지별 최소 손실을 누적하면 작은 쿼리도 정확하게 계산 가능. 상한보다 큰 쿼리는 모든 나머지의 기본 경로 금액 이상이므로 (목표 금액+최소 손실)/z로 응답.

z=50이고 모든 도로가49원이면 나머지1의 기본 금액은2401원. 그보다 작은 같은 나머지 금액은 불가능하므로 작은 쿼리를 무조건 최종 손실 식에 넣으면 안 됨.

시간 O((z−1)^2×(N+M)+Q), 공간 O(Nz+z²+Q). 최대 10^18원의 답은 long long으로 계산.

## 코드와 줄별 설명

[제출 코드](solution.c) · [사이트 채점 기록](grading.json) · [별도 로컬 검사](local_checks.json)

~~~c
#include <stdlib.h>
#include <string.h>

static long long* process_rpg(int n, int z, int* const roads[], size_t road_count, const long long queries[], size_t query_count) {
    const int infinity = 0x3f3f3f3f;
    int limit = (z - 1) * (z - 1);
    int* turns = (int*)malloc((size_t)n * z * sizeof(int));
    memset(turns, 0x3f, (size_t)n * z * sizeof(int));
    turns[0] = 0;
    int* small = (int*)malloc((size_t)(limit + 1) * sizeof(int));
    int loss[50];
    for (int r = 0; r < z; ++r) loss[r] = infinity;
    for (int money = 0; money <= limit; ++money) {
        int remainder = money % z;
        int* row = turns + (size_t)remainder * n;
        int best = infinity;
        for (int city = 0; city < n; ++city) if (row[city] < best) best = row[city];
        if (best != infinity) {
            int deficit = z * best - money;
            if (deficit < loss[remainder]) loss[remainder] = deficit;
            for (size_t e = 0; e < road_count; ++e) {
                int from = roads[e][0], to = roads[e][1], gain = roads[e][2];
                if (money + gain > limit) continue;
                int before = row[from] < best + 1 ? row[from] : best + 1;
                int* target = turns + (size_t)((money + gain) % z) * n + to;
                if (before + 1 < *target) *target = before + 1;
            }
        }
        small[money] = loss[remainder] == infinity ? -1 : (money + loss[remainder]) / z;
        memset(row, 0x3f, (size_t)n * sizeof(int));
    }
    long long* answer = (long long*)malloc(query_count * sizeof(long long));
    for (size_t q = 0; q < query_count; ++q) {
        long long money = queries[q];
        int remainder = (int)(money % z);
        if (money <= limit) answer[q] = small[(int)money];
        else if (loss[remainder] == infinity) answer[q] = -1;
        else answer[q] = (money + loss[remainder]) / z;
    }
    free(turns); free(small);
    return answer;
}

long long* solution(int n, int z, int** roads, size_t roads_rows, size_t roads_cols, long long queries[], size_t queries_len) {
    (void)roads_cols;
    return process_rpg(n, z, roads, roads_rows, queries, queries_len);
}

// 전체 코드 줄별 설명
// #include <stdlib.h>  // 작은 금액 DP와 동적 반환 배열의 메모리 관리
// #include <string.h>  // 순환 DP 행을 도달 불가 값으로 빠르게 초기화
// 
// static long long* process_rpg(int n, int z, int* const roads[], size_t road_count, const long long queries[], size_t query_count) {  // 도시·금액 DP로 모든 쿼리를 처리하는 공통 계산부
//     const int infinity = 0x3f3f3f3f;  // 도달하지 못한 도시·금액 상태를 나타내는 큰 턴 수
//     int limit = (z - 1) * (z - 1);  // 나머지별 최소 손실을 실현하는 기본 획득액은 이 범위 안에 존재
//     int* turns = (int*)malloc((size_t)n * z * sizeof(int));  // 도로 한 번의 획득액이 z 미만이라 금액 행 z개만 순환 저장
//     memset(turns, 0x3f, (size_t)n * z * sizeof(int));  // 처음에는 모든 도시·금액 상태가 도달 불가
//     turns[0] = 0;  // 0번 도시에서 0원·0턴으로 시작
//     int* small = (int*)malloc((size_t)(limit + 1) * sizeof(int));  // 기본 금액 상한 이하의 정확한 답을 저장
//     int loss[50];  // 나머지마다 지금까지 발견한 최소 손실 z×턴수−획득액
//     for (int r = 0; r < z; ++r) loss[r] = infinity;  // 아직 도달하지 못한 나머지는 별도로 유지
//     for (int money = 0; money <= limit; ++money) {  // 도로로 얻은 기본 금액을 작은 값부터 차례로 계산
//         int remainder = money % z;  // 현재 금액 행이 차지하는 순환 저장 칸
//         int* row = turns + (size_t)remainder * n;  // 현재 금액으로 각 도시에 도착한 최소 턴 수
//         int best = infinity;  // 현재 금액을 가진 상태 전체의 최소 턴 수
//         for (int city = 0; city < n; ++city) if (row[city] < best) best = row[city];  // 어느 도시에서든 순간이동을 시작할 수 있으므로 전역 최솟값 계산
//         if (best != infinity) {  // 도로·순간이동만으로 현재 금액을 만들 수 있는 경우
//             int deficit = z * best - money;  // 같은 턴 수를 모두 z원 획득에 썼을 때와의 차이
//             if (deficit < loss[remainder]) loss[remainder] = deficit;  // 같은 나머지를 만드는 더 효율적인 기본 경로 기록
//             for (size_t e = 0; e < road_count; ++e) {  // 현재 금액에서 사용할 수 있는 모든 일방통행 도로 확인
//                 int from = roads[e][0], to = roads[e][1], gain = roads[e][2];  // 도로의 출발 도시·도착 도시·획득액
//                 if (money + gain > limit) continue;  // 기본 경로의 상한을 넘는 금액 행은 계산하지 않음
//                 int before = row[from] < best + 1 ? row[from] : best + 1;  // 이미 출발 도시에 있거나, 가장 빠른 상태에서 한 턴 순간이동하기
//                 int* target = turns + (size_t)((money + gain) % z) * n + to;  // 획득액을 더한 미래 금액·도착 도시의 순환 저장 칸
//                 if (before + 1 < *target) *target = before + 1;  // 도로를 타는 한 턴을 더해 도착 상태의 최소 턴 갱신
//             }  // 현재 금액에서의 도로 이동 전파 끝
//         }  // 도달 가능한 기본 경로의 손실과 다음 금액 갱신 끝
//         small[money] = loss[remainder] == infinity ? -1 : (money + loss[remainder]) / z;  // 현재 금액 이하의 같은 나머지 기본 경로 뒤에 z원 획득 턴을 붙인 정확한 답
//         memset(row, 0x3f, (size_t)n * sizeof(int));  // 처리한 행은 비워 두어 z원 뒤의 금액이 안전하게 재사용
//     }  // 기본 금액 범위와 모든 도달 가능한 나머지 계산 끝
//     long long* answer = (long long*)malloc(query_count * sizeof(long long));  // 10^18원 쿼리의 턴 수도 담을 64비트 결과 배열
//     for (size_t q = 0; q < query_count; ++q) {  // 미리 계산한 작은 답과 나머지 손실로 각 쿼리에 O(1) 응답
//         long long money = queries[q];  // 정확히 만들어야 할 금액
//         int remainder = (int)(money % z);  // 머무르기로 바뀌지 않는 금액의 나머지
//         if (money <= limit) answer[q] = small[(int)money];  // 기본 경로 금액이 쿼리보다 클 수 있는 작은 값은 별도 답 사용
//         else if (loss[remainder] == infinity) answer[q] = -1;  // 어떤 도로 조합으로도 만들 수 없는 나머지
//         else answer[q] = (money + loss[remainder]) / z;  // 최소 손실의 기본 경로를 쓴 뒤 부족한 z원 배수를 머무르기로 채움
//     }  // 모든 쿼리 답 작성 끝
//     free(turns); free(small);  // 전처리용 순환 DP와 작은 답 배열 해제
//     return answer;  // 호출자가 사용할 동적 64비트 답 배열
// }  // 공통 RPG 계산부 끝
// 
// long long* solution(int n, int z, int** roads, size_t roads_rows, size_t roads_cols, long long queries[], size_t queries_len) {  // 프로그래머스 C 템플릿의 도시·도로·쿼리를 공통 계산부로 전달
//     (void)roads_cols;  // 도로의 각 행은 항상 출발·도착·획득액 세 칸이라 별도 열 수는 사용하지 않음
//     return process_rpg(n, z, roads, roads_rows, queries, queries_len);  // 쿼리 순서대로 동적 할당한 64비트 답 배열 반환
// }  // C 풀이 함수 끝

// 풀이 요약
// 한 턴에 최대 z원을 얻으므로, 손실을 z×턴수−획득액으로 정의. 같은 목표 금액에서는 손실이 작을수록 턴 수도 작음.
// 가만히 z원 얻기는 위치를 바꾸지 않으므로 마지막에 몰아서 처리해도 됨. 전처리에서는 도로와 순간이동만 사용한 기본 경로를 찾기.
// 각 나머지의 최소 손실 경로 중 획득액도 최소인 것을 선택. 도로를 지난 직후의 나머지가 반복되면 그 사이 획득액과 손실은 모두 z의 양의 배수.
// 그 반복 구간을 순간이동 한 번으로 바꾸면 손실이 줄거나, 같은 손실에서 기본 획득액이 줄어들어 모순. 따라서 기본 경로의 도로는 최대 z−1번이고 획득액은 (z−1)^2 이하.
// 이 상한까지 금액·도시별 최소 턴을 계산. 순간이동은 현재 금액의 전역 최소 턴+1로 모든 도로 출발점을 고려해 도시 사이 간선을 따로 만들지 않음.
// 도로 획득액이 1..z−1이라 금액 행 z개만 순환 저장. 처리한 행은 비우고 미래 행만 갱신하면 전체 금액×도시 배열이 필요 없음.
// 금액을 증가시키며 나머지별 최소 손실을 누적하면 작은 쿼리도 정확하게 계산 가능. 상한보다 큰 쿼리는 모든 나머지의 기본 경로 금액 이상이므로 (목표 금액+최소 손실)/z로 응답.
// z=50이고 모든 도로가49원이면 나머지1의 기본 금액은2401원. 그보다 작은 같은 나머지 금액은 불가능하므로 작은 쿼리를 무조건 최종 손실 식에 넣으면 안 됨.
// 시간 O((z−1)^2×(N+M)+Q), 공간 O(Nz+z²+Q). 최대 10^18원의 답은 long long으로 계산.
~~~

## 채점 기록

2026-10-24 사이트 채점: 정답 100/100. 1번째 제출에서 통과. C 제출 내역에서도 같은 날짜의 정답 기록 확인.

줄별 설명과 풀이 요약을 포함한 코드를 제출. 로컬 검사 횟수와 실행 시간은 사이트 채점 기록과 별도로 보관.
