# 도둑질

[레벨 4 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/42897) · Level 4 · C++

## 풀이

원형에서 첫 집과 마지막 집은 동시에 선택 불가. 마지막 집을 뺀 구간과 첫 집을 뺀 구간의 선형 DP 중 큰 값 선택.

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

int solution(vector<int> money) {
    int n = (int)money.size();
    auto best = [&](int start, int end) { int previous = 0, current = 0; for (int i = start; i < end; ++i) { int next = max(current, previous + money[i]); previous = current; current = next; } return current; };
    return max(best(0, n - 1), best(1, n));
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
// int solution(vector<int> money) {  // 도둑질 풀이 함수 정의
//     int n = (int)money.size();  // 집 수 n 저장
//     auto best = [&](int start, int end) { int previous = 0, current = 0; for (int i = start; i < end; ++i) { int next = max(current, previous + money[i]); previous = current; current = next; } return current; };  // 구간별 선형 DP 람다. 직전 두 상태를 사용해 현재 집을 털지 않는 값과 한 집 건너 현재 돈을 더한 값 비교
//     return max(best(0, n - 1), best(1, n));  // 마지막 집 제외·첫 집 제외 두 구간의 최대 수익 중 큰 값 반환
// }  // 함수 끝
//

// 풀이 요약
// 원형에서 첫 집과 마지막 집은 동시에 선택 불가. 마지막 집을 뺀 구간과 첫 집을 뺀 구간의 선형 DP 중 큰 값 선택.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:48:42
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level4/extra_42897_%EB%8F%84%EB%91%91%EC%A7%88/README.md)
