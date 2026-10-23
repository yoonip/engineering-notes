# 접미사인지 확인하기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181908) · Level 0 · C++

## 풀이

후보가 원본보다 길지 않은지 확인하고 끝부분을 비교

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
using namespace std;

int solution(string my_string, string is_suffix) {
    return my_string.size() >= is_suffix.size() && my_string.compare(my_string.size() - is_suffix.size(), is_suffix.size(), is_suffix) == 0;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int solution(string my_string, string is_suffix) {  // 접미사인지 확인하기 풀이 시작
//     return my_string.size() >= is_suffix.size() && my_string.compare(my_string.size() - is_suffix.size(), is_suffix.size(), is_suffix) == 0;  // &&로 길이를 먼저 확인한 뒤 compare로 끝부분이 접미사 후보와 같은지 비교
// }  // 블록 끝

// 풀이 요약
// 후보가 원본보다 길지 않은지 확인하고 끝부분을 비교
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:57:52
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181908_%EC%A0%91%EB%AF%B8%EC%82%AC%EC%9D%B8%EC%A7%80_%ED%99%95%EC%9D%B8%ED%95%98%EA%B8%B0/README.md)
