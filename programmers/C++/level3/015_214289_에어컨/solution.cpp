#include <algorithm>
#include <array>
#include <vector>
using namespace std;

int solution(int temperature, int t1, int t2, int a, int b, vector<int> onboard) {
    int outside = temperature + 10, low = t1 + 10, high = t2 + 10;
    const int INF = 1000000000; array<int, 51> dp; dp.fill(INF); dp[outside] = 0;
    for (int time = 1; time < (int)onboard.size(); ++time) {
        array<int, 51> next; next.fill(INF);
        for (int current = 0; current <= 50; ++current) if (dp[current] != INF) {
            int natural = current + (current < outside) - (current > outside);
            int targets[4] = {natural, current, current - 1, current + 1}, costs[4] = {0, b, a, a};
            for (int choice = 0; choice < 4; ++choice) {
                int target = targets[choice];
                if (target < 0 || target > 50 || (onboard[time] && (target < low || target > high))) continue;
                next[target] = min(next[target], dp[current] + costs[choice]);
            }
        }
        dp = next;
    }
    return *min_element(dp.begin(), dp.end());
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <array>  // 크기가 고정된 array
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(int temperature, int t1, int t2, int a, int b, vector<int> onboard) {  // 승객이 탈 때 쾌적 온도를 지키는 최소 전력 비용
// int outside = temperature + 10, low = t1 + 10, high = t2 + 10;  // 음수 온도를 없애도록 가능한 온도 범위를 10만큼 옮기기
// const int INF = 1000000000; array<int, 51> dp; dp.fill(INF); dp[outside] = 0;  // 초기 실내 온도에서 시작하는 최소 비용 저장
// for (int time = 1; time < (int)onboard.size(); ++time) {  // 다음 분의 승객 조건을 순서대로 적용
// array<int, 51> next; next.fill(INF);  // 다음 시각의 최소 비용 초기화
// for (int current = 0; current <= 50; ++current) if (dp[current] != INF) {  // 도달한 온도 상태만 처리
// int natural = current + (current < outside) - (current > outside);  // 에어컨을 끄면 바깥 온도 쪽으로 한 칸 이동
// int targets[4] = {natural, current, current - 1, current + 1}, costs[4] = {0, b, a, a};  // 끄기, 유지, 한 칸 냉방 및 난방의 선택 만들기
// for (int choice = 0; choice < 4; ++choice) {  // 네 운전 선택 검사
// int target = targets[choice];  // 선택 결과의 실내 온도 읽기
// if (target < 0 || target > 50 || (onboard[time] && (target < low || target > high))) continue;  // 범위 밖이나 승객에게 불편한 온도를 제외
// next[target] = min(next[target], dp[current] + costs[choice]);  // 해당 온도의 최소 전력 비용 갱신
// }  // 블록 끝
// }  // 블록 끝
// dp = next;  // 다음 시각의 비용을 현재 상태로 바꾸기
// }  // 블록 끝
// return *min_element(dp.begin(), dp.end());  // 마지막 시각의 최소 비용 반환
// }  // 블록 끝

// 풀이 요약
// 시간과 실내 온도를 상태로 에어컨 끄기, 온도 유지, 냉난방의 최소 비용을 갱신하고 승객이 있을 때 쾌적 온도만 허용
