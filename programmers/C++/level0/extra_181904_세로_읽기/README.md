# 세로 읽기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181904) · Level 0 · C++

## 풀이

열 번호를 0부터 시작하는 인덱스로 바꾸고 m칸 간격의 문자를 읽기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
using namespace std;

string solution(string my_string, int m, int c) {
    string answer;
    for (size_t i = c - 1; i < my_string.size(); i += m) answer += my_string[i];
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// string solution(string my_string, int m, int c) {  // 세로 읽기 풀이 시작
//     string answer;  // 지정된 열의 문자를 위에서 아래로 모을 결과
//     for (size_t i = c - 1; i < my_string.size(); i += m) answer += my_string[i];  // 열을 0부터 시작하는 위치로 바꾸고 for에서 m씩 이동하며 같은 열의 문자를 연결
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 열 번호를 0부터 시작하는 인덱스로 바꾸고 m칸 간격의 문자를 읽기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:59:04
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181904_%EC%84%B8%EB%A1%9C_%EC%9D%BD%EA%B8%B0/README.md)
