#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

int solution(int** info, size_t info_rows, size_t info_cols, int n, int m) {
    (void)info_cols;
    int* dp = malloc((size_t)m * sizeof(*dp)); int* next = malloc((size_t)m * sizeof(*next));
    for (int b = 0; b < m; ++b) dp[b] = n;
    dp[0] = 0;
    for (size_t i = 0; i < info_rows; ++i) {
        for (int b = 0; b < m; ++b) next[b] = n;
        for (int b = 0; b < m; ++b) if (dp[b] < n) {
            int a_next = dp[b] + info[i][0], b_next = b + info[i][1];
            if (a_next < n && a_next < next[b]) next[b] = a_next;
            if (b_next < m && dp[b] < next[b_next]) next[b_next] = dp[b];
        }
        int* temp = dp; dp = next; next = temp;
    }
    int answer = n;
    for (int b = 0; b < m; ++b) if (dp[b] < answer) answer = dp[b];
    free(dp); free(next);
    return answer < n ? answer : -1;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <ctype.h>  // 문자 종류 확인과 대소문자 변환
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
// #include <math.h>  // 정수 제곱근 계산 등에 쓸 수학 함수
//
// int solution(int** info, size_t info_rows, size_t info_cols, int n, int m) {  // DP(작은 상태의 최적값을 저장하는 방법)로 B 흔적마다 최소 A 흔적만 유지
//     (void)info_cols;  // 입력 형식에만 필요한 길이 값은 계산에서 생략
//     int* dp = malloc((size_t)m * sizeof(*dp)); int* next = malloc((size_t)m * sizeof(*next));  // B 흔적별 최소 A 흔적 / 현재 물건을 맡긴 뒤의 흔적 상태 공간 확보
//     for (int b = 0; b < m; ++b) dp[b] = n;  // B에게 이미 남은 흔적 순서대로 확인; B 흔적별 최소 A 흔적 갱신
//     dp[0] = 0;  // B 흔적별 최소 A 흔적 갱신
//     for (size_t i = 0; i < info_rows; ++i) {  // 맡길 물건 번호 순서대로 확인
//         for (int b = 0; b < m; ++b) next[b] = n;  // B에게 이미 남은 흔적 순서대로 확인; 현재 물건을 맡긴 뒤의 흔적 상태 갱신
//         for (int b = 0; b < m; ++b) if (dp[b] < n) {  // A 흔적이 체포 기준 미만인 상태에서만 이번 물건 배정
//             int a_next = dp[b] + info[i][0], b_next = b + info[i][1];  // A가 현재 물건을 맡을 때의 흔적 / B가 현재 물건을 맡을 때의 흔적 저장
//             if (a_next < n && a_next < next[b]) next[b] = a_next;  // A가 맡아도 기준 미만이고 기존 배정보다 흔적이 적으면 갱신
//             if (b_next < m && dp[b] < next[b_next]) next[b_next] = dp[b];  // B가 맡아도 기준 미만이면 해당 B 흔적에 대한 최소 A 흔적 갱신
//         }  // 이 범위 끝
//         int* temp = dp; dp = next; next = temp;  // B 흔적별 최소 A 흔적 / 현재 물건을 맡긴 뒤의 흔적 상태 저장
//     }  // 이 범위 끝
//     int answer = n;  // 잡히지 않는 최소 A 흔적 저장
//     for (int b = 0; b < m; ++b) if (dp[b] < answer) answer = dp[b];  // 체포 기준을 지킨 상태 중 A의 흔적 최솟값 선택
//     free(dp); free(next);  // B 흔적별 최소 A 흔적 / 현재 물건을 맡긴 뒤의 흔적 상태 임시 공간 정리
//     return answer < n ? answer : -1;  // 잡히지 않는 최소 A 흔적로 최종값 계산
// }  // 이 범위 끝

// 풀이 요약
// DP(작은 상태의 최적값을 저장하는 방법)로 B 흔적마다 최소 A 흔적만 유지
// 각 물건을 A 또는 B에게 배정하되 흔적이 n,m 이상이 되는 선택은 버리기; 시간 O(물건 수*m), 공간 O(m)
// 예: info=[[1,2],[2,3],[2,1]], n=4,m=4이면 가능한 최소 A 흔적은 2
