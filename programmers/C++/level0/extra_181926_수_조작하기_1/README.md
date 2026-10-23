# 수 조작하기 1

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181926) · Level 0 · C++

## 풀이

조작 문자마다 정해진 증감량을 현재 수에 적용

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
using namespace std;

int solution(int n, string control) {
    for (char c : control) {
        if (c == 'w') ++n;
        else if (c == 's') --n;
        else if (c == 'd') n += 10;
        else if (c == 'a') n -= 10;
    }
    return n;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int solution(int n, string control) {  // 수 조작하기 1 풀이 시작
//     for (char c : control) {  // 범위 for로 각 조작 문자를 읽기
//         if (c == 'w') ++n;  // if와 ==로 w 명령을 검사하고 ++로 현재 수에 1을 더하기
//         else if (c == 's') --n;  // else if로 s 명령을 검사하고 --로 현재 수에서 1을 빼기
//         else if (c == 'd') n += 10;  // else if로 d 명령을 검사하고 +=로 현재 수에 10을 더하기
//         else if (c == 'a') n -= 10;  // else if로 a 명령을 검사하고 -=로 현재 수에서 10을 빼기
//     }  // 블록 끝
//     return n;  // return으로 조작을 모두 적용한 정수를 반환
// }  // 블록 끝

// 풀이 요약
// 조작 문자마다 정해진 증감량을 현재 수에 적용
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:41:23
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181926_%EC%88%98_%EC%A1%B0%EC%9E%91%ED%95%98%EA%B8%B0_1/README.md)
