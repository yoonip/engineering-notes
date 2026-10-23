# 다음 큰 숫자

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12911) · Level 2 · C++

## 풀이

가장 낮은 1비트를 위쪽으로 올리고 나머지 바뀐 1비트를 낮은 자리에 모아 다음 큰 정수 구하기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
int solution(int n) {
    int lowest = n & -n;
    int raised = n + lowest;
    int tail = ((n ^ raised) >> 2) / lowest;
    return raised | tail;
}

// 전체 코드 줄별 설명
// int solution(int n) {  // 1비트 수를 유지하는 다음 큰 정수 계산
// int lowest = n & -n;  // 가장 낮은 1비트를 비트 AND로 분리
// int raised = n + lowest;  // 그 1비트를 위쪽의 첫 0 자리로 올리기
// int tail = ((n ^ raised) >> 2) / lowest;  // 이동으로 바뀐 나머지 1비트를 가장 낮은 자리에 모으기
// return raised | tail;  // 1비트 수가 같으면서 가장 작은 큰 정수 반환
// }  // 블록 끝

// 풀이 요약
// 가장 낮은 1비트를 위쪽으로 올리고 나머지 바뀐 1비트를 낮은 자리에 모아 다음 큰 정수 구하기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:43:21
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/extra_12911_%EB%8B%A4%EC%9D%8C_%ED%81%B0_%EC%88%AB%EC%9E%90/README.md)
