# 사칙연산

[레벨 4 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/1843) · Level 4 · C++

## 풀이

각 연속 구간의 최댓값·최솟값을 함께 DP. 뺄셈에서는 오른쪽 최솟값이 전체 최댓값에 필요하므로 둘 다 유지.

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

int solution(vector<string> arr) {
    int n = ((int)arr.size() + 1) / 2; vector<vector<int>> maximum(n, vector<int>(n, -1000000000)), minimum(n, vector<int>(n, 1000000000));
    for (int i = 0; i < n; ++i) maximum[i][i] = minimum[i][i] = stoi(arr[i * 2]);
    for (int length = 2; length <= n; ++length) for (int left = 0; left + length <= n; ++left) {
        int right = left + length - 1;
        for (int split = left; split < right; ++split) {
            bool plus = arr[split * 2 + 1] == "+";
            int high = maximum[left][split] + (plus ? maximum[split + 1][right] : -minimum[split + 1][right]);
            int low = minimum[left][split] + (plus ? minimum[split + 1][right] : -maximum[split + 1][right]);
            maximum[left][right] = max(maximum[left][right], high); minimum[left][right] = min(minimum[left][right], low);
        }
    }
    return maximum[0][n - 1];
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
// int solution(vector<string> arr) {  // 사칙연산 풀이 함수 정의
//     int n = ((int)arr.size() + 1) / 2; vector<vector<int>> maximum(n, vector<int>(n, -1000000000)), minimum(n, vector<int>(n, 1000000000));  // 숫자 수 n을 구하고 모든 구간의 최댓값·최솟값 표를 극단값으로 초기화
//     for (int i = 0; i < n; ++i) maximum[i][i] = minimum[i][i] = stoi(arr[i * 2]);  // 숫자 하나인 구간은 문자열을 정수로 바꾼 값으로 최대·최소 동일하게 설정
//     for (int length = 2; length <= n; ++length) for (int left = 0; left + length <= n; ++left) {  // 짧은 구간부터 길이와 왼쪽 끝을 선택
//         int right = left + length - 1;  // 현재 구간의 오른쪽 끝 계산
//         for (int split = left; split < right; ++split) {  // 마지막으로 계산할 연산자의 모든 분할 위치 검사
//             bool plus = arr[split * 2 + 1] == "+";  // 분할 연산자가 덧셈인지 확인
//             int high = maximum[left][split] + (plus ? maximum[split + 1][right] : -minimum[split + 1][right]);  // 덧셈은 양쪽 최댓값, 뺄셈은 왼쪽 최대 - 오른쪽 최소로 최대 후보 계산
//             int low = minimum[left][split] + (plus ? minimum[split + 1][right] : -maximum[split + 1][right]);  // 덧셈은 양쪽 최솟값, 뺄셈은 왼쪽 최소 - 오른쪽 최대로 최소 후보 계산
//             maximum[left][right] = max(maximum[left][right], high); minimum[left][right] = min(minimum[left][right], low);  // 현재 구간의 최대·최소를 각 후보로 갱신
//         }  // 블록 끝
//     }  // 블록 끝
//     return maximum[0][n - 1];  // 전체 수식 구간의 최댓값 반환
// }  // 함수 끝
//

// 풀이 요약
// 각 연속 구간의 최댓값·최솟값을 함께 DP. 뺄셈에서는 오른쪽 최솟값이 전체 최댓값에 필요하므로 둘 다 유지.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:51:24
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level4/extra_1843_%EC%82%AC%EC%B9%99%EC%97%B0%EC%82%B0/README.md)
