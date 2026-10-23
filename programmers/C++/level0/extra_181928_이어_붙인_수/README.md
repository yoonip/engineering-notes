# 이어 붙인 수

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181928) · Level 0 · C++

## 풀이

홀수와 짝수를 각각 원래 순서대로 이어 붙인 정수 두 개를 더하기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <vector>
using namespace std;

int solution(vector<int> num_list) {
    int odd = 0, even = 0;
    for (int value : num_list) {
        if (value % 2) odd = odd * 10 + value;
        else even = even * 10 + value;
    }
    return odd + even;
}

// 전체 코드 줄별 설명
// #include <vector>  // 길이를 늘릴 수 있는 vector
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int solution(vector<int> num_list) {  // 이어 붙인 수 풀이 시작
//     int odd = 0, even = 0;  // 홀수와 짝수를 이어 붙인 결과를 각각 0으로 초기화
//     for (int value : num_list) {  // 범위 for로 정수 목록의 각 원소를 읽기
//         if (value % 2) odd = odd * 10 + value;  // 나머지 연산자 %로 홀수를 골라 기존 수를 10배 한 뒤 마지막 자릿수로 붙이기
//         else even = even * 10 + value;  // else에서 짝수를 골라 기존 수를 10배 한 뒤 마지막 자릿수로 붙이기
//     }  // 블록 끝
//     return odd + even;  // 홀수끼리 연결한 수와 짝수끼리 연결한 수의 합을 반환
// }  // 블록 끝

// 풀이 요약
// 홀수와 짝수를 각각 원래 순서대로 이어 붙인 정수 두 개를 더하기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:39:21
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181928_%EC%9D%B4%EC%96%B4_%EB%B6%99%EC%9D%B8_%EC%88%98/README.md)
