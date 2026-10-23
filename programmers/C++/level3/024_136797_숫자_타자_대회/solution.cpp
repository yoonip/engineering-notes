#include <algorithm>
#include <array>
#include <cstdlib>
#include <string>
using namespace std;

int solution(string numbers) {
    int row[10] = {3,0,0,0,1,1,1,2,2,2}, col[10] = {1,0,1,2,0,1,2,0,1,2}, weight[10][10];
    for (int a = 0; a < 10; ++a) for (int b = 0; b < 10; ++b) { int dr = abs(row[a] - row[b]), dc = abs(col[a] - col[b]); weight[a][b] = a == b ? 1 : 3 * min(dr, dc) + 2 * abs(dr - dc); }
    const int INF = 1000000000; array<array<int, 10>, 10> dp; for (auto& line : dp) line.fill(INF); dp[4][6] = 0;
    for (char c : numbers) {
        int target = c - '0'; array<array<int, 10>, 10> next; for (auto& line : next) line.fill(INF);
        for (int left = 0; left < 10; ++left) for (int right = 0; right < 10; ++right) if (dp[left][right] != INF) {
            if (target != right) next[target][right] = min(next[target][right], dp[left][right] + weight[left][target]);
            if (target != left) next[left][target] = min(next[left][target], dp[left][right] + weight[right][target]);
        }
        dp = next;
    }
    int answer = INF; for (const auto& line : dp) answer = min(answer, *min_element(line.begin(), line.end()));
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <array>  // 크기가 고정된 array
// #include <cstdlib>  // 정수 절댓값 같은 기본 유틸리티
// #include <string>  // 문자열을 담는 string
// using namespace std;  // std:: 접두사 생략
// int solution(string numbers) {  // 두 엄지의 위치별 최소 입력 비용 갱신
// int row[10] = {3,0,0,0,1,1,1,2,2,2}, col[10] = {1,0,1,2,0,1,2,0,1,2}, weight[10][10];  // 숫자 키패드 좌표와 이동 비용 표 선언
// for (int a = 0; a < 10; ++a) for (int b = 0; b < 10; ++b) { int dr = abs(row[a] - row[b]), dc = abs(col[a] - col[b]); weight[a][b] = a == b ? 1 : 3 * min(dr, dc) + 2 * abs(dr - dc); }  // 대각선과 직선 이동의 최소 비용 계산
// const int INF = 1000000000; array<array<int, 10>, 10> dp; for (auto& line : dp) line.fill(INF); dp[4][6] = 0;  // 두 손가락이 4와 6에 놓인 초기 상태
// for (char c : numbers) {  // 누를 숫자를 순서대로 처리
// int target = c - '0'; array<array<int, 10>, 10> next; for (auto& line : next) line.fill(INF);  // 다음 숫자를 누른 뒤의 최소 비용 초기화
// for (int left = 0; left < 10; ++left) for (int right = 0; right < 10; ++right) if (dp[left][right] != INF) {  // 도달한 손가락 위치 상태 검사
// if (target != right) next[target][right] = min(next[target][right], dp[left][right] + weight[left][target]);  // 오른손이 없는 목표에 왼손을 움직이기
// if (target != left) next[left][target] = min(next[left][target], dp[left][right] + weight[right][target]);  // 왼손이 없는 목표에 오른손을 움직이기
// }  // 블록 끝
// dp = next;  // 다음 입력을 위한 상태로 바꾸기
// }  // 블록 끝
// int answer = INF; for (const auto& line : dp) answer = min(answer, *min_element(line.begin(), line.end()));  // 모든 최종 손가락 위치 중 최소 비용 구하기
// return answer;  // 숫자열을 입력하는 최소 가중치 반환
// }  // 블록 끝

// 풀이 요약
// 두 손가락 위치를 상태로 다음 숫자를 누를 손가락을 선택하고 같은 키 중복 점유를 막으며 최소 가중치 갱신
