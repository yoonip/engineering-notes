# 미로 탈출 명령어

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/150365) · Level 3 · C++

## 풀이

남은 거리와 이동 횟수의 홀짝으로 도착 가능성을 확인하며 매 단계 사전순으로 가장 빠른 가능한 이동 고르기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <cstdlib>
#include <string>
using namespace std;

string solution(int n, int m, int x, int y, int r, int c, int k) {
    int distance = abs(x - r) + abs(y - c);
    if (distance > k || (k - distance) % 2) return "impossible";
    string letters = "dlru", answer; int dr[4] = {1, 0, 0, -1}, dc[4] = {0, -1, 1, 0};
    for (int step = 0; step < k; ++step) {
        int remaining = k - step - 1;
        for (int d = 0; d < 4; ++d) {
            int nx = x + dr[d], ny = y + dc[d];
            if (nx < 1 || nx > n || ny < 1 || ny > m) continue;
            int needed = abs(nx - r) + abs(ny - c);
            if (needed <= remaining && (remaining - needed) % 2 == 0) { answer += letters[d]; x = nx; y = ny; break; }
        }
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <cstdlib>  // 정수 절댓값 같은 기본 유틸리티
// #include <string>  // 문자열을 담는 string
// using namespace std;  // std:: 접두사 생략
// string solution(int n, int m, int x, int y, int r, int c, int k) {  // 남은 거리와 홀짝을 보며 사전순 최소 경로 선택
// int distance = abs(x - r) + abs(y - c);  // 시작점과 도착점의 맨해튼 거리 구하기
// if (distance > k || (k - distance) % 2) return "impossible";  // 필요한 거리보다 짧거나 홀짝이 다르면 불가능
// string letters = "dlru", answer; int dr[4] = {1, 0, 0, -1}, dc[4] = {0, -1, 1, 0};  // 사전순의 이동 문자와 방향 선언
// for (int step = 0; step < k; ++step) {  // 정확히 k번의 이동을 차례대로 정하기
// int remaining = k - step - 1;  // 이번 이동 뒤 남는 횟수
// for (int d = 0; d < 4; ++d) {  // 사전순으로 가능한 다음 이동 고르기
// int nx = x + dr[d], ny = y + dc[d];  // 이동 후 좌표 계산
// if (nx < 1 || nx > n || ny < 1 || ny > m) continue;  // 미로 밖으로 나가면 제외
// int needed = abs(nx - r) + abs(ny - c);  // 새 위치에서 목표까지 필요한 거리 구하기
// if (needed <= remaining && (remaining - needed) % 2 == 0) { answer += letters[d]; x = nx; y = ny; break; }  // 남은 이동으로 도착할 수 있는 첫 문자 선택
// }  // 블록 끝
// }  // 블록 끝
// return answer;  // 사전순으로 가장 빠른 이동 문자열 반환
// }  // 블록 끝

// 풀이 요약
// 남은 거리와 이동 횟수의 홀짝으로 도착 가능성을 확인하며 매 단계 사전순으로 가장 빠른 가능한 이동 고르기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:49:48
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/022_150365_%EB%AF%B8%EB%A1%9C_%ED%83%88%EC%B6%9C_%EB%AA%85%EB%A0%B9%EC%96%B4/README.md)
