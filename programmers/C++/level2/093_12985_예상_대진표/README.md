# 예상 대진표

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12985) · Level 2 · C++

## 풀이

매 라운드의 두 참가자 번호를 올림 나눗셈으로 절반씩 줄여 같은 번호가 되는 단계 세기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
int solution(int n, int a, int b) {
    (void)n;
    int rounds = 0;
    while (a != b) {
        a = (a + 1) / 2; b = (b + 1) / 2;
        ++rounds;
    }
    return rounds;
}

// 전체 코드 줄별 설명
// int solution(int n, int a, int b) {  // 라운드마다 번호를 절반으로 줄여 만나는 차례 계산
// (void)n;  // 참가자 번호가 만나는 단계만 계산하므로 전체 수는 직접 사용하지 않음
// int rounds = 0;  // 두 참가자가 만날 때까지의 라운드 수 초기화
// while (a != b) {  // 두 번호가 같은 다음 대진표 위치가 될 때까지 반복
// a = (a + 1) / 2; b = (b + 1) / 2;  // 다음 라운드의 참가자 번호로 바꾸기
// ++rounds;  // 진행한 라운드 수 늘리기
// }  // 블록 끝
// return rounds;  // 두 참가자가 만나는 라운드 반환
// }  // 블록 끝

// 풀이 요약
// 매 라운드의 두 참가자 번호를 올림 나눗셈으로 절반씩 줄여 같은 번호가 되는 단계 세기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:31:18
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/093_12985_%EC%98%88%EC%83%81_%EB%8C%80%EC%A7%84%ED%91%9C/README.md)
