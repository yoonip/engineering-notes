# 한 번만 등장한 문자

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120896) · Level 0 · C++

## 풀이

소문자별 등장 횟수를 센 뒤 a부터 z까지 확인. 정확히 한 번 등장한 문자만 붙여 사전순 결과를 만들기

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

string solution(string s) {
    int counts[26] = {};
    for (char c : s) ++counts[c - 'a'];
    string answer;
    for (int i = 0; i < 26; ++i) if (counts[i] == 1) answer += char('a' + i);
    return answer;
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
// string solution(string s) {  // 한 번만 등장한 문자 풀이 시작
//     int counts[26] = {};  // int 배열 counts의 26개 원소를 {}로 0 초기화하여 a부터 z까지의 등장 횟수를 저장
//     for (char c : s) ++counts[c - 'a'];  // 범위 기반 for로 각 문자 c를 읽고 c - a에 해당하는 인덱스의 빈도를 1 증가
//     string answer;  // string 변수 answer를 빈 문자열로 만들어 한 번만 나온 문자들을 붙일 준비
//     for (int i = 0; i < 26; ++i) if (counts[i] == 1) answer += char('a' + i);  // for로 a부터 z에 해당하는 인덱스 i를 순회. 빈도가 1이면 a + i를 char로 변환하여 answer 끝에 붙이기
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 소문자별 등장 횟수를 센 뒤 a부터 z까지 확인. 정확히 한 번 등장한 문자만 붙여 사전순 결과를 만들기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:27:03
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120896_%ED%95%9C_%EB%B2%88%EB%A7%8C_%EB%93%B1%EC%9E%A5%ED%95%9C_%EB%AC%B8%EC%9E%90/README.md)
