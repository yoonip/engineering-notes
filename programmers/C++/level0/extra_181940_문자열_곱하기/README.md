# 문자열 곱하기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181940) · Level 0 · C++

## 풀이

입력 문자열을 k번 순서대로 이어 붙이기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
using namespace std;

string solution(string my_string, int k) {
    string answer;
    for (int i = 0; i < k; ++i) answer += my_string;
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// string solution(string my_string, int k) {  // 문자열 곱하기 풀이 시작
//     string answer;  // 원본을 k번 이어 붙일 문자열
//     for (int i = 0; i < k; ++i) answer += my_string;  // for로 k번 반복하고 +=로 원본 문자열을 결과 뒤에 연결
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 입력 문자열을 k번 순서대로 이어 붙이기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:32:56
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181940_%EB%AC%B8%EC%9E%90%EC%97%B4_%EA%B3%B1%ED%95%98%EA%B8%B0/README.md)
