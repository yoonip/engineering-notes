# 가사 검색

[레벨 4 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/60060) · Level 4 · C++

## 풀이

단어를 길이별로 분류해 정방향·역방향 정렬. 물음표가 앞이면 뒤집어 접두사 검색으로 통일하고, ?를 a·z로 바꾼 사전순 범위의 개수를 계산.

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <vector>
#include <array>
#include <algorithm>
#include <numeric>
#include <functional>
#include <unordered_set>
#include <unordered_map>
#include <map>
#include <set>
#include <queue>
#include <deque>
#include <tuple>
#include <utility>
#include <climits>
#include <cstdlib>
using namespace std;

vector<int> solution(vector<string> words, vector<string> queries) {
    unordered_map<int, vector<string>> forward, backward;
    for (string word : words) { int length = (int)word.size(); forward[length].push_back(word); reverse(word.begin(), word.end()); backward[length].push_back(word); }
    for (auto& group : forward) sort(group.second.begin(), group.second.end()); for (auto& group : backward) sort(group.second.begin(), group.second.end());
    vector<int> answer;
    for (string query : queries) {
        bool reversed = query[0] == '?'; if (reversed) reverse(query.begin(), query.end());
        auto& group = reversed ? backward[(int)query.size()] : forward[(int)query.size()];
        string low = query, high = query; replace(low.begin(), low.end(), '?', 'a'); replace(high.begin(), high.end(), '?', 'z');
        answer.push_back(upper_bound(group.begin(), group.end(), high) - lower_bound(group.begin(), group.end(), low));
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열 string 사용 준비
// #include <vector>  // 가변 길이 배열 vector 사용 준비
// #include <array>  // 고정 크기 배열 array 사용 준비
// #include <algorithm>  // 정렬·탐색·최솟값 등 표준 알고리즘 사용 준비
// #include <numeric>  // gcd·accumulate 등 수치 알고리즘 사용 준비
// #include <functional>  // 함수 래퍼와 greater 등 비교 함수 객체 사용 준비
// #include <unordered_set>  // 중복 없는 원소를 저장하는 해시 집합 사용 준비
// #include <unordered_map>  // 키로 값을 찾는 해시 맵 사용 준비
// #include <map>  // 키 순서가 유지되는 맵 사용 준비
// #include <set>  // 중복 제거와 정렬을 함께 하는 집합 사용 준비
// #include <queue>  // FIFO 큐와 우선순위 큐 사용 준비
// #include <deque>  // 양 끝 삽입·삭제를 지원하는 덱 사용 준비
// #include <tuple>  // 여러 상태 값을 묶는 tuple 사용 준비
// #include <utility>  // pair·move 등 유틸리티 사용 준비
// #include <climits>  // 정수 범위 상수 사용 준비
// #include <cstdlib>  // 정수 절댓값 등 표준 유틸리티 함수 사용 준비
// using namespace std;  // 표준 이름의 std:: 접두사 생략
//
// vector<int> solution(vector<string> words, vector<string> queries) {  // 가사 검색 풀이 함수 정의
//     unordered_map<int, vector<string>> forward, backward;  // 길이별 정방향 단어와 뒤집은 단어 목록 준비
//     for (string word : words) { int length = (int)word.size(); forward[length].push_back(word); reverse(word.begin(), word.end()); backward[length].push_back(word); }  // 각 단어를 길이별로 저장하고 뒤집은 단어도 별도 목록에 저장
//     for (auto& group : forward) sort(group.second.begin(), group.second.end()); for (auto& group : backward) sort(group.second.begin(), group.second.end());  // 길이별 두 단어 목록을 각각 사전순 정렬
//     vector<int> answer;  // 쿼리별 일치 개수를 담을 결과 배열 준비
//     for (string query : queries) {  // 검색어를 하나씩 처리
//         bool reversed = query[0] == '?'; if (reversed) reverse(query.begin(), query.end());  // 물음표가 앞에 있으면 검색어를 뒤집어 고정 접두사가 앞에 오도록 변환
//         auto& group = reversed ? backward[(int)query.size()] : forward[(int)query.size()];  // 검색어 방향과 길이에 대응하는 단어 그룹 선택
//         string low = query, high = query; replace(low.begin(), low.end(), '?', 'a'); replace(high.begin(), high.end(), '?', 'z');  // 물음표를 모두 a로 바꾼 하한 문자열과 z로 바꾼 상한 문자열 생성
//         answer.push_back(upper_bound(group.begin(), group.end(), high) - lower_bound(group.begin(), group.end(), low));  // upper_bound(상한) - lower_bound(하한)으로 일치 범위의 크기 추가
//     }  // 블록 끝
//     return answer;  // 쿼리 순서의 일치 단어 개수 반환
// }  // 함수 끝
//

// 풀이 요약
// 단어를 길이별로 분류해 정방향·역방향 정렬. 물음표가 앞이면 뒤집어 접두사 검색으로 통일하고, ?를 a·z로 바꾼 사전순 범위의 개수를 계산.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:47:25
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level4/extra_60060_%EA%B0%80%EC%82%AC_%EA%B2%80%EC%83%89/README.md)
