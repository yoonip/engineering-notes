# 기둥과 보 설치

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/60061) · Level 3 · C++

## 풀이

설치 때는 해당 구조물의 지지 조건을 검사하고 삭제 때는 남은 구조물 전체의 유효성을 확인해 필요하면 되돌리기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <array>
#include <set>
#include <vector>
using namespace std;

vector<vector<int>> solution(int n, vector<vector<int>> build_frame) {
    (void)n; set<array<int,3>> structures;
    auto has = [&](int x, int y, int kind) { return structures.count({x,y,kind}) != 0; };
    auto valid = [&](int x, int y, int kind) {
        if (kind == 0) return y == 0 || has(x,y - 1,0) || has(x - 1,y,1) || has(x,y,1);
        return has(x,y - 1,0) || has(x + 1,y - 1,0) || (has(x - 1,y,1) && has(x + 1,y,1));
    };
    for (const auto& frame : build_frame) {
        int x = frame[0], y = frame[1], kind = frame[2];
        if (frame[3] == 1) { if (valid(x,y,kind)) structures.insert({x,y,kind}); }
        else {
            structures.erase({x,y,kind}); bool all_valid = true;
            for (auto [sx,sy,sk] : structures) if (!valid(sx,sy,sk)) { all_valid = false; break; }
            if (!all_valid) structures.insert({x,y,kind});
        }
    }
    vector<vector<int>> answer; for (const auto& structure : structures) answer.push_back({structure[0],structure[1],structure[2]});
    return answer;
}

// 전체 코드 줄별 설명
// #include <array>  // 크기가 고정된 array
// #include <set>  // 정렬된 집합과 중복을 허용하는 multiset
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<vector<int>> solution(int n, vector<vector<int>> build_frame) {  // 설치·삭제 뒤 지지 조건이 유지되는지 확인
// (void)n; set<array<int,3>> structures;  // 설치된 기둥과 보를 좌표와 종류로 저장
// auto has = [&](int x, int y, int kind) { return structures.count({x,y,kind}) != 0; };  // 해당 위치의 구조물이 있는지 확인
// auto valid = [&](int x, int y, int kind) {  // 하나의 구조물이 설치 규칙을 만족하는지 검사
// if (kind == 0) return y == 0 || has(x,y - 1,0) || has(x - 1,y,1) || has(x,y,1);  // 기둥은 바닥, 아래 기둥, 양쪽 보 중 하나에 받쳐야 함
// return has(x,y - 1,0) || has(x + 1,y - 1,0) || (has(x - 1,y,1) && has(x + 1,y,1));  // 보는 양 끝 기둥이나 양쪽 보에 지지되어야 함
// };  // 블록 끝
// for (const auto& frame : build_frame) {  // 설치 및 삭제 명령을 순서대로 처리
// int x = frame[0], y = frame[1], kind = frame[2];  // 구조물의 좌표와 종류 읽기
// if (frame[3] == 1) { if (valid(x,y,kind)) structures.insert({x,y,kind}); }  // 설치 조건을 만족할 때만 추가
// else {  // 삭제 후 남은 구조물들의 안정성 검사
// structures.erase({x,y,kind}); bool all_valid = true;  // 우선 구조물을 지우고 검사 결과 초기화
// for (auto [sx,sy,sk] : structures) if (!valid(sx,sy,sk)) { all_valid = false; break; }  // 남은 구조물 중 규칙 위반이 있는지 확인
// if (!all_valid) structures.insert({x,y,kind});  // 다른 구조물이 불안정해지면 삭제 되돌리기
// }  // 블록 끝
// }  // 블록 끝
// vector<vector<int>> answer; for (const auto& structure : structures) answer.push_back({structure[0],structure[1],structure[2]});  // 정렬된 집합 순서로 결과 만들기
// return answer;  // 최종 기둥과 보 목록 반환
// }  // 블록 끝

// 풀이 요약
// 설치 때는 해당 구조물의 지지 조건을 검사하고 삭제 때는 남은 구조물 전체의 유효성을 확인해 필요하면 되돌리기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:42:08
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/054_60061_%EA%B8%B0%EB%91%A5%EA%B3%BC_%EB%B3%B4_%EC%84%A4%EC%B9%98/README.md)
