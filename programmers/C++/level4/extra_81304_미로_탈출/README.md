# 미로 탈출

[레벨 4 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/81304) · Level 4 · C++

## 풀이

현재 방과 함정 비트마스크를 하나의 상태로 둔 다익스트라. 양 끝 함정 활성 여부가 다를 때만 간선 방향이 뒤집힘.

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

int solution(int n, int start, int end, vector<vector<int>> roads, vector<int> traps) {
    vector<int> bits(n + 1, 0); for (int i = 0; i < (int)traps.size(); ++i) bits[traps[i]] = 1 << i;
    vector<vector<tuple<int, int, bool>>> graph(n + 1);
    for (const auto& road : roads) { graph[road[0]].push_back({road[1], road[2], false}); graph[road[1]].push_back({road[0], road[2], true}); }
    int states = 1 << traps.size(); vector<vector<long long>> distance(n + 1, vector<long long>(states, LLONG_MAX));
    priority_queue<tuple<long long, int, int>, vector<tuple<long long, int, int>>, greater<tuple<long long, int, int>>> heap;
    distance[start][0] = 0; heap.push({0, start, 0});
    while (!heap.empty()) {
        auto [cost, node, mask] = heap.top(); heap.pop();
        if (cost != distance[node][mask]) continue;
        if (node == end) return (int)cost;
        bool active = (mask & bits[node]) != 0;
        for (const auto& [neighbor, weight, backwards] : graph[node]) {
            bool flipped = active != ((mask & bits[neighbor]) != 0);
            if (flipped != backwards) continue;
            int next_mask = mask ^ bits[neighbor]; long long next_cost = cost + weight;
            if (next_cost < distance[neighbor][next_mask]) { distance[neighbor][next_mask] = next_cost; heap.push({next_cost, neighbor, next_mask}); }
        }
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
// int solution(int n, int start, int end, vector<vector<int>> roads, vector<int> traps) {  // 미로 탈출 풀이 함수 정의
//     vector<int> bits(n + 1, 0); for (int i = 0; i < (int)traps.size(); ++i) bits[traps[i]] = 1 << i;  // 함정 방마다 서로 다른 비트를 배정하고 일반 방은 0으로 둠
//     vector<vector<tuple<int, int, bool>>> graph(n + 1);  // 원래 방향과 역방향을 구분해 저장할 인접 리스트 준비
//     for (const auto& road : roads) { graph[road[0]].push_back({road[1], road[2], false}); graph[road[1]].push_back({road[0], road[2], true}); }  // 도로를 정방향·역방향 정보와 함께 양쪽 인접 목록에 저장
//     int states = 1 << traps.size(); vector<vector<long long>> distance(n + 1, vector<long long>(states, LLONG_MAX));  // 함정 상태 수만큼 방별 최소 비용 배열을 무한대로 초기화
//     priority_queue<tuple<long long, int, int>, vector<tuple<long long, int, int>>, greater<tuple<long long, int, int>>> heap;  // 비용이 작은 상태부터 꺼낼 최소 힙 준비
//     distance[start][0] = 0; heap.push({0, start, 0});  // 시작 방·비활성 함정 상태를 비용 0으로 삽입
//     while (!heap.empty()) {  // 방문할 상태가 남아 있는 동안 최단 경로 탐색
//         auto [cost, node, mask] = heap.top(); heap.pop();  // 비용 cost, 현재 방 node, 함정 상태 mask 추출
//         if (cost != distance[node][mask]) continue;  // 이후 더 짧은 경로가 발견된 오래된 힙 항목이면 건너뜀
//         if (node == end) return (int)cost;  // 도착 방을 최소 비용으로 꺼냈으므로 그 비용 반환
//         bool active = (mask & bits[node]) != 0;  // 현재 방의 함정 활성 여부 계산
//         for (const auto& [neighbor, weight, backwards] : graph[node]) {  // 현재 방과 연결된 각 도로의 이웃·비용·원래 역방향 여부 확인
//             bool flipped = active != ((mask & bits[neighbor]) != 0);  // 두 방의 활성 여부가 다르면 도로 방향이 뒤집힌 상태
//             if (flipped != backwards) continue;  // 현재 방향으로 갈 수 없는 간선이면 건너뜀
//             int next_mask = mask ^ bits[neighbor]; long long next_cost = cost + weight;  // 이웃 방에 진입해 함정 비트를 토글하고 새 비용 계산
//             if (next_cost < distance[neighbor][next_mask]) { distance[neighbor][next_mask] = next_cost; heap.push({next_cost, neighbor, next_mask}); }  // 이전보다 짧은 경로면 거리 갱신 후 힙에 새 상태 추가
//         }  // 블록 끝
//     }  // 블록 끝
//     return -1;  // 도착 가능한 상태가 없으면 -1 반환
// }  // 함수 끝
//

// 풀이 요약
// 현재 방과 함정 비트마스크를 하나의 상태로 둔 다익스트라. 양 끝 함정 활성 여부가 다를 때만 간선 방향이 뒤집힘.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:44:24
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level4/extra_81304_%EB%AF%B8%EB%A1%9C_%ED%83%88%EC%B6%9C/README.md)
