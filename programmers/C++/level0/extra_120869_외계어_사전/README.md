# 외계어 사전

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120869) · Level 0 · C++

## 풀이

정렬한 문자 목록이 같으면 각 글자를 정확히 한 번씩 모두 사용한 단어임

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
#include <cmath>
#include <sstream>
#include <climits>
#include <cctype>
#include <iostream>
#include <functional>

using namespace std;

int solution(vector<string> spell, vector<string> dic) {
    string target;
    for (const string& letter : spell) target += letter;
    sort(target.begin(), target.end());
    for (string word : dic) {
        sort(word.begin(), word.end());
        if (word == target) return 1;
    }
    return 2;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
// #include <algorithm>  // 정렬·검색·뒤집기 알고리즘
// #include <numeric>  // accumulate·iota 등 수치 연산
// #include <cmath>  // 제곱근 등 수학 함수
// #include <sstream>  // 문자열을 항목별로 읽을 스트림
// #include <climits>  // INT_MIN·INT_MAX 등 정수 범위 상수
// #include <cctype>  // 문자 검사와 대소문자 변환
// #include <iostream>  // cin·cout 표준 입출력
// #include <functional>  // greater·multiplies 등 함수 객체
//
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int solution(vector<string> spell, vector<string> dic) {  // 외계어 사전 풀이 시작
//     string target;  // spell의 글자를 모두 합친 비교 기준
//     for (const string& letter : spell) target += letter;  // 주어진 글자들을 한 문자열로 연결
//     sort(target.begin(), target.end());  // target를 오름차순 정렬
//     for (string word : dic) {  // 사전 단어를 하나씩 정렬해 글자 구성 비교
//         sort(word.begin(), word.end());  // word를 오름차순 정렬
//         if (word == target) return 1;  // 정렬한 글자 구성이 같으면 spell을 정확히 한 번씩 쓴 단어이므로 1 반환
//     }  // 블록 끝
//     return 2;  // 주어진 글자를 정확히 한 번씩 쓴 단어가 없음
// }  // 블록 끝

// 풀이 요약
// 정렬한 문자 목록이 같으면 각 글자를 정확히 한 번씩 모두 사용한 단어임
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:55:24
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120869_%EC%99%B8%EA%B3%84%EC%96%B4_%EC%82%AC%EC%A0%84/README.md)
