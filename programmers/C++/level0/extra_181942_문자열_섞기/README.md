# 문자열 섞기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181942) · Level 0 · C++

## 풀이

두 문자열에서 같은 위치의 문자를 번갈아 연결

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
using namespace std;

string solution(string str1, string str2) {
    string answer;
    for (size_t i = 0; i < str1.size(); ++i) { answer += str1[i]; answer += str2[i]; }
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// string solution(string str1, string str2) {  // 문자열 섞기 풀이 시작
//     string answer;  // 두 문자열의 문자를 번갈아 모을 결과
//     for (size_t i = 0; i < str1.size(); ++i) { answer += str1[i]; answer += str2[i]; }  // size_t 인덱스를 for로 순회하며 []로 두 문자열의 문자를 번갈아 붙이기
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 두 문자열에서 같은 위치의 문자를 번갈아 연결
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:32:32
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181942_%EB%AC%B8%EC%9E%90%EC%97%B4_%EC%84%9E%EA%B8%B0/README.md)
