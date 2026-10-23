# 두 수의 합

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181846) · Level 0 · C++

## 풀이

두 문자열을 뒤에서부터 읽어 각 자릿수와 올림을 더하기. 결과의 일의 자리를 answer 뒤에 붙이고 십의 자리를 다음 올림으로 넘긴 뒤, 역순으로 쌓인 answer를 마지막에 뒤집기

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

string solution(string a, string b) {
    int i = (int)a.size() - 1, j = (int)b.size() - 1, carry = 0;
    string answer;
    while (i >= 0 || j >= 0 || carry) {
        int sum = carry;
        if (i >= 0) sum += a[i--] - '0';
        if (j >= 0) sum += b[j--] - '0';
        answer.push_back('0' + sum % 10);
        carry = sum / 10;
    }
    reverse(answer.begin(), answer.end());
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
// string solution(string a, string b) {  // 두 수의 합 풀이 시작
//     int i = (int)a.size() - 1, j = (int)b.size() - 1, carry = 0;  // i와 j를 각 문자열의 마지막 자릿수 인덱스로 두고 올림 carry를 0으로 초기화
//     string answer;  // 일의 자리부터 계산한 숫자 문자를 역순으로 담을 결과 문자열 answer를 선언
//     while (i >= 0 || j >= 0 || carry) {  // 어느 쪽에든 처리할 자릿수가 남거나 마지막 올림이 있는 동안 덧셈을 반복
//         int sum = carry;  // 현재 자리의 합 sum을 이전 자리에서 넘어온 올림 carry로 초기화
//         if (i >= 0) sum += a[i--] - '0';  // a의 자릿수가 남아 있으면 '0'을 빼 숫자로 바꿔 더하고, 후위 감소로 다음 높은 자리로 이동
//         if (j >= 0) sum += b[j--] - '0';  // b의 자릿수가 남아 있으면 숫자로 바꿔 더하고 j를 다음 높은 자리로 이동
//         answer.push_back('0' + sum % 10);  // sum을 10으로 나눈 나머지를 숫자 문자로 바꾸어 answer 뒤에 추가
//         carry = sum / 10;  // 정수 나눗셈으로 sum의 십의 자리를 구해 다음 자리의 올림 carry에 저장
//     }  // 블록 끝
//     reverse(answer.begin(), answer.end());  // 일의 자리부터 쌓은 answer를 reverse로 뒤집어 일반적인 자릿수 순서로 바꾸기
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 두 문자열을 뒤에서부터 읽어 각 자릿수와 올림을 더하기. 결과의 일의 자리를 answer 뒤에 붙이고 십의 자리를 다음 올림으로 넘긴 뒤, 역순으로 쌓인 answer를 마지막에 뒤집기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:20:24
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181846_%EB%91%90_%EC%88%98%EC%9D%98_%ED%95%A9/README.md)
