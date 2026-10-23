#include <algorithm>
#include <functional>
#include <utility>
#include <vector>
using namespace std;

vector<int> solution(vector<vector<int>> users, vector<int> emoticons) {
    vector<int> rates(emoticons.size());
    pair<int, int> best{0, 0};
    function<void(int)> dfs = [&](int index) {
        if (index == (int)emoticons.size()) {
            int subscribers = 0, revenue = 0;
            for (const auto& user : users) {
                int cost = 0;
                for (int i = 0; i < (int)emoticons.size(); ++i) if (rates[i] >= user[0]) cost += emoticons[i] * (100 - rates[i]) / 100;
                if (cost >= user[1]) ++subscribers;
                else revenue += cost;
            }
            best = max(best, make_pair(subscribers, revenue));
            return;
        }
        for (int rate : {10, 20, 30, 40}) { rates[index] = rate; dfs(index + 1); }
    };
    dfs(0);
    return {best.first, best.second};
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <functional>  // 재귀 람다를 담는 function과 함수 객체
// #include <utility>  // 두 값을 묶는 pair와 이동 유틸리티
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<int> solution(vector<vector<int>> users, vector<int> emoticons) {  // 가입자 수 우선, 같은 수면 매출 최대화
// vector<int> rates(emoticons.size());  // 이모티콘별 할인율 선택 저장
// pair<int, int> best{0, 0};  // 가입자 수를 우선하고 매출을 다음으로 비교
// function<void(int)> dfs = [&](int index) {  // 각 이모티콘의 할인율을 하나씩 정하기
// if (index == (int)emoticons.size()) {  // 모든 할인율을 정했으면 사용자 반응 계산
// int subscribers = 0, revenue = 0;  // 현재 조합의 가입자 수와 매출 초기화
// for (const auto& user : users) {  // 사용자별 구매 금액 계산
// int cost = 0;  // 현재 사용자의 구매 금액 초기화
// for (int i = 0; i < (int)emoticons.size(); ++i) if (rates[i] >= user[0]) cost += emoticons[i] * (100 - rates[i]) / 100;  // 원하는 할인율 이상인 상품만 할인 가격으로 더하기
// if (cost >= user[1]) ++subscribers;  // 기준 금액 이상이면 플러스 가입자로 세기
// else revenue += cost;  // 가입하지 않으면 구매 금액을 매출에 더하기
// }  // 블록 끝
// best = max(best, make_pair(subscribers, revenue));  // pair의 사전순 비교로 더 나은 조합 고르기
// return;  // 완성한 할인율 조합의 처리를 끝
// }  // 블록 끝
// for (int rate : {10, 20, 30, 40}) { rates[index] = rate; dfs(index + 1); }  // 현재 상품의 네 할인율을 모두 탐색
// };  // 블록 끝
// dfs(0);  // 첫 이모티콘부터 할인율 선택
// return {best.first, best.second};  // 최대 가입자 수와 그때의 최대 매출 반환
// }  // 블록 끝

// 풀이 요약
// 모든 이모티콘의 네 할인율 조합을 탐색하고 가입자 수를 우선하며 동률에서 매출이 큰 조합 선택
