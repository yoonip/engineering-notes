#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

int solution(int temperature, int t1, int t2, int a, int b, int onboard[], size_t onboard_len) {
    int outside = temperature + 10, low = t1 + 10, high = t2 + 10, dp[51], next[51]; const int inf = 1000000000;
    for (int i = 0; i <= 50; ++i) dp[i] = inf; dp[outside] = 0;
    for (size_t time = 1; time < onboard_len; ++time) {
        for (int i = 0; i <= 50; ++i) next[i] = inf;
        for (int current = 0; current <= 50; ++current) if (dp[current] < inf) {
            int natural = current + (current < outside) - (current > outside), targets[4] = {natural,current,current - 1,current + 1}, costs[4] = {0,b,a,a};
            for (int j = 0; j < 4; ++j) {
                int target = targets[j]; if (target < 0 || target > 50 || (onboard[time] && (target < low || target > high))) continue;
                if (dp[current] + costs[j] < next[target]) next[target] = dp[current] + costs[j];
            }
        }
        memcpy(dp, next, sizeof(dp));
    }
    int answer = inf; for (int i = 0; i <= 50; ++i) if (dp[i] < answer) answer = dp[i];
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
// int solution(int temperature, int t1, int t2, int a, int b, int onboard[], size_t onboard_len) {  // DP 상태는 현재 시각의 온도별 최소 소비전력; 매 분 전원 끄기(무료 자연 변화), 유지(b), 1도 상승·하강(a)을 모두 비교
//     int outside = temperature + 10, low = t1 + 10, high = t2 + 10, dp[51], next[51]; const int inf = 1000000000;  // 음수 보정한 외부 온도 / 승객 허용 온도 하한 / 승객 허용 온도 상한 저장
//     for (int i = 0; i <= 50; ++i) dp[i] = inf; dp[outside] = 0;  // 온도 초기화 위치 순서대로 확인; 현재 온도별 최소 전력 갱신
//     for (size_t time = 1; time < onboard_len; ++time) {  // 처리할 다음 분 순서대로 확인
//         for (int i = 0; i <= 50; ++i) next[i] = inf;  // 온도 초기화 위치 순서대로 확인; 다음 분의 온도별 최소 전력 갱신
//         for (int current = 0; current <= 50; ++current) if (dp[current] < inf) {  // 도달 가능한 실내 온도 상태에서만 다음 1분으로 전이
//             int natural = current + (current < outside) - (current > outside), targets[4] = {natural,current,current - 1,current + 1}, costs[4] = {0,b,a,a};  // 에어컨을 끈 다음 분 온도 / 끄기 유지 내리기 올리기의 다음 온도 / 네 동작의 추가 전력 저장
//             for (int j = 0; j < 4; ++j) {  // 에어컨 동작 번호 순서대로 확인
//                 int target = targets[j]; if (target < 0 || target > 50 || (onboard[time] && (target < low || target > high))) continue;  // 시험할 다음 실내 온도 저장
//                 if (dp[current] + costs[j] < next[target]) next[target] = dp[current] + costs[j];  // 다음 온도에 도달하는 전기 요금이 더 적으면 갱신
//             }  // 이 범위 끝
//         }  // 이 범위 끝
//         memcpy(dp, next, sizeof(dp));  // 현재 온도별 최소 전력 / 다음 분의 온도별 최소 전력 복사
//     }  // 이 범위 끝
//     int answer = inf; for (int i = 0; i <= 50; ++i) if (dp[i] < answer) answer = dp[i];  // 마지막 시각의 가능한 실내 온도 중 최소 전력 선택
//     return answer;  // 승객 조건을 지킨 최소 전력 반환
// }  // 이 범위 끝

// 풀이 요약
// DP 상태는 현재 시각의 온도별 최소 소비전력; 매 분 전원 끄기(무료 자연 변화), 유지(b), 1도 상승·하강(a)을 모두 비교
// 탑승 시각의 다음 온도가 쾌적 범위 밖이면 제외하기; 마지막 시각 이후의 비용은 더하지 않음; 시간 O(51T), 공간 O(51)
// 예: 28도에서 26도까지 두 번 냉방한 뒤 계속 유지할 수도 있지만, 24도까지 더 냉방하고 전원을 꺼 자연 상승시키면 첫 예제에서 총 40이 됨
