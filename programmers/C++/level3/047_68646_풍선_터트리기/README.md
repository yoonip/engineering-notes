# 풍선 터트리기

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/68646) · Level 3 · C++

## 풀이

왼쪽 또는 오른쪽에서 새 최솟값이 되는 풍선들을 세고 두 방향에서 중복한 전체 최솟값 하나 빼기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <climits>
#include <vector>
using namespace std;

int solution(vector<int> a) {
    int answer = 0, minimum = INT_MAX;
    for (int value : a) if (value < minimum) { ++answer; minimum = value; }
    minimum = INT_MAX;
    for (auto it = a.rbegin(); it != a.rend(); ++it) if (*it < minimum) { ++answer; minimum = *it; }
    return answer - 1;
}

// 전체 코드 줄별 설명
// #include <climits>  // 정수 자료형의 최솟값·최댓값
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<int> a) {  // 양쪽 최솟값으로 끝까지 남을 수 있는 풍선 판정
// int answer = 0, minimum = INT_MAX;  // 한쪽 방향의 새 최솟값 수 세기
// for (int value : a) if (value < minimum) { ++answer; minimum = value; }  // 왼쪽에서 새 최솟값이 되는 풍선은 남길 수 있음
// minimum = INT_MAX;  // 반대쪽 탐색의 최솟값 초기화
// for (auto it = a.rbegin(); it != a.rend(); ++it) if (*it < minimum) { ++answer; minimum = *it; }  // 오른쪽에서도 새 최솟값 풍선 세기
// return answer - 1;  // 양쪽에서 중복한 전체 최솟값 하나 빼기
// }  // 블록 끝

// 풀이 요약
// 왼쪽 또는 오른쪽에서 새 최솟값이 되는 풍선들을 세고 두 방향에서 중복한 전체 최솟값 하나 빼기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:39:56
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/047_68646_%ED%92%8D%EC%84%A0_%ED%84%B0%ED%8A%B8%EB%A6%AC%EA%B8%B0/README.md)
