# [PCCP 기출문제] 3번 / 충돌위험 찾기

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/340211) · Level 2 · C++

## 풀이

모든 로봇을 초 단위로 함께 이동시키고 매 시각 좌표별 로봇 수가 둘 이상인 위치 세기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <map>
#include <utility>
#include <vector>
using namespace std;

int solution(vector<vector<int>> points, vector<vector<int>> routes) {
    struct Robot { int r, c, index; vector<int> route; };
    vector<Robot> robots;
    for (const auto& route : routes) robots.push_back({points[route[0] - 1][0], points[route[0] - 1][1], 1, route});
    int answer = 0;
    while (!robots.empty()) {
        map<pair<int, int>, int> counts;
        vector<Robot> next;
        for (Robot robot : robots) {
            ++counts[{robot.r, robot.c}];
            if (robot.index == (int)robot.route.size()) continue;
            const auto& target = points[robot.route[robot.index] - 1];
            if (robot.r != target[0]) robot.r += robot.r < target[0] ? 1 : -1;
            else if (robot.c != target[1]) robot.c += robot.c < target[1] ? 1 : -1;
            if (robot.r == target[0] && robot.c == target[1]) ++robot.index;
            next.push_back(move(robot));
        }
        for (const auto& entry : counts) if (entry.second >= 2) ++answer;
        robots = move(next);
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <map>  // 키를 정렬해 보관하는 map
// #include <utility>  // 두 값을 묶는 pair와 이동 유틸리티
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<vector<int>> points, vector<vector<int>> routes) {  // 매초 같은 좌표에 모인 로봇 충돌 세기
// struct Robot { int r, c, index; vector<int> route; };  // 로봇의 위치와 다음 경유지 인덱스 및 경로 묶기
// vector<Robot> robots;  // 아직 이동을 마치지 않은 로봇 저장
// for (const auto& route : routes) robots.push_back({points[route[0] - 1][0], points[route[0] - 1][1], 1, route});  // 각 경로의 첫 점에 로봇을 배치
// int answer = 0;  // 충돌 위험 발생 수 초기화
// while (!robots.empty()) {  // 모든 로봇이 경로를 마칠 때까지 시간별로 처리
// map<pair<int, int>, int> counts;  // 현재 시각의 좌표별 로봇 수 세기
// vector<Robot> next;  // 한 초 뒤에도 남는 로봇 저장
// for (Robot robot : robots) {  // 현재 시각의 각 로봇 처리
// ++counts[{robot.r, robot.c}];  // 이동하기 전 현재 위치의 로봇 수 늘리기
// if (robot.index == (int)robot.route.size()) continue;  // 마지막 지점에 도착한 로봇은 다음 시각에서 제외
// const auto& target = points[robot.route[robot.index] - 1];  // 다음 경유지 좌표 읽기
// if (robot.r != target[0]) robot.r += robot.r < target[0] ? 1 : -1;  // 행 방향을 우선해 한 칸 움직이기
// else if (robot.c != target[1]) robot.c += robot.c < target[1] ? 1 : -1;  // 행이 같으면 열 방향으로 한 칸 움직이기
// if (robot.r == target[0] && robot.c == target[1]) ++robot.index;  // 경유지에 도착하면 다음 목표를 가리킴
// next.push_back(move(robot));  // 이동한 로봇을 다음 시각의 목록에 넣기
// }  // 블록 끝
// for (const auto& entry : counts) if (entry.second >= 2) ++answer;  // 같은 시각 같은 좌표에 둘 이상 있으면 한 번 세기
// robots = move(next);  // 다음 시각의 상태로 바꾸기
// }  // 블록 끝
// return answer;  // 누적 충돌 위험 수 반환
// }  // 블록 끝

// 풀이 요약
// 모든 로봇을 초 단위로 함께 이동시키고 매 시각 좌표별 로봇 수가 둘 이상인 위치 세기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:26:48
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/010_340211_%EC%B6%A9%EB%8F%8C%EC%9C%84%ED%97%98_%EC%B0%BE%EA%B8%B0/README.md)
