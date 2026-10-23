# 다리를 지나는 트럭

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/42583) · Level 2 · C++

## 풀이

다리 위 트럭의 퇴장 시각과 하중을 관리하며 필요하면 가장 이른 퇴장 시각으로 이동해 다음 트럭 올리기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <deque>
#include <utility>
#include <vector>
using namespace std;

int solution(int bridge_length, int weight, vector<int> truck_weights) {
    deque<pair<int, int>> bridge;
    int time = 0, load = 0;
    for (int truck : truck_weights) {
        ++time;
        while (!bridge.empty() && (bridge.front().second <= time || load + truck > weight)) {
            auto [leaving, exit_time] = bridge.front(); bridge.pop_front();
            time = max(time, exit_time); load -= leaving;
        }
        bridge.push_back({truck, time + bridge_length});
        load += truck;
    }
    return bridge.back().second;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <deque>  // 양 끝에서 넣고 뺄 수 있는 deque
// #include <utility>  // 두 값을 묶는 pair와 이동 유틸리티
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(int bridge_length, int weight, vector<int> truck_weights) {  // 다리 위 하중과 퇴장 시각으로 트럭 통과 계산
// deque<pair<int, int>> bridge;  // 다리 위 트럭의 무게와 나갈 시각 저장
// int time = 0, load = 0;  // 현재 시각과 다리 하중 초기화
// for (int truck : truck_weights) {  // 대기 트럭을 순서대로 올리기
// ++time;  // 다음 트럭이 올라갈 수 있는 최소 시각으로 이동
// while (!bridge.empty() && (bridge.front().second <= time || load + truck > weight)) {  // 이미 나갈 트럭이나 하중 때문에 먼저 나가야 할 트럭 처리
// auto [leaving, exit_time] = bridge.front(); bridge.pop_front();  // 가장 먼저 나갈 트럭 꺼내기
// time = max(time, exit_time); load -= leaving;  // 필요하면 시각을 건너뛰고 다리 하중 줄이기
// }  // 블록 끝
// bridge.push_back({truck, time + bridge_length});  // 새 트럭의 퇴장 시각 기록
// load += truck;  // 다리 위 하중 늘리기
// }  // 블록 끝
// return bridge.back().second;  // 마지막 트럭이 다리를 나가는 시각 반환
// }  // 블록 끝

// 풀이 요약
// 다리 위 트럭의 퇴장 시각과 하중을 관리하며 필요하면 가장 이른 퇴장 시각으로 이동해 다음 트럭 올리기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:25:20
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/083_42583_%EB%8B%A4%EB%A6%AC%EB%A5%BC_%EC%A7%80%EB%82%98%EB%8A%94_%ED%8A%B8%EB%9F%AD/README.md)
