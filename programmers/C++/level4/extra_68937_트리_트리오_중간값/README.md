# 트리 트리오 중간값

[레벨 4 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/68937) · Level 4 · C++

## 풀이

BFS로 지름 양 끝을 구함. 한 끝에서 최대 거리인 정점이 여러 개면 답은 지름이고, 양쪽 모두 유일하면 지름 - 1.

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

int solution(int n, vector<vector<int>> edges) {
    vector<vector<int>> graph(n + 1);
    for (const auto& edge : edges) { graph[edge[0]].push_back(edge[1]); graph[edge[1]].push_back(edge[0]); }
    auto distances = [&](int start) {
        vector<int> distance(n + 1, -1); queue<int> pending; distance[start] = 0; pending.push(start);
        while (!pending.empty()) { int node = pending.front(); pending.pop(); for (int neighbor : graph[node]) if (distance[neighbor] == -1) { distance[neighbor] = distance[node] + 1; pending.push(neighbor); } }
        return distance;
    };
    auto initial = distances(1); int first = max_element(initial.begin(), initial.end()) - initial.begin();
    auto distance = distances(first); int diameter = *max_element(distance.begin(), distance.end());
    if (count(distance.begin(), distance.end(), diameter) >= 2) return diameter;
    int second = find(distance.begin(), distance.end(), diameter) - distance.begin(); auto other = distances(second);
    return count(other.begin(), other.end(), diameter) >= 2 ? diameter : diameter - 1;
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
// int solution(int n, vector<vector<int>> edges) {  // 트리 트리오 중간값 풀이 함수 정의
//     vector<vector<int>> graph(n + 1);  // 정점별 인접 리스트 준비
//     for (const auto& edge : edges) { graph[edge[0]].push_back(edge[1]); graph[edge[1]].push_back(edge[0]); }  // 각 트리 간선을 양쪽 인접 목록에 저장
//     auto distances = [&](int start) {  // 한 시작점에서 전체 거리를 구하는 BFS 람다
//         vector<int> distance(n + 1, -1); queue<int> pending; distance[start] = 0; pending.push(start);  // 거리는 미방문 -1, 시작점 거리는 0으로 두고 큐에 시작점 삽입
//         while (!pending.empty()) { int node = pending.front(); pending.pop(); for (int neighbor : graph[node]) if (distance[neighbor] == -1) { distance[neighbor] = distance[node] + 1; pending.push(neighbor); } }  // 미방문 이웃의 거리를 현재 + 1로 기록하며 큐 순서대로 탐색
//         return distance;  // 시작점에서 모든 정점까지의 거리 배열 반환
//     };  // 블록 끝
//     auto initial = distances(1); int first = max_element(initial.begin(), initial.end()) - initial.begin();  // 임의의 1번 정점에서 가장 먼 정점 first를 지름의 한 끝으로 선택
//     auto distance = distances(first); int diameter = *max_element(distance.begin(), distance.end());  // first에서 거리를 다시 구하고 최댓값을 지름으로 저장
//     if (count(distance.begin(), distance.end(), diameter) >= 2) return diameter;  // 지름 길이로 떨어진 정점이 두 개 이상이면 중간값의 최대도 지름
//     int second = find(distance.begin(), distance.end(), diameter) - distance.begin(); auto other = distances(second);  // 반대쪽 끝 second에서 거리 배열을 한 번 더 계산
//     return count(other.begin(), other.end(), diameter) >= 2 ? diameter : diameter - 1;  // 반대 끝에서도 지름 거리 정점이 여러 개면 지름, 양쪽 유일하면 지름 - 1 반환
// }  // 함수 끝
//

// 풀이 요약
// BFS로 지름 양 끝을 구함. 한 끝에서 최대 거리인 정점이 여러 개면 답은 지름이고, 양쪽 모두 유일하면 지름 - 1.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:45:12
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level4/extra_68937_%ED%8A%B8%EB%A6%AC_%ED%8A%B8%EB%A6%AC%EC%98%A4_%EC%A4%91%EA%B0%84%EA%B0%92/README.md)
