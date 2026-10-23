# 할 일 목록

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181885) · Level 0 · C++

## 풀이

할 일과 완료 여부를 짝지은 뒤 완료되지 않은 일만 원래 순서대로 남기기

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

vector<string> solution(vector<string> todo_list, vector<bool> finished) {
    vector<string> answer;
    for (int i = 0; i < (int)todo_list.size(); ++i) if (!finished[i]) answer.push_back(todo_list[i]);
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
// vector<string> solution(vector<string> todo_list, vector<bool> finished) {  // 할 일 목록 풀이 시작
//     vector<string> answer;  // 아직 끝내지 않은 할 일
//     for (int i = 0; i < (int)todo_list.size(); ++i) if (!finished[i]) answer.push_back(todo_list[i]);  // 완료 표시가 거짓인 할 일만 원래 순서로 남기기
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 할 일과 완료 여부를 짝지은 뒤 완료되지 않은 일만 원래 순서대로 남기기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:07:16
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181885_%ED%95%A0_%EC%9D%BC_%EB%AA%A9%EB%A1%9D/README.md)
