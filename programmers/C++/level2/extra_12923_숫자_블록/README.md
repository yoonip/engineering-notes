# 숫자 블록

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12923) · Level 2 · C++

## 풀이

각 위치의 약수 쌍을 검사해 천만 이하의 가장 큰 진약수를 고르고 1번 위치는 0으로 두기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <vector>
using namespace std;

vector<int> solution(long long begin, long long end) {
    vector<int> answer;
    for (long long value = begin; value <= end; ++value) {
        if (value == 1) { answer.push_back(0); continue; }
        int block = 1;
        for (long long divisor = 2; divisor <= value / divisor; ++divisor) if (value % divisor == 0) {
            long long partner = value / divisor;
            if (partner <= 10000000) { block = (int)partner; break; }
            block = (int)divisor;
        }
        answer.push_back(block);
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<int> solution(long long begin, long long end) {  // 천만 이하의 가장 큰 진약수를 블록 번호로 선택
// vector<int> answer;  // 구간별 최종 숫자 블록 저장
// for (long long value = begin; value <= end; ++value) {  // 요청된 번호 범위만 순회
// if (value == 1) { answer.push_back(0); continue; }  // 1번 위치에는 블록을 놓지 않음
// int block = 1;  // 다른 진약수가 없을 때의 블록 번호
// for (long long divisor = 2; divisor <= value / divisor; ++divisor) if (value % divisor == 0) {  // 제곱근까지 약수 쌍 검사
// long long partner = value / divisor;  // 현재 약수와 짝인 큰 약수 구하기
// if (partner <= 10000000) { block = (int)partner; break; }  // 사용할 수 있는 가장 큰 짝 약수이면 선택하고 끝
// block = (int)divisor;  // 큰 짝을 쓸 수 없으면 작은 약수를 후보로 유지
// }  // 블록 끝
// answer.push_back(block);  // 현재 위치의 블록 번호 기록
// }  // 블록 끝
// return answer;  // 요청 구간의 블록 번호 반환
// }  // 블록 끝

// 풀이 요약
// 각 위치의 약수 쌍을 검사해 천만 이하의 가장 큰 진약수를 고르고 1번 위치는 0으로 두기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:39:58
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/extra_12923_%EC%88%AB%EC%9E%90_%EB%B8%94%EB%A1%9D/README.md)
