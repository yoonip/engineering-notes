# 짝수 행 세기

[레벨 4 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/68647) · Level 4 · C++

## 풀이

열마다 1의 수를 보존하며 배치. 짝수 행 수만 DP 상태로 두고, 기존 짝수·홀수 행 중 몇 곳에 1을 넣는지 조합 수를 곱해 전이.

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

int solution(vector<vector<int>> a) {
    const int mod = 10000019; int n = (int)a.size(), columns = (int)a[0].size();
    vector<vector<int>> choose(n + 1, vector<int>(n + 1, 0));
    for (int total = 0; total <= n; ++total) { choose[total][0] = choose[total][total] = 1; for (int selected = 1; selected < total; ++selected) choose[total][selected] = (choose[total - 1][selected - 1] + choose[total - 1][selected]) % mod; }
    vector<int> dp(n + 1, 0); dp[n] = 1;
    for (int c = 0; c < columns; ++c) {
        int ones = 0; for (int r = 0; r < n; ++r) ones += a[r][c];
        vector<int> next(n + 1, 0);
        for (int even = 0; even <= n; ++even) if (dp[even]) {
            int low = max(0, ones - (n - even)), high = min(even, ones);
            for (int changed = low; changed <= high; ++changed) {
                int new_even = even + ones - 2 * changed;
                long long ways = 1LL * dp[even] * choose[even][changed] % mod * choose[n - even][ones - changed] % mod;
                next[new_even] = (next[new_even] + ways) % mod;
            }
        }
        dp.swap(next);
    }
    return dp[n];
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
// int solution(vector<vector<int>> a) {  // 짝수 행 세기 풀이 함수 정의
//     const int mod = 10000019; int n = (int)a.size(), columns = (int)a[0].size();  // 모듈러 상수와 행 수 n·열 수 columns 저장
//     vector<vector<int>> choose(n + 1, vector<int>(n + 1, 0));  // 행 선택 경우의 수에 사용할 조합 표 준비
//     for (int total = 0; total <= n; ++total) { choose[total][0] = choose[total][total] = 1; for (int selected = 1; selected < total; ++selected) choose[total][selected] = (choose[total - 1][selected - 1] + choose[total - 1][selected]) % mod; }  // 파스칼 항등식으로 n까지의 조합 수를 모듈러로 계산
//     vector<int> dp(n + 1, 0); dp[n] = 1;  // 짝수 행 수별 DP를 준비하고, 아무 열도 없을 때 모든 행이 짝수인 상태를 1로 설정
//     for (int c = 0; c < columns; ++c) {  // 입력 행렬의 열을 하나씩 배치
//         int ones = 0; for (int r = 0; r < n; ++r) ones += a[r][c];  // 현재 열에서 보존해야 할 1의 개수 ones 계산
//         vector<int> next(n + 1, 0);  // 이번 열을 배치한 뒤의 DP 배열 준비
//         for (int even = 0; even <= n; ++even) if (dp[even]) {  // 가능한 짝수 행 수 상태만 전이
//             int low = max(0, ones - (n - even)), high = min(even, ones);  // 짝수 행에서 1을 넣을 수 있는 개수 changed의 최솟값·최댓값 계산
//             for (int changed = low; changed <= high; ++changed) {  // 짝수 행에 놓는 1의 개수를 가능한 범위에서 선택
//                 int new_even = even + ones - 2 * changed;  // 짝수→홀수와 홀수→짝수 변화를 반영한 새 짝수 행 수 계산
//                 long long ways = 1LL * dp[even] * choose[even][changed] % mod * choose[n - even][ones - changed] % mod;  // 기존 경우의 수에 짝수 행·홀수 행 선택 조합 수를 곱함. 곱은 long long 사용
//                 next[new_even] = (next[new_even] + ways) % mod;  // 같은 새 짝수 행 수로 오는 경우의 수를 누적
//             }  // 블록 끝
//         }  // 블록 끝
//         dp.swap(next);  // 현재 열을 반영한 DP로 교체
//     }  // 블록 끝
//     return dp[n];  // 모든 행이 짝수인 상태 dp[n]의 경우의 수 반환
// }  // 함수 끝
//

// 풀이 요약
// 열마다 1의 수를 보존하며 배치. 짝수 행 수만 DP 상태로 두고, 기존 짝수·홀수 행 중 몇 곳에 1을 넣는지 조합 수를 곱해 전이.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:45:41
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level4/extra_68647_%EC%A7%9D%EC%88%98_%ED%96%89_%EC%84%B8%EA%B8%B0/README.md)
