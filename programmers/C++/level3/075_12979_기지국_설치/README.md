# 기지국 설치

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12979) · Level 3 · C++

## 풀이

기존 기지국 사이와 양 끝의 미수신 구간을 찾아 새 기지국의 수신 폭으로 올림 나눗셈

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <vector>
using namespace std;

int solution(int n, vector<int> stations, int w) {
    long long coverage = 2LL * w + 1, next_start = 1, answer = 0;
    for (int station : stations) {
        long long gap = station - 1LL * w - next_start;
        if (gap > 0) answer += (gap + coverage - 1) / coverage;
        next_start = max(next_start, station + 1LL * w + 1);
    }
    if (next_start <= n) { long long gap = n - next_start + 1; answer += (gap + coverage - 1) / coverage; }
    return (int)answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(int n, vector<int> stations, int w) {  // 미수신 구간 길이를 새 기지국 수신 폭으로 나누기
// long long coverage = 2LL * w + 1, next_start = 1, answer = 0;  // 한 기지국의 범위와 아직 덮지 않은 첫 아파트 저장
// for (int station : stations) {  // 기존 기지국을 왼쪽부터 처리
// long long gap = station - 1LL * w - next_start;  // 기존 기지국 앞의 빈 구간 길이 구하기
// if (gap > 0) answer += (gap + coverage - 1) / coverage;  // 빈 구간을 새 기지국으로 덮는 최소 수를 올림 나눗셈으로 더하기
// next_start = max(next_start, station + 1LL * w + 1);  // 다음 미수신 아파트 위치 갱신
// }  // 블록 끝
// if (next_start <= n) { long long gap = n - next_start + 1; answer += (gap + coverage - 1) / coverage; }  // 마지막 기존 기지국 뒤의 빈 구간을 덮기
// return (int)answer;  // 추가해야 하는 최소 기지국 수 반환
// }  // 블록 끝

// 풀이 요약
// 기존 기지국 사이와 양 끝의 미수신 구간을 찾아 새 기지국의 수신 폭으로 올림 나눗셈
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:47:15
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level3/075_12979_%EA%B8%B0%EC%A7%80%EA%B5%AD_%EC%84%A4%EC%B9%98/README.md)
