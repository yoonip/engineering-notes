# 코드 처리하기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181932) · Level 0 · C++

## 풀이

문자 1은 모드를 바꾸고, 나머지는 모드와 인덱스 홀짝이 같을 때만 연결

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
using namespace std;

string solution(string code) {
    string answer;
    int mode = 0;
    for (size_t i = 0; i < code.size(); ++i) {
        if (code[i] == '1') mode = 1 - mode;
        else if ((int)(i % 2) == mode) answer += code[i];
    }
    return answer.empty() ? "EMPTY" : answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// string solution(string code) {  // 코드 처리하기 풀이 시작
//     string answer;  // 현재 모드와 홀짝이 맞는 문자만 모을 결과
//     int mode = 0;  // 문자 선택 규칙을 나타내는 모드를 0으로 초기화
//     for (size_t i = 0; i < code.size(); ++i) {  // size_t형 인덱스를 for로 증가시키며 각 위치를 차례로 처리
//         if (code[i] == '1') mode = 1 - mode;  // if로 모드 변경 문자를 검사하고 1에서 현재 값을 빼 0과 1을 전환
//         else if ((int)(i % 2) == mode) answer += code[i];  // %로 인덱스의 홀짝을 구해 모드와 같으면 +=로 문자를 연결
//     }  // 블록 끝
//     return answer.empty() ? "EMPTY" : answer;  // empty와 삼항 연산자 ?:로 결과가 비었으면 EMPTY 문자열을 반환
// }  // 블록 끝

// 풀이 요약
// 문자 1은 모드를 바꾸고, 나머지는 모드와 인덱스 홀짝이 같을 때만 연결
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:35:33
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181932_%EC%BD%94%EB%93%9C_%EC%B2%98%EB%A6%AC%ED%95%98%EA%B8%B0/README.md)
