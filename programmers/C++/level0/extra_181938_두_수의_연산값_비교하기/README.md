# 두 수의 연산값 비교하기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181938) · Level 0 · C++

## 풀이

a와 b를 이어 붙인 수와 2ab를 계산한 뒤 큰 값을 반환

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <string>
using namespace std;

int solution(int a, int b) {
    return max(stoi(to_string(a) + to_string(b)), 2 * a * b);
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·검색·뒤집기 알고리즘
// #include <string>  // 문자열을 다룰 string
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int solution(int a, int b) {  // 두 수의 연산값 비교하기 풀이 시작
//     return max(stoi(to_string(a) + to_string(b)), 2 * a * b);  // to_string으로 연결한 수를 stoi로 정수화하고 max로 2ab와 비교
// }  // 블록 끝

// 풀이 요약
// a와 b를 이어 붙인 수와 2ab를 계산한 뒤 큰 값을 반환
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:33:40
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181938_%EB%91%90_%EC%88%98%EC%9D%98_%EC%97%B0%EC%82%B0%EA%B0%92_%EB%B9%84%EA%B5%90%ED%95%98%EA%B8%B0/README.md)
