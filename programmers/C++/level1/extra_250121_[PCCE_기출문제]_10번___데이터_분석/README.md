# [PCCE 기출문제] 10번 / 데이터 분석

[레벨 1 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/250121) · Level 1 · C++

## 풀이

항목 이름을 열 번호로 바꾸고 필터 조건을 먼저 적용. 남긴 행을 정렬 기준 열의 값으로 오름차순 정렬.

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
#include <functional>
#include <unordered_set>
#include <unordered_map>
#include <sstream>
#include <cctype>
#include <cstdlib>
#include <cstdio>
#include <cmath>
#include <queue>
#include <set>
#include <climits>
#include <iostream>
using namespace std;

vector<vector<int>> solution(vector<vector<int>> data, string ext, int val_ext, string sort_by) {
    unordered_map<string, int> column = {{"code", 0}, {"date", 1}, {"maximum", 2}, {"remain", 3}};
    vector<vector<int>> answer;
    for (const auto& row : data) if (row[column[ext]] < val_ext) answer.push_back(row);
    int index = column[sort_by];
    sort(answer.begin(), answer.end(), [index](const auto& a, const auto& b) { return a[index] < b[index]; });
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열 string 사용 준비
// #include <vector>  // 가변 길이 배열 vector 사용 준비
// #include <algorithm>  // 정렬·탐색·최솟값 등 표준 알고리즘 사용 준비
// #include <numeric>  // gcd·accumulate 등 수치 알고리즘 사용 준비
// #include <functional>  // 함수 래퍼와 greater 등 비교 함수 객체 사용 준비
// #include <unordered_set>  // 중복 없는 원소를 저장하는 해시 집합 사용 준비
// #include <unordered_map>  // 키로 값을 찾는 해시 맵 사용 준비
// #include <sstream>  // 문자열을 토큰으로 나눠 읽을 스트림 사용 준비
// #include <cctype>  // 숫자·대소문자 검사와 변환 함수 사용 준비
// #include <cstdlib>  // 정수 절댓값 등 표준 유틸리티 함수 사용 준비
// #include <cstdio>  // snprintf 등 형식 있는 입출력 함수 사용 준비
// #include <cmath>  // 제곱근 등 수학 함수 사용 준비
// #include <queue>  // FIFO 큐와 우선순위 큐 사용 준비
// #include <set>  // 중복 제거와 정렬을 함께 하는 집합 사용 준비
// #include <climits>  // 정수 범위 상수 사용 준비
// #include <iostream>  // cin·cout 표준 입출력 사용 준비
// using namespace std;  // 표준 이름의 std:: 접두사 생략
//
// vector<vector<int>> solution(vector<vector<int>> data, string ext, int val_ext, string sort_by) {  // [PCCE 기출문제] 10번 / 데이터 분석 풀이 함수 정의
//     unordered_map<string, int> column = {{"code", 0}, {"date", 1}, {"maximum", 2}, {"remain", 3}};  // 항목 이름을 code·date·maximum·remain의 열 번호에 연결
//     vector<vector<int>> answer;  // 필터를 통과한 행을 저장할 결과 배열 준비
//     for (const auto& row : data) if (row[column[ext]] < val_ext) answer.push_back(row);  // ext 열의 값이 val_ext보다 작은 행만 결과에 복사
//     int index = column[sort_by];  // sort_by에 해당하는 정렬 기준 열 번호 저장
//     sort(answer.begin(), answer.end(), [index](const auto& a, const auto& b) { return a[index] < b[index]; });  // 람다에 기준 열 index를 값으로 캡처해 그 열의 값으로 오름차순 정렬
//     return answer;  // 필터와 정렬을 마친 행들 반환
// }  // 함수 끝
//

// 풀이 요약
// 항목 이름을 열 번호로 바꾸고 필터 조건을 먼저 적용. 남긴 행을 정렬 기준 열의 값으로 오름차순 정렬.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:04:50
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level1/extra_250121_%5BPCCE_%EA%B8%B0%EC%B6%9C%EB%AC%B8%EC%A0%9C%5D_10%EB%B2%88___%EB%8D%B0%EC%9D%B4%ED%84%B0_%EB%B6%84%EC%84%9D/README.md)
