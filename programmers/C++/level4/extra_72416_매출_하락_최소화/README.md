# 매출 하락 최소화

[레벨 4 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/72416) · Level 4 · C++

## 풀이

각 직원이 참석할 때와 불참할 때의 최소 손실을 트리 DP로 계산. 팀장이 불참하면 자식 중 최소 한 명이 참석하도록 가장 싼 추가 비용 반영.

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

int solution(vector<int> sales, vector<vector<int>> links) {
    int n = (int)sales.size(); vector<vector<int>> children(n);
    for (const auto& link : links) children[link[0] - 1].push_back(link[1] - 1);
    vector<int> order(1, 0);
    for (int i = 0; i < (int)order.size(); ++i) for (int child : children[order[i]]) order.push_back(child);
    vector<long long> attend(sales.begin(), sales.end()), absent(n, 0);
    for (auto it = order.rbegin(); it != order.rend(); ++it) {
        int node = *it; if (children[node].empty()) continue;
        long long total = 0, extra = LLONG_MAX;
        for (int child : children[node]) { long long best = min(attend[child], absent[child]); total += best; extra = min(extra, attend[child] - best); }
        attend[node] += total; absent[node] = total + extra;
    }
    return (int)min(attend[0], absent[0]);
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
// int solution(vector<int> sales, vector<vector<int>> links) {  // 매출 하락 최소화 풀이 함수 정의
//     int n = (int)sales.size(); vector<vector<int>> children(n);  // 직원 수와 팀원 자식 목록 준비
//     for (const auto& link : links) children[link[0] - 1].push_back(link[1] - 1);  // 1기준 팀장·팀원 번호를 0기준 자식 관계로 변환
//     vector<int> order(1, 0);  // 대표 0번에서 시작할 탐색 순서 준비
//     for (int i = 0; i < (int)order.size(); ++i) for (int child : children[order[i]]) order.push_back(child);  // 부모가 자식보다 먼저 나오도록 트리 순서 생성
//     vector<long long> attend(sales.begin(), sales.end()), absent(n, 0);  // 참석 비용 attend는 자기 매출로, 불참 비용 absent는 0으로 초기화
//     for (auto it = order.rbegin(); it != order.rend(); ++it) {  // 자식부터 계산하도록 탐색 순서를 뒤집어 처리
//         int node = *it; if (children[node].empty()) continue;  // 현재 직원이 팀원이 없는 리프이면 초기 비용 그대로 사용
//         long long total = 0, extra = LLONG_MAX;  // 자식별 최소 비용 합 total과 참석을 강제할 최소 추가 비용 extra 준비
//         for (int child : children[node]) { long long best = min(attend[child], absent[child]); total += best; extra = min(extra, attend[child] - best); }  // 자식의 참석·불참 중 작은 값을 합산하고, 참석으로 바꿀 때 필요한 최소 차이 기록
//         attend[node] += total; absent[node] = total + extra;  // 본인이 참석하면 자식 선택은 자유. 불참하면 자식 한 명의 참석 비용을 추가
//     }  // 블록 끝
//     return (int)min(attend[0], absent[0]);  // 대표의 참석·불참 중 작은 전체 손실 반환
// }  // 함수 끝
//

// 풀이 요약
// 각 직원이 참석할 때와 불참할 때의 최소 손실을 트리 DP로 계산. 팀장이 불참하면 자식 중 최소 한 명이 참석하도록 가장 싼 추가 비용 반영.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:44:47
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level4/extra_72416_%EB%A7%A4%EC%B6%9C_%ED%95%98%EB%9D%BD_%EC%B5%9C%EC%86%8C%ED%99%94/README.md)
