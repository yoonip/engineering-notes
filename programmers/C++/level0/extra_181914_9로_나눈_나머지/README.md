# 9로 나눈 나머지

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181914) · Level 0 · C++

## 풀이

각 자리 숫자를 더하고 9로 나눈 나머지를 유지

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
using namespace std;

int solution(string number) {
    int answer = 0;
    for (char c : number) answer = (answer + c - '0') % 9;
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int solution(string number) {  // 9로 나눈 나머지 풀이 시작
//     int answer = 0;  // 정수형 결과 누적값을 0으로 초기화
//     for (char c : number) answer = (answer + c - '0') % 9;  // 범위 for로 각 숫자 문자를 정수로 바꾸어 더하고 % 9로 나머지를 유지
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 각 자리 숫자를 더하고 9로 나눈 나머지를 유지
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:54:44
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181914_9%EB%A1%9C_%EB%82%98%EB%88%88_%EB%82%98%EB%A8%B8%EC%A7%80/README.md)
