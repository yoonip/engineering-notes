# 영어가 싫어요

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120894) · Level 0 · C++

## 풀이

현재 위치에서 일치하는 영어 숫자를 찾기. 기존 값에 10을 곱하고 그 숫자를 더한 뒤, 읽은 단어 길이만큼 다음 위치로 이동

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

long long solution(string numbers) {
    vector<string> words = {"zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"};
    long long answer = 0;
    size_t pos = 0;
    while (pos < numbers.size()) {
        for (int d = 0; d < 10; ++d)
            if (numbers.compare(pos, words[d].size(), words[d]) == 0) {
                answer = answer * 10 + d; pos += words[d].size(); break;
            }
    }
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
// long long solution(string numbers) {  // 영어가 싫어요 풀이 시작
//     vector<string> words = {"zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"};  // words를 보관할 컨테이너 준비
//     long long answer = 0;  // 영어 숫자를 읽으며 십진수로 쌓을 값
//     size_t pos = 0;  // 아직 해석하지 않은 영어 숫자의 시작 위치
//     while (pos < numbers.size()) {  // 모든 영어 숫자를 읽을 때까지 반복
//         for (int d = 0; d < 10; ++d)  // 현재 부분과 일치하는 zero~nine 찾기
//             if (numbers.compare(pos, words[d].size(), words[d]) == 0) {  // 현재 위치에 해당 숫자의 영어 이름이 맞는 경우
//                 answer = answer * 10 + d; pos += words[d].size(); break;  // break는 현재 계산을 마친 뒤 가장 안쪽 반복문을 종료
//             }  // 블록 끝
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 현재 위치에서 일치하는 영어 숫자를 찾기. 기존 값에 10을 곱하고 그 숫자를 더한 뒤, 읽은 단어 길이만큼 다음 위치로 이동
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:45:23
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120894_%EC%98%81%EC%96%B4%EA%B0%80_%EC%8B%AB%EC%96%B4%EC%9A%94/README.md)
