# 문자열 잘라서 정렬하기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181866) · Level 0 · C++

## 풀이

x로 나눈 뒤 빈 조각은 버리고 남은 문자열을 정렬

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

vector<string> solution(string myString) {
    vector<string> answer;
    istringstream stream(myString);
    string part;
    while (getline(stream, part, 'x')) if (!part.empty()) answer.push_back(part);
    sort(answer.begin(), answer.end());
    return answer;
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
// vector<string> solution(string myString) {  // 문자열 잘라서 정렬하기 풀이 시작
//     vector<string> answer;  // x로 나눈 뒤 빈 조각을 뺀 문자열 목록
//     istringstream stream(myString);  // myString를 공백 단위로 읽을 스트림 stream
//     string part;  // x 사이에서 읽은 현재 문자열 조각
//     while (getline(stream, part, 'x')) if (!part.empty()) answer.push_back(part);  // getline으로 x를 구분자로 부분 문자열을 읽고 빈 문자열을 제외
//     sort(answer.begin(), answer.end());  // sort로 주어진 구간을 지정한 기준에 따라 오름차순으로 정렬
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// x로 나눈 뒤 빈 조각은 버리고 남은 문자열을 정렬
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:12:34
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181866_%EB%AC%B8%EC%9E%90%EC%97%B4_%EC%9E%98%EB%9D%BC%EC%84%9C_%EC%A0%95%EB%A0%AC%ED%95%98%EA%B8%B0/README.md)
