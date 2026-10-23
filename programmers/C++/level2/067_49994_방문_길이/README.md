# 방문 길이

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/49994) · Level 2 · C++

## 풀이

이동 구역 안의 경로를 양 끝 좌표 순서가 통일된 간선으로 저장해 방향에 관계없이 한 번씩 세기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <array>
#include <set>
#include <string>
#include <utility>
using namespace std;

int solution(string dirs) {
    int x = 0, y = 0;
    set<array<int, 4>> edges;
    for (char command : dirs) {
        int nx = x + (command == 'R') - (command == 'L'), ny = y + (command == 'U') - (command == 'D');
        if (nx < -5 || nx > 5 || ny < -5 || ny > 5) continue;
        pair<int, int> a{x, y}, b{nx, ny};
        if (a > b) swap(a, b);
        edges.insert({a.first, a.second, b.first, b.second});
        x = nx; y = ny;
    }
    return (int)edges.size();
}

// 전체 코드 줄별 설명
// #include <array>  // 크기가 고정된 array
// #include <set>  // 정렬된 집합과 중복을 허용하는 multiset
// #include <string>  // 문자열을 담는 string
// #include <utility>  // 두 값을 묶는 pair와 이동 유틸리티
// using namespace std;  // std:: 접두사 생략
// int solution(string dirs) {  // 양방향을 같은 간선으로 보고 처음 간 길만 세기
// int x = 0, y = 0;  // 시작 좌표를 원점으로 두기
// set<array<int, 4>> edges;  // 방향을 구분하지 않는 이동 경로 저장
// for (char command : dirs) {  // 각 방향 명령 처리
// int nx = x + (command == 'R') - (command == 'L'), ny = y + (command == 'U') - (command == 'D');  // 명령에 따른 다음 좌표 계산
// if (nx < -5 || nx > 5 || ny < -5 || ny > 5) continue;  // 허용 구역 밖으로 나가는 명령은 무시
// pair<int, int> a{x, y}, b{nx, ny};  // 경로의 양 끝 좌표 만들기
// if (a > b) swap(a, b);  // 반대 방향으로 지나도 같은 키가 되도록 좌표 순서를 통일
// edges.insert({a.first, a.second, b.first, b.second});  // 현재 경로를 중복 없이 집합에 넣기
// x = nx; y = ny;  // 실제 위치를 다음 좌표로 바꾸기
// }  // 블록 끝
// return (int)edges.size();  // 처음 지나간 경로의 수 반환
// }  // 블록 끝

// 풀이 요약
// 이동 구역 안의 경로를 양 끝 좌표 순서가 통일된 간선으로 저장해 방향에 관계없이 한 번씩 세기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:18:33
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/067_49994_%EB%B0%A9%EB%AC%B8_%EA%B8%B8%EC%9D%B4/README.md)
