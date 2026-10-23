# 안티세포

[레벨 4 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/86054) · Level 4 · C++

## 풀이

구간별 누적합과 DP로 가능한 결과 배열 수 계산. 오른쪽 끝에서 같은 질량 두 덩어리를 합칠 수 있는지 병합 깊이로 확인하며 이전 분할 위치의 경우의 수를 추가.

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

vector<int> solution(vector<int> a, vector<int> s) {
    const int mod = 1000000007; int offset = 0; vector<int> answer;
    for (int length : s) {
        vector<long long> prefix(length + 1, 0); vector<int> depth(length, 0), dp(length + 1, 0); dp[0] = 1;
        unordered_map<long long, int> positions; positions.reserve(length * 2 + 1); positions[0] = 0;
        for (int right = 0; right < length; ++right) {
            int value = a[offset + right]; prefix[right + 1] = prefix[right] + value; positions[prefix[right + 1]] = right + 1;
            int left = right; long long mass = value, ways = dp[right];
            while (left > 0) {
                int previous = left - 1; long long ratio = mass / a[offset + previous], remainder = mass % a[offset + previous];
                if (remainder || ratio == 0 || (ratio & (ratio - 1))) break;
                int required = __builtin_ctzll((unsigned long long)ratio);
                if (required > depth[previous]) break;
                left = positions.at(prefix[left] - mass); mass *= 2; ++depth[right]; ways += dp[left];
            }
            dp[right + 1] = ways % mod;
        }
        answer.push_back(dp[length]); offset += length;
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
// vector<int> solution(vector<int> a, vector<int> s) {  // 안티세포 풀이 함수 정의
//     const int mod = 1000000007; int offset = 0; vector<int> answer;  // 모듈러, 현재 구간 시작 offset, 구간별 답 배열 준비
//     for (int length : s) {  // s에 주어진 구간 길이를 하나씩 처리
//         vector<long long> prefix(length + 1, 0); vector<int> depth(length, 0), dp(length + 1, 0); dp[0] = 1;  // 구간 누적합 prefix, 오른쪽 끝별 병합 깊이 depth, 접두 구간 경우의 수 dp 준비. 빈 구간은 1가지
//         unordered_map<long long, int> positions; positions.reserve(length * 2 + 1); positions[0] = 0;  // 양수 누적합에서 인덱스를 찾을 맵을 준비하고 빈 접두합 위치 0 저장
//         for (int right = 0; right < length; ++right) {  // 오른쪽 끝을 한 칸씩 늘리며 DP 계산
//             int value = a[offset + right]; prefix[right + 1] = prefix[right] + value; positions[prefix[right + 1]] = right + 1;  // 현재 질량을 읽어 누적합에 더하고 그 누적합의 위치 기록
//             int left = right; long long mass = value, ways = dp[right];  // 새 원소 하나를 마지막 덩어리로 두고 시작 위치·질량·기존 경우의 수 설정
//             while (left > 0) {  // 왼쪽에 같은 질량을 만들 수 있는 동안 병합 확장
//                 int previous = left - 1; long long ratio = mass / a[offset + previous], remainder = mass % a[offset + previous];  // 직전 원소에 대한 질량 비율과 나머지를 계산
//                 if (remainder || ratio == 0 || (ratio & (ratio - 1))) break;  // 정수 배수가 아니거나 비율이 양의 2의 거듭제곱이 아니면 병합 불가
//                 int required = __builtin_ctzll((unsigned long long)ratio);  // 2의 거듭제곱 지수를 구해 왼쪽 덩어리에 필요한 병합 깊이 계산
//                 if (required > depth[previous]) break;  // 직전 위치가 만들 수 있는 깊이보다 더 필요하면 중단
//                 left = positions.at(prefix[left] - mass); mass *= 2; ++depth[right]; ways += dp[left];  // 누적합으로 같은 질량의 왼쪽 경계를 찾아 두 덩어리를 합치고, 그 앞 DP 경우의 수 추가
//             }  // 블록 끝
//             dp[right + 1] = ways % mod;  // 현재 오른쪽 끝까지의 경우의 수를 모듈러로 저장
//         }  // 블록 끝
//         answer.push_back(dp[length]); offset += length;  // 현재 구간 답을 추가하고 다음 구간의 시작 offset 이동
//     }  // 블록 끝
//     return answer;  // 각 구간의 서로 다른 결과 배열 수 반환
// }  // 함수 끝
//

// 풀이 요약
// 구간별 누적합과 DP로 가능한 결과 배열 수 계산. 오른쪽 끝에서 같은 질량 두 덩어리를 합칠 수 있는지 병합 깊이로 확인하며 이전 분할 위치의 경우의 수를 추가.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:44:00
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level4/extra_86054_%EC%95%88%ED%8B%B0%EC%84%B8%ED%8F%AC/README.md)
