#include <iostream>  // C++ 스트림 입력과 출력

int main() {  // 최소 동전 수 계산 시작
    int n, target, coins[20], dp[1001];  // 동전과 금액 상태의 고정 상한
    std::cin >> n >> target;  // 종류 수와 목표 금액
    for (int i = 0; i < n; ++i) std::cin >> coins[i];  // 양의 동전 값 읽기
    for (int s = 0; s <= target; ++s) dp[s] = target + 1;  // 불가능 상태로 초기화
    dp[0] = 0;  // 빈 선택으로 금액 0 구성
    for (int s = 1; s <= target; ++s) {  // 더 작은 금액이 먼저 정해지는 순서
        for (int i = 0; i < n; ++i) {  // 마지막 동전의 모든 후보
            if (coins[i] <= s && dp[s - coins[i]] + 1 < dp[s]) {  // 유효하고 더 좋은 전이
                dp[s] = dp[s - coins[i]] + 1;  // 동전 하나를 추가한 최솟값
            }  // 전이 갱신 끝
        }  // 동전 후보 순회 끝
    }  // 금액 상태 계산 끝
    int answer = dp[target] == target + 1 ? -1 : dp[target];  // 불가능을 출력 규약으로 변환
    std::cout << answer << "\n";  // 최소 개수 또는 -1 출력
    return 0;  // 정상 종료
}  // 프로그램 끝
