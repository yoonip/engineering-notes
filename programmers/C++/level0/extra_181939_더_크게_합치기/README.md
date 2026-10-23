# 더 크게 합치기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181939) · Level 0 · C++

## 풀이

두 정수를 두 순서로 이어 붙이고 더 큰 값을 반환

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <string>
using namespace std;

int solution(int a, int b) {
    return max(stoi(to_string(a) + to_string(b)), stoi(to_string(b) + to_string(a)));
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·검색·뒤집기 알고리즘
// #include <string>  // 문자열을 다룰 string
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int solution(int a, int b) {  // 더 크게 합치기 풀이 시작
//     return max(stoi(to_string(a) + to_string(b)), stoi(to_string(b) + to_string(a)));  // to_string과 +로 두 순서의 문자열을 만들고 stoi와 max로 큰 정수를 구하기
// }  // 블록 끝

// 풀이 요약
// 두 정수를 두 순서로 이어 붙이고 더 큰 값을 반환
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:33:25
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181939_%EB%8D%94_%ED%81%AC%EA%B2%8C_%ED%95%A9%EC%B9%98%EA%B8%B0/README.md)
