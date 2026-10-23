# 문자열 겹쳐쓰기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181943) · Level 0 · C++

## 풀이

시작 위치 s부터 덮어쓸 문자열 길이만큼 교체

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
using namespace std;

string solution(string my_string, string overwrite_string, int s) {
    my_string.replace(s, overwrite_string.size(), overwrite_string);
    return my_string;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// string solution(string my_string, string overwrite_string, int s) {  // 문자열 겹쳐쓰기 풀이 시작
//     my_string.replace(s, overwrite_string.size(), overwrite_string);  // replace로 위치 s부터 새 문자열 길이만큼 덮어씁니다
//     return my_string;  // return으로 교체를 마친 문자열을 반환
// }  // 블록 끝

// 풀이 요약
// 시작 위치 s부터 덮어쓸 문자열 길이만큼 교체
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:32:12
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181943_%EB%AC%B8%EC%9E%90%EC%97%B4_%EA%B2%B9%EC%B3%90%EC%93%B0%EA%B8%B0/README.md)
