# 무지의 먹방 라이브

[레벨 4 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/42891) · Level 4 · C++

## 풀이

음식 시간을 작은 순서로 정렬해 같은 높이의 층을 한 번에 제거. 다음 층을 전부 못 먹으면 남은 음식 번호를 정렬해 k의 나머지 위치 선택.

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

int solution(vector<int> food_times, long long k) {
    if (accumulate(food_times.begin(), food_times.end(), 0LL) <= k) return -1;
    vector<pair<int, int>> foods;
    for (int i = 0; i < (int)food_times.size(); ++i) foods.push_back({food_times[i], i + 1});
    sort(foods.begin(), foods.end()); int n = (int)foods.size(), previous = 0;
    for (int position = 0; position < n; ++position) {
        int remaining = n - position; long long cost = 1LL * (foods[position].first - previous) * remaining;
        if (cost > k) { vector<int> order; for (int i = position; i < n; ++i) order.push_back(foods[i].second); sort(order.begin(), order.end()); return order[k % remaining]; }
        k -= cost; previous = foods[position].first;
    }
    return -1;
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
// int solution(vector<int> food_times, long long k) {  // 무지의 먹방 라이브 풀이 함수 정의
//     if (accumulate(food_times.begin(), food_times.end(), 0LL) <= k) return -1;  // 전체 식사 시간이 k 이하면 남은 음식이 없으므로 -1 반환
//     vector<pair<int, int>> foods;  // 남은 시간과 원래 1기준 번호를 함께 저장할 배열 준비
//     for (int i = 0; i < (int)food_times.size(); ++i) foods.push_back({food_times[i], i + 1});  // 음식마다 시간·번호 쌍 생성
//     sort(foods.begin(), foods.end()); int n = (int)foods.size(), previous = 0;  // 시간순 정렬하고 전체 음식 수 n과 이전에 제거한 높이 previous 준비
//     for (int position = 0; position < n; ++position) {  // 시간이 작은 음식부터 층 단위로 제거
//         int remaining = n - position; long long cost = 1LL * (foods[position].first - previous) * remaining;  // 남은 음식 수와 다음 높이까지 먹는 총시간 cost를 long long으로 계산
//         if (cost > k) { vector<int> order; for (int i = position; i < n; ++i) order.push_back(foods[i].second); sort(order.begin(), order.end()); return order[k % remaining]; }  // 층 전체를 못 먹으면 남은 음식의 원래 번호를 정렬해 k % remaining 위치 반환
//         k -= cost; previous = foods[position].first;  // 현재 층의 시간을 k에서 빼고 제거한 높이 갱신
//     }  // 블록 끝
//     return -1;  // 모든 음식을 제거한 경우 -1 반환
// }  // 함수 끝
//

// 풀이 요약
// 음식 시간을 작은 순서로 정렬해 같은 높이의 층을 한 번에 제거. 다음 층을 전부 못 먹으면 남은 음식 번호를 정렬해 k의 나머지 위치 선택.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:49:16
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level4/extra_42891_%EB%AC%B4%EC%A7%80%EC%9D%98_%EB%A8%B9%EB%B0%A9_%EB%9D%BC%EC%9D%B4%EB%B8%8C/README.md)
