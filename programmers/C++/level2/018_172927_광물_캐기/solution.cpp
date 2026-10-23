#include <algorithm>
#include <array>
#include <climits>
#include <functional>
#include <map>
#include <string>
#include <vector>
using namespace std;

int solution(vector<int> picks, vector<string> minerals) {
    vector<array<int, 3>> blocks;
    for (int start = 0; start < (int)minerals.size(); start += 5) {
        array<int, 3> costs{0, 0, 0};
        for (int j = start; j < min(start + 5, (int)minerals.size()); ++j) {
            if (minerals[j] == "diamond") { costs[0] += 1; costs[1] += 5; costs[2] += 25; }
            else if (minerals[j] == "iron") { costs[0] += 1; costs[1] += 1; costs[2] += 5; }
            else { ++costs[0]; ++costs[1]; ++costs[2]; }
        }
        blocks.push_back(costs);
    }
    map<array<int, 4>, int> memo;
    function<int(int, array<int, 3>)> dfs = [&](int index, array<int, 3> remaining) {
        if (index == (int)blocks.size() || remaining[0] + remaining[1] + remaining[2] == 0) return 0;
        array<int, 4> key{index, remaining[0], remaining[1], remaining[2]};
        if (memo.count(key)) return memo[key];
        int best = INT_MAX;
        for (int pick = 0; pick < 3; ++pick) if (remaining[pick] > 0) {
            --remaining[pick];
            best = min(best, blocks[index][pick] + dfs(index + 1, remaining));
            ++remaining[pick];
        }
        return memo[key] = best;
    };
    return dfs(0, {picks[0], picks[1], picks[2]});
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <array>  // 크기가 고정된 array
// #include <climits>  // 정수 자료형의 최솟값·최댓값
// #include <functional>  // 재귀 람다를 담는 function과 함수 객체
// #include <map>  // 키를 정렬해 보관하는 map
// #include <string>  // 문자열을 담는 string
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<int> picks, vector<string> minerals) {  // 곡괭이 수를 상태로 묶음별 최소 피로도 찾기
// vector<array<int, 3>> blocks;  // 다섯 광물 묶음마다 곡괭이 종류별 피로도 저장
// for (int start = 0; start < (int)minerals.size(); start += 5) {  // 광물을 다섯 개씩 묶기
// array<int, 3> costs{0, 0, 0};  // 묶음의 세 종류 피로도 초기화
// for (int j = start; j < min(start + 5, (int)minerals.size()); ++j) {  // 마지막 묶음의 남은 광물까지 처리
// if (minerals[j] == "diamond") { costs[0] += 1; costs[1] += 5; costs[2] += 25; }  // 다이아몬드의 종류별 피로도를 더하기
// else if (minerals[j] == "iron") { costs[0] += 1; costs[1] += 1; costs[2] += 5; }  // 철의 종류별 피로도를 더하기
// else { ++costs[0]; ++costs[1]; ++costs[2]; }  // 돌은 모든 곡괭이에서 피로도 1을 더하기
// }  // 블록 끝
// blocks.push_back(costs);  // 완성한 묶음의 비용 저장
// }  // 블록 끝
// map<array<int, 4>, int> memo;  // 묶음 위치와 남은 곡괭이 수별 최소 피로도를 기억
// function<int(int, array<int, 3>)> dfs = [&](int index, array<int, 3> remaining) {  // 사용할 곡괭이를 재귀적으로 선택
// if (index == (int)blocks.size() || remaining[0] + remaining[1] + remaining[2] == 0) return 0;  // 광물이나 곡괭이가 끝나면 추가 비용은 없음
// array<int, 4> key{index, remaining[0], remaining[1], remaining[2]};  // 메모이제이션 키 만들기
// if (memo.count(key)) return memo[key];  // 이미 계산한 상태는 저장된 값 반환
// int best = INT_MAX;  // 현재 상태의 최소 피로도 초기화
// for (int pick = 0; pick < 3; ++pick) if (remaining[pick] > 0) {  // 남아 있는 종류의 곡괭이만 선택
// --remaining[pick];  // 선택한 곡괭이 한 개를 사용
// best = min(best, blocks[index][pick] + dfs(index + 1, remaining));  // 현재 묶음 비용과 이후 최소 비용을 더해 비교
// ++remaining[pick];  // 다른 선택을 위해 곡괭이 되돌리기
// }  // 블록 끝
// return memo[key] = best;  // 최소 비용을 기억한 뒤 반환
// };  // 블록 끝
// return dfs(0, {picks[0], picks[1], picks[2]});  // 첫 묶음부터 주어진 곡괭이로 탐색
// }  // 블록 끝

// 풀이 요약
// 광물을 다섯 개씩 묶어 곡괭이별 비용을 구하고 남은 곡괭이 수를 상태로 메모이제이션하여 최소 피로도 구하기
