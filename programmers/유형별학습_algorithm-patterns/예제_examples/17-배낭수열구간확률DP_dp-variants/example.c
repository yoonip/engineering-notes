#include <stdio.h>  // 표준 입력과 출력 함수

int main(void) {  // 두 DP 변형의 독립 실행
    int n, capacity, dp[101] = {0};  // 용량 이하의 최대 가치
    scanf("%d %d", &n, &capacity);  // 물건 수와 배낭 용량
    for (int i = 0; i < n; ++i) {  // 현재 물건을 한 번씩 반영
        int weight, value;  // 현재 물건의 정보
        scanf("%d %d", &weight, &value);  // 양의 무게와 가치
        for (int w = capacity; w >= weight; --w) {  // 현재 물건의 재사용을 막는 내림차순
            int candidate = dp[w - weight] + value;  // 현재 물건을 고른 가치
            if (candidate > dp[w]) dp[w] = candidate;  // 더 좋은 선택 유지
        }  // 한 물건의 용량 갱신 끝
    }  // 배낭 계산 끝
    int m, sequence[30], length[30], best = 0;  // LIS의 값과 끝 위치 상태
    scanf("%d", &m);  // 수열 길이
    for (int i = 0; i < m; ++i) {  // 앞에서부터 LIS 상태 계산
        scanf("%d", &sequence[i]);  // 현재 수열 원소
        length[i] = 1;  // 현재 원소만 고른 길이
        for (int j = 0; j < i; ++j) {  // 앞선 끝 위치 후보
            if (sequence[j] < sequence[i] && length[j] + 1 > length[i]) length[i] = length[j] + 1;  // 엄격 증가 전이
        }  // 이전 위치 확인 끝
        if (length[i] > best) best = length[i];  // 전체 LIS 길이 유지
    }  // 수열 계산 끝
    printf("KNAPSACK %d\nLIS %d\n", dp[capacity], best);  // 두 DP 결과를 구분해 출력
    return 0;  // 정상 종료
}  // 프로그램 끝
