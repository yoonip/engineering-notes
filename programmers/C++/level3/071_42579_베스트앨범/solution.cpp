#include <algorithm>
#include <map>
#include <string>
#include <utility>
#include <vector>
using namespace std;

vector<int> solution(vector<string> genres, vector<int> plays) {
    map<string,int> totals; map<string,vector<pair<int,int>>> songs;
    vector<string> order;
    for (int i = 0; i < (int)genres.size(); ++i) {
        if (!totals.count(genres[i])) order.push_back(genres[i]);
        totals[genres[i]] += plays[i]; songs[genres[i]].push_back({-plays[i],i});
    }
    stable_sort(order.begin(), order.end(), [&](const string& a, const string& b) { return totals[a] > totals[b]; });
    vector<int> answer;
    for (const string& genre : order) { auto& ranked = songs[genre]; sort(ranked.begin(), ranked.end()); for (int i = 0; i < min(2, (int)ranked.size()); ++i) answer.push_back(ranked[i].second); }
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <map>  // 키를 정렬해 보관하는 map
// #include <string>  // 문자열을 담는 string
// #include <utility>  // 두 값을 묶는 pair와 이동 유틸리티
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<int> solution(vector<string> genres, vector<int> plays) {  // 총재생 수가 큰 장르에서 상위 두 곡 선택
// map<string,int> totals; map<string,vector<pair<int,int>>> songs;  // 장르별 총재생 수와 곡별 재생 수 및 번호 저장
// vector<string> order;  // 처음 등장한 장르 순서를 보존
// for (int i = 0; i < (int)genres.size(); ++i) {  // 각 곡을 해당 장르에 등록
// if (!totals.count(genres[i])) order.push_back(genres[i]);  // 새 장르이면 입력 순서 기록
// totals[genres[i]] += plays[i]; songs[genres[i]].push_back({-plays[i],i});  // 큰 재생 수와 작은 번호가 먼저 오도록 음수 재생 수 저장
// }  // 블록 끝
// stable_sort(order.begin(), order.end(), [&](const string& a, const string& b) { return totals[a] > totals[b]; });  // 총재생 수가 많은 장르부터 정렬
// vector<int> answer;  // 베스트 앨범의 곡 번호 저장
// for (const string& genre : order) { auto& ranked = songs[genre]; sort(ranked.begin(), ranked.end()); for (int i = 0; i < min(2, (int)ranked.size()); ++i) answer.push_back(ranked[i].second); }  // 장르별 재생 수와 번호 기준의 상위 두 곡 고르기
// return answer;  // 앨범에 수록할 곡 번호 반환
// }  // 블록 끝

// 풀이 요약
// 장르별 총재생 수로 장르를 정렬하고 각 장르에서 재생 수 내림차순과 고유 번호 오름차순의 상위 두 곡 선택
