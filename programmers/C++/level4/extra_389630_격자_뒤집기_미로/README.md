# 격자 뒤집기 미로

[레벨 4 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/389630) · Level 4 · C++

## 풀이

행 뒤집기 조합을 비트마스크로 전부 검사. 각 열은 유지·뒤집기 중 큰 점수를 선택. 두 변이 모두 짝수일 때는 방문할 수 없는 홀수 색 한 칸의 최소 손실도 반영.

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

int solution(vector<vector<int>> visible, vector<vector<int>> hidden, int k) {
    int n = (int)visible.size(), m = (int)visible[0].size(), answer = INT_MIN;
    bool skip = n % 2 == 0 && m % 2 == 0;
    for (int mask = 0; mask < (1 << n); ++mask) {
        int total = -k * __builtin_popcount((unsigned)mask), best_loss = INT_MIN;
        for (int c = 0; c < m; ++c) {
            int front = 0, back = 0, low_front = 101, low_back = 101;
            for (int r = 0; r < n; ++r) {
                int a = visible[r][c], b = hidden[r][c];
                if (mask & (1 << r)) swap(a, b);
                front += a; back += b;
                if (skip && (r + c) % 2) { low_front = min(low_front, a); low_back = min(low_back, b); }
            }
            int normal = max(front, back - k); total += normal;
            if (skip) best_loss = max(best_loss, max(front - low_front, back - low_back - k) - normal);
        }
        if (skip) total += best_loss;
        answer = max(answer, total);
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
// int solution(vector<vector<int>> visible, vector<vector<int>> hidden, int k) {  // 격자 뒤집기 미로 풀이 함수 정의
//     int n = (int)visible.size(), m = (int)visible[0].size(), answer = INT_MIN;  // 격자의 행 수 n, 열 수 m, 최대 점수 answer의 초기값 저장
//     bool skip = n % 2 == 0 && m % 2 == 0;  // 가로·세로가 모두 짝수여서 한 칸을 제외해야 하는 경우인지 표시
//     for (int mask = 0; mask < (1 << n); ++mask) {  // 각 비트가 한 행의 뒤집기를 뜻하는 모든 조합 검사
//         int total = -k * __builtin_popcount((unsigned)mask), best_loss = INT_MIN;  // 뒤집은 행 수 × 비용 k를 먼저 빼고, 한 칸 제외에 따른 최선의 보정값 준비
//         for (int c = 0; c < m; ++c) {  // 현재 행 조합에서 열별 최선의 선택 계산
//             int front = 0, back = 0, low_front = 101, low_back = 101;  // 열을 유지·뒤집었을 때의 합 front·back과 제외 가능한 최소 칸 값 준비
//             for (int r = 0; r < n; ++r) {  // 현재 열의 모든 행 검사
//                 int a = visible[r][c], b = hidden[r][c];  // 현재 칸의 보이는 값 a와 숨은 값 b 읽기
//                 if (mask & (1 << r)) swap(a, b);  // 행이 뒤집혔으면 보이는 면과 숨은 면 교환
//                 front += a; back += b;  // 두 면에서 각각 얻는 열 점수 누적
//                 if (skip && (r + c) % 2) { low_front = min(low_front, a); low_back = min(low_back, b); }  // 한 칸 제외가 필요하면 홀수 색 칸의 최소값을 면별로 갱신
//             }  // 블록 끝
//             int normal = max(front, back - k); total += normal;  // 열 유지 점수와 뒤집기 비용을 뺀 점수 중 큰 값을 합산
//             if (skip) best_loss = max(best_loss, max(front - low_front, back - low_back - k) - normal);  // 이 열에서 한 칸을 제외했을 때 원래 선택보다 얼마나 바뀌는지 계산해 최선의 보정값 갱신
//         }  // 블록 끝
//         if (skip) total += best_loss;  // 한 칸 제외가 필요하면 가장 손실이 작은 보정값 반영
//         answer = max(answer, total);  // 현재 행 뒤집기 조합의 점수로 전체 최댓값 갱신
//     }  // 블록 끝
//     return answer;  // 가능한 모든 뒤집기 조합 중 최대 점수 반환
// }  // 함수 끝
//

// 풀이 요약
// 행 뒤집기 조합을 비트마스크로 전부 검사. 각 열은 유지·뒤집기 중 큰 점수를 선택. 두 변이 모두 짝수일 때는 방문할 수 없는 홀수 색 한 칸의 최소 손실도 반영.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:41:27
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level4/extra_389630_%EA%B2%A9%EC%9E%90_%EB%92%A4%EC%A7%91%EA%B8%B0_%EB%AF%B8%EB%A1%9C/README.md)
