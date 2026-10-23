# JadenCase 문자열 만들기

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12951) · Level 2 · C++

## 풀이

공백 뒤 첫 문자는 대문자로, 단어 안의 나머지 문자는 소문자로 바꾸며 공백을 그대로 보존

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <cctype>
#include <string>
using namespace std;

string solution(string s) {
    bool first = true;
    for (char& c : s) {
        if (c == ' ') first = true;
        else { c = (char)(first ? toupper((unsigned char)c) : tolower((unsigned char)c)); first = false; }
    }
    return s;
}

// 전체 코드 줄별 설명
// #include <cctype>  // 문자 분류와 대소문자 변환
// #include <string>  // 문자열을 담는 string
// using namespace std;  // std:: 접두사 생략
// string solution(string s) {  // 공백을 유지하며 단어의 첫 글자만 대문자로 변경
// bool first = true;  // 다음 문자가 단어의 첫 글자인지 표시
// for (char& c : s) {  // 원본 문자열의 각 문자를 참조로 수정하기
// if (c == ' ') first = true;  // 공백 뒤에서는 새 단어가 시작
// else { c = (char)(first ? toupper((unsigned char)c) : tolower((unsigned char)c)); first = false; }  // 첫 문자는 대문자, 나머지는 소문자로 바꾸고 단어 안쪽으로 이동
// }  // 블록 끝
// return s;  // 원래 공백을 유지한 JadenCase 문자열 반환
// }  // 블록 끝

// 풀이 요약
// 공백 뒤 첫 문자는 대문자로, 단어 안의 나머지 문자는 소문자로 바꾸며 공백을 그대로 보존
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:35:34
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/100_12951_JadenCase_%EB%AC%B8%EC%9E%90%EC%97%B4_%EB%A7%8C%EB%93%A4%EA%B8%B0/README.md)
