#include <queue>
#include <string>
#include <unordered_set>
#include <utility>
#include <vector>
using namespace std;

int solution(string begin, string target, vector<string> words) {
    queue<pair<string,int>> q; unordered_set<string> visited{begin}; q.push({begin,0});
    while (!q.empty()) {
        auto [word,steps] = q.front(); q.pop();
        if (word == target) return steps;
        for (const string& candidate : words) if (!visited.count(candidate)) {
            int differences = 0; for (int i = 0; i < (int)word.size(); ++i) differences += word[i] != candidate[i];
            if (differences == 1) { visited.insert(candidate); q.push({candidate,steps + 1}); }
        }
    }
    return 0;
}

// 전체 코드 줄별 설명
// #include <queue>  // BFS 큐와 우선순위 큐
// #include <string>  // 문자열을 담는 string
// #include <unordered_set>  // 중복을 걸러 낼 해시 집합
// #include <utility>  // 두 값을 묶는 pair와 이동 유틸리티
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(string begin, string target, vector<string> words) {  // 한 글자씩 바꿔 목표 단어까지 가는 최소 횟수
// queue<pair<string,int>> q; unordered_set<string> visited{begin}; q.push({begin,0});  // 시작 단어에서 최소 변환 수 탐색을 시작
// while (!q.empty()) {  // 변환 횟수가 적은 단어부터 처리
// auto [word,steps] = q.front(); q.pop();  // 현재 단어와 횟수 꺼내기
// if (word == target) return steps;  // 목표에 도착하면 최소 횟수 반환
// for (const string& candidate : words) if (!visited.count(candidate)) {  // 아직 방문하지 않은 사전 단어 검사
// int differences = 0; for (int i = 0; i < (int)word.size(); ++i) differences += word[i] != candidate[i];  // 서로 다른 글자 위치 수 세기
// if (differences == 1) { visited.insert(candidate); q.push({candidate,steps + 1}); }  // 정확히 한 글자만 다르면 다음 상태로 넣기
// }  // 블록 끝
// }  // 블록 끝
// return 0;  // 주어진 단어들로 변환할 수 없으면 0 반환
// }  // 블록 끝

// 풀이 요약
// 한 글자만 다른 사전 단어로 이동하는 그래프에서 너비 우선 탐색으로 목표까지의 최소 변환 수 구하기
