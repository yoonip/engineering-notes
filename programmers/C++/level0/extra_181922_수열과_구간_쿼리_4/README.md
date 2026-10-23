# 수열과 구간 쿼리 4

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181922) · Level 0 · C++

## 풀이

각 구간에서 인덱스가 k의 배수인 원소를 1씩 증가

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <vector>
using namespace std;

vector<int> solution(vector<int> arr, vector<vector<int>> queries) {
    for (const auto& query : queries) {
        int start = query[0], end = query[1], k = query[2];
        for (int i = start; i <= end; ++i) if (k ? i % k == 0 : i == 0) ++arr[i];
    }
    return arr;
}

// 전체 코드 줄별 설명
// #include <vector>  // 길이를 늘릴 수 있는 vector
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// vector<int> solution(vector<int> arr, vector<vector<int>> queries) {  // 수열과 구간 쿼리 4 풀이 시작
//     for (const auto& query : queries) {  // 범위 for와 const auto 참조로 각 쿼리를 복사 없이 읽기
//         int start = query[0], end = query[1], k = query[2];  // []로 현재 쿼리의 시작, 끝, 배수 기준 k를 읽기
//         for (int i = start; i <= end; ++i) if (k ? i % k == 0 : i == 0) ++arr[i];  // 양 끝을 포함한 구간에서 인덱스가 k의 배수인 원소만 1 증가
//     }  // 블록 끝
//     return arr;  // return으로 모든 쿼리를 적용한 배열을 반환
// }  // 블록 끝

// 풀이 요약
// 각 구간에서 인덱스가 k의 배수인 원소를 1씩 증가
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:43:21
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181922_%EC%88%98%EC%97%B4%EA%B3%BC_%EA%B5%AC%EA%B0%84_%EC%BF%BC%EB%A6%AC_4/README.md)
