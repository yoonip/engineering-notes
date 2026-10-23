# 2개 이하로 다른 비트

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/77885) · Level 2 · C++

## 풀이

가장 낮은 0비트를 찾아 1로 바꾸고 바로 아래 1비트를 0으로 바꾸어 두 비트 이내에서 가장 작은 큰 수 만들기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <vector>
using namespace std;

vector<long long> solution(vector<long long> numbers) {
    vector<long long> answer;
    for (long long number : numbers) {
        long long zero = (~number) & (number + 1);
        answer.push_back(number + zero - (zero >> 1));
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<long long> solution(vector<long long> numbers) {  // 낮은 비트를 바꿔 두 비트 이내의 다음 수 계산
// vector<long long> answer;  // 각 수보다 큰 최소 후보 저장
// for (long long number : numbers) {  // 입력 수를 하나씩 처리
// long long zero = (~number) & (number + 1);  // 가장 낮은 0비트 위치를 비트 반전과 AND로 찾기
// answer.push_back(number + zero - (zero >> 1));  // 해당 0을 1로 바꾸고 바로 아래 1을 0으로 바꾸기
// }  // 블록 끝
// return answer;  // 다른 비트가 두 개 이하인 최소 큰 수 반환
// }  // 블록 끝

// 풀이 요약
// 가장 낮은 0비트를 찾아 1로 바꾸고 바로 아래 1비트를 0으로 바꾸어 두 비트 이내에서 가장 작은 큰 수 만들기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:39:44
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/054_77885_2%EA%B0%9C_%EC%9D%B4%ED%95%98%EB%A1%9C_%EB%8B%A4%EB%A5%B8_%EB%B9%84%ED%8A%B8/README.md)
