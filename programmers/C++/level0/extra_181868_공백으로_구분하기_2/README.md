# 공백으로 구분하기 2

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181868) · Level 0 · C++

## 풀이

입력 스트림의 >>는 연속 공백과 양 끝 공백을 건너뛰므로, 읽힌 단어만 차례로 모으기

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

vector<string> solution(string my_string) {
    istringstream stream(my_string);
    vector<string> answer;
    string word;
    while (stream >> word) answer.push_back(word);
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
// vector<string> solution(string my_string) {  // 공백으로 구분하기 2 풀이 시작
//     istringstream stream(my_string);  // my_string를 공백 단위로 읽을 스트림 stream
//     vector<string> answer;  // 여러 공백을 건너뛰며 읽은 단어 목록
//     string word;  // 스트림에서 방금 읽은 단어
//     while (stream >> word) answer.push_back(word);  // 공백을 건너뛰며 단어를 읽어 순서대로 추가
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 입력 스트림의 >>는 연속 공백과 양 끝 공백을 건너뛰므로, 읽힌 단어만 차례로 모으기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:12:10
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181868_%EA%B3%B5%EB%B0%B1%EC%9C%BC%EB%A1%9C_%EA%B5%AC%EB%B6%84%ED%95%98%EA%B8%B0_2/README.md)
