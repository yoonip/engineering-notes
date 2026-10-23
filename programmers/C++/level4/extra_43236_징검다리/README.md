# 징검다리

[레벨 4 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/43236) · Level 4 · C++

## 풀이

최소 간격을 답 후보로 이진 탐색. 직전 남긴 바위와 너무 가까운 바위를 제거했을 때 n개 이하로 가능하면 더 큰 간격 탐색.

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <vector>
#include <array>
#include <algorithm>
#include <numeric>
#include <functional>
#include <unordered_set>
#include <unordered_map>
#include <map>
#include <set>
#include <queue>
#include <deque>
#include <tuple>
#include <utility>
#include <climits>
#include <cstdlib>
using namespace std;

int solution(int distance, vector<int> rocks, int n) {
    sort(rocks.begin(), rocks.end()); rocks.push_back(distance);
    int low = 1, high = distance, answer = 0;
    while (low <= high) {
        int gap = low + (high - low) / 2, previous = 0, removed = 0;
        for (int position : rocks) { if (position - previous < gap) ++removed; else previous = position; if (removed > n) break; }
        if (removed <= n) { answer = gap; low = gap + 1; } else high = gap - 1;
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열 string 사용 준비
// #include <vector>  // 가변 길이 배열 vector 사용 준비
// #include <array>  // 고정 크기 배열 array 사용 준비
// #include <algorithm>  // 정렬·탐색·최솟값 등 표준 알고리즘 사용 준비
// #include <numeric>  // gcd·accumulate 등 수치 알고리즘 사용 준비
// #include <functional>  // 함수 래퍼와 greater 등 비교 함수 객체 사용 준비
// #include <unordered_set>  // 중복 없는 원소를 저장하는 해시 집합 사용 준비
// #include <unordered_map>  // 키로 값을 찾는 해시 맵 사용 준비
// #include <map>  // 키 순서가 유지되는 맵 사용 준비
// #include <set>  // 중복 제거와 정렬을 함께 하는 집합 사용 준비
// #include <queue>  // FIFO 큐와 우선순위 큐 사용 준비
// #include <deque>  // 양 끝 삽입·삭제를 지원하는 덱 사용 준비
// #include <tuple>  // 여러 상태 값을 묶는 tuple 사용 준비
// #include <utility>  // pair·move 등 유틸리티 사용 준비
// #include <climits>  // 정수 범위 상수 사용 준비
// #include <cstdlib>  // 정수 절댓값 등 표준 유틸리티 함수 사용 준비
// using namespace std;  // 표준 이름의 std:: 접두사 생략
//
// int solution(int distance, vector<int> rocks, int n) {  // 징검다리 풀이 함수 정의
//     sort(rocks.begin(), rocks.end()); rocks.push_back(distance);  // 바위를 위치순으로 정렬하고 도착점도 마지막 위치로 추가
//     int low = 1, high = distance, answer = 0;  // 가능한 최소 간격의 탐색 범위와 현재 답 준비
//     while (low <= high) {  // 최소 간격의 가능한 경계를 이진 탐색
//         int gap = low + (high - low) / 2, previous = 0, removed = 0;  // 시험할 간격 gap, 마지막 남긴 위치 previous, 제거 수 removed 준비
//         for (int position : rocks) { if (position - previous < gap) ++removed; else previous = position; if (removed > n) break; }  // gap보다 가까운 위치를 제거하고, 충분히 멀면 남김. 제거 수가 n을 넘으면 검사 중단
//         if (removed <= n) { answer = gap; low = gap + 1; } else high = gap - 1;  // n개 이내로 제거 가능하면 답을 저장하고 더 큰 간격, 아니면 더 작은 간격 탐색
//     }  // 블록 끝
//     return answer;  // 유지할 수 있는 최소 간격의 최댓값 반환
// }  // 함수 끝
//

// 풀이 요약
// 최소 간격을 답 후보로 이진 탐색. 직전 남긴 바위와 너무 가까운 바위를 제거했을 때 n개 이하로 가능하면 더 큰 간격 탐색.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:48:15
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level4/extra_43236_%EC%A7%95%EA%B2%80%EB%8B%A4%EB%A6%AC/README.md)
