# 쌍둥이 빌딩 숲

[레벨 4 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/140105) · Level 4 · C++

## 풀이

빌딩 쌍 수와 보이는 쌍 수로 DP. 새 쌍 때문에 보이는 수가 늘어나는 경우와 2 × (쌍 수 - 1)개 배치로 보이는 수를 유지하는 경우를 합침.

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

int solution(int n, int count) {
    const int mod = 1000000007;
    vector<int> dp(count + 1, 0); dp[0] = 1;
    for (int pairs = 1; pairs <= n; ++pairs) {
        vector<int> next(count + 1, 0);
        for (int visible = 1; visible <= min(pairs, count); ++visible) next[visible] = (dp[visible - 1] + 2LL * (pairs - 1) * dp[visible]) % mod;
        dp.swap(next);
    }
    return dp[count];
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
// int solution(int n, int count) {  // 쌍둥이 빌딩 숲 풀이 함수 정의
//     const int mod = 1000000007;  // 정답에 적용할 모듈러 상수 저장
//     vector<int> dp(count + 1, 0); dp[0] = 1;  // 보이는 쌍 수별 경우의 수를 준비하고 빈 배치 dp[0] = 1로 시작
//     for (int pairs = 1; pairs <= n; ++pairs) {  // 빌딩 쌍을 하나씩 늘리며 경우의 수 계산
//         vector<int> next(count + 1, 0);  // 이번 쌍을 추가한 결과 배열 준비
//         for (int visible = 1; visible <= min(pairs, count); ++visible) next[visible] = (dp[visible - 1] + 2LL * (pairs - 1) * dp[visible]) % mod;  // 보이는 수가 하나 늘어나는 경우와 유지되는 배치 경우를 합산. 곱은 long long으로 계산
//         dp.swap(next);  // 새 쌍 수의 DP 결과로 교체
//     }  // 블록 끝
//     return dp[count];  // n쌍에서 정확히 count쌍이 보이는 경우의 수 반환
// }  // 함수 끝
//

// 풀이 요약
// 빌딩 쌍 수와 보이는 쌍 수로 DP. 새 쌍 때문에 보이는 수가 늘어나는 경우와 2 × (쌍 수 - 1)개 배치로 보이는 수를 유지하는 경우를 합침.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:43:12
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level4/extra_140105_%EC%8C%8D%EB%91%A5%EC%9D%B4_%EB%B9%8C%EB%94%A9_%EC%88%B2/README.md)
