# 조이스틱

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/42860) · Level 2 · C++

## 풀이

각 문자의 위아래 변경 비용을 더하고 연속된 A 구간을 건너뛰는 두 방향의 왕복 이동 비용 비교

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <string>
using namespace std;

int solution(string name) {
    int vertical = 0, n = (int)name.size();
    for (char c : name) vertical += min(c - 'A', 'Z' - c + 1);
    int horizontal = n - 1;
    for (int index = 0; index < n; ++index) {
        int next = index + 1;
        while (next < n && name[next] == 'A') ++next;
        int tail = n - next;
        horizontal = min({horizontal, 2 * index + tail, index + 2 * tail});
    }
    return vertical + horizontal;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <string>  // 문자열을 담는 string
// using namespace std;  // std:: 접두사 생략
// int solution(string name) {  // 문자 변경 비용과 A 구간 우회 거리 비교
// int vertical = 0, n = (int)name.size();  // 문자 변경 횟수와 이름 길이 구하기
// for (char c : name) vertical += min(c - 'A', 'Z' - c + 1);  // 위와 아래 중 짧은 문자 변경 횟수를 더하기
// int horizontal = n - 1;  // 끝까지 한 방향으로 이동하는 횟수로 초기화
// for (int index = 0; index < n; ++index) {  // 방향을 바꿀 위치를 모두 검사
// int next = index + 1;  // 현재 위치 다음에서 연속된 A 구간 찾기
// while (next < n && name[next] == 'A') ++next;  // 변경할 필요 없는 A 구간을 건너뛰기
// int tail = n - next;  // 뒤쪽에서 처리해야 하는 구간 길이 구하기
// horizontal = min({horizontal, 2 * index + tail, index + 2 * tail});  // 양방향 왕복 순서 중 최소 가로 이동 고르기
// }  // 블록 끝
// return vertical + horizontal;  // 문자 변경과 커서 이동의 최소 합 반환
// }  // 블록 끝

// 풀이 요약
// 각 문자의 위아래 변경 비용을 더하고 연속된 A 구간을 건너뛰는 두 방향의 왕복 이동 비용 비교
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:22:10
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/074_42860_%EC%A1%B0%EC%9D%B4%EC%8A%A4%ED%8B%B1/README.md)
