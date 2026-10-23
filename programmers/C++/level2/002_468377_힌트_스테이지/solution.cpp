#include <algorithm>
#include <functional>
#include <vector>
using namespace std;

int solution(vector<vector<int>> cost, vector<vector<int>> hint) {
    int n = (int)cost.size();
    vector<int> tickets(n, 0);
    int answer = 0;
    for (const auto& row : cost) answer += row[0];
    function<void(int, int)> dfs = [&](int stage, int total) {
        total += cost[stage][min(tickets[stage], n - 1)];
        if (stage == n - 1) {
            answer = min(answer, total);
            return;
        }
        dfs(stage + 1, total);
        const auto& bundle = hint[stage];
        for (int j = 1; j < (int)bundle.size(); ++j) ++tickets[bundle[j] - 1];
        dfs(stage + 1, total + bundle[0]);
        for (int j = 1; j < (int)bundle.size(); ++j) --tickets[bundle[j] - 1];
    };
    dfs(0, 0);
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <functional>  // 재귀 람다를 담는 function과 함수 객체
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<vector<int>> cost, vector<vector<int>> hint) {  // 힌트 구입과 사용을 함께 따져 최소 비용 찾기
// int n = (int)cost.size();  // 전체 스테이지 수 구하기
// vector<int> tickets(n, 0);  // 스테이지별로 받은 힌트 수를 0으로 초기화
// int answer = 0;  // 힌트 없이 진행하는 비용을 상한으로 사용
// for (const auto& row : cost) answer += row[0];  // 각 스테이지의 기본 비용을 더하기
// function<void(int, int)> dfs = [&](int stage, int total) {  // 스테이지와 누적 비용을 상태로 재귀 탐색
// total += cost[stage][min(tickets[stage], n - 1)];  // 받은 힌트 수에 해당하는 현재 스테이지 비용을 더하기
// if (stage == n - 1) {  // 마지막 스테이지를 마쳤는지 확인
// answer = min(answer, total);  // 최소 총비용 갱신
// return;  // 완성한 경로의 탐색을 끝
// }  // 블록 끝
// dfs(stage + 1, total);  // 힌트 묶음을 사지 않는 경우 탐색
// const auto& bundle = hint[stage];  // 현재 스테이지에서 살 수 있는 힌트 묶음 읽기
// for (int j = 1; j < (int)bundle.size(); ++j) ++tickets[bundle[j] - 1];  // 묶음에 포함된 스테이지별 힌트 수 늘리기
// dfs(stage + 1, total + bundle[0]);  // 묶음 가격을 지불한 경우 탐색
// for (int j = 1; j < (int)bundle.size(); ++j) --tickets[bundle[j] - 1];  // 다른 선택을 위해 힌트 수 되돌리기
// };  // 블록 끝
// dfs(0, 0);  // 첫 스테이지부터 모든 구매 선택 탐색
// return answer;  // 최소 총비용 반환
// }  // 블록 끝

// 풀이 요약
// 각 스테이지에서 힌트 묶음을 사거나 사지 않는 선택을 재귀 탐색하고 다음 스테이지의 힌트 수를 되돌리며 최소 비용 구하기
