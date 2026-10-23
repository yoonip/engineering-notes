# 수열과 구간 쿼리 3

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181924) · Level 0 · C++

## 풀이

쿼리에 주어진 두 인덱스의 원소를 차례대로 교환

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <vector>
using namespace std;

vector<int> solution(vector<int> arr, vector<vector<int>> queries) {
    for (const auto& query : queries) swap(arr[query[0]], arr[query[1]]);
    return arr;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·검색·뒤집기 알고리즘
// #include <vector>  // 길이를 늘릴 수 있는 vector
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// vector<int> solution(vector<int> arr, vector<vector<int>> queries) {  // 수열과 구간 쿼리 3 풀이 시작
//     for (const auto& query : queries) swap(arr[query[0]], arr[query[1]]);  // 범위 for로 쿼리를 읽고 swap으로 지정된 두 원소를 교환
//     return arr;  // return으로 모든 쿼리를 적용한 배열을 반환
// }  // 블록 끝

// 풀이 요약
// 쿼리에 주어진 두 인덱스의 원소를 차례대로 교환
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:42:27
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181924_%EC%88%98%EC%97%B4%EA%B3%BC_%EA%B5%AC%EA%B0%84_%EC%BF%BC%EB%A6%AC_3/README.md)
