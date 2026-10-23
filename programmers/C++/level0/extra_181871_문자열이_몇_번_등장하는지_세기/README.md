# 문자열이 몇 번 등장하는지 세기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181871) · Level 0 · C++

## 풀이

모든 시작 위치를 검사하므로 패턴이 서로 겹쳐 등장하는 경우도 모두 세기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
#include <functional>
#include <unordered_set>
#include <sstream>
#include <cctype>
#include <cstdlib>
using namespace std;

int solution(string myString, string pat) {
    int count = 0;
    for (size_t pos = myString.find(pat); pos != string::npos; pos = myString.find(pat, pos + 1)) ++count;
    return count;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
// #include <algorithm>  // 정렬·검색·뒤집기 알고리즘
// #include <numeric>  // accumulate·iota 등 수치 연산
// #include <functional>  // greater·multiplies 등 함수 객체
// #include <unordered_set>  // 중복을 거를 해시 집합
// #include <sstream>  // 문자열을 항목별로 읽을 스트림
// #include <cctype>  // 문자 검사와 대소문자 변환
// #include <cstdlib>  // 정수 변환과 절댓값 등 표준 함수
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int solution(string myString, string pat) {  // 문자열이 몇 번 등장하는지 세기 풀이 시작
//     int count = 0;  // 패턴이 등장한 시작 위치의 수
//     for (size_t pos = myString.find(pat); pos != string::npos; pos = myString.find(pat, pos + 1)) ++count;  // 발견 위치의 한 칸 뒤부터 다시 찾아 겹치는 등장도 포함
//     return count;  // 조건을 만족한 횟수 값을 반환하고 함수를 끝
// }  // 블록 끝

// 풀이 요약
// 모든 시작 위치를 검사하므로 패턴이 서로 겹쳐 등장하는 경우도 모두 세기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:10:56
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181871_%EB%AC%B8%EC%9E%90%EC%97%B4%EC%9D%B4_%EB%AA%87_%EB%B2%88_%EB%93%B1%EC%9E%A5%ED%95%98%EB%8A%94%EC%A7%80_%EC%84%B8%EA%B8%B0/README.md)
