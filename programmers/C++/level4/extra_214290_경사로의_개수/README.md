# 경사로의 개수

[레벨 4 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/214290) · Level 4 · C++

## 풀이

높이 차이별 이동 간선을 미리 분류. 수열 d를 한 번 따르는 경로 수를 전이 행렬로 만들고, k번 반복은 행렬 거듭제곱으로 계산.

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

int solution(vector<vector<int>> grid, vector<int> d, int k) {
    const int mod = 1000000007;
    int n = (int)grid.size(), m = (int)grid[0].size(), size = n * m;
    unordered_map<int, vector<pair<int, int>>> edges;
    int dr[4] = {-1, 1, 0, 0}, dc[4] = {0, 0, -1, 1};
    for (int r = 0; r < n; ++r) for (int c = 0; c < m; ++c) for (int direction = 0; direction < 4; ++direction) {
        int nr = r + dr[direction], nc = c + dc[direction];
        if (0 <= nr && nr < n && 0 <= nc && nc < m) edges[grid[nr][nc] - grid[r][c]].push_back({r * m + c, nr * m + nc});
    }
    vector<vector<int>> matrix(size, vector<int>(size));
    for (int start = 0; start < size; ++start) {
        vector<int> ways(size, 0); ways[start] = 1;
        for (int slope : d) {
            vector<int> next(size, 0);
            for (const auto& edge : edges[slope]) next[edge.second] = (next[edge.second] + ways[edge.first]) % mod;
            ways.swap(next);
        }
        matrix[start] = move(ways);
    }
    auto multiply = [&](const vector<vector<int>>& a, const vector<vector<int>>& b) {
        vector<vector<int>> result(a.size(), vector<int>(size, 0));
        for (int i = 0; i < (int)a.size(); ++i) for (int middle = 0; middle < size; ++middle) if (a[i][middle])
            for (int end = 0; end < size; ++end) result[i][end] = (result[i][end] + 1LL * a[i][middle] * b[middle][end]) % mod;
        return result;
    };
    vector<vector<int>> answer(1, vector<int>(size, 1));
    while (k) {
        if (k & 1) answer = multiply(answer, matrix);
        k /= 2;
        if (k) matrix = multiply(matrix, matrix);
    }
    return (int)(accumulate(answer[0].begin(), answer[0].end(), 0LL) % mod);
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
// int solution(vector<vector<int>> grid, vector<int> d, int k) {  // 경사로의 개수 풀이 함수 정의
//     const int mod = 1000000007;  // 경로 수를 나눌 모듈러 상수 저장
//     int n = (int)grid.size(), m = (int)grid[0].size(), size = n * m;  // 격자 크기와 전체 칸 수 size 계산
//     unordered_map<int, vector<pair<int, int>>> edges;  // 높이 차이를 키로 이동 가능한 간선들을 모을 해시 맵 준비
//     int dr[4] = {-1, 1, 0, 0}, dc[4] = {0, 0, -1, 1};  // 상하좌우의 행·열 이동량 저장
//     for (int r = 0; r < n; ++r) for (int c = 0; c < m; ++c) for (int direction = 0; direction < 4; ++direction) {  // 모든 칸에서 네 방향 이동 검사
//         int nr = r + dr[direction], nc = c + dc[direction];  // 이웃 칸 좌표 계산
//         if (0 <= nr && nr < n && 0 <= nc && nc < m) edges[grid[nr][nc] - grid[r][c]].push_back({r * m + c, nr * m + nc});  // 범위 안의 이웃이면 높이 차이에 따라 출발·도착 칸 번호를 분류해 저장
//     }  // 블록 끝
//     vector<vector<int>> matrix(size, vector<int>(size));  // d 한 묶음을 따르는 출발점별 도착 경로 수 행렬 준비
//     for (int start = 0; start < size; ++start) {  // 모든 칸을 각각 시작점으로 선택
//         vector<int> ways(size, 0); ways[start] = 1;  // 현재 시작점에 도달한 경로 수 1로 초기화
//         for (int slope : d) {  // d에 주어진 높이 차이를 차례로 적용
//             vector<int> next(size, 0);  // 이번 높이 차이를 적용한 다음 경로 수 배열 준비
//             for (const auto& edge : edges[slope]) next[edge.second] = (next[edge.second] + ways[edge.first]) % mod;  // 해당 경사 간선마다 출발 칸의 경로 수를 도착 칸에 누적하고 나머지 계산
//             ways.swap(next);  // 이번 높이 차이까지 반영한 경로 수로 교체
//         }  // 블록 끝
//         matrix[start] = move(ways);  // 시작점의 한 묶음 경로 수를 전이 행렬의 행으로 이동
//     }  // 블록 끝
//     auto multiply = [&](const vector<vector<int>>& a, const vector<vector<int>>& b) {  // 두 경로 수 행렬을 합성하는 곱셈 람다
//         vector<vector<int>> result(a.size(), vector<int>(size, 0));  // 왼쪽 행 수와 도착 칸 수에 맞는 결과 행렬 준비
//         for (int i = 0; i < (int)a.size(); ++i) for (int middle = 0; middle < size; ++middle) if (a[i][middle])  // 각 출발·중간 칸을 검사하되 경로 수가 0인 항은 건너뜀
//             for (int end = 0; end < size; ++end) result[i][end] = (result[i][end] + 1LL * a[i][middle] * b[middle][end]) % mod;  // 출발→중간과 중간→도착 경로 수를 곱해 누적. 곱은 long long으로 계산
//         return result;  // 합성한 경로 수 행렬 반환
//     };  // 블록 끝
//     vector<vector<int>> answer(1, vector<int>(size, 1));  // 모든 칸에서 시작할 수 있도록 시작 분포를 1로 초기화
//     while (k) {  // 반복 횟수 k의 이진 자릿수를 처리
//         if (k & 1) answer = multiply(answer, matrix);  // 현재 비트가 1이면 해당 길이 전이를 결과 분포에 적용
//         k /= 2;  // 다음 이진 자릿수로 이동
//         if (k) matrix = multiply(matrix, matrix);  // 남은 비트가 있으면 행렬을 제곱해 전이 길이 두 배로 증가
//     }  // 블록 끝
//     return (int)(accumulate(answer[0].begin(), answer[0].end(), 0LL) % mod);  // 모든 시작점·도착점 조합의 경로 수 합을 나머지로 반환
// }  // 함수 끝
//

// 풀이 요약
// 높이 차이별 이동 간선을 미리 분류. 수열 d를 한 번 따르는 경로 수를 전이 행렬로 만들고, k번 반복은 행렬 거듭제곱으로 계산.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:42:31
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level4/extra_214290_%EA%B2%BD%EC%82%AC%EB%A1%9C%EC%9D%98_%EA%B0%9C%EC%88%98/README.md)
