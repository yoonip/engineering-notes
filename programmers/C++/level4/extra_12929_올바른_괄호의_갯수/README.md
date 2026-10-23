# 올바른 괄호의 갯수

[레벨 4 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12929) · Level 4 · C++

## 풀이

첫 여는 괄호와 짝인 닫는 괄호를 기준으로 안쪽·뒤쪽 괄호열로 분리. 두 부분의 경우의 수를 곱해 모든 분할에 대해 합산.

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

int solution(int n) {
    vector<long long> dp(n + 1, 0); dp[0] = 1;
    for (int pairs = 1; pairs <= n; ++pairs) for (int inside = 0; inside < pairs; ++inside) dp[pairs] += dp[inside] * dp[pairs - 1 - inside];
    return (int)dp[n];
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
// int solution(int n) {  // 올바른 괄호의 갯수 풀이 함수 정의
//     vector<long long> dp(n + 1, 0); dp[0] = 1;  // 괄호 쌍 수별 경우의 수를 준비하고 빈 괄호열은 1가지로 설정
//     for (int pairs = 1; pairs <= n; ++pairs) for (int inside = 0; inside < pairs; ++inside) dp[pairs] += dp[inside] * dp[pairs - 1 - inside];  // 전체 pairs쌍을 첫 괄호 안 inside쌍과 뒤 pairs - 1 - inside쌍으로 나눠 카탈란 점화식 누적
//     return (int)dp[n];  // n쌍으로 만들 수 있는 올바른 괄호열 수 반환
// }  // 함수 끝
//

// 풀이 요약
// 첫 여는 괄호와 짝인 닫는 괄호를 기준으로 안쪽·뒤쪽 괄호열로 분리. 두 부분의 경우의 수를 곱해 모든 분할에 대해 합산.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:51:10
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level4/extra_12929_%EC%98%AC%EB%B0%94%EB%A5%B8_%EA%B4%84%ED%98%B8%EC%9D%98_%EA%B0%AF%EC%88%98/README.md)
