# 문자열의 뒤의 n글자

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181910) · Level 0 · C++

## 풀이

뒤에서 n번째 위치부터 끝까지 반환

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
using namespace std;

string solution(string my_string, int n) {
    return my_string.substr(my_string.size() - n);
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// string solution(string my_string, int n) {  // 문자열의 뒤의 n글자 풀이 시작
//     return my_string.substr(my_string.size() - n);  // size에서 n을 뺀 위치부터 끝까지 substr로 추출해 반환
// }  // 블록 끝

// 풀이 요약
// 뒤에서 n번째 위치부터 끝까지 반환
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:57:12
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181910_%EB%AC%B8%EC%9E%90%EC%97%B4%EC%9D%98_%EB%92%A4%EC%9D%98_n%EA%B8%80%EC%9E%90/README.md)
