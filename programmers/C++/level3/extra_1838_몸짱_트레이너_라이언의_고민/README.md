# 몸짱 트레이너 라이언의 고민

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/1838) · Level 3 · C++

## 풀이

동시 이용자 수의 최댓값을 구하고 최소 맨해튼 거리를 큰 값부터 검사하며 기존 배치 주변의 금지 영역으로 다음 칸 고르기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <cstdlib>
#include <vector>
using namespace std;

int solution(int n, int m, vector<vector<int>> timetable) {
    (void)m; vector<int> delta(1322,0);
    for (const auto& slot : timetable) { ++delta[slot[0]]; --delta[slot[1] + 1]; }
    int current = 0, peak = 0; for (int change : delta) { current += change; peak = max(peak,current); }
    if (peak <= 1) return 0;
    for (int distance = 2 * n - 2; distance >= 1; --distance) {
        for (int offset = 0; offset < n; ++offset) {
            vector<vector<bool>> blocked(n, vector<bool>(n,false)); int placed = 0;
            for (int position = offset; position < n * n; ++position) {
                int r = position / n, c = position % n; if (blocked[r][c]) continue;
                if (++placed == peak) return distance;
                for (int row = r; row < min(n,r + distance); ++row) {
                    int reach = distance - 1 - abs(row - r);
                    for (int col = max(0,c - reach); col <= min(n - 1,c + reach); ++col) blocked[row][col] = true;
                }
            }
        }
    }
    return 1;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <cstdlib>  // 정수 절댓값 같은 기본 유틸리티
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(int n, int m, vector<vector<int>> timetable) {  // 최대 동시 이용자 수에 맞는 최소 거리 배치 찾기
// (void)m; vector<int> delta(1322,0);  // 시간별 동시 이용자 수의 변화량 저장
// for (const auto& slot : timetable) { ++delta[slot[0]]; --delta[slot[1] + 1]; }  // 이용 시작과 종료 직후의 변화량 등록
// int current = 0, peak = 0; for (int change : delta) { current += change; peak = max(peak,current); }  // 최대 동시 이용자 수 구하기
// if (peak <= 1) return 0;  // 동시에 이용하는 사람이 하나 이하면 최소 거리를 고려하지 않음
// for (int distance = 2 * n - 2; distance >= 1; --distance) {  // 가능한 최소 간격을 큰 값부터 검사
// for (int offset = 0; offset < n; ++offset) {  // 첫 행의 시작 위치를 바꾸어 배치를 시도
// vector<vector<bool>> blocked(n, vector<bool>(n,false)); int placed = 0;  // 기존 배치와 너무 가까운 칸을 표시
// for (int position = offset; position < n * n; ++position) {  // 행 우선 순서로 배치할 수 있는 칸 고르기
// int r = position / n, c = position % n; if (blocked[r][c]) continue;  // 기존 사람과 거리가 부족한 칸은 건너뛰기
// if (++placed == peak) return distance;  // 모든 동시 이용자를 놓으면 현재 간격이 최댓값
// for (int row = r; row < min(n,r + distance); ++row) {  // 앞으로 검사할 행에서 금지되는 마름모 영역을 표시
// int reach = distance - 1 - abs(row - r);  // 해당 행에서 최소 간격을 어기는 열 범위 구하기
// for (int col = max(0,c - reach); col <= min(n - 1,c + reach); ++col) blocked[row][col] = true;  // 맨해튼 거리가 distance보다 작은 칸을 금지
// }  // 블록 끝
// }  // 블록 끝
// }  // 블록 끝
// }  // 블록 끝
// return 1;  // 최소 한 칸의 간격은 확보할 수 있음
// }  // 블록 끝

// 풀이 요약
// 동시 이용자 수의 최댓값을 구하고 최소 맨해튼 거리를 큰 값부터 검사하며 기존 배치 주변의 금지 영역으로 다음 칸 고르기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:49:37
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/extra_1838_%EB%AA%B8%EC%A7%B1_%ED%8A%B8%EB%A0%88%EC%9D%B4%EB%84%88_%EB%9D%BC%EC%9D%B4%EC%96%B8%EC%9D%98_%EA%B3%A0%EB%AF%BC/README.md)
