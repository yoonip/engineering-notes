# 가장 큰 삼각형 덩어리

[레벨 4 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/389629) · Level 4 · C++

## 풀이

삼각형들을 최대 차수 2인 그래프로 만들어 경로·사이클로 분해. 각 경로에서 같은 원래 격자 칸이 중복되지 않는 최장 구간을 투 포인터로 찾음. 사이클은 두 바퀴 길이로 펼쳐 검사.

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

int solution(vector<vector<int>> grid) {
    int n = (int)grid.size(), m = (int)grid[0].size(), cells = n * m;
    vector<array<int, 2>> graph(cells * 2, array<int, 2>{-1, -1});
    vector<int> degree(cells * 2, 0);
    auto connect = [&](int a, int b) { graph[a][degree[a]++] = b; graph[b][degree[b]++] = a; };
    for (int r = 0; r < n; ++r) for (int c = 0; c < m; ++c) {
        int base = 2 * (r * m + c);
        if (r + 1 < n) connect(base + 1, base + 2 * m);
        if (c + 1 < m) connect(base + (grid[r][c] == 1), base + 2 + (grid[r][c + 1] == -1));
    }
    vector<bool> seen(cells * 2, false);
    vector<int> last(cells, -1), stamp(cells, -1);
    int answer = 1, component = 0;
    auto inspect = [&](int start) {
        vector<int> order; int previous = -1, current = start;
        while (!seen[current]) {
            seen[current] = true; order.push_back(current / 2); int next = -1;
            for (int d = 0; d < degree[current]; ++d) if (graph[current][d] != previous) { next = graph[current][d]; break; }
            if (next == -1) break;
            previous = current; current = next;
        }
        bool cycle = current == start && degree[start] == 2;
        int length = (int)order.size(), left = 0; ++component;
        for (int right = 0; right < length * (cycle ? 2 : 1); ++right) {
            int cell = order[right % length];
            if (stamp[cell] == component) left = max(left, last[cell] + 1);
            left = max(left, right - length + 1); stamp[cell] = component; last[cell] = right;
            answer = max(answer, right - left + 1);
        }
    };
    for (int node = 0; node < cells * 2; ++node) if (!seen[node] && degree[node] < 2) inspect(node);
    for (int node = 0; node < cells * 2; ++node) if (!seen[node]) inspect(node);
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
// int solution(vector<vector<int>> grid) {  // 가장 큰 삼각형 덩어리 풀이 함수 정의
//     int n = (int)grid.size(), m = (int)grid[0].size(), cells = n * m;  // 행·열 크기와 원래 격자 칸 수 cells 저장
//     vector<array<int, 2>> graph(cells * 2, array<int, 2>{-1, -1});  // 칸마다 두 삼각형을 두고, 삼각형당 최대 두 이웃을 저장할 그래프 준비
//     vector<int> degree(cells * 2, 0);  // 각 삼각형의 연결된 이웃 수 degree를 0으로 초기화
//     auto connect = [&](int a, int b) { graph[a][degree[a]++] = b; graph[b][degree[b]++] = a; };  // 두 삼각형을 양방향으로 연결하고 각각 차수를 증가시키는 람다
//     for (int r = 0; r < n; ++r) for (int c = 0; c < m; ++c) {  // 각 격자 칸의 아래쪽·오른쪽 연결 검사
//         int base = 2 * (r * m + c);  // 현재 칸에 속한 두 삼각형의 시작 번호 base 계산
//         if (r + 1 < n) connect(base + 1, base + 2 * m);  // 아래 칸이 있으면 아래쪽 삼각형과 다음 칸의 위쪽 삼각형 연결
//         if (c + 1 < m) connect(base + (grid[r][c] == 1), base + 2 + (grid[r][c + 1] == -1));  // 오른쪽 칸이 있으면 두 대각선 방향에 맞춰 맞닿은 삼각형 연결
//     }  // 블록 끝
//     vector<bool> seen(cells * 2, false);  // 그래프에서 처리한 삼각형을 표시할 seen 준비
//     vector<int> last(cells, -1), stamp(cells, -1);  // 원래 칸별 마지막 등장 위치 last와 어느 연결 요소에서 사용했는지 stamp 준비
//     int answer = 1, component = 0;  // 최대 구간 길이 answer는 1, 연결 요소 구분 번호 component는 0으로 시작
//     auto inspect = [&](int start) {  // 한 경로 또는 사이클을 순서대로 읽고 최장 구간을 구하는 람다
//         vector<int> order; int previous = -1, current = start;  // 방문 순서 order, 직전 삼각형 previous, 현재 삼각형 current 준비
//         while (!seen[current]) {  // 아직 방문하지 않은 삼각형을 따라 이동
//             seen[current] = true; order.push_back(current / 2); int next = -1;  // 삼각형을 방문 표시하고 원래 격자 칸 번호를 순서에 추가
//             for (int d = 0; d < degree[current]; ++d) if (graph[current][d] != previous) { next = graph[current][d]; break; }  // 직전 삼각형으로 돌아가지 않는 다음 이웃 찾기
//             if (next == -1) break;  // 이웃이 없으면 경로 끝이므로 탐색 종료
//             previous = current; current = next;  // 직전·현재 삼각형을 한 칸씩 전진
//         }  // 블록 끝
//         bool cycle = current == start && degree[start] == 2;  // 시작점으로 돌아왔고 차수가 2이면 사이클로 구분
//         int length = (int)order.size(), left = 0; ++component;  // 방문 순서 길이와 구간의 왼쪽 끝을 준비하고 새 연결 요소 번호 부여
//         for (int right = 0; right < length * (cycle ? 2 : 1); ++right) {  // 사이클은 경계를 넘는 구간까지 보도록 두 배 길이, 경로는 한 번만 순회
//             int cell = order[right % length];  // 순환 인덱스로 현재 원래 칸 번호 조회
//             if (stamp[cell] == component) left = max(left, last[cell] + 1);  // 같은 연결 요소에서 이미 나온 칸이면 중복이 빠지도록 왼쪽 끝 전진
//             left = max(left, right - length + 1); stamp[cell] = component; last[cell] = right;  // 한 바퀴보다 길어지지 않게 제한하고 현재 칸의 등장 위치 갱신
//             answer = max(answer, right - left + 1);  // 중복 칸이 없는 현재 구간 길이로 최댓값 갱신
//         }  // 블록 끝
//     };  // 블록 끝
//     for (int node = 0; node < cells * 2; ++node) if (!seen[node] && degree[node] < 2) inspect(node);  // 차수가 2보다 작은 끝점부터 경로 요소 검사
//     for (int node = 0; node < cells * 2; ++node) if (!seen[node]) inspect(node);  // 남은 미방문 삼각형은 사이클이므로 별도로 검사
//     return answer;  // 같은 원래 칸을 중복 사용하지 않는 최대 삼각형 구간 길이 반환
// }  // 함수 끝
//

// 풀이 요약
// 삼각형들을 최대 차수 2인 그래프로 만들어 경로·사이클로 분해. 각 경로에서 같은 원래 격자 칸이 중복되지 않는 최장 구간을 투 포인터로 찾음. 사이클은 두 바퀴 길이로 펼쳐 검사.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:42:00
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level4/extra_389629_%EA%B0%80%EC%9E%A5_%ED%81%B0_%EC%82%BC%EA%B0%81%ED%98%95_%EB%8D%A9%EC%96%B4%EB%A6%AC/README.md)
