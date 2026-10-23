# 거리두기 확인하기

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/81302) · Level 2 · C++

## 풀이

모든 사람 쌍의 맨해튼 거리를 구하고 거리 1은 바로 제외하며 거리 2는 중간 경로의 파티션 검사

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <cstdlib>
#include <string>
#include <utility>
#include <vector>
using namespace std;

vector<int> solution(vector<vector<string>> places) {
    vector<int> answer;
    for (const auto& room : places) {
        vector<pair<int, int>> people;
        for (int r = 0; r < 5; ++r) for (int c = 0; c < 5; ++c) if (room[r][c] == 'P') people.push_back({r, c});
        bool valid = true;
        for (int i = 0; i < (int)people.size(); ++i) for (int j = i + 1; j < (int)people.size(); ++j) {
            auto [r1, c1] = people[i]; auto [r2, c2] = people[j];
            int distance = abs(r1 - r2) + abs(c1 - c2);
            if (distance == 1) valid = false;
            if (distance == 2) {
                if (r1 == r2 && room[r1][(c1 + c2) / 2] != 'X') valid = false;
                else if (c1 == c2 && room[(r1 + r2) / 2][c1] != 'X') valid = false;
                else if (r1 != r2 && c1 != c2 && (room[r1][c2] != 'X' || room[r2][c1] != 'X')) valid = false;
            }
        }
        answer.push_back(valid);
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <cstdlib>  // 정수 절댓값 같은 기본 유틸리티
// #include <string>  // 문자열을 담는 string
// #include <utility>  // 두 값을 묶는 pair와 이동 유틸리티
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<int> solution(vector<vector<string>> places) {  // 두 칸 이내의 응시자 사이에 칸막이가 있는지 확인
// vector<int> answer;  // 대기실별 거리두기 준수 여부 저장
// for (const auto& room : places) {  // 각 대기실 검사
// vector<pair<int, int>> people;  // 사람이 앉은 좌표 모으기
// for (int r = 0; r < 5; ++r) for (int c = 0; c < 5; ++c) if (room[r][c] == 'P') people.push_back({r, c});  // 사람의 위치만 저장
// bool valid = true;  // 현재 대기실이 규칙을 지킨다고 초기화
// for (int i = 0; i < (int)people.size(); ++i) for (int j = i + 1; j < (int)people.size(); ++j) {  // 서로 다른 두 사람의 모든 쌍 검사
// auto [r1, c1] = people[i]; auto [r2, c2] = people[j];  // 두 좌표를 구조 분해로 읽기
// int distance = abs(r1 - r2) + abs(c1 - c2);  // 맨해튼 거리 계산
// if (distance == 1) valid = false;  // 바로 붙어 앉은 경우는 위반
// if (distance == 2) {  // 두 칸 거리에서는 사이의 파티션 확인
// if (r1 == r2 && room[r1][(c1 + c2) / 2] != 'X') valid = false;  // 같은 행이면 중간 칸이 파티션이어야 함
// else if (c1 == c2 && room[(r1 + r2) / 2][c1] != 'X') valid = false;  // 같은 열이면 중간 칸이 파티션이어야 함
// else if (r1 != r2 && c1 != c2 && (room[r1][c2] != 'X' || room[r2][c1] != 'X')) valid = false;  // 대각선이면 두 중간 경로를 모두 막아야 함
// }  // 블록 끝
// }  // 블록 끝
// answer.push_back(valid);  // bool을 1 또는 0으로 변환해 기록
// }  // 블록 끝
// return answer;  // 모든 대기실의 검사 결과 반환
// }  // 블록 끝

// 풀이 요약
// 모든 사람 쌍의 맨해튼 거리를 구하고 거리 1은 바로 제외하며 거리 2는 중간 경로의 파티션 검사
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:39:22
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/053_81302_%EA%B1%B0%EB%A6%AC%EB%91%90%EA%B8%B0_%ED%99%95%EC%9D%B8%ED%95%98%EA%B8%B0/README.md)
