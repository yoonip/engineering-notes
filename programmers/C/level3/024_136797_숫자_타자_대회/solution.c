#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

int solution(const char* numbers) {
    int row[10] = {3,0,0,0,1,1,1,2,2,2}, col[10] = {1,0,1,2,0,1,2,0,1,2}, weights[10][10], dp[10][10], next[10][10];
    for (int i = 0; i < 10; ++i) for (int j = 0; j < 10; ++j) { int dr = abs(row[i] - row[j]), dc = abs(col[i] - col[j]); weights[i][j] = i == j ? 1 : 3 * (dr < dc ? dr : dc) + 2 * abs(dr - dc); dp[i][j] = 1000000000; }
    dp[4][6] = 0;
    for (size_t p = 0; numbers[p]; ++p) {
        int target = numbers[p] - '0';
        for (int i = 0; i < 10; ++i) for (int j = 0; j < 10; ++j) next[i][j] = 1000000000;
        for (int left = 0; left < 10; ++left) for (int right = 0; right < 10; ++right) if (dp[left][right] < 1000000000) {
            int cost = dp[left][right];
            if (target != right && cost + weights[left][target] < next[target][right]) next[target][right] = cost + weights[left][target];
            if (target != left && cost + weights[right][target] < next[left][target]) next[left][target] = cost + weights[right][target];
        }
        memcpy(dp, next, sizeof(dp));
    }
    int answer = 1000000000; for (int i = 0; i < 10; ++i) for (int j = 0; j < 10; ++j) if (dp[i][j] < answer) answer = dp[i][j];
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
// int solution(const char* numbers) {  // 두 손가락의 위치가 같을 수 없다는 조건을 지키며, 다음 숫자를 왼손·오른손으로 누르는 두 선택을 DP로 비교
//     int row[10] = {3,0,0,0,1,1,1,2,2,2}, col[10] = {1,0,1,2,0,1,2,0,1,2}, weights[10][10], dp[10][10], next[10][10];  // 숫자 버튼별 행 / 숫자 버튼별 열 저장
//     for (int i = 0; i < 10; ++i) for (int j = 0; j < 10; ++j) { int dr = abs(row[i] - row[j]), dc = abs(col[i] - col[j]); weights[i][j] = i == j ? 1 : 3 * (dr < dc ? dr : dc) + 2 * abs(dr - dc); dp[i][j] = 1000000000; }  // 첫 버튼 순서대로 확인; 둘째 버튼 갱신
//     dp[4][6] = 0;  // 왼손 오른손 위치별 최소 비용 갱신
//     for (size_t p = 0; numbers[p]; ++p) {  // 입력 숫자 위치 순서대로 확인
//         int target = numbers[p] - '0';  // 이번에 누를 숫자 저장
//         for (int i = 0; i < 10; ++i) for (int j = 0; j < 10; ++j) next[i][j] = 1000000000;  // 첫 버튼 순서대로 확인; 둘째 버튼 갱신
//         for (int left = 0; left < 10; ++left) for (int right = 0; right < 10; ++right) if (dp[left][right] < 1000000000) {  // 왼손 숫자 위치 순서대로 확인; 오른손 숫자 위치 갱신
//             int cost = dp[left][right];  // 현재 손 배치까지의 비용 저장
//             if (target != right && cost + weights[left][target] < next[target][right]) next[target][right] = cost + weights[left][target];  // 오른손과 겹치지 않는 왼손 이동 중 더 싼 누적 비용만 기록
//             if (target != left && cost + weights[right][target] < next[left][target]) next[left][target] = cost + weights[right][target];  // 왼손과 겹치지 않는 오른손 이동 중 더 싼 누적 비용만 기록
//         }  // 이 범위 끝
//         memcpy(dp, next, sizeof(dp));  // 왼손 오른손 위치별 최소 비용 / 다음 숫자를 누른 후의 최소 비용 복사
//     }  // 이 범위 끝
//     int answer = 1000000000; for (int i = 0; i < 10; ++i) for (int j = 0; j < 10; ++j) if (dp[i][j] < answer) answer = dp[i][j];  // 모든 숫자를 누르는 최소 비용 / 첫 버튼 / 둘째 버튼 저장
//     return answer;  // 모든 숫자를 누르는 최소 비용 반환
// }  // 이 범위 끝

// 풀이 요약
// 두 손가락의 위치가 같을 수 없다는 조건을 지키며, 다음 숫자를 왼손·오른손으로 누르는 두 선택을 DP로 비교
// 이동 비용은 가능한 대각선을 3씩, 나머지 직선을 2씩 더하며 같은 키는 1; 각 글자 직후에는 한 손이 그 글자 위에 있어 가능한 상태 수가 제한됨; 전체 시간 O(100L), 상태 공간 O(100) 이내
// 예: 이미 오른손이 6에 있을 때 6을 누르면 반드시 오른손으로 비용 1을 지불하기; 다른 손을 6으로 옮기는 선택은 금지하기
