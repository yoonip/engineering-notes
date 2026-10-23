# 카카오 앱 정리하기

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/468374) · Level 3 · C++

## 풀이

이동 축을 한 방향의 펼친 좌표로 바꾸고 앱 사이의 간격 제약을 큐로 전파해 밀림과 경계 이동 처리

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <array>
#include <queue>
#include <utility>
#include <vector>
using namespace std;

vector<vector<int>> solution(vector<vector<int>> board, vector<vector<int>> commands) {
    int n = (int)board.size(), m = (int)board[0].size(), count = 0;
    for (const auto& row : board) for (int value : row) count = max(count, value);
    vector<array<int, 3>> apps(count, array<int, 3>{-1, -1, 1});
    for (int r = 0; r < n; ++r) for (int c = 0; c < m; ++c) if (board[r][c] > 0) {
        auto& app = apps[board[r][c] - 1];
        if (app[0] == -1) app = {r, c, 1};
        else app[2] = max({app[2], r - app[0] + 1, c - app[1] + 1});
    }
    for (const auto& command : commands) {
        int number = command[0] - 1, direction = command[1], axis = direction % 2, side = 1 - axis, length = axis == 0 ? n : m;
        bool reverse = direction >= 3;
        vector<long long> positions(count);
        for (int i = 0; i < count; ++i) positions[i] = reverse ? length - apps[i][2] - apps[i][axis] : apps[i][axis];
        vector<vector<pair<int, int>>> graph(count);
        for (int i = 0; i < count; ++i) for (int j = 0; j < i; ++j) {
            if (apps[i][side] >= apps[j][side] + apps[j][2] || apps[j][side] >= apps[i][side] + apps[i][2]) continue;
            int first = positions[i] < positions[j] ? i : j, second = first == i ? j : i;
            graph[first].push_back({second, apps[first][2]});
            graph[second].push_back({first, apps[second][2] - length});
        }
        auto normalize = [&](long long value, int size) {
            long long remainder = value % length;
            if (remainder > length - size) value += length - remainder;
            return value;
        };
        positions[number] = normalize(positions[number] + 1, apps[number][2]);
        queue<int> q; vector<bool> queued(count, false); q.push(number); queued[number] = true;
        while (!q.empty()) {
            int current = q.front(); q.pop(); queued[current] = false;
            for (auto [other, gap] : graph[current]) {
                long long needed = normalize(positions[current] + gap, apps[other][2]);
                if (needed > positions[other]) {
                    positions[other] = needed;
                    if (!queued[other]) { queued[other] = true; q.push(other); }
                }
            }
        }
        for (int i = 0; i < count; ++i) { int coordinate = (int)(positions[i] % length); apps[i][axis] = reverse ? length - apps[i][2] - coordinate : coordinate; }
    }
    vector<vector<int>> answer(n, vector<int>(m, 0));
    for (int i = 0; i < count; ++i) for (int r = apps[i][0]; r < apps[i][0] + apps[i][2]; ++r) for (int c = apps[i][1]; c < apps[i][1] + apps[i][2]; ++c) answer[r][c] = i + 1;
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <array>  // 크기가 고정된 array
// #include <queue>  // BFS 큐와 우선순위 큐
// #include <utility>  // 두 값을 묶는 pair와 이동 유틸리티
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<vector<int>> solution(vector<vector<int>> board, vector<vector<int>> commands) {  // 앱을 밀 때 간격 제약과 화면 경계 반영
// int n = (int)board.size(), m = (int)board[0].size(), count = 0;  // 보드 크기와 앱 수 구하기
// for (const auto& row : board) for (int value : row) count = max(count, value);  // 가장 큰 앱 번호 찾기
// vector<array<int, 3>> apps(count, array<int, 3>{-1, -1, 1});  // 앱별 시작 행, 시작 열, 정사각형 크기 저장
// for (int r = 0; r < n; ++r) for (int c = 0; c < m; ++c) if (board[r][c] > 0) {  // 앱이 차지한 칸 읽기
// auto& app = apps[board[r][c] - 1];  // 현재 앱의 위치 정보를 참조
// if (app[0] == -1) app = {r, c, 1};  // 처음 만난 칸을 왼쪽 위 좌표로 두기
// else app[2] = max({app[2], r - app[0] + 1, c - app[1] + 1});  // 앱의 전체 정사각형 크기 갱신
// }  // 블록 끝
// for (const auto& command : commands) {  // 앱 이동 명령을 순서대로 처리
// int number = command[0] - 1, direction = command[1], axis = direction % 2, side = 1 - axis, length = axis == 0 ? n : m;  // 이동 축과 반대 축 및 축 길이 구하기
// bool reverse = direction >= 3;  // 반대 방향은 좌표를 뒤집어 같은 증가 방향으로 처리
// vector<long long> positions(count);  // 현재 이동 축의 펼친 좌표 저장
// for (int i = 0; i < count; ++i) positions[i] = reverse ? length - apps[i][2] - apps[i][axis] : apps[i][axis];  // 방향에 맞는 시작 좌표로 변환
// vector<vector<pair<int, int>>> graph(count);  // 서로 밀어내는 앱 사이의 최소 간격 제약 저장
// for (int i = 0; i < count; ++i) for (int j = 0; j < i; ++j) {  // 앱 쌍의 충돌 가능성 검사
// if (apps[i][side] >= apps[j][side] + apps[j][2] || apps[j][side] >= apps[i][side] + apps[i][2]) continue;  // 반대 축에서 겹치지 않으면 간섭하지 않음
// int first = positions[i] < positions[j] ? i : j, second = first == i ? j : i;  // 이동 축에서 앞선 앱과 뒤 앱 고르기
// graph[first].push_back({second, apps[first][2]});  // 앞 앱의 크기만큼 뒤 앱과 간격 두기
// graph[second].push_back({first, apps[second][2] - length});  // 보드가 이어지는 반대편 간격 제약도 두기
// }  // 블록 끝
// auto normalize = [&](long long value, int size) {  // 앱이 보드 경계에 걸치면 다음 시작 경계로 넘기기
// long long remainder = value % length;  // 보드 한 바퀴 안의 좌표 구하기
// if (remainder > length - size) value += length - remainder;  // 앱 전체가 들어갈 수 없는 남은 구간을 건너뛰기
// return value;  // 경계에 맞춘 펼친 좌표 반환
// };  // 블록 끝
// positions[number] = normalize(positions[number] + 1, apps[number][2]);  // 지정 앱을 한 칸 이동시키기
// queue<int> q; vector<bool> queued(count, false); q.push(number); queued[number] = true;  // 위치가 바뀐 앱부터 제약을 전파
// while (!q.empty()) {  // 밀려나는 앱의 좌표가 안정될 때까지 처리
// int current = q.front(); q.pop(); queued[current] = false;  // 현재 앱을 큐에서 꺼내기
// for (auto [other, gap] : graph[current]) {  // 이 앱과 간섭하는 다른 앱의 위치 확인
// long long needed = normalize(positions[current] + gap, apps[other][2]);  // 충돌을 피하기 위한 최소 좌표 계산
// if (needed > positions[other]) {  // 다른 앱을 더 밀어야 하는지 확인
// positions[other] = needed;  // 필요한 위치로 앱 옮기기
// if (!queued[other]) { queued[other] = true; q.push(other); }  // 아직 대기 중이 아니면 전파 큐에 넣기
// }  // 블록 끝
// }  // 블록 끝
// }  // 블록 끝
// for (int i = 0; i < count; ++i) { int coordinate = (int)(positions[i] % length); apps[i][axis] = reverse ? length - apps[i][2] - coordinate : coordinate; }  // 보드 안의 원래 방향 좌표로 되돌리기
// }  // 블록 끝
// vector<vector<int>> answer(n, vector<int>(m, 0));  // 이동 후 보드를 비운 상태로 만들기
// for (int i = 0; i < count; ++i) for (int r = apps[i][0]; r < apps[i][0] + apps[i][2]; ++r) for (int c = apps[i][1]; c < apps[i][1] + apps[i][2]; ++c) answer[r][c] = i + 1;  // 앱별 최종 정사각형 위치 채우기
// return answer;  // 명령을 모두 적용한 보드 반환
// }  // 블록 끝

// 풀이 요약
// 이동 축을 한 방향의 펼친 좌표로 바꾸고 앱 사이의 간격 제약을 큐로 전파해 밀림과 경계 이동 처리
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:43:56
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level3/006_468374_%EC%B9%B4%EC%B9%B4%EC%98%A4_%EC%95%B1_%EC%A0%95%EB%A6%AC%ED%95%98%EA%B8%B0/README.md)
