# 메뉴 리뉴얼

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/72411) · Level 2 · C++

## 풀이

주문별 메뉴 조합의 빈도를 코스 크기마다 세고 두 번 이상 주문된 최빈 조합들을 사전순으로 반환

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <functional>
#include <map>
#include <string>
#include <vector>
using namespace std;

vector<string> solution(vector<string> orders, vector<int> course) {
    for (string& order : orders) sort(order.begin(), order.end());
    vector<string> answer;
    for (int size : course) {
        map<string, int> counts;
        for (const string& order : orders) {
            string chosen;
            function<void(int)> dfs = [&](int start) {
                if ((int)chosen.size() == size) { ++counts[chosen]; return; }
                for (int i = start; i < (int)order.size(); ++i) { chosen.push_back(order[i]); dfs(i + 1); chosen.pop_back(); }
            };
            dfs(0);
        }
        int highest = 0;
        for (const auto& entry : counts) highest = max(highest, entry.second);
        if (highest >= 2) for (const auto& entry : counts) if (entry.second == highest) answer.push_back(entry.first);
    }
    sort(answer.begin(), answer.end());
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <functional>  // 재귀 람다를 담는 function과 함수 객체
// #include <map>  // 키를 정렬해 보관하는 map
// #include <string>  // 문자열을 담는 string
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<string> solution(vector<string> orders, vector<int> course) {  // 같은 메뉴 조합의 주문 수를 세어 코스 선택
// for (string& order : orders) sort(order.begin(), order.end());  // 같은 메뉴 조합을 같은 문자열로 세도록 정렬
// vector<string> answer;  // 선정한 코스 메뉴 조합 저장
// for (int size : course) {  // 요청한 각 코스 크기 처리
// map<string, int> counts;  // 해당 크기의 조합별 주문 수 세기
// for (const string& order : orders) {  // 주문별 조합을 생성
// string chosen;  // 현재 선택한 메뉴 저장
// function<void(int)> dfs = [&](int start) {  // 다음 메뉴의 시작 위치를 상태로 조합 탐색
// if ((int)chosen.size() == size) { ++counts[chosen]; return; }  // 지정 크기를 채우면 빈도 늘리기
// for (int i = start; i < (int)order.size(); ++i) { chosen.push_back(order[i]); dfs(i + 1); chosen.pop_back(); }  // 메뉴를 하나 선택하고 다음 위치에서 이어 고른 뒤 되돌리기
// };  // 블록 끝
// dfs(0);  // 현재 주문의 첫 메뉴부터 조합을 생성
// }  // 블록 끝
// int highest = 0;  // 해당 코스 크기의 최대 주문 수 초기화
// for (const auto& entry : counts) highest = max(highest, entry.second);  // 조합별 빈도의 최댓값 찾기
// if (highest >= 2) for (const auto& entry : counts) if (entry.second == highest) answer.push_back(entry.first);  // 두 번 이상 주문된 최빈 조합을 모두 고르기
// }  // 블록 끝
// sort(answer.begin(), answer.end());  // 모든 코스의 결과를 사전순 정렬
// return answer;  // 선정된 코스 메뉴 목록 반환
// }  // 블록 끝

// 풀이 요약
// 주문별 메뉴 조합의 빈도를 코스 크기마다 세고 두 번 이상 주문된 최빈 조합들을 사전순으로 반환
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:40:39
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/058_72411_%EB%A9%94%EB%89%B4_%EB%A6%AC%EB%89%B4%EC%96%BC/README.md)
