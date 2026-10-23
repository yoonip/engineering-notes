# 모음사전

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/84512) · Level 2 · C++

## 풀이

각 자릿수에서 앞선 모음이 차지하는 사전 항목 수와 현재 접두사 하나를 더해 순서 구하기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
using namespace std;

int solution(string word) {
    int weights[5] = {781, 156, 31, 6, 1};
    string vowels = "AEIOU";
    int answer = 0;
    for (int i = 0; i < (int)word.size(); ++i) answer += (int)vowels.find(word[i]) * weights[i] + 1;
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 담는 string
// using namespace std;  // std:: 접두사 생략
// int solution(string word) {  // 접두사별 사전 묶음 크기로 단어 순번 계산
// int weights[5] = {781, 156, 31, 6, 1};  // 각 자릿수의 모음 하나가 건너뛰는 사전 항목 수
// string vowels = "AEIOU";  // 모음의 사전순 저장
// int answer = 0;  // 단어 순서 초기화
// for (int i = 0; i < (int)word.size(); ++i) answer += (int)vowels.find(word[i]) * weights[i] + 1;  // 앞선 모음으로 시작하는 항목 수와 현재 접두사 한 개를 더하기
// return answer;  // 사전에서 단어의 순서 반환
// }  // 블록 끝

// 풀이 요약
// 각 자릿수에서 앞선 모음이 차지하는 사전 항목 수와 현재 접두사 하나를 더해 순서 구하기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:39:02
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/052_84512_%EB%AA%A8%EC%9D%8C%EC%82%AC%EC%A0%84/README.md)
