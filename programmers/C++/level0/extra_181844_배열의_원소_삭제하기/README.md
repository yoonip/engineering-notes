# 배열의 원소 삭제하기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181844) · Level 0 · C++

## 풀이

삭제 대상 집합에 없는 원소만 원래 순서대로 남기기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
#include <functional>
#include <unordered_set>
#include <sstream>
#include <cctype>
#include <cstdlib>
using namespace std;

vector<int> solution(vector<int> arr, vector<int> delete_list) {
    unordered_set<int> removed(delete_list.begin(), delete_list.end());
    vector<int> answer;
    for (int value : arr) if (!removed.count(value)) answer.push_back(value);
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
// #include <algorithm>  // 정렬·검색·뒤집기 알고리즘
// #include <numeric>  // accumulate·iota 등 수치 연산
// #include <functional>  // greater·multiplies 등 함수 객체
// #include <unordered_set>  // 중복을 거를 해시 집합
// #include <sstream>  // 문자열을 항목별로 읽을 스트림
// #include <cctype>  // 문자 검사와 대소문자 변환
// #include <cstdlib>  // 정수 변환과 절댓값 등 표준 함수
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// vector<int> solution(vector<int> arr, vector<int> delete_list) {  // 배열의 원소 삭제하기 풀이 시작
//     unordered_set<int> removed(delete_list.begin(), delete_list.end());  // unordered_set으로 중복 없는 값의 집합을 준비
//     vector<int> answer;  // 삭제 목록에 없는 값만 남길 배열
//     for (int value : arr) if (!removed.count(value)) answer.push_back(value);  // 삭제 집합에 없는 원소만 원래 순서로 남기기
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 삭제 대상 집합에 없는 원소만 원래 순서대로 남기기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:22:40
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181844_%EB%B0%B0%EC%97%B4%EC%9D%98_%EC%9B%90%EC%86%8C_%EC%82%AD%EC%A0%9C%ED%95%98%EA%B8%B0/README.md)
