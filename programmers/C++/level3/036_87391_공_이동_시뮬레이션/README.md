# 공 이동 시뮬레이션

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/87391) · Level 3 · C++

## 풀이

목표 좌표에서 이동 명령을 역순으로 되돌리며 가능한 시작 행과 열의 구간을 확장하고 교집합이 사라지는지 확인

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <array>
#include <vector>
using namespace std;

long long solution(int n, int m, int x, int y, vector<vector<int>> queries) {
    array<array<long long, 2>, 2> bounds{{{y,y},{x,x}}}; long long lengths[2] = {m,n};
    for (int i = (int)queries.size() - 1; i >= 0; --i) {
        int command = queries[i][0], axis = command / 2; long long distance = queries[i][1];
        long long low = bounds[axis][0], high = bounds[axis][1], length = lengths[axis];
        if (command % 2 == 0) { if (low != 0) low += distance; high = min(length - 1, high + distance); }
        else { if (high != length - 1) high -= distance; low = max(0LL, low - distance); }
        if (low > high) return 0;
        bounds[axis] = {low, high};
    }
    return (bounds[0][1] - bounds[0][0] + 1) * (bounds[1][1] - bounds[1][0] + 1);
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <array>  // 크기가 고정된 array
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// long long solution(int n, int m, int x, int y, vector<vector<int>> queries) {  // 명령을 거꾸로 되돌려 가능한 시작 구간 계산
// array<array<long long, 2>, 2> bounds{{{y,y},{x,x}}}; long long lengths[2] = {m,n};  // 목표에서 가능한 열과 행의 닫힌 구간을 시작
// for (int i = (int)queries.size() - 1; i >= 0; --i) {  // 이동 명령을 역순으로 되돌리기
// int command = queries[i][0], axis = command / 2; long long distance = queries[i][1];  // 이동 축과 거리 읽기
// long long low = bounds[axis][0], high = bounds[axis][1], length = lengths[axis];  // 해당 축의 현재 후보 구간 읽기
// if (command % 2 == 0) { if (low != 0) low += distance; high = min(length - 1, high + distance); }  // 왼쪽 또는 위쪽 이동을 역으로 확장
// else { if (high != length - 1) high -= distance; low = max(0LL, low - distance); }  // 오른쪽 또는 아래쪽 이동을 역으로 확장
// if (low > high) return 0;  // 가능한 시작 좌표가 없어지면 0 반환
// bounds[axis] = {low, high};  // 되돌린 구간 저장
// }  // 블록 끝
// return (bounds[0][1] - bounds[0][0] + 1) * (bounds[1][1] - bounds[1][0] + 1);  // 행과 열 후보 수의 곱 반환
// }  // 블록 끝

// 풀이 요약
// 목표 좌표에서 이동 명령을 역순으로 되돌리며 가능한 시작 행과 열의 구간을 확장하고 교집합이 사라지는지 확인
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:53:37
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level3/036_87391_%EA%B3%B5_%EC%9D%B4%EB%8F%99_%EC%8B%9C%EB%AE%AC%EB%A0%88%EC%9D%B4%EC%85%98/README.md)
