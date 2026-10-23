# 문자 리스트를 문자열로 변환하기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181941) · Level 0 · C++

## 풀이

문자열 배열의 원소를 입력 순서대로 연결

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <vector>
using namespace std;

string solution(vector<string> arr) {
    string answer;
    for (const string& text : arr) answer += text;
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// string solution(vector<string> arr) {  // 문자 리스트를 문자열로 변환하기 풀이 시작
//     string answer;  // 입력 원소들을 순서대로 이어 붙일 문자열
//     for (const string& text : arr) answer += text;  // 범위 for에서 각 문자열을 const 참조로 읽고 +=로 순서대로 연결
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 문자열 배열의 원소를 입력 순서대로 연결
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:32:46
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181941_%EB%AC%B8%EC%9E%90_%EB%A6%AC%EC%8A%A4%ED%8A%B8%EB%A5%BC_%EB%AC%B8%EC%9E%90%EC%97%B4%EB%A1%9C_%EB%B3%80%ED%99%98%ED%95%98%EA%B8%B0/README.md)
