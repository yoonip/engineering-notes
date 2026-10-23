# 노란불 신호등

[레벨 1 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/468371) · Level 1 · C++

## 풀이

전체 신호 주기의 최소공배수까지만 검사. 각 시각에 모든 신호가 노란 구간인지 확인하고 처음 맞는 시각 반환.

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
#include <functional>
#include <unordered_set>
#include <unordered_map>
#include <sstream>
#include <cctype>
#include <cstdlib>
#include <cstdio>
#include <cmath>
#include <queue>
#include <set>
#include <climits>
#include <iostream>
using namespace std;

int solution(vector<vector<int>> signals) {
    long long period = 1;
    for (const auto& s : signals) { long long cycle = s[0] + s[1] + s[2]; period = period / gcd(period, cycle) * cycle; }
    for (long long t = 1; t <= period; ++t) {
        bool all_yellow = true;
        for (const auto& s : signals) {
            long long pos = (t - 1) % (s[0] + s[1] + s[2]);
            if (pos < s[0] || pos >= s[0] + s[1]) { all_yellow = false; break; }
        }
        if (all_yellow) return (int)t;
    }
    return -1;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열 string 사용 준비
// #include <vector>  // 가변 길이 배열 vector 사용 준비
// #include <algorithm>  // 정렬·탐색·최솟값 등 표준 알고리즘 사용 준비
// #include <numeric>  // gcd·accumulate 등 수치 알고리즘 사용 준비
// #include <functional>  // 함수 래퍼와 greater 등 비교 함수 객체 사용 준비
// #include <unordered_set>  // 중복 없는 원소를 저장하는 해시 집합 사용 준비
// #include <unordered_map>  // 키로 값을 찾는 해시 맵 사용 준비
// #include <sstream>  // 문자열을 토큰으로 나눠 읽을 스트림 사용 준비
// #include <cctype>  // 숫자·대소문자 검사와 변환 함수 사용 준비
// #include <cstdlib>  // 정수 절댓값 등 표준 유틸리티 함수 사용 준비
// #include <cstdio>  // snprintf 등 형식 있는 입출력 함수 사용 준비
// #include <cmath>  // 제곱근 등 수학 함수 사용 준비
// #include <queue>  // FIFO 큐와 우선순위 큐 사용 준비
// #include <set>  // 중복 제거와 정렬을 함께 하는 집합 사용 준비
// #include <climits>  // 정수 범위 상수 사용 준비
// #include <iostream>  // cin·cout 표준 입출력 사용 준비
// using namespace std;  // 표준 이름의 std:: 접두사 생략
//
// int solution(vector<vector<int>> signals) {  // 노란불 신호등 풀이 함수 정의
//     long long period = 1;  // 전체 신호 상태가 반복되는 주기 period를 1에서 시작
//     for (const auto& s : signals) { long long cycle = s[0] + s[1] + s[2]; period = period / gcd(period, cycle) * cycle; }  // 각 신호의 주기 cycle을 구하고, 최대공약수로 먼저 나눈 뒤 곱해 period의 최소공배수 갱신
//     for (long long t = 1; t <= period; ++t) {  // 1초부터 전체 반복 주기까지 작은 시각 순서로 검사
//         bool all_yellow = true;  // 이번 시각에 모든 신호가 노랗다고 가정
//         for (const auto& s : signals) {  // 각 신호의 노란 구간을 하나씩 확인
//             long long pos = (t - 1) % (s[0] + s[1] + s[2]);  // 시작이 1초이므로 t - 1을 사용해 현재 신호 주기 안의 위치 pos 계산
//             if (pos < s[0] || pos >= s[0] + s[1]) { all_yellow = false; break; }  // 초록 구간이거나 노랑 종료 이후면 가정을 취소하고 신호 검사 중단
//         }  // 블록 끝
//         if (all_yellow) return (int)t;  // 모든 신호의 검사를 통과하면 가장 이른 시각 t 반환
//     }  // 블록 끝
//     return -1;  // 한 주기 안에 맞는 시각이 없으면 -1 반환
// }  // 함수 끝
//

// 풀이 요약
// 전체 신호 주기의 최소공배수까지만 검사. 각 시각에 모든 신호가 노란 구간인지 확인하고 처음 맞는 시각 반환.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:59:56
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level1/extra_468371_%EB%85%B8%EB%9E%80%EB%B6%88_%EC%8B%A0%ED%98%B8%EB%93%B1/README.md)
