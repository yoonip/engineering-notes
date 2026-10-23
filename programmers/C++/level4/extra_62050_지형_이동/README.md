# 지형 이동

[레벨 4 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/62050) · Level 4 · C++

## 풀이

높이 차이가 제한 이하면 이동 비용 0, 넘으면 차이만큼 사다리 비용. 최소 힙으로 가장 싼 경계부터 붙이는 프림 알고리즘 적용.

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

int solution(vector<vector<int>> land, int height) {
    int n = (int)land.size(), answer = 0; vector<vector<bool>> visited(n, vector<bool>(n, false));
    priority_queue<tuple<int, int, int>, vector<tuple<int, int, int>>, greater<tuple<int, int, int>>> heap; heap.push({0, 0, 0});
    int dr[4] = {-1, 1, 0, 0}, dc[4] = {0, 0, -1, 1};
    while (!heap.empty()) {
        auto [cost, r, c] = heap.top(); heap.pop(); if (visited[r][c]) continue; visited[r][c] = true; answer += cost;
        for (int direction = 0; direction < 4; ++direction) {
            int nr = r + dr[direction], nc = c + dc[direction];
            if (0 <= nr && nr < n && 0 <= nc && nc < n && !visited[nr][nc]) { int gap = abs(land[r][c] - land[nr][nc]); heap.push({gap <= height ? 0 : gap, nr, nc}); }
        }
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
// int solution(vector<vector<int>> land, int height) {  // 지형 이동 풀이 함수 정의
//     int n = (int)land.size(), answer = 0; vector<vector<bool>> visited(n, vector<bool>(n, false));  // 지형 크기 n, 사다리 비용 합 answer, 연결된 칸 표시 준비
//     priority_queue<tuple<int, int, int>, vector<tuple<int, int, int>>, greater<tuple<int, int, int>>> heap; heap.push({0, 0, 0});  // 최소 비용 경계를 꺼낼 힙에 시작 칸을 비용 0으로 삽입
//     int dr[4] = {-1, 1, 0, 0}, dc[4] = {0, 0, -1, 1};  // 상하좌우 행·열 이동량 저장
//     while (!heap.empty()) {  // 연결할 후보 칸이 남아 있는 동안 탐색
//         auto [cost, r, c] = heap.top(); heap.pop(); if (visited[r][c]) continue; visited[r][c] = true; answer += cost;  // 최소 경계 비용 칸을 꺼내 미방문이면 연결 표시하고 그 비용을 전체 비용에 추가
//         for (int direction = 0; direction < 4; ++direction) {  // 현재 칸의 네 이웃 검사
//             int nr = r + dr[direction], nc = c + dc[direction];  // 이웃 칸 좌표 계산
//             if (0 <= nr && nr < n && 0 <= nc && nc < n && !visited[nr][nc]) { int gap = abs(land[r][c] - land[nr][nc]); heap.push({gap <= height ? 0 : gap, nr, nc}); }  // 미연결 이웃이면 높이 차이를 구해, 허용 범위는 0원·나머지는 차이 비용으로 힙에 삽입
//         }  // 블록 끝
//     }  // 블록 끝
//     return answer;  // 모든 칸을 연결한 최소 사다리 비용 반환
// }  // 함수 끝
//

// 풀이 요약
// 높이 차이가 제한 이하면 이동 비용 0, 넘으면 차이만큼 사다리 비용. 최소 힙으로 가장 싼 경계부터 붙이는 프림 알고리즘 적용.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:47:01
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level4/extra_62050_%EC%A7%80%ED%98%95_%EC%9D%B4%EB%8F%99/README.md)
